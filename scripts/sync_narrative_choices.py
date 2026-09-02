"""Backfill ``config/narrative_choices.yaml`` with any canonical decision point
it is still missing.

The questionnaire captures the player's canon (see ``narrative_choices.py``).
New choices get added to the pipeline over time; this script keeps a player's
working copy in step by appending a blank stub — ``answer: ""``, ``detail: ""`` —
for every catalogue entry whose ``id`` is absent from its group. Existing
questions, answers, ordering and the file's header comment are never touched, so
the script is safe to re-run and a no-op once the file is complete.

Run it after ``/me-build-timeline``:

    python scripts/sync_narrative_choices.py config/narrative_choices.yaml
    python scripts/sync_narrative_choices.py config/narrative_choices.yaml --check
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from pathlib import Path

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts import narrative_choices as nc

# Canonical trilogy decision points, in the order they should appear in each
# group. Every entry is a stub: {id, prompt, options}. `options: []` means the
# answer is free text. Keep prompts free of ": " so they emit unquoted.
CATALOG: dict[str, list[dict]] = {
    "shepard": [
        {"id": "background", "prompt": "Shepard's pre-service history.", "options": ["Spacer", "Colonist", "Earthborn"]},
        {"id": "profile", "prompt": "Shepard's psychological profile / reputation.", "options": ["Sole Survivor", "War Hero", "Ruthless"]},
        {"id": "class", "prompt": "Shepard's combat class.", "options": ["Soldier", "Engineer", "Adept", "Infiltrator", "Sentinel", "Vanguard"]},
        {"id": "gender", "prompt": "Shepard's gender / pronouns.", "options": []},
        {"id": "first_name", "prompt": "Shepard's first name.", "options": []},
        {"id": "alignment", "prompt": "Shepard's overall morality lean across the trilogy.", "options": ["Paragon", "Renegade", "mixed"]},
        {"id": "romance", "prompt": "Shepard's romance(s) across the trilogy.", "options": []},
    ],
    "me1": [
        {"id": "council_fate", "prompt": "The Council aboard the Destiny Ascension at the Battle of the Citadel.", "options": ["saved", "sacrificed"]},
        {"id": "kirrahe_virmire", "prompt": "Kirrahe and the salarian STG team at the Virmire base.", "options": []},
        {"id": "wrex_virmire", "prompt": "Wrex on Virmire.", "options": ["alive", "dead"]},
        {"id": "rachni_queen", "prompt": "The rachni queen on Noveria.", "options": ["freed", "killed"]},
        {"id": "virmire_survivor", "prompt": "Who survived Virmire.", "options": ["Ashley", "Kaidan"]},
        {"id": "feros_colony", "prompt": "Feros - the ExoGeni colonists, the Thorian, and Shiala's fate.", "options": []},
        {"id": "bring_down_the_sky", "prompt": "Bring Down the Sky - the batarian extremist Balak on Asteroid X57.", "options": ["Balak stopped", "Balak let go"]},
        {"id": "conrad_verner", "prompt": "The first run-in with Conrad Verner on the Citadel.", "options": ["talked him down", "drew a weapon on him"]},
        {"id": "saren_confrontation", "prompt": "Saren in the Citadel Tower.", "options": ["talked into suicide", "fought to the death"]},
        {"id": "council_composition", "prompt": "The new Council's composition after the battle (human-led, all-alien, who sits on it).", "options": []},
    ],
    "me2": [
        {"id": "zaeed_loyalty", "prompt": "Zaeed's loyalty mission - the refinery and Vido Santiago.", "options": []},
        {"id": "grunt_loyalty", "prompt": "Grunt's loyalty mission - the Rite of Passage on Tuchanka.", "options": []},
        {"id": "samara_loyalty", "prompt": "Samara's loyalty mission - the hunt for Morinth.", "options": ["Morinth killed", "Samara killed"]},
        {"id": "kasumi_loyalty", "prompt": "Kasumi's loyalty mission - Keiji's graybox.", "options": ["kept", "destroyed"]},
        {"id": "jacob_loyalty", "prompt": "Jacob's loyalty mission - his father on Aeia.", "options": []},
        {"id": "miranda_loyalty", "prompt": "Miranda's loyalty mission - protecting Oriana.", "options": []},
        {"id": "tali_trial", "prompt": "Tali's loyalty mission - the Alarei, the trial before the Admiralty Board, and the data on her father.", "options": []},
        {"id": "thane_loyalty", "prompt": "Thane's loyalty mission - his son Kolyat on the Citadel.", "options": []},
        {"id": "mordin_loyalty", "prompt": "Mordin's loyalty mission - Maelon and the genophage data.", "options": ["data saved", "data destroyed"]},
        {"id": "garrus_loyalty", "prompt": "Garrus's loyalty mission - Sidonis.", "options": ["Sidonis killed", "Sidonis spared"]},
        {"id": "legion_loyalty", "prompt": "Legion's loyalty mission - the heretic geth station.", "options": ["heretics rewritten", "heretics destroyed"]},
        {"id": "jack_meeting", "prompt": "The casual encounter Jack offers when first recruited.", "options": ["yes", "no"]},
        {"id": "jack_loyalty", "prompt": "Jack's loyalty mission - Aresh at the Pragia facility.", "options": ["Aresh spared", "Aresh shot"]},
        {"id": "overlord", "prompt": "Overlord - David Archer after the VI experiment.", "options": ["left with Cerberus", "sent to Grissom Academy"]},
        {"id": "loyalty_missions", "prompt": "Which squad loyalty missions were completed.", "options": []},
        {"id": "kelly_chambers", "prompt": "Yeoman Kelly Chambers after the Collector abduction.", "options": ["survived", "lost"]},
        {"id": "collector_base", "prompt": "The Collector Base after the Suicide Mission.", "options": ["destroyed", "kept"]},
        {"id": "suicide_mission", "prompt": "Who lived and who died in the Suicide Mission.", "options": []},
        {"id": "iff_delay", "prompt": "Whether the abducted Normandy crew survived (how long you delayed after the IFF mission).", "options": []},
        {"id": "shadow_broker", "prompt": "The Lair of the Shadow Broker - Liara and the Broker's fate.", "options": []},
        {"id": "arrival", "prompt": "The Arrival - the batarian Alpha Relay and the Bahak system.", "options": []},
    ],
    "me3": [
        {"id": "grissom_academy", "prompt": "Grissom Academy - Jack and the biotic students.", "options": []},
        {"id": "tuchanka_bomb", "prompt": "Priority Tuchanka - the genophage-project bomb.", "options": []},
        {"id": "genophage", "prompt": "The state of the genophage.", "options": ["cured", "sabotaged"]},
        {"id": "mordin_fate", "prompt": "Mordin at the Shroud during the genophage cure.", "options": ["died at the Shroud", "survived"]},
        {"id": "krogan_leader", "prompt": "The krogan leader during the cure (Wrex or Wreav).", "options": ["Wrex", "Wreav"]},
        {"id": "salarian_councilor", "prompt": "The salarian Dalatrass's offer to trade the cure for STG support.", "options": ["refused the deal", "took the deal"]},
        {"id": "geth_quarian", "prompt": "Geth versus quarians at Rannoch.", "options": ["peace", "geth destroyed", "quarians destroyed"]},
        {"id": "rannoch", "prompt": "Rannoch's outcome - who lived, Legion's fate, Tali's fate.", "options": []},
        {"id": "citadel_coup", "prompt": "The Cerberus coup on the Citadel - Udina, the Virmire survivor at gunpoint, Thane's intervention.", "options": []},
        {"id": "thessia", "prompt": "Thessia - the mission for the Prothean VI and Kai Leng.", "options": []},
        {"id": "grunt_fate", "prompt": "Grunt and Aralakh Company at the Attican Traverse rachni mission.", "options": []},
        {"id": "leviathan", "prompt": "Leviathan - tracking down and dealing with the Leviathans.", "options": []},
        {"id": "omega", "prompt": "The Omega DLC - whether Aria retook Omega.", "options": ["yes", "no"]},
        {"id": "miranda_fate", "prompt": "Miranda's fate at the Sanctuary facility.", "options": ["lived", "died"]},
        {"id": "samara_daughter", "prompt": "The Ardat-Yakshi monastery - Falere, Rila, and Samara's fate.", "options": []},
        {"id": "virmire_survivor_rejoins", "prompt": "Whether the Virmire survivor (see me1 virmire_survivor) rejoined the Normandy crew.", "options": ["yes", "no"]},
        {"id": "javik", "prompt": "Whether Javik joined the squad (From Ashes).", "options": ["yes", "no"]},
        {"id": "allers", "prompt": "Whether Diana Allers joined the Normandy as embedded press.", "options": ["yes", "no"]},
        {"id": "conrad", "prompt": "Whether Conrad Verner helped gather war assets on the Citadel.", "options": ["yes", "no"]},
        {"id": "joker_edi_romance", "prompt": "Joker and EDI's relationship - whether you encouraged it.", "options": ["encouraged", "discouraged"]},
        {"id": "citadel_dlc", "prompt": "The Citadel DLC outcome (the party, the clone, who showed up).", "options": []},
        {"id": "final_choice", "prompt": "The final choice at the Crucible.", "options": ["Destroy", "Control", "Synthesis", "Refuse"]},
        {"id": "shepard_fate", "prompt": "Shepard's fate at the end.", "options": []},
        {"id": "ending_epilogue", "prompt": "The epilogue beats - the squad's fate, the memorial wall, the Normandy, the stargazer.", "options": []},
    ],
}

GROUP_ORDER = list(CATALOG)


def _needs_quote(s: str) -> bool:
    return (
        not s
        or s != s.strip()
        or s[:1] in "-?:#*&!|>%@`\"'[]{},"
        or ": " in s
        or " #" in s
        or "\n" in s
    )


def _scalar(s: str) -> str:
    if _needs_quote(s):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def _fmt(stub: dict) -> str:
    opts = "[" + ", ".join(_scalar(str(o)) for o in stub.get("options") or []) + "]"
    return (
        f"  - id: {stub['id']}\n"
        f"    prompt: {_scalar(stub['prompt'])}\n"
        f"    options: {opts}\n"
        f'    answer: ""\n'
        f'    detail: ""\n'
    )


def missing(path: Path) -> list[tuple[str, str]]:
    """Return ``[(group, id), ...]`` for catalogue entries absent from the file."""
    data = nc.load_choices(path)
    out: list[tuple[str, str]] = []
    for group, stubs in CATALOG.items():
        have = {q["id"] for q in data.get(group, [])}
        out += [(group, s["id"]) for s in stubs if s["id"] not in have]
    return out


def sync(path: Path, *, write: bool = True) -> list[tuple[str, str]]:
    """Append a blank stub for every missing catalogue entry.

    Existing bytes (header comment, existing questions, formatting) are left
    exactly as they were; new stubs are inserted at the end of their group's
    block. Returns the ``(group, id)`` pairs that were added.
    """
    path = Path(path)
    added = missing(path)
    if not added or not write:
        return added

    added_by_group: dict[str, list[str]] = {}
    for group, qid in added:
        added_by_group.setdefault(group, []).append(qid)

    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    header_re = {f"{g}:" for g in GROUP_ORDER}
    hdr = {
        line.rstrip("\n"): i
        for i, line in enumerate(lines)
        if line.rstrip("\n") in header_re
    }
    positions = sorted(hdr.values())

    out: list[str] = lines[: positions[0]] if positions else list(lines)
    for j, start in enumerate(positions):
        end = positions[j + 1] if j + 1 < len(positions) else len(lines)
        group = lines[start].rstrip("\n")[:-1]
        block = lines[start:end]
        k = len(block)
        while k > 0 and block[k - 1].strip() == "":
            k -= 1
        body, trailer = block[:k], block[k:]
        out += body
        for qid in added_by_group.get(group, []):
            stub = next(s for s in CATALOG[group] if s["id"] == qid)
            out.append(_fmt(stub))
        out += trailer

    # Any catalogue group with no header in the file at all — append it whole.
    for group in GROUP_ORDER:
        if f"{group}:" not in hdr and group in added_by_group:
            if out and not out[-1].endswith("\n"):
                out.append("\n")
            out.append(f"\n{group}:\n")
            for qid in added_by_group[group]:
                stub = next(s for s in CATALOG[group] if s["id"] == qid)
                out.append(_fmt(stub))

    path.write_text("".join(out), encoding="utf-8")
    nc.load_choices(path)  # fail loudly if the rewrite produced anything invalid
    return added


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path, help="path to narrative_choices.yaml")
    ap.add_argument(
        "--check",
        action="store_true",
        help="report missing choices and exit 1 without writing",
    )
    args = ap.parse_args(argv)

    if not args.path.exists():
        print(f"{args.path}: not found", file=sys.stderr)
        return 2

    if args.check:
        gaps = sync(args.path, write=False)
        if gaps:
            for group, qid in gaps:
                print(f"missing: {group}.{qid}")
            return 1
        print("narrative_choices.yaml has every catalogue choice")
        return 0

    added = sync(args.path)
    if added:
        print(f"added {len(added)} stub(s) to {args.path}:")
        for group, qid in added:
            print(f"  + {group}.{qid}")
    else:
        print(f"{args.path} already has every catalogue choice")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
