import json

import yaml

from scripts import common, new_run


def test_new_run_creates_expected_shape(tmp_path):
    run = new_run.new_run("garrus", ["the cost of war", "loyalty"], 8000, tmp_path)
    assert run.parent == tmp_path
    assert run.name.startswith("garrus_the-cost-of-war-loyalty_")
    assert (run / "sections").is_dir()
    assert (run / "packs").is_dir()
    assert json.loads((run / "sources.json").read_text()) == {}

    text = (run / "outline.yaml").read_text()
    assert text.splitlines()[0].startswith("# UNAPPROVED")
    assert common.outline_is_approved(run) is False

    data = yaml.safe_load(text)
    assert data["narrator"] == "garrus"
    assert data["themes"] == ["the cost of war", "loyalty"]
    assert data["brief"] == ""
    assert data["target_words"] == 8000
    assert data["sections"] == []
    assert data["form"] == "" and data["form_note"] == ""


def test_new_run_records_a_named_form(tmp_path):
    run = new_run.new_run("wrex", ["war"], 9000, tmp_path, form="evening")
    assert yaml.safe_load((run / "outline.yaml").read_text())["form"] == "evening"


def test_new_run_records_brief(tmp_path):
    run = new_run.new_run("tali", ["home"], 6000, tmp_path,
                          brief="speaks by phone after a fight, a bit tired")
    data = yaml.safe_load((run / "outline.yaml").read_text())
    assert data["brief"] == "speaks by phone after a fight, a bit tired"


def test_new_run_disambiguates(tmp_path):
    a = new_run.new_run("garrus", ["war"], 8000, tmp_path)
    b = new_run.new_run("garrus", ["war"], 8000, tmp_path)
    assert a != b
    assert b.name.endswith("_2")
