from pathlib import Path

import pytest

from scripts import narrative_choices as nc

CHOICES = Path(__file__).parent.parent / "config" / "narrative_choices.yaml"

BLANK = (
    "shepard:\n"
    "  - id: background\n"
    "    prompt: Pre-service history\n"
    "    options: [Spacer, Colonist, Earthborn]\n"
    "    answer: ''\n"
    "    detail: ''\n"
    "me1:\n"
    "  - id: wrex_virmire\n"
    "    prompt: Wrex on Virmire\n"
    "    options: [alive, dead]\n"
    "    answer: ''\n"
    "    detail: ''\n"
    "  - id: genophage\n"
    "    prompt: Genophage\n"
    "    options: [cured, sabotaged]\n"
    "    answer: ''\n"
    "    detail: ''\n"
)


def test_choices_file_exists_and_loads():
    assert CHOICES.exists()
    choices = nc.load_choices(CHOICES)
    assert "shepard" in choices
    assert "me1" in choices and "me2" in choices and "me3" in choices


def test_is_blank_true_when_no_answers(tmp_path):
    p = tmp_path / "blank.yaml"
    p.write_text(BLANK)
    assert nc.is_blank(nc.load_choices(p)) is True


def test_single_option_counts_as_an_answer(tmp_path):
    # Narrowing a question's options to one choice IS the answer.
    p = tmp_path / "narrowed.yaml"
    p.write_text(
        "me1:\n"
        "  - id: wrex_virmire\n"
        "    prompt: Wrex on Virmire\n"
        "    options: [alive]\n"
        "    answer: ''\n"
        "    detail: ''\n"
    )
    choices = nc.load_choices(p)
    assert nc.is_blank(choices) is False
    assert "alive" in nc.summary_for_prompt(choices)


def test_load_choices_rejects_out_of_range_answer(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text(
        "me1:\n"
        "  - id: wrex_virmire\n"
        "    prompt: Wrex on Virmire\n"
        "    options: [alive, dead]\n"
        "    answer: maybe\n"
        "    detail: ''\n"
    )
    with pytest.raises(ValueError):
        nc.load_choices(p)


def test_load_choices_accepts_valid_answer(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text(
        "me1:\n"
        "  - id: wrex_virmire\n"
        "    prompt: Wrex on Virmire\n"
        "    options: [alive, dead]\n"
        "    answer: dead\n"
        "    detail: shot him on the ramp\n"
    )
    choices = nc.load_choices(p)
    assert nc.is_blank(choices) is False


def test_load_choices_accepts_free_text_answer(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text(
        "shepard:\n"
        "  - id: romance\n"
        "    prompt: Romance\n"
        "    options: []\n"
        "    answer: Garrus\n"
        "    detail: ''\n"
    )
    assert nc.load_choices(p)["shepard"][0]["answer"] == "Garrus"


@pytest.mark.parametrize("missing", ["prompt", "options", "answer", "detail"])
def test_load_choices_rejects_missing_key(tmp_path, missing):
    fields = {"id": "x", "prompt": "p", "options": "[]", "answer": "''", "detail": "''"}
    del fields[missing]
    body = "shepard:\n  - " + "\n    ".join(f"{k}: {v}" for k, v in fields.items()) + "\n"
    p = tmp_path / f"missing_{missing}.yaml"
    p.write_text(body)
    with pytest.raises(ValueError):
        nc.load_choices(p)


def test_main_handles_missing_file(tmp_path, capsys):
    rc = nc.main([str(tmp_path / "nope.yaml")])
    assert rc == 0
    assert capsys.readouterr().out.strip() == "all questions unanswered"


def test_summary_only_names_answered_questions(tmp_path):
    p = tmp_path / "partial.yaml"
    p.write_text(BLANK)
    choices = nc.load_choices(p)
    for q in choices["shepard"]:
        if q["id"] == "background":
            q["answer"] = "Earthborn"
    summary = nc.summary_for_prompt(choices)
    assert "Earthborn" in summary
    # unanswered questions must not surface
    assert "wrex" not in summary.lower()
    assert "genophage" not in summary.lower()
    assert nc.is_blank(choices) is False
