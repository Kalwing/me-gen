"""The scene layer — occasions, and who was in the room.

``timeline/events/`` answers *what happened to the galaxy*. ``scenes/`` answers *what
happened between these people, and who was there to see it*. An episode built only on the
event spine structurally cannot have a section about a party, a hangout or a piece of
banter — that uniformity was the shape of the data, not a stylistic habit.

Every beat cites the chunks it came from, so compression cannot quietly drop causality.

Usage::

    python scripts/scenes.py --list
    python scripts/scenes.py --list --for wrex     # with attendance marked
    python scripts/scenes.py --show citadel-party-apartment
    python scripts/scenes.py --check               # validate the whole set
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

from scripts.common import REPO_ROOT

SCENES_DIR = REPO_ROOT / "scenes"
CHUNKS_PATH = REPO_ROOT / "data" / "chunks" / "chunks.jsonl"

KINDS = ("hangout", "party", "banter", "downtime", "ceremony", "mission-aside", "argument")

_REQUIRED = ("scene_id", "title", "kind", "game", "when", "where",
             "participants", "beats", "source_chunks")

#: Collective names that stand for "anyone who served aboard". A scene `heard_by` one of
#: these was ship gossip: every crew narrator may reference it, but only as hearsay.
CREW_GROUPS = {
    "normandy crew", "the normandy crew", "the crew", "crew",
    "ground team", "squad", "the squad",
}


# --------------------------------------------------------------------------
# loading + validation
# --------------------------------------------------------------------------

def load_scene(path: Path) -> dict:
    """Parse and validate one scene record."""
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: a scene file must hold one mapping")

    missing = [k for k in _REQUIRED if not data.get(k)]
    if missing:
        raise ValueError(f"{path}: missing or empty scene keys: {missing}")
    if data["scene_id"] != path.stem:
        raise ValueError(f"{path}: filename must match scene_id {data['scene_id']!r}")
    if data["kind"] not in KINDS:
        raise ValueError(f"{path}: kind {data['kind']!r} must be one of {KINDS}")

    for i, beat in enumerate(data["beats"]):
        if not isinstance(beat, dict) or not str(beat.get("text", "")).strip():
            raise ValueError(f"{path}: beat {i} has no text")
        if not beat.get("source_chunks"):
            raise ValueError(f"{path}: beat {i} has no source_chunks — every beat is traceable")
        if beat.get("conditional") and not str(beat.get("choice", "")).strip():
            raise ValueError(
                f"{path}: beat {i} has a conditional but no choice label — "
                "name what's being decided, e.g. choice: graybox destroyed"
            )

    participants = {_norm(p) for p in data["participants"]}
    stray = [p for p in (data.get("private_to") or []) if _norm(p) not in participants]
    if stray:
        raise ValueError(f"{path}: private_to names non-participants: {stray}")

    for i, variant in enumerate(data.get("variants") or []):
        if not variant.get("source_chunks"):
            raise ValueError(f"{path}: variant {i} has no source_chunks")
        if variant.get("condition") and not str(variant.get("choice", "")).strip():
            raise ValueError(
                f"{path}: variant {i} has a condition but no choice label — "
                "name what's being decided, e.g. choice: romanced Garrus"
            )

    data.setdefault("private_to", [])
    data.setdefault("heard_by", [])
    data.setdefault("requires", [])
    data.setdefault("variants", [])
    data.setdefault("related_scenes", [])
    data.setdefault("related_events", [])
    return data


def load_scenes(scenes_dir: Path = SCENES_DIR) -> dict[str, dict]:
    """Load every scene record, keyed by ``scene_id``."""
    out: dict[str, dict] = {}
    for p in sorted(Path(scenes_dir).glob("*.yaml")):
        scene = load_scene(p)
        sid = scene["scene_id"]
        if sid in out:
            raise ValueError(f"{p}: duplicate scene_id {sid!r}")
        out[sid] = scene
    return out


def cited_chunks(scene: dict) -> list[str]:
    """Every chunk id the record leans on — top level, beats and variants."""
    out = list(scene.get("source_chunks") or [])
    for block in list(scene.get("beats") or []) + list(scene.get("variants") or []):
        out.extend(block.get("source_chunks") or [])
    return sorted(set(out))


def known_chunk_ids(path: Path = CHUNKS_PATH) -> set[str]:
    path = Path(path)
    if not path.exists():
        return set()
    with path.open(encoding="utf-8") as fh:
        return {json.loads(line)["chunk_id"] for line in fh if line.strip()}


# --------------------------------------------------------------------------
# attendance
# --------------------------------------------------------------------------

def _norm(name: str) -> str:
    """Lowercase, and turn every separator into a space.

    Punctuation splits rather than vanishes, so "Tali'Zorah vas Normandy" tokenises to
    ``tali zorah vas normandy`` and the narrator id ``tali`` finds it.
    """
    return " ".join(re.sub(r"[^a-z0-9]+", " ", str(name or "").lower()).split())


def _names_match(narrator: str, listed: str) -> bool:
    """Does a narrator id match a name as written in a scene record?

    Records name people the way the wiki does ("Urdnot Wrex", "Tali'Zorah vas Normandy");
    narrators are bible ids ("wrex", "tali"). Match on whole words so "ash" cannot claim
    "Ashley" by accident.
    """
    n, l = _norm(narrator), _norm(listed)
    if not n or not l:
        return False
    return n == l or n in l.split() or l in n.split()


def attendance(scene: dict, narrator: str) -> str:
    """How this narrator may speak about this scene.

    ``witnessed`` — they were there; write it as seen.
    ``heard``     — it reached them afterwards; write it as gossip, inference or teasing.
    ``absent``    — they have no route to it; do not place them near it.
    """
    if any(_names_match(narrator, p) for p in scene.get("participants") or []):
        return "witnessed"
    for listed in scene.get("heard_by") or []:
        if _norm(listed) in CREW_GROUPS or _names_match(narrator, listed):
            return "heard"
    return "absent"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _list_line(scene: dict, narrator: str = "") -> str:
    who = ", ".join(scene.get("participants") or [])
    mark = f"  [{attendance(scene, narrator)}]" if narrator else ""
    return (f"{scene['scene_id']}  ({scene['kind']}, {scene['game']}){mark}\n"
            f"    {scene['title']} — {who}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Query the scene layer.")
    ap.add_argument("--scenes-dir", type=Path, default=SCENES_DIR)
    ap.add_argument("--list", action="store_true", help="one entry per scene")
    ap.add_argument("--show", metavar="SCENE_ID", help="print one full record")
    ap.add_argument("--for", dest="narrator", default="",
                    help="mark attendance for this narrator")
    ap.add_argument("--check", action="store_true",
                    help="validate every record and its chunk references")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    loaded = load_scenes(args.scenes_dir)

    if args.show:
        scene = loaded.get(args.show)
        if scene is None:
            print(f"unknown scene {args.show!r}", file=sys.stderr)
            return 1
        if args.narrator:
            scene = {**scene, "attendance": attendance(scene, args.narrator)}
        print(json.dumps(scene, indent=2, ensure_ascii=False, default=str) if args.json
              else yaml.safe_dump(scene, sort_keys=False, allow_unicode=True))
        return 0

    if args.check:
        known = known_chunk_ids()
        bad = []
        for scene in loaded.values():
            if known:
                bad += [f"{scene['scene_id']}: unknown chunk {c}"
                        for c in cited_chunks(scene) if c not in known]
            bad += [f"{scene['scene_id']}: unknown related scene {s}"
                    for s in scene["related_scenes"] if s not in loaded]
        for line in bad:
            print(line, file=sys.stderr)
        print(f"{len(loaded)} scene(s) checked")
        return 1 if bad else 0

    scenes_out = list(loaded.values())
    if args.narrator:
        scenes_out = [s for s in scenes_out if attendance(s, args.narrator) != "absent"]
    if args.json:
        print(json.dumps(scenes_out, indent=2, ensure_ascii=False, default=str))
    else:
        for scene in scenes_out:
            print(_list_line(scene, args.narrator))
        print(f"\n{len(scenes_out)} scene(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
