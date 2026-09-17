import json
from pathlib import Path

import pytest
import yaml

from scripts import build_bm25, build_pack


@pytest.fixture
def world(tmp_path):
    """A miniature repo: index, scenes, events, canon store and an approved outline."""
    root = tmp_path

    (root / "data" / "chunks").mkdir(parents=True)
    (root / "data" / "chunks" / "chunks.jsonl").write_text(
        '{"chunk_id": "party_001", "source": "party", "page": "Citadel: Party", "section": "", '
        '"game": "Mass Effect 3", "text": "Joker suggests throwing a party at the apartment.", '
        '"url": "u"}\n'
        '{"chunk_id": "monument_001", "source": "monument", "page": "Krogan Monument", '
        '"section": "", "game": "Mass Effect 3", '
        '"text": "The Krogan Monument is a statue of a krogan warrior in the Presidium lake.", '
        '"url": "u"}\n', encoding="utf-8")

    (root / "page_summaries").mkdir()
    (root / "page_summaries" / "krogan-monument.md").write_text(
        "---\ntitle: Krogan Monument\nurl: u\ngame: Mass Effect 3\ntype: location\n"
        "characters: [Grunt]\n---\n\nCommissioned to commemorate the krogan.\n", encoding="utf-8")

    (root / "scenes").mkdir()
    (root / "scenes" / "citadel-party-apartment.yaml").write_text(
        "scene_id: citadel-party-apartment\ntitle: The Party\nkind: party\n"
        "game: Mass Effect 3\nwhen: 2186\nwhere: the apartment\n"
        "participants: [Shepard, Urdnot Wrex, Grunt]\nheard_by: [Normandy crew]\n"
        "beats:\n  - text: Wrex and Grunt trade insults on the balcony.\n"
        "    source_chunks: [party_001]\nsource_chunks: [party_001]\n", encoding="utf-8")
    (root / "scenes" / "citadel-jack-private.yaml").write_text(
        "scene_id: citadel-jack-private\ntitle: Jack's Varren\nkind: hangout\n"
        "game: Mass Effect 3\nwhen: 2186\nwhere: the apartment\n"
        "participants: [Shepard, Jack]\nprivate_to: [Shepard, Jack]\nheard_by: []\n"
        "beats:\n  - text: Jack brings a varren.\n    source_chunks: [party_001]\n"
        "source_chunks: [party_001]\n", encoding="utf-8")

    (root / "timeline" / "events").mkdir(parents=True)
    (root / "timeline" / "events" / "citadel-dlc-archives.yaml").write_text(yaml.safe_dump({
        "event_id": "citadel-dlc-archives", "title": "The Archives", "game": "Mass Effect 3",
        "chronological_order": 100, "summary": "Shepard uncovered the clone in the Archives.",
        "characters": ["Shepard", "Urdnot Wrex"], "consequences": ["The Normandy was retaken."],
        "source_chunks": ["party_001"]}), encoding="utf-8")

    (root / "codex").mkdir()
    (root / "codex" / "places.md").write_text(
        "# Places\n\n- The Krogan Monument stands in the Presidium lake.\n", encoding="utf-8")

    (root / "config" / "canon").mkdir(parents=True)
    (root / "config" / "canon" / "choices.yaml").write_text(
        "me3:\n  - id: grunt_fate\n    prompt: Grunt\n    options: [alive]\n"
        "    answer: ''\n    detail: 'Saved the rachni, he got out alive'\n", encoding="utf-8")
    (root / "config" / "canon" / "overrides.yaml").write_text(
        "overrides:\n  - id: aralakh-died\n    kind: correction\n"
        "    scope: [Grunt, citadel-party-apartment]\n"
        "    statement: Aralakh Company was wiped out at Utukku.\n"
        "    overrides: the codex bullet\n    added: 2026-09-07\n", encoding="utf-8")
    (root / "config" / "canon" / "questions.yaml").write_text("questions:\n", encoding="utf-8")
    (root / "config" / "canon" / "resolved.yaml").write_text("resolved:\n", encoding="utf-8")

    index = root / "data" / "bm25_index.pkl"
    build_bm25.build(root / "data" / "chunks" / "chunks.jsonl", index,
                     summaries_dir=root / "page_summaries", scenes_dir=root / "scenes")

    run = root / "output" / "run1"
    (run / "packs").mkdir(parents=True)
    (run / "outline.yaml").write_text(yaml.safe_dump({
        "narrator": "wrex", "themes": ["war"], "brief": "", "form": "evening",
        "form_note": "one night", "target_words": 800,
        "sections": [{
            "id": "one-last-party", "title": "One Last Party",
            "events": ["citadel-dlc-archives"], "scenes": ["citadel-party-apartment"],
            "retrieval": ["krogan monument", "apartment party"],
            "promises": ["Wrex on the Monument"], "target_words": 800,
        }]}), encoding="utf-8")
    return build_pack.Repo(root), run


