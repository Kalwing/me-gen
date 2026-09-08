"""Resolve the canon store (``config/canon/``) into the single view agents consume.

The store is split by who writes each file, so the file the user lives in is never
machine-rewritten:

``choices.yaml``    the player's questionnaire — user-owned, agents never write it.
``overrides.yaml``  canon that beats the corpus — user-owned, agents never write it.
``questions.yaml``  what an agent could not resolve — agent-appended, user-answered.
``resolved.yaml``   conflicts settled under split authority — agent-appended audit log.

Authority runs override > question > choices. A choice settles *which branch happened*;
only an override settles staging against the corpus as well.

Usage::

    python scripts/canon.py                       # human summary
    python scripts/canon.py --json                # machine view
    python scripts/canon.py --for 'Wrex,Grunt' --json
    python scripts/canon.py --ask 'question: ...' # append to questions.yaml
    python scripts/canon.py --log-resolution 'resolution: ...'

Open questions and unanswered choices warn on stderr. They never block a run.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

import yaml

from scripts import narrative_choices as nc
from scripts.common import REPO_ROOT

CANON_DIR = REPO_ROOT / "config" / "canon"

# Highest authority first — this is the order entries come back in.
_AUTHORITY_RANK = {"override": 0, "question": 1, "choices": 2}

GROUP_LABELS = nc.GROUP_LABELS


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------

def _load_list(path: Path, key: str) -> list[dict]:
    """Read the ``key:`` list out of one agent-appended file. Absent/empty is fine."""
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = data.get(key) or []
    if not isinstance(items, list):
        raise ValueError(f"{path}: {key!r} must be a list")
    return [i for i in items if isinstance(i, dict)]


def _choice_entries(choices: dict) -> tuple[list[dict], list[str]]:
    entries: list[dict] = []
    unanswered: list[str] = []
    for group, questions in choices.items():
        for q in questions:
            answer = nc._answer(q)
            qid = str(q.get("id", "?"))
            if not answer:
                unanswered.append(f"{group}.{qid}")
                continue
            entries.append({
                "id": qid,
                "authority": "choices",
                "group": group,
                "prompt": nc._norm(q.get("prompt")),
                "answer": answer,
                "detail": nc._norm(q.get("detail")),
            })
    return entries, unanswered


def _override_entries(overrides: list[dict]) -> list[dict]:
    return [{
        "id": str(o.get("id", "?")),
        "authority": "override",
        "kind": nc._norm(o.get("kind")) or "correction",
        "scope": [nc._norm(s) for s in (o.get("scope") or [])],
        "statement": nc._norm(o.get("statement")),
        "overrides": nc._norm(o.get("overrides")),
        "added": nc._norm(o.get("added")),
    } for o in overrides]


def _is_open(q: dict) -> bool:
    status = nc._norm(q.get("status")).lower()
    if status in ("answered", "closed"):
        return False
    return not nc._norm(q.get("answer"))


def load_canon(canon_dir: Path = CANON_DIR) -> dict:
    """Merge the four files into one resolved view.

    A missing store is not an error — generation falls back to default canon.
    """
    canon_dir = Path(canon_dir)
    choices_path = canon_dir / "choices.yaml"
    choices = nc.load_choices(choices_path) if choices_path.exists() else {}

    choice_entries, unanswered = _choice_entries(choices)
    overrides = _override_entries(_load_list(canon_dir / "overrides.yaml", "overrides"))
    questions = _load_list(canon_dir / "questions.yaml", "questions")
    resolved = _load_list(canon_dir / "resolved.yaml", "resolved")

    answered_questions = [{
        "id": str(q.get("id", "?")),
        "authority": "question",
        "group": "questions",
        "prompt": nc._norm(q.get("question")),
        "answer": nc._norm(q.get("answer")),
        "detail": nc._norm(q.get("context")),
    } for q in questions if not _is_open(q)]

    entries = overrides + answered_questions + choice_entries
    entries.sort(key=lambda e: _AUTHORITY_RANK.get(e["authority"], 9))
    return {
        "canon": entries,
        "unanswered": unanswered,
        "open_questions": [q for q in questions if _is_open(q)],
        "resolved": resolved,
    }


# --------------------------------------------------------------------------
# filtering
# --------------------------------------------------------------------------

def _touches(entity: str, text: str) -> bool:
    return bool(entity) and entity in text


def _entry_matches(entry: dict, entities: list[str]) -> bool:
    if entry["authority"] == "override":
        scope = [s.lower() for s in entry.get("scope") or []]
        if not scope:
            return True  # unscoped override governs everywhere
        return any(e in s or s in e for s in scope for e in entities)
    haystack = " ".join(str(entry.get(k, "")) for k in ("id", "prompt", "answer", "detail")).lower()
    return any(_touches(e, haystack) for e in entities)


def filter_for(store: dict, entities: list[str]) -> dict:
    """Narrow a resolved store to the canon bearing on a section's entities.

    This is what goes into an evidence pack: the handful of canon facts that touch
    this section, not the whole questionnaire.
    """
    wanted = [e.strip().lower() for e in entities if e and e.strip()]
    out = dict(store)
    out["canon"] = [e for e in store["canon"] if _entry_matches(e, wanted)]
    return out


# --------------------------------------------------------------------------
# appending (agent-owned files only)
# --------------------------------------------------------------------------

def _parse_fragment(fragment: str) -> dict:
    """Accept inline YAML or a path to a YAML file. Must resolve to one mapping."""
    text = fragment
    candidate = Path(fragment)
    try:
        if candidate.is_file():
            text = candidate.read_text(encoding="utf-8")
    except OSError:
        pass
    data = yaml.safe_load(text)
    if isinstance(data, list) and len(data) == 1:
        data = data[0]
    if not isinstance(data, dict):
        raise ValueError("fragment must be a YAML mapping (or a file holding one)")
    return data


def _next_id(prefix: str, existing: list[dict]) -> str:
    today = _dt.date.today().isoformat()
    stem = f"{prefix}-{today}-"
    taken = {str(i.get("id", "")) for i in existing}
    n = 1
    while f"{stem}{n:03d}" in taken:
        n += 1
    return f"{stem}{n:03d}"


def _append(path: Path, key: str, entry: dict) -> None:
    """Append one item under ``key:`` as text, so the file's comments survive."""
    text = path.read_text(encoding="utf-8") if path.exists() else f"{key}:\n"
    if f"{key}:" not in text:
        text = text.rstrip("\n") + f"\n{key}:\n"
    block = yaml.safe_dump([entry], sort_keys=False, allow_unicode=True, width=88)
    indented = "".join(f"  {line}\n" for line in block.rstrip("\n").splitlines())
    path.write_text(text.rstrip("\n") + "\n" + indented, encoding="utf-8")


