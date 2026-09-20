"""Episodes whose sections alternate between narrators — and monologues left exactly as they were."""
from pathlib import Path

import pytest
import yaml

from scripts import (assemble_episode, assemble_performance, build_pack, check_repetition,
                     common, new_run)
from tests.test_build_pack import world  # noqa: F401 — the miniature-repo fixture

MONO = {"narrator": "garrus", "sections": [{"id": "a"}, {"id": "b"}]}
DUO = {"narrator": "tali", "narrators": ["tali", "liara"], "sections": [
    {"id": "a", "narrator": "tali"}, {"id": "b", "narrator": "liara"},
    {"id": "c", "narrator": "tali"}]}


def test_monologue_has_one_voice_and_checks_its_first_section():
    assert common.episode_narrators(MONO) == ["garrus"]
    assert not common.is_multi_voice(MONO)
    assert common.section_narrator(MONO, MONO["sections"][1]) == "garrus"
    assert common.voice_check_sections(MONO) == ["a"]


def test_dialogue_checks_the_first_turn_of_each_voice():
    assert common.episode_narrators(DUO) == ["tali", "liara"]
    assert common.is_multi_voice(DUO)
    assert common.section_narrator(DUO, DUO["sections"][1]) == "liara"
    assert common.voice_check_sections(DUO) == ["a", "b"]


def test_headings_name_the_speaker_only_when_there_is_more_than_one():
    assert common.section_heading(MONO, {"id": "a", "title": "Palaven"}) == "## Palaven"
    assert common.section_heading(DUO, DUO["sections"][1] | {"title": "Sunset"}) == \
        "## Sunset — Liara"
    assert common.voices_title(DUO) == "Tali & Liara"
    assert common.voices_title(MONO) == "Garrus"


def test_new_run_monologue_writes_no_narrators_key(tmp_path):
    run = new_run.new_run("garrus", ["war"], 8000, tmp_path)
    data = yaml.safe_load((run / "outline.yaml").read_text())
    assert data["narrator"] == "garrus" and "narrators" not in data


def test_new_run_records_every_voice(tmp_path):
    run = new_run.new_run(["tali", "liara"], ["home"], 8000, tmp_path)
    assert run.name.startswith("tali-liara_home_")
    data = yaml.safe_load((run / "outline.yaml").read_text())
    assert data["narrator"] == "tali"
    assert data["narrators"] == ["tali", "liara"]


def _make_duo(run: Path, narrators=("wrex", "jack")):
    outline = yaml.safe_load((run / "outline.yaml").read_text())
    first = outline["sections"][0]
    outline["narrator"], outline["narrators"] = narrators[0], list(narrators)
    first["narrator"] = narrators[0]
    outline["sections"] = [first, {**first, "id": "reply", "title": "Reply",
                                   "narrator": narrators[1]}]
    (run / "outline.yaml").write_text(yaml.safe_dump(outline, sort_keys=False))


def test_monologue_pack_carries_no_turn_fields(world):  # noqa: F811
    repo, run = world
    pack = build_pack.build(repo, run, "one-last-party")
    assert pack["section"]["narrator"] == "wrex"
    assert not {"voices", "listeners", "previous"} & set(pack["section"])


def test_each_turn_takes_attendance_from_its_own_speaker(world):  # noqa: F811
    repo, run = world
    _make_duo(run)
    first = build_pack.build(repo, run, "one-last-party")
    reply = build_pack.build(repo, run, "reply")
    assert first["attendance"] == {"citadel-party-apartment": "witnessed"}
    # Wrex was at the party; Jack was not, and it reaches her only as Normandy gossip.
    assert reply["attendance"] == {"citadel-party-apartment": "heard"}
    assert reply["section"]["narrator"] == "jack"
    assert reply["section"]["listeners"] == ["wrex"]
    assert reply["section"]["previous"] == {"id": "one-last-party", "narrator": "wrex"}
    assert first["section"]["previous"] is None
    assert "Answers `one-last-party` (wrex)" in (run / "packs" / "reply.md").read_text()


def test_a_turn_with_an_undeclared_speaker_hard_stops(world):  # noqa: F811
    repo, run = world
    _make_duo(run)
    outline = yaml.safe_load((run / "outline.yaml").read_text())
    outline["sections"][1]["narrator"] = "garrus"
    (run / "outline.yaml").write_text(yaml.safe_dump(outline, sort_keys=False))
    with pytest.raises(build_pack.ThinPack, match="not one of the episode's"):
        build_pack.build(repo, run, "reply")


def test_catchphrase_is_exempt_only_in_its_own_speakers_turns():
    line = "keelah se'lai my people finally home"
    sections = {"a": f"she said {line} again", "b": f"and {line} tonight",
                "c": f"then {line} once more"}
    flags = check_repetition.find_repeats(
        sections, n=4, catchphrases_by_section={"a": [line], "b": [], "c": [line]})
    flagged = {sid for ids in flags.values() for sid in ids}
    # Tali's catchphrase in her two turns is fine; in Liara's mouth ("b") it is not.
    assert "b" in flagged
    only_tali = check_repetition.find_repeats(
        {"a": sections["a"], "c": sections["c"]}, n=4,
        catchphrases_by_section={"a": [line], "c": [line]})
    assert only_tali == {}


def _assembled_run(tmp_path, outline: dict) -> Path:
    run = tmp_path / "run"
    (run / "sections").mkdir(parents=True)
    (run / "outline.yaml").write_text(yaml.safe_dump(outline, sort_keys=False))
    for s in outline["sections"]:
        body = f"Words for {s['id']} spoken at sunset."
        (run / "sections" / f"{s['id']}.md").write_text(body)
        (run / "sections" / f"{s['id']}.performance.md").write_text(f"[soft] {body}")
    return run


def test_assembled_dialogue_names_each_speaker(tmp_path):
    outline = {**DUO, "themes": ["home"], "sections": [
        s | {"title": f"Turn {s['id']}"} for s in DUO["sections"]]}
    run = _assembled_run(tmp_path, outline)
    text = assemble_episode.assemble(run).read_text()
    assert text.splitlines()[0] == "# Tali & Liara — Mass Effect"
    assert "## Turn a — Tali" in text and "## Turn b — Liara" in text
    perf = assemble_performance.assemble(run).read_text()
    assert "## Turn b — Liara" in perf and "switch voice" in perf


def test_assembled_monologue_is_unchanged(tmp_path):
    outline = {**MONO, "themes": ["war"], "sections": [
        s | {"title": f"Turn {s['id']}"} for s in MONO["sections"]]}
    run = _assembled_run(tmp_path, outline)
    text = assemble_episode.assemble(run).read_text()
    assert text.splitlines()[0] == "# Garrus — Mass Effect"
    assert "## Turn a\n" in text and "—  " not in text and "## Turn a —" not in text