def test_pack_is_written_as_json_and_markdown(world):
    repo, run = world
    pack = build_pack.build(repo, run, "one-last-party")
    assert (run / "packs" / "one-last-party.json").is_file()
    assert (run / "packs" / "one-last-party.md").is_file()
    on_disk = json.loads((run / "packs" / "one-last-party.json").read_text())
    assert on_disk["section"]["id"] == "one-last-party"
    assert on_disk == pack


def test_pack_carries_promises_and_required_facts(world):
    repo, run = world
    pack = build_pack.build(repo, run, "one-last-party")
    assert pack["promises"] == ["Wrex on the Monument"]
    facts = [f["fact"] for f in pack["required_facts"]]
    assert "Shepard uncovered the clone in the Archives." in facts
    assert "The Normandy was retaken." in facts
    assert pack["required_facts"][0]["event_id"] == "citadel-dlc-archives"


def test_attendance_is_computed_not_written(world):
    repo, run = world
    pack = build_pack.build(repo, run, "one-last-party")
    assert pack["attendance"] == {"citadel-party-apartment": "witnessed"}


def test_evidence_is_tagged_with_the_key_that_found_it(world):
    repo, run = world
    pack = build_pack.build(repo, run, "one-last-party")
    keys = {e["for_key"] for e in pack["evidence"]}
    assert keys <= {"krogan monument", "apartment party"}
    assert "krogan monument" in keys
    assert {e["kind"] for e in pack["evidence"]} & {"summary", "scene", "page"}


def test_codex_lines_are_carried_with_their_line_numbers(world):
    repo, run = world
    pack = build_pack.build(repo, run, "one-last-party")
    hit = next(c for c in pack["codex"] if "Krogan Monument" in c["text"])
    assert hit["file"] == "codex/places.md" and hit["line"] == 3


def test_canon_is_narrowed_to_the_sections_entities(world):
    repo, run = world
    pack = build_pack.build(repo, run, "one-last-party")
    ids = {c["id"] for c in pack["canon"]}
    assert "aralakh-died" in ids, "an override scoped to this scene must reach the pack"


def test_an_override_scoped_to_a_scene_is_recorded_as_a_conflict(world):
    repo, run = world
    pack = build_pack.build(repo, run, "one-last-party")
    conflict = next(c for c in pack["conflicts"] if c["canon_id"] == "aralakh-died")
    assert "citadel-party-apartment" in conflict["evidence_said"]
    assert "override" in conflict["resolution"]


def test_resolutions_are_logged_to_the_canon_store_once(world):
    repo, run = world
    build_pack.build(repo, run, "one-last-party")
    build_pack.build(repo, run, "one-last-party")
    logged = yaml.safe_load((repo.canon_dir / "resolved.yaml").read_text())["resolved"]
    assert len(logged) == 1
    assert logged[0]["section"] == "one-last-party"


# --- hard stops -----------------------------------------------------------