def ask(canon_dir: Path, fragment: str) -> str:
    """Append an unresolved question to ``questions.yaml``; return its id.

    Idempotent on the question text, so a re-run of the same section does not fill
    the user's inbox with duplicates.
    """
    canon_dir = Path(canon_dir)
    path = canon_dir / "questions.yaml"
    data = _parse_fragment(fragment)
    question = nc._norm(data.get("question"))
    if not question:
        raise ValueError("--ask fragment needs a `question:` field")

    existing = _load_list(path, "questions")
    for q in existing:
        if nc._norm(q.get("question")) == question:
            return str(q.get("id", "?"))

    entry = {
        "id": str(data.get("id") or _next_id("q", existing)),
        "raised_by": nc._norm(data.get("raised_by")),
        "question": question,
        "context": nc._norm(data.get("context")),
        "options": list(data.get("options") or []),
        "answer": nc._norm(data.get("answer")),
        "status": nc._norm(data.get("status")) or "open",
    }
    _append(path, "questions", entry)
    return entry["id"]


def log_resolution(canon_dir: Path, fragment: str) -> str:
    """Append a settled conflict to ``resolved.yaml``; return its id."""
    canon_dir = Path(canon_dir)
    path = canon_dir / "resolved.yaml"
    data = _parse_fragment(fragment)
    if not nc._norm(data.get("resolution")):
        raise ValueError("--log-resolution fragment needs a `resolution:` field")

    existing = _load_list(path, "resolved")
    entry = {
        "id": str(data.get("id") or _next_id("r", existing)),
        "run": nc._norm(data.get("run")),
        "section": nc._norm(data.get("section")),
        "config_said": nc._norm(data.get("config_said")),
        "evidence_said": nc._norm(data.get("evidence_said")),
        "resolution": nc._norm(data.get("resolution")),
        "date": nc._norm(data.get("date")) or _dt.date.today().isoformat(),
    }
    _append(path, "resolved", entry)
    return entry["id"]


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def _one_line(text: str, limit: int = 150) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[: limit - 1].rstrip() + "…"


def summary_text(store: dict) -> str:
    """Human-readable canon: grouped, authority marked, not a 55-item wall."""
    entries = store["canon"]
    if not entries:
        return "all questions unanswered"

    lines: list[str] = []
    overrides = [e for e in entries if e["authority"] == "override"]
    if overrides:
        lines.append("OVERRIDES — authoritative over the corpus")
        for e in overrides:
            scope = ", ".join(e["scope"]) or "everywhere"
            lines.append(f"  {e['id']} [{e['kind']}] ({scope})")
            lines.append(f"      {_one_line(e['statement'])}")
        lines.append("")

    by_group: dict[str, list[dict]] = {}
    for e in entries:
        if e["authority"] == "override":
            continue
        by_group.setdefault(e["group"], []).append(e)
    for group, items in by_group.items():
        lines.append(GROUP_LABELS.get(group, group.title()))
        for e in items:
            mark = " [answered question]" if e["authority"] == "question" else ""
            line = f"  {e['id']} = {e['answer']}{mark}"
            if e["detail"]:
                line += f" — {_one_line(e['detail'], 110)}"
            lines.append(line)
        lines.append("")
    return "\n".join(lines).rstrip()


def warnings_for(store: dict) -> list[str]:
    out = []
    if store["unanswered"]:
        out.append(
            f"{len(store['unanswered'])} unanswered choice(s) — default canon applies: "
            + ", ".join(store["unanswered"][:8])
            + ("…" if len(store["unanswered"]) > 8 else "")
        )
    for q in store["open_questions"]:
        out.append(f"open question {q.get('id', '?')}: {_one_line(nc._norm(q.get('question')))}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Resolve and query the canon store.")
    ap.add_argument("--canon-dir", type=Path, default=CANON_DIR)
    ap.add_argument("--for", dest="entities", default="",
                    help="comma-separated entities, scene ids or event ids to narrow to")
    ap.add_argument("--json", action="store_true", help="machine view")
    ap.add_argument("--ask", metavar="YAML", help="append a question to questions.yaml")
    ap.add_argument("--log-resolution", metavar="YAML", dest="log_resolution",
                    help="append a settled conflict to resolved.yaml")
    args = ap.parse_args(argv)

    if args.ask:
        print(ask(args.canon_dir, args.ask))
        return 0
    if args.log_resolution:
        print(log_resolution(args.canon_dir, args.log_resolution))
        return 0

    store = load_canon(args.canon_dir)
    if args.entities:
        store = filter_for(store, args.entities.split(","))

    if args.json:
        print(json.dumps(store, indent=2, ensure_ascii=False, default=str))
    else:
        print(summary_text(store))
    for w in warnings_for(store):
        print(f"warning: {w}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
