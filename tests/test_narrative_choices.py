from pathlib import Path

import pytest

from scripts import narrative_choices as nc

TEMPLATE = Path(__file__).parent.parent / "config" / "narrative_choices.template.yaml"


def test_template_exists_and_loads():
    assert TEMPLATE.exists()
    choices = nc.load_choices(TEMPLATE)
    assert "shepard" in choices
    assert "me1" in choices and "me2" in choices and "me3" in choices


def test_template_is_blank():
    assert nc.is_blank(nc.load_choices(TEMPLATE)) is True


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


def test_summary_only_names_answered_questions():
    choices = nc.load_choices(TEMPLATE)
    for q in choices["shepard"]:
        if q["id"] == "background":
            q["answer"] = "Earthborn"
    for q in choices["me1"]:
        if q["id"] == "council_fate":
            q["answer"] = "sacrificed"
    summary = nc.summary_for_prompt(choices)
    assert "Earthborn" in summary
    assert "sacrificed" in summary
    # unanswered questions must not surface
    assert "wrex" not in summary.lower()
    assert "genophage" not in summary.lower()
    assert nc.is_blank(choices) is False
