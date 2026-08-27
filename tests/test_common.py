from pathlib import Path

import pytest

from scripts import common

FIXTURES = Path(__file__).parent / "fixtures"


def test_slugify_basic():
    assert common.slugify("The Virmire Mission!") == "the-virmire-mission"
    assert common.slugify("Mass Effect 2  (game)") == "mass-effect-2-game"
    assert common.slugify("--already-slug--") == "already-slug"


def test_frontmatter_roundtrip(tmp_path):
    p = tmp_path / "page.md"
    fm = {"title": "Virmire", "characters": ["Shepard", "Wrex"]}
    common.write_frontmatter_md(p, fm, "Body text here.\n")
    got_fm, body = common.read_frontmatter_md(p)
    assert got_fm == fm
    assert body.strip() == "Body text here."


def test_read_frontmatter_md_requires_block(tmp_path):
    p = tmp_path / "bad.md"
    p.write_text("no frontmatter here\n")
    with pytest.raises(ValueError):
        common.read_frontmatter_md(p)


def test_load_event_ok():
    ev = common.load_event(FIXTURES / "events" / "virmire_decision.yaml")
    assert ev["event_id"] == "virmire_decision"
    assert ev["chronological_order"] == 42
    assert "Shepard" in ev["characters"]


def test_load_event_missing_key(tmp_path):
    p = tmp_path / "broken.yaml"
    p.write_text("event_id: x\ntitle: y\n")
    with pytest.raises(ValueError):
        common.load_event(p)


def test_load_events_maps_by_id():
    events = common.load_events(FIXTURES / "events")
    assert set(events) == {"virmire_decision"}


def test_outline_is_approved(tmp_path):
    run = tmp_path / "run"
    run.mkdir()
    assert common.outline_is_approved(run) is False  # missing file
    (run / "outline.yaml").write_text("# UNAPPROVED — remove this line to approve\nnarrator: garrus\n")
    assert common.outline_is_approved(run) is False
    (run / "outline.yaml").write_text("narrator: garrus\nsections: []\n")
    assert common.outline_is_approved(run) is True


def test_word_count():
    assert common.word_count("one two   three\nfour") == 4
