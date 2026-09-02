from pathlib import Path

from scripts import narrative_choices as nc
from scripts import sync_narrative_choices as sync

REAL = Path(__file__).parent.parent / "config" / "narrative_choices.yaml"

MINIMAL = (
    "# header comment\n"
    "#\n"
    "shepard:\n"
    "  - id: gender\n"
    "    prompt: Shepard's gender / pronouns.\n"
    "    options: []\n"
    '    answer: "Male"\n'
    '    detail: ""\n'
    "\n"
    "me1:\n"
    "  - id: wrex_virmire\n"
    "    prompt: Wrex on Virmire.\n"
    "    options: [alive]\n"
    "    answer: ''\n"
    '    detail: ""\n'
    "\n"
    "me2:\n"
    "  - id: collector_base\n"
    "    prompt: The Collector Base after the Suicide Mission.\n"
    "    options: [destroyed]\n"
    "    answer: ''\n"
    '    detail: ""\n'
    "\n"
    "me3:\n"
    "  - id: final_choice\n"
    "    prompt: The final choice at the Crucible.\n"
    "    options: [Destroy, Control, Synthesis, Refuse]\n"
    '    answer: "Synthesis"\n'
    '    detail: ""\n'
)


def test_catalog_is_self_consistent():
    # every catalogue prompt emits as an unquoted scalar (no ": " etc.)
    for group, stubs in sync.CATALOG.items():
        ids = [s["id"] for s in stubs]
        assert len(ids) == len(set(ids)), f"{group}: duplicate id in catalogue"
        for s in stubs:
            assert set(s) >= {"id", "prompt", "options"}
            assert not sync._needs_quote(s["prompt"]), f"{s['id']}: prompt needs quoting"


def test_real_file_is_in_sync():
    # the committed questionnaire must already contain every catalogue choice
    assert sync.sync(REAL, write=False) == []


def test_sync_appends_missing_stubs(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text(MINIMAL)
    added = sync.sync(p)

    assert added  # something was missing
    assert ("me3", "genophage") in added

    choices = nc.load_choices(p)  # still valid YAML in the required schema
    ids = {q["id"] for qs in choices.values() for q in qs}
    assert "genophage" in ids and "grissom_academy" in ids

    # existing answers and the header comment are untouched
    text = p.read_text()
    assert text.startswith("# header comment\n")
    assert 'answer: "Synthesis"' in text
    for q in choices["me3"]:
        if q["id"] == "genophage":
            assert q["answer"] == "" and q["detail"] == ""


def test_sync_is_idempotent(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text(MINIMAL)
    sync.sync(p)
    once = p.read_text()
    assert sync.sync(p) == []
    assert p.read_text() == once


def test_sync_preserves_a_narrowed_answer(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text(MINIMAL)
    sync.sync(p)
    choices = nc.load_choices(p)
    # wrex_virmire kept its single narrowed option => still counts as answered
    assert nc.is_blank(choices) is False
    assert "alive" in nc.summary_for_prompt(choices)


def test_check_mode_exit_codes(tmp_path, capsys):
    p = tmp_path / "c.yaml"
    p.write_text(MINIMAL)
    assert sync.main([str(p), "--check"]) == 1
    assert "missing:" in capsys.readouterr().out

    sync.main([str(p)])
    capsys.readouterr()
    assert sync.main([str(p), "--check"]) == 0


def test_missing_file_returns_2(tmp_path, capsys):
    assert sync.main([str(tmp_path / "nope.yaml")]) == 2
