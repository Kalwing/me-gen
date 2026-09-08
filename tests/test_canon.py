from pathlib import Path

import pytest
import yaml

from scripts import canon

CANON_DIR = Path(__file__).parent.parent / "config" / "canon"


def _write_store(tmp_path, *, choices=None, overrides=None, questions=None, resolved=None):
    d = tmp_path / "canon"
    d.mkdir()
    (d / "choices.yaml").write_text(choices or (
        "me1:\n"
        "  - id: wrex_virmire\n"
        "    prompt: Wrex on Virmire\n"
        "    options: [alive]\n"
        "    answer: ''\n"
        "    detail: 'talked him down'\n"
        "  - id: council_fate\n"
        "    prompt: The Council\n"
        "    options: [saved, sacrificed]\n"
        "    answer: ''\n"
        "    detail: ''\n"
    ))
    (d / "overrides.yaml").write_text(overrides or "overrides:\n")
    (d / "questions.yaml").write_text(questions or "questions:\n")
    (d / "resolved.yaml").write_text(resolved or "resolved:\n")
    return d


# --- the real store -------------------------------------------------------

def test_real_store_has_all_four_files():
    for name in ("choices.yaml", "overrides.yaml", "questions.yaml", "resolved.yaml"):
        assert (CANON_DIR / name).exists(), f"config/canon/{name} missing"


def test_real_store_loads():
    store = canon.load_canon(CANON_DIR)
    assert store["canon"], "the real store should resolve to at least one canon entry"
    ids = {e["id"] for e in store["canon"]}
    assert "shepard-born-on-the-normandy" in ids


# --- resolution -----------------------------------------------------------

def test_narrowed_option_is_an_answered_choice(tmp_path):
    store = canon.load_canon(_write_store(tmp_path))
    entry = next(e for e in store["canon"] if e["id"] == "wrex_virmire")
    assert entry["answer"] == "alive"
    assert entry["authority"] == "choices"
    assert "council_fate" in " ".join(store["unanswered"])


def test_overrides_carry_override_authority_and_sort_first(tmp_path):
    d = _write_store(tmp_path, overrides=(
        "overrides:\n"
        "  - id: aralakh-died\n"
        "    kind: correction\n"
        "    scope: [Grunt]\n"
        "    statement: Aralakh Company was wiped out at Utukku.\n"
        "    overrides: codex bullet\n"
        "    added: 2026-09-07\n"
    ))
    store = canon.load_canon(d)
    assert store["canon"][0]["id"] == "aralakh-died"
    assert store["canon"][0]["authority"] == "override"


def test_answered_question_becomes_canon_open_one_does_not(tmp_path):
    d = _write_store(tmp_path, questions=(
        "questions:\n"
        "  - id: q-1\n"
        "    raised_by: run/section\n"
        "    question: Did Wrex attend the arena?\n"
        "    context: ''\n"
        "    options: [attended, heard about it]\n"
        "    answer: attended\n"
        "    status: answered\n"
        "  - id: q-2\n"
        "    raised_by: run/section\n"
        "    question: Was Grunt at the party?\n"
        "    context: ''\n"
        "    options: []\n"
        "    answer: ''\n"
        "    status: open\n"
    ))
    store = canon.load_canon(d)
    ids = {e["id"] for e in store["canon"]}
    assert "q-1" in ids and "q-2" not in ids
    assert next(e for e in store["canon"] if e["id"] == "q-1")["authority"] == "question"
    assert [q["id"] for q in store["open_questions"]] == ["q-2"]


# --- filtering ------------------------------------------------------------

def test_filter_for_narrows_to_matching_entities(tmp_path):
    d = _write_store(tmp_path, overrides=(
        "overrides:\n"
        "  - id: aralakh-died\n"
        "    kind: correction\n"
        "    scope: [Grunt, Aralakh Company]\n"
        "    statement: Wiped out at Utukku.\n"
        "    overrides: codex\n"
        "    added: 2026-09-07\n"
    ))
    store = canon.filter_for(canon.load_canon(d), ["Wrex"])
    ids = {e["id"] for e in store["canon"]}
    assert "wrex_virmire" in ids
    assert "aralakh-died" not in ids

    store = canon.filter_for(canon.load_canon(d), ["Grunt"])
    ids = {e["id"] for e in store["canon"]}
    assert "aralakh-died" in ids
    assert "wrex_virmire" not in ids


