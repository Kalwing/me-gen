"""(Re)build timeline/master_timeline.yaml from timeline/events/*.yaml.

master_timeline.yaml is a *derived* index: this rebuilds it from whatever event
files exist, sorted by chronological_order and deduplicated. It is written
atomically (temp + rename), and event files that fail to parse or are missing
keys are skipped rather than aborting the rebuild — so an interrupted
`/me-build-timeline` can just be run again and this step always produces a
consistent index over the events completed so far.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from scripts import common

_KEYS = ("event_id", "title", "game", "chronological_order")


def rebuild(events_dir: Path, out_path: Path) -> int:
    events_dir, out_path = Path(events_dir), Path(out_path)
    rows: list[dict] = []
    seen: set[str] = set()
    for p in sorted(events_dir.glob("*.yaml")):
        try:
            ev = common.load_event(p)
        except (ValueError, yaml.YAMLError):
            continue  # half-written / malformed event file — skip, don't abort
        if ev["event_id"] in seen:
            continue
        seen.add(ev["event_id"])
        rows.append({k: ev[k] for k in _KEYS})
    rows.sort(key=lambda r: (r["chronological_order"], r["event_id"]))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_name(out_path.name + ".tmp")
    tmp.write_text(yaml.safe_dump(rows, sort_keys=False, allow_unicode=True),
                   encoding="utf-8")
    tmp.replace(out_path)
    return len(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Rebuild master_timeline.yaml from event files")
    ap.add_argument("--events", type=Path, default=Path("timeline/events"))
    ap.add_argument("--out", type=Path, default=Path("timeline/master_timeline.yaml"))
    a = ap.parse_args()
    n = rebuild(a.events, a.out)
    print(f"master_timeline.yaml: {n} events -> {a.out}")