def test_unknown_scene_id_hard_stops(world):
    repo, run = world
    outline = yaml.safe_load((run / "outline.yaml").read_text())
    outline["sections"][0]["scenes"] = ["no-such-scene"]
    (run / "outline.yaml").write_text(yaml.safe_dump(outline))
    with pytest.raises(build_pack.ThinPack, match="no-such-scene"):
        build_pack.build(repo, run, "one-last-party")


def test_unknown_event_id_hard_stops(world):
    repo, run = world
    outline = yaml.safe_load((run / "outline.yaml").read_text())
    outline["sections"][0]["events"] = ["no-such-event"]
    (run / "outline.yaml").write_text(yaml.safe_dump(outline))
    with pytest.raises(build_pack.ThinPack, match="no-such-event"):
        build_pack.build(repo, run, "one-last-party")


def test_a_retrieval_key_that_finds_nothing_hard_stops(world):
    repo, run = world
    outline = yaml.safe_load((run / "outline.yaml").read_text())
    outline["sections"][0]["retrieval"] = ["zzzzz nothing matches this"]
    (run / "outline.yaml").write_text(yaml.safe_dump(outline))
    with pytest.raises(build_pack.ThinPack, match="zzzzz"):
        build_pack.build(repo, run, "one-last-party")


def test_allow_thin_downgrades_a_hard_stop_to_a_warning(world):
    repo, run = world
    outline = yaml.safe_load((run / "outline.yaml").read_text())
    outline["sections"][0]["retrieval"] = ["zzzzz nothing matches this", "krogan monument"]
    (run / "outline.yaml").write_text(yaml.safe_dump(outline))
    pack = build_pack.build(repo, run, "one-last-party", allow_thin=True)
    assert any("zzzzz" in w for w in pack["warnings"])


def test_an_unapproved_outline_hard_stops(world):
    repo, run = world
    text = (run / "outline.yaml").read_text()
    (run / "outline.yaml").write_text("# UNAPPROVED — remove this line\n" + text)
    with pytest.raises(build_pack.ThinPack, match="UNAPPROVED"):
        build_pack.build(repo, run, "one-last-party")


def test_a_scene_the_narrator_cannot_reach_is_warned_about(world):
    repo, run = world
    outline = yaml.safe_load((run / "outline.yaml").read_text())
    outline["sections"][0]["scenes"] = ["citadel-party-apartment", "citadel-jack-private"]
    (run / "outline.yaml").write_text(yaml.safe_dump(outline))
    pack = build_pack.build(repo, run, "one-last-party")
    assert pack["attendance"]["citadel-jack-private"] == "absent"
    assert any("citadel-jack-private" in w for w in pack["warnings"])


# --- CLI ------------------------------------------------------------------

def test_cli_builds_every_section_and_exits_zero(world, capsys):
    repo, run = world
    rc = build_pack.main([str(run), "--all", "--root", str(repo.root)])
    assert rc == 0
    assert (run / "packs" / "one-last-party.json").is_file()


def test_cli_exits_non_zero_and_names_the_gap(world, capsys):
    repo, run = world
    outline = yaml.safe_load((run / "outline.yaml").read_text())
    outline["sections"][0]["retrieval"] = ["zzzzz nothing matches this"]
    (run / "outline.yaml").write_text(yaml.safe_dump(outline))
    assert build_pack.main([str(run), "--all", "--root", str(repo.root)]) != 0
    assert "zzzzz" in capsys.readouterr().err


def test_pack_carries_the_form_description_and_note(world):
    """The section-writer only sees the pack, so the form has to travel in it.

    A form id alone ("motivational") does not tell the writer what the section is for;
    the description from config/forms.yaml and the run's own form_note do.
    """
    repo, run = world
    pack = build_pack.build(repo, run, "one-last-party")
    section = pack["section"]
    assert section["form"] == "evening"
    assert section["form_note"] == "one night"
    assert "one occasion, one night" in section["form_description"].lower()

    rendered = (run / "packs" / "one-last-party.md").read_text(encoding="utf-8")
    assert "## Form" in rendered
    assert "one night" in rendered
