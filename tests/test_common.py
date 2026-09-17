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


# --- form-driven episode length -------------------------------------------

def test_every_form_declares_a_word_budget():
    """Length comes from the form, so every form must say how long its sections run."""
    for fid, form in common.load_forms().items():
        wps = form["words_per_section"]
        lo, hi = form["words_clamp"]
        assert 200 <= wps <= 2000, f"{fid}: implausible words_per_section {wps}"
        assert 0 < lo < hi, f"{fid}: bad words_clamp {form['words_clamp']}"
        # The clamp must be reachable from the form's own section range, or it is a
        # rule that always fires and the words_per_section figure is decorative.
        n_lo, n_hi = form["section_count"]
        assert n_lo * wps <= hi and n_hi * wps >= lo, (
            f"{fid}: clamp {form['words_clamp']} unreachable from "
            f"{form['section_count']} x {wps}")


def test_target_words_for_multiplies_then_clamps():
    forms = {"demo": {"id": "demo", "section_count": [8, 30],
                      "words_per_section": 350, "words_clamp": [4000, 11000]}}
    assert common.target_words_for(forms["demo"], 20) == 7000      # inside the clamp
    assert common.target_words_for(forms["demo"], 8) == 4000       # clamped up
    assert common.target_words_for(forms["demo"], 40) == 11000     # clamped down


def test_target_words_for_falls_back_when_a_form_omits_the_keys():
    """A hand-written form without the new keys still yields a usable number."""
    assert common.target_words_for({"id": "x", "section_count": [8, 14]}, 8) > 0
