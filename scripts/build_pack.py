"""Build a section's evidence pack — deterministically, from the approved outline.

The writer composes no queries. Every retrieval the episode performs is named in
``outline.yaml`` at the gate, where a wrong key is cheap to fix, and executed here. A pack
is a file on disk: what the section is for, which canon governs it, which occasions it may
draw on and from what vantage, and the evidence that came back, each item tagged with the
key that found it.

The point of the hard stop is that a silent retrieval failure is indistinguishable from
success, and the writer's fallback for missing evidence is its own memory of Mass Effect —
which is where wrong-but-plausible facts live. An empty pack must be a failed exit and a
visible file, not improvisation.

Usage::

    python scripts/build_pack.py <run-dir> <section-id>
    python scripts/build_pack.py <run-dir> --all
    python scripts/build_pack.py <run-dir> --all --allow-thin
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path

import yaml

from scripts import canon as canon_mod
from scripts import common, retrieve, scenes as scenes_mod

#: Per-key retrieval budget. Scenes and summaries are guaranteed slots so the occasion
#: layer cannot be crowded out by the mission pages next door, which is exactly how a
#: section about a party came back holding nine chunks about mercenaries.
PER_KIND = {"scene": 4, "summary": 4, "page": 8}


class ThinPack(RuntimeError):
    """The outline asks for something the corpus cannot supply. Fix the outline."""


@dataclasses.dataclass(frozen=True)
class Repo:
    """Where everything lives. Injectable so the tests can build a miniature repo."""
    root: Path

    @property
    def index(self) -> Path:
        return self.root / "data" / "bm25_index.pkl"

    @property
    def scenes_dir(self) -> Path:
        return self.root / "scenes"

    @property
    def events_dir(self) -> Path:
        return self.root / "timeline" / "events"

    @property
    def codex_dir(self) -> Path:
        return self.root / "codex"

    @property
    def canon_dir(self) -> Path:
        return self.root / "config" / "canon"


def default_repo() -> Repo:
    return Repo(common.REPO_ROOT)


# --------------------------------------------------------------------------
# pieces of a pack
# --------------------------------------------------------------------------

def _load_outline(run_dir: Path) -> dict:
    path = Path(run_dir) / "outline.yaml"
    if not path.exists():
        raise ThinPack(f"{path}: no outline to build from")
    if not common.outline_is_approved(Path(run_dir)):
        raise ThinPack(f"{path} is still marked UNAPPROVED — the user approves it first")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _section(outline: dict, section_id: str) -> dict:
    for s in outline.get("sections") or []:
        if s.get("id") == section_id:
            return s
    known = ", ".join(s.get("id", "?") for s in outline.get("sections") or [])
    raise ThinPack(f"no section {section_id!r} in the outline (have: {known})")


def _required_facts(repo: Repo, section: dict, gaps: list[str]) -> list[dict]:
    """Event summaries and consequences, as third-person prose the narrator must transpose."""
    out: list[dict] = []
    for event_id in section.get("events") or []:
        path = repo.events_dir / f"{event_id}.yaml"
        if not path.exists():
            gaps.append(f"unknown event id {event_id!r} — no {path}")
            continue
        event = common.load_event(path)
        people = [str(c) for c in event.get("characters") or []]
        for fact in [event["summary"], *(event.get("consequences") or [])]:
            fact = " ".join(str(fact).split())
            actor = next((p for p in people if p.lower() in fact.lower()), "")
            out.append({"event_id": event_id, "fact": fact, "actor": actor})
    return out


def _scene_records(repo: Repo, section: dict, narrator: str,
                   gaps: list[str], warnings: list[str]) -> tuple[list[dict], dict[str, str]]:
    all_scenes = scenes_mod.load_scenes(repo.scenes_dir) if repo.scenes_dir.is_dir() else {}
    records, attendance = [], {}
    for scene_id in section.get("scenes") or []:
        scene = all_scenes.get(scene_id)
        if scene is None:
            gaps.append(f"unknown scene id {scene_id!r} — no scenes/{scene_id}.yaml")
            continue
        records.append(scene)
        attendance[scene_id] = scenes_mod.attendance(scene, narrator)
        if attendance[scene_id] == "absent":
            warnings.append(
                f"{narrator} has no route to scene {scene_id!r} — not a participant and not "
                "in heard_by; do not place them near it")
    return records, attendance


def _turn(outline: dict, section: dict, gaps: list[str]) -> dict:
    """Who else is speaking, and which turn this one answers — multi-voice episodes only.

    A monologue pack gains nothing here, so it is byte-for-byte what it was. In an episode
    whose sections alternate between voices, the writer needs the other speakers (they are
    the listener) and the previous section (the turn it is replying to); the prose of that
    turn is staging, not evidence, and is read from `sections/` at write time.
    """
    if not common.is_multi_voice(outline):
        return {}
    voices = common.episode_narrators(outline)
    declared = [str(v) for v in outline.get("narrators") or []]
    if not section.get("narrator"):
        gaps.append(f"section {section.get('id')!r} names no `narrator:` in a multi-voice "
                    f"episode ({', '.join(voices)})")
    elif declared and section["narrator"] not in declared:
        gaps.append(f"section {section.get('id')!r} narrator {section['narrator']!r} is not "
                    f"one of the episode's `narrators:` ({', '.join(declared)})")
    narrator = common.section_narrator(outline, section)
    sections = outline.get("sections") or []
    idx = next(i for i, s in enumerate(sections) if s.get("id") == section.get("id"))
    prev = sections[idx - 1] if idx > 0 else None
    return {
        "voices": voices,
        "listeners": [v for v in voices if v != narrator],
        "previous": ({"id": prev["id"], "narrator": common.section_narrator(outline, prev)}
                     if prev else None),
    }


def _subject(repo: "Repo", outline: dict, warnings: list[str]) -> dict:
    """Who the episode is about, and where the writer reads them.

    Shepard is the default and needs no explanation — he is in the corpus, in the scene
    records, in every narrator's life. A named subject is usually not: an original
    character never appears in `participants` or `heard_by`, so the attendance machinery
    can only ever say "absent" about them. That is a property of the corpus, not a fact
    about the evening, and the writer is told so here rather than left to infer it — along
    with the rule for reading it: the notes' timeline stretches govern where they were,
    not the guest list of any one occasion.
    """
    slug = common.episode_subject(outline)
    rel = common.subject_notes_rel(slug)
    exists = (repo.root / rel).is_file()
    if not exists:
        warnings.append(f"the episode's subject {slug!r} has no {rel} — the writer has "
                        f"nothing to characterize them from")
    if slug != common.DEFAULT_SUBJECT:
        warnings.append(
            f"{common.display_name(slug)} is the subject but is not in the corpus: no scene "
            f"record will ever list them in `participants` or `heard_by`, so a record's "
            f"silence is not absence. Their presence comes from {rel}, by its timeline "
            f"stretches rather than its named occasions — where those notes put them with "
            f"the crew they were at that period's occasions too, and outside those "
            f"stretches they were not there. The notes still bind absolutely on the "
            f"load-bearing facts: relationships, habits, dates, deaths, deeds.")
    return {"slug": slug, "display": common.display_name(slug),
            "notes": rel if exists else "", "default": slug == common.DEFAULT_SUBJECT}


def _entities(section: dict, scene_records: list[dict], narrator: str) -> list[str]:
    """What this section is about, for narrowing the canon store."""
    out = {narrator, *(section.get("scenes") or []), *(section.get("events") or [])}
    for scene in scene_records:
        out.update(str(p) for p in scene.get("participants") or [])
    out.update(str(k) for k in section.get("retrieval") or [])
    return sorted(e for e in out if e)


def _evidence(repo: Repo, section: dict, gaps: list[str]) -> list[dict]:
    """Run each retrieval key with a per-kind budget; a key that finds nothing is a gap."""
    out: list[dict] = []
    seen: set[str] = set()
    for key in section.get("retrieval") or []:
        hits = retrieve.retrieve_by_kind(repo.index, [key], per_kind=PER_KIND)
        if not hits:
            gaps.append(f"retrieval key {key!r} returned nothing in any kind")
            continue
        for hit in hits:
            if hit["chunk_id"] in seen:
                continue
            seen.add(hit["chunk_id"])
            out.append({
                "chunk_id": hit["chunk_id"], "kind": hit["kind"], "page": hit.get("page", ""),
                "section": hit.get("section", ""), "game": hit.get("game", ""),
                "scene_id": hit.get("scene_id", ""), "text": hit["text"],
                "url": hit.get("url", ""), "for_key": key,
            })
    return out


def _codex(repo: Repo, section: dict) -> list[dict]:
    """Codex lines touching this section's keys, cited by file and line.

    A codex bullet carries the authority of a sourced chunk with none of the traceability,
    so it arrives here located precisely enough to check.
    """
    keys = [k.lower() for k in (section.get("retrieval") or []) if k]
    out: list[dict] = []
    if not repo.codex_dir.is_dir():
        return out
    for path in sorted(repo.codex_dir.glob("*.md")):
        rel = f"codex/{path.name}"
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            low = line.lower()
            for key in keys:
                terms = [t for t in key.split() if len(t) > 3]
                if terms and all(t in low for t in terms):
                    out.append({"file": rel, "line": n, "text": line.strip(), "for_key": key})
                    break
    return out


#: The protagonist is in every scene, so an override scoped only to them is a standing fact
#: about who Shepard is — not a dispute with any particular staging. It reaches the pack as
#: canon either way; it just does not get reported as a conflict forty times. The episode's
#: subject joins this set when a run names one: they are as ever-present as Shepard is.
_UBIQUITOUS = {"shepard", "commander shepard"}


def _conflicts(canon_entries: list[dict], scene_records: list[dict],
               ubiquitous: set[str] = _UBIQUITOUS) -> list[dict]:
    """Where canon and a scene record speak to the same occasion.

    Split authority: the canon store owns *which branch happened*, the corpus owns *how it
    was staged*. An `overrides.yaml` entry is the exception — it was marked deliberate, so
    it owns both, and the scene record yields where the two disagree.

    A conflict is only raised where the override actually bears on this occasion: its scope
    names the scene, or someone in it other than the protagonist.
    """
    out: list[dict] = []
    for scene in scene_records:
        names = {str(p).lower() for p in scene.get("participants") or []} - ubiquitous
        names.add(scene["scene_id"].lower())
        for entry in canon_entries:
            if entry["authority"] == "override":
                scope = [s.lower() for s in entry.get("scope") or []]
                if not scope or not any(s in n or n in s for s in scope for n in names):
                    continue
                out.append({
                    "canon_id": entry["id"],
                    "config_said": entry["statement"],
                    "evidence_said": f"scenes/{scene['scene_id']}.yaml — {scene['title']}",
                    "resolution": (
                        f"override {entry['id']!r} is authoritative over the corpus; where the "
                        f"scene record disagrees, the override is narrated and the record is not"),
                })
    return out


# --------------------------------------------------------------------------
# rendering + writing
# --------------------------------------------------------------------------

def _form_description(repo: "Repo", form_id: str) -> str:
    """The form's own description from `config/forms.yaml`, or "" when it can't be read.

    The section-writer sees nothing but the pack, so the form has to travel inside it: an
    id alone says nothing about what the section is *doing*. A missing or unreadable forms
    file is not worth failing a build over — the id still ships.
    """
    if not form_id:
        return ""
    path = repo.root / "config" / "forms.yaml"
    if not path.is_file():
        path = common.FORMS_PATH
    try:
        form = common.load_forms(path).get(form_id) or {}
    except (OSError, ValueError):
        return ""
    return " ".join(str(form.get("description", "")).split())


def _as_markdown(pack: dict) -> str:
    s = pack["section"]
    lines = [f"# Pack — {s['title']}", "",
             f"`{s['id']}` · form `{s['form']}` · target {s['target_words']} words", ""]
    if s.get("voices"):
        prev = s.get("previous")
        lines += [f"Voice: **{s['narrator']}**, speaking to {', '.join(s['listeners'])}. "
                  + (f"Answers `{prev['id']}` ({prev['narrator']})." if prev
                     else "Opens the exchange."), ""]

    def block(title: str, rows: list[str]) -> None:
        lines.append(f"## {title}")
        lines.extend(rows or ["_(none)_"])
        lines.append("")

    sub = pack["subject"]
    block("Subject", [
        f"The episode is about **{sub['display']}** — whom the narrator addresses and "
        f"characterizes."]
        + ([f"Read `{sub['notes']}`."] if sub["notes"] else ["_(no notes file)_"]))
    block("Form", [f"**{s['form'] or 'unset'}** — {s.get('form_description') or '_(no description)_'}",
                   "", f"This run's note: {s.get('form_note') or '_(none)_'}"])
    block("Promises", [f"- {p}" for p in pack["promises"]])
    block("Required facts", [f"- ({f['event_id']}) {f['fact']}" for f in pack["required_facts"]])
    block("Canon", [f"- **{c['id']}** [{c['authority']}] "
                    f"{c.get('answer') or c.get('statement', '')}" for c in pack["canon"]])
    block("Attendance", [f"- `{k}` — **{v}**" for k, v in pack["attendance"].items()])
    block("Scenes", [f"- `{sc['scene_id']}` {sc['title']} ({sc['kind']}, {sc['when']}) — "
                     f"{len(sc.get('beats') or [])} beats" for sc in pack["scenes"]])
    block("Conflicts", [f"- **{c['canon_id']}**: {c['resolution']}" for c in pack["conflicts"]])
    block("Codex", [f"- `{c['file']}:{c['line']}` {c['text']}" for c in pack["codex"]])
    block("Evidence", [f"- `{e['chunk_id']}` [{e['kind']}] ({e['for_key']}) — {e['text']}"
                       for e in pack["evidence"]])
    block("Warnings", [f"- {w}" for w in pack["warnings"]])
    return "\n".join(lines)


def build(repo: Repo, run_dir: Path, section_id: str, *, allow_thin: bool = False) -> dict:
    """Assemble one pack, write it, and return it. Raises ``ThinPack`` on a gap."""
    run_dir = Path(run_dir)
    outline = _load_outline(run_dir)
    section = _section(outline, section_id)
    narrator = common.section_narrator(outline, section)

    gaps: list[str] = []
    warnings: list[str] = []
    turn = _turn(outline, section, gaps)

    subject = _subject(repo, outline, warnings)
    required_facts = _required_facts(repo, section, gaps)
    scene_records, attendance = _scene_records(repo, section, narrator, gaps, warnings)
    evidence = _evidence(repo, section, gaps)

    store = canon_mod.load_canon(repo.canon_dir)
    entries = canon_mod.filter_for(store, _entities(section, scene_records, narrator))["canon"]
    conflicts = _conflicts(entries, scene_records,
                           _UBIQUITOUS | {subject["slug"], subject["display"].lower()})

    if not (section.get("events") or section.get("scenes")):
        gaps.append(f"section {section_id!r} anchors to neither an event nor a scene")

    if gaps:
        if not allow_thin:
            raise ThinPack("; ".join(gaps))
        warnings.extend(gaps)

    form_id = outline.get("form", "")
    pack = {
        "section": {"id": section["id"], "title": section.get("title", section["id"]),
                    "target_words": section.get("target_words", 0),
                    "form": form_id, "form_description": _form_description(repo, form_id),
                    "form_note": outline.get("form_note", "") or "",
                    "narrator": narrator, **turn},
        "subject": subject,
        "promises": list(section.get("promises") or []),
        "required_facts": required_facts,
        "canon": entries,
        "scenes": scene_records,
        "attendance": attendance,
        "evidence": evidence,
        "codex": _codex(repo, section),
        "conflicts": conflicts,
        "warnings": warnings,
    }

    for conflict in conflicts:
        _log_once(repo, run_dir, section_id, conflict)

    packs = run_dir / "packs"
    packs.mkdir(parents=True, exist_ok=True)
    (packs / f"{section_id}.json").write_text(
        json.dumps(pack, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    (packs / f"{section_id}.md").write_text(_as_markdown(pack) + "\n", encoding="utf-8")
    return pack


def _log_once(repo: Repo, run_dir: Path, section_id: str, conflict: dict) -> None:
    """Record a silently-settled conflict, without re-logging it on every rebuild."""
    existing = canon_mod._load_list(repo.canon_dir / "resolved.yaml", "resolved")
    for row in existing:
        if row.get("section") == section_id and row.get("config_said") == conflict["config_said"]:
            return
    canon_mod.log_resolution(repo.canon_dir, yaml.safe_dump({
        "run": Path(run_dir).name,
        "section": section_id,
        "config_said": conflict["config_said"],
        "evidence_said": conflict["evidence_said"],
        "resolution": conflict["resolution"],
    }, sort_keys=False, allow_unicode=True))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build a section's evidence pack.")
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("section_id", nargs="?", help="omit with --all")
    ap.add_argument("--all", action="store_true", help="build every section in the outline")
    ap.add_argument("--allow-thin", action="store_true",
                    help="downgrade the hard stop to a warning — you are choosing to write "
                         "a section the corpus cannot ground")
    ap.add_argument("--root", type=Path, default=None, help="repo root (default: this repo)")
    args = ap.parse_args(argv)

    repo = Repo(Path(args.root)) if args.root else default_repo()
    try:
        outline = _load_outline(args.run_dir)
    except ThinPack as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.all:
        wanted = [s["id"] for s in outline.get("sections") or []]
    elif args.section_id:
        wanted = [args.section_id]
    else:
        ap.error("give a section id or --all")

    failed = 0
    for section_id in wanted:
        try:
            pack = build(repo, args.run_dir, section_id, allow_thin=args.allow_thin)
        except ThinPack as exc:
            print(f"error: {section_id}: {exc}", file=sys.stderr)
            failed += 1
            continue
        print(f"{section_id}: {len(pack['evidence'])} evidence, {len(pack['scenes'])} scene(s), "
              f"{len(pack['canon'])} canon, {len(pack['warnings'])} warning(s)")
        for w in pack["warnings"]:
            print(f"  warning: {w}", file=sys.stderr)
    if failed:
        print(f"{failed} section(s) could not be grounded — fix the outline's keys, or "
              f"re-run with --allow-thin to write them anyway", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
