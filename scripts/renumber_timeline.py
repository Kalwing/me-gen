"""Deterministically renumber `chronological_order` across every timeline event.

Run this **once, after the whole `/me-build-timeline` sweep is complete**. The
sweep dispatches many `timeline-extractor` batches that each run in isolation and
guess a *global* `chronological_order` integer with no coordination — so ME3
events routinely land in the middle of the ME1 range and the master index is only
locally sorted. Nothing else fixes this.

This pass ignores the guessed integers' absolute values and re-derives the order
from data every event already carries:

    sort key = (year parsed from `date`, game rank ME1<ME2<ME3,
                current chronological_order as a local hint, event_id)

then rewrites `chronological_order` as 10, 20, 30, ... in that order. Only the
`chronological_order:` line of each event file is touched (surgical replace — the
rest of the file, including formatting, is left byte-for-byte). Idempotent: a
second run is a no-op.

Intra-year order stays approximate. A year like 2186 CE holds dozens of events;
within it the old per-batch hint is the only tiebreak, so mission-level sequence
inside a single year is not guaranteed correct — only the year and game are.

    python scripts/renumber_timeline.py            # renumber + rebuild master
    python scripts/renumber_timeline.py --dry-run  # show the plan, write nothing
    python scripts/renumber_timeline.py --check     # exit 1 if order has drifted
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from scripts import common  # noqa: E402

STEP = 10

_GAME_RANK = {
    "Mass Effect": 1,
    "Mass Effect 1": 1,
    "Mass Effect 2": 2,
    "Mass Effect 3": 3,
}
_ORDER_LINE = re.compile(r"^chronological_order:.*$", re.M)


def parse_year(date_str: object) -> int:
    """First 3-4 digit run in the `date` field ('2157-2158 CE' -> 2157,
    'approx. 1980s CE' -> 1980). 9999 (sorts last) if nothing parses."""
    m = re.search(r"\d{3,4}", str(date_str or ""))
    return int(m.group()) if m else 9999


def game_rank(game_str: object) -> int:
    g = str(game_str or "").strip()
    if g in _GAME_RANK:
        return _GAME_RANK[g]
    m = re.search(r"[123]", g)
    return int(m.group()) if m else 1


def sort_key(ev: dict) -> tuple:
    return (
        parse_year(ev.get("date")),
        game_rank(ev.get("game")),
        ev.get("chronological_order", 0),
        ev["event_id"],
    )


def _load_all(events_dir: Path) -> list[tuple[Path, dict]]:
    out: list[tuple[Path, dict]] = []
    for p in sorted(Path(events_dir).glob("*.yaml")):
        try:
            out.append((p, common.load_event(p)))
        except (ValueError, yaml.YAMLError):
            print(f"  skip (unparseable): {p}", file=sys.stderr)
    return out


def plan(events_dir: Path) -> list[tuple[Path, dict, int, int]]:
    """Return [(path, event, old_order, new_order), ...] in the new order."""
    rows = _load_all(events_dir)
    rows.sort(key=lambda pe: sort_key(pe[1]))
    return [
        (p, ev, ev.get("chronological_order"), (i + 1) * STEP)
        for i, (p, ev) in enumerate(rows)
    ]


def renumber(events_dir: Path, *, dry_run: bool = False) -> int:
    changed = 0
    for p, _ev, old, new in plan(events_dir):
        if old == new:
            continue
        changed += 1
        if dry_run:
            continue
        text = p.read_text(encoding="utf-8")
        new_text, n = _ORDER_LINE.subn(f"chronological_order: {new}", text, count=1)
        if n != 1:
            raise RuntimeError(f"{p}: expected one 'chronological_order:' line, found {n}")
        tmp = p.with_name(p.name + ".tmp")
        tmp.write_text(new_text, encoding="utf-8")
        tmp.replace(p)
    return changed


def check(events_dir: Path) -> list[str]:
    """Report events whose stored order disagrees with the deterministic order.

    Compares the sequence you get sorting by (chronological_order, event_id) with
    the sequence the deterministic sort_key produces. Empty list => in order.
    """
    rows = _load_all(events_dir)
    by_stored = [ev["event_id"] for _p, ev in
                 sorted(rows, key=lambda pe: (pe[1].get("chronological_order", 0), pe[1]["event_id"]))]
    by_derived = [ev["event_id"] for _p, ev in sorted(rows, key=lambda pe: sort_key(pe[1]))]
    return [f"{a}  !=  {b}" for a, b in zip(by_stored, by_derived) if a != b]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--events", type=Path, default=Path("timeline/events"))
    ap.add_argument("--dry-run", action="store_true",
                    help="print the renumber plan; write nothing")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the stored order has drifted from the derived order")
    ap.add_argument("--no-rebuild", action="store_true",
                    help="skip rebuilding master_timeline.yaml afterwards")
    a = ap.parse_args()

    if a.check:
        drift = check(a.events)
        if drift:
            print(f"chronological_order drift ({len(drift)} events out of place):")
            for line in drift[:20]:
                print(f"  {line}")
            sys.exit(1)
        print("chronological_order: in deterministic order, nothing to do")
        sys.exit(0)

    if a.dry_run:
        rows = plan(a.events)
        moves = [(ev["event_id"], old, new) for _p, ev, old, new in rows if old != new]
        for eid, old, new in moves:
            print(f"  {old!s:>6} -> {new:<6}  {eid}")
        print(f"{len(moves)} of {len(rows)} events would move")
        sys.exit(0)

    n = renumber(a.events)
    print(f"renumbered {n} event file(s) in steps of {STEP}")
    if not a.no_rebuild:
        from scripts import rebuild_master_timeline as rmt
        total = rmt.rebuild(a.events, Path("timeline/master_timeline.yaml"))
        print(f"master_timeline.yaml: {total} events")
