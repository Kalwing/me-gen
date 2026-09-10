"""Backfill ``config/canon/choices.yaml`` with any canonical decision point
it is still missing.

The questionnaire captures the player's canon (see ``narrative_choices.py``).
New choices get added to the pipeline over time; this script keeps a player's
working copy in step by appending a blank stub — ``answer: ""``, ``detail: ""`` —
for every catalogue entry whose ``id`` is absent from its group. Existing
questions, answers, ordering and the file's header comment are never touched, so
the script is safe to re-run and a no-op once the file is complete.

Run it after ``/me-build-timeline``:

    python scripts/sync_narrative_choices.py config/canon/choices.yaml
    python scripts/sync_narrative_choices.py config/canon/choices.yaml --check
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
        {"id": "toombs_fate", "prompt": "I Remember Me - Corporal Toombs and Dr. Wayne at the Cerberus survival lab.", "options": []},
        {"id": "major_kyle", "prompt": "The Cult - Major Kyle and the biotic commune on Presrop.", "options": []},
        {"id": "rana_thanoptis", "prompt": "Rana Thanoptis, the asari researcher, on Virmire (she reappears in Mass Effect 2).", "options": []},
        {"id": "noveria_garage_evidence", "prompt": "Noveria - Qui'in's evidence of Anoleis's corruption.", "options": []},
        {"id": "gianna_parasini", "prompt": "Noveria - helping Gianna Parasini move against Anoleis and Hermia.", "options": []},
        {"id": "helena_blake", "prompt": "Helena Blake's crime syndicate (resolved with Aria in Mass Effect 2).", "options": []},
        {"id": "fist_fate", "prompt": "Fist at Chora's Den and the evidence handed to Barla Von's contact.", "options": []},
        {"id": "scan_the_keepers", "prompt": "Scan the Keepers - Chorban and Jahleed's keeper-scanning project on the Citadel.", "options": []},
        {"id": "doctor_michel", "prompt": "Dr. Chloe Michel and the blackmail at the Citadel med clinic.", "options": []},
        {"id": "citadel_jenna_chora_den", "prompt": "Rita's sister Jenna undercover at Chora's Den, and Chellick's arms sting.", "options": []},
        {"id": "emily_wong_data", "prompt": "Emily Wong and Fist's data on the Shadow Broker.", "options": []},
        {"id": "admiral_kahoku", "prompt": "Admiral Kahoku, the missing marines, and the Cerberus labs at Binthu.", "options": []},
        {"id": "pinnacle_station", "prompt": "Pinnacle Station - Ahern's survival wager.", "options": []},
        {"id": "ernesto_zabaleta", "prompt": "Old, Unhappy, Far-off Things - the veteran Ernesto Zabaleta on the Citadel.", "options": []},
        {"id": "noveria_espionage", "prompt": "Noveria - the espionage and wiretap job for the smugglers.", "options": []},
        {"id": "opold_smuggling", "prompt": "Noveria - the hanar Opold's package and Inamorda.", "options": []},
        {"id": "xeltans_complaint", "prompt": "Xeltan's Complaint and Sha'ira the Consort on the Citadel.", "options": []},
        {"id": "khalisah_al_jilani", "prompt": "The reporter Khalisah al-Jilani's interviews across the trilogy (charm, rebuff, or punch).", "options": []},
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
        {"id": "veetor_fate", "prompt": "Freedom's Progress - Veetor, handed to Cerberus or released to the Migrant Fleet.", "options": []},
        {"id": "kal_reegar_haestrom", "prompt": "Haestrom - Kal'Reegar during the retrieval of Tali.", "options": []},
        {"id": "mordin_grunt_dispute", "prompt": "The argument between Mordin and Grunt aboard the Normandy - whose side you took.", "options": []},
        {"id": "jack_miranda_dispute", "prompt": "The Jack and Miranda confrontation aboard the Normandy - whose side you took.", "options": []},
        {"id": "elnora_illium", "prompt": "Illium - Elnora, the asari who armed Morinth, during Samara's hunt.", "options": []},
        {"id": "patriarch_omega", "prompt": "Omega - the Patriarch's last stand during Aria's arc.", "options": []},
        {"id": "ish_citadel", "prompt": "The Citadel - Ish the smuggler and his packages.", "options": []},
        {"id": "blue_rose_illium", "prompt": "Illium - Charr and Ereba, the Blue Rose of Illium.", "options": []},
        {"id": "anaya_illium_cases", "prompt": "Illium - Officer Anaya, the volus murder, and Pitne For's smuggling.", "options": []},
        {"id": "darius_nonuel", "prompt": "The eezo negotiation on Nonuel and the Alliance-installed Darius.", "options": []},
        {"id": "daniel_hostage", "prompt": "Omega - the batarians holding Dr. Daniel Abbott near Mordin's clinic.", "options": []},
        {"id": "forvan_afterlife", "prompt": "Omega - Forvan and the poisoned drink at Afterlife.", "options": []},
        {"id": "jonn_whitson", "prompt": "Omega - the freelancer Jonn Whitson during the Archangel job.", "options": []},
        {"id": "nassana_dantius", "prompt": "Illium - Nassana Dantius during Thane's recruitment.", "options": []},
        {"id": "niftu_cal", "prompt": "Illium - Niftu Cal, the biotic god volus, during Samara's recruitment.", "options": []},
        {"id": "liara_observer", "prompt": "Illium - Liara's hunt for the Observer in her own office.", "options": []},
        {"id": "flux_signal_tracking", "prompt": "Citadel - Signal Tracking and the rogue AI signal at Flux.", "options": []},
        {"id": "schells_gambler", "prompt": "Citadel - Schells the gambler and his casino scanner.", "options": []},
        {"id": "citadel_planting_a_bug", "prompt": "Citadel - planting a bug for C-Sec.", "options": []},
        {"id": "legion_cerberus", "prompt": "Whether Legion was handed over to Cerberus at the end of Mass Effect 2.", "options": []},
        {"id": "tali_legion_dispute", "prompt": "The Tali and Legion argument aboard the Normandy - whose side you took.", "options": []},
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
        {"id": "hanar_diplomat_zymandis", "prompt": "The indoctrinated hanar diplomat Zymandis and Jondum Bau (Kasumi present changes the outcome).", "options": []},
        {"id": "illusive_man_confrontation", "prompt": "The final confrontation with the Illusive Man on the Crucible.", "options": []},
        {"id": "koris_rannoch", "prompt": "Admiral Zaal'Koris shot down on Rannoch - save him or save his crew.", "options": []},
        {"id": "petrovsky_fate", "prompt": "Omega DLC - General Petrovsky's fate after Aria retakes Omega.", "options": []},
        {"id": "omega_reactor", "prompt": "Omega DLC - the reactor and the civilians in the path of the power routing.", "options": []},
        {"id": "gellix_scientists", "prompt": "Gellix - rescuing Brynn Cole and the defecting Cerberus scientists.", "options": []},
        {"id": "burns_l2_reparations", "prompt": "MSV Ontario - Burns and the L2 biotic reparations standoff.", "options": []},
        {"id": "terra_firma_saracino", "prompt": "Citadel - the Terra Firma protest and endorsing Charles Saracino.", "options": []},
        {"id": "petrovsky_family_argument", "prompt": "Citadel - the Petrovsky family's argument over therapy.", "options": []},
        {"id": "presidium_hanar_preacher", "prompt": "Citadel Presidium - the preaching hanar and the permit dispute.", "options": []},
        {"id": "sommers_csec", "prompt": "Citadel - Bailey and the Sommers C-Sec justice case.", "options": []},
        {"id": "kelly_me3", "prompt": "Kelly Chambers at the Citadel refugee camp - the spying reprimand and the dinner invitation.", "options": []},
        {"id": "wrex_citadel_standoff", "prompt": "The Wrex genophage standoff in the Normandy docking bay - whether C-Sec kills him.", "options": []},
        {"id": "ghorek_mercy", "prompt": "Citadel - the dying krogan Ghorek and the question of mercy.", "options": []},
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
    ap.add_argument("path", type=Path, nargs="?", default=nc.CHOICES_PATH,
                    help="path to the choices questionnaire (default: config/canon/choices.yaml)")
    ap.add_argument(
        "--check",
        action="store_true",
        help="report missing choices and exit 1 without writing",
    )
    args = ap.parse_args(argv)
    args.path = nc.resolve_path(args.path)

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