def test_filter_for_matches_override_scope_on_scene_ids(tmp_path):
    d = _write_store(tmp_path, overrides=(
        "overrides:\n"
        "  - id: aralakh-died\n"
        "    kind: correction\n"
        "    scope: [citadel-grunt-csec]\n"
        "    statement: Wiped out at Utukku.\n"
        "    overrides: codex\n"
        "    added: 2026-09-07\n"
    ))
    store = canon.filter_for(canon.load_canon(d), ["citadel-grunt-csec"])
    assert {e["id"] for e in store["canon"]} == {"aralakh-died"}


def test_unscoped_override_applies_to_every_section(tmp_path):
    d = _write_store(tmp_path, overrides=(
        "overrides:\n"
        "  - id: global-thing\n"
        "    kind: au\n"
        "    scope: []\n"
        "    statement: Everything is on fire.\n"
        "    overrides: nothing\n"
        "    added: 2026-09-07\n"
    ))
    store = canon.filter_for(canon.load_canon(d), ["Tali"])
    assert "global-thing" in {e["id"] for e in store["canon"]}


# --- writing --------------------------------------------------------------

def test_ask_appends_a_question_with_a_generated_id(tmp_path):
    d = _write_store(tmp_path)
    qid = canon.ask(d, "question: Was Wrex at the party?\nraised_by: wrex/party\n")
    assert qid.startswith("q-")
    data = yaml.safe_load((d / "questions.yaml").read_text())
    assert data["questions"][0]["id"] == qid
    assert data["questions"][0]["status"] == "open"
    assert canon.load_canon(d)["open_questions"][0]["question"] == "Was Wrex at the party?"


def test_ask_is_idempotent_on_the_same_question(tmp_path):
    d = _write_store(tmp_path)
    first = canon.ask(d, "question: Same?\nraised_by: a\n")
    second = canon.ask(d, "question: Same?\nraised_by: b\n")
    assert first == second
    assert len(yaml.safe_load((d / "questions.yaml").read_text())["questions"]) == 1


def test_ask_preserves_the_files_comments(tmp_path):
    d = _write_store(tmp_path, questions="# keep me\nquestions:\n")
    canon.ask(d, "question: Anything?\n")
    assert "# keep me" in (d / "questions.yaml").read_text()


def test_ask_rejects_a_fragment_with_no_question(tmp_path):
    d = _write_store(tmp_path)
    with pytest.raises(ValueError):
        canon.ask(d, "context: no question here\n")


def test_log_resolution_appends(tmp_path):
    d = _write_store(tmp_path)
    rid = canon.log_resolution(d, (
        "run: wrex_x\nsection: party\nconfig_said: I let Garrus win\n"
        "evidence_said: presidium, not an arcade\nresolution: outcome from config, staging from scene\n"
    ))
    assert rid.startswith("r-")
    data = yaml.safe_load((d / "resolved.yaml").read_text())
    assert data["resolved"][0]["resolution"].startswith("outcome from config")


def test_log_resolution_requires_a_resolution(tmp_path):
    d = _write_store(tmp_path)
    with pytest.raises(ValueError):
        canon.log_resolution(d, "run: x\n")


# --- CLI ------------------------------------------------------------------

def test_cli_summary_marks_authority_and_warns_about_open_questions(tmp_path, capsys):
    d = _write_store(tmp_path, questions=(
        "questions:\n"
        "  - id: q-2\n"
        "    question: Was Grunt at the party?\n"
        "    answer: ''\n"
        "    status: open\n"
    ))
    assert canon.main(["--canon-dir", str(d)]) == 0
    out = capsys.readouterr()
    assert "wrex_virmire" in out.out
    assert "open question" in out.err.lower()


def test_cli_json_for_entity(tmp_path, capsys):
    import json
    d = _write_store(tmp_path)
    assert canon.main(["--canon-dir", str(d), "--for", "Wrex", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert [e["id"] for e in payload["canon"]] == ["wrex_virmire"]


def test_cli_missing_store_does_not_crash(tmp_path, capsys):
    assert canon.main(["--canon-dir", str(tmp_path / "nope")]) == 0
    assert "unanswered" in capsys.readouterr().out.lower()
