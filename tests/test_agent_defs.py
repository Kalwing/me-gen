from pathlib import Path

import yaml

AGENTS = Path(__file__).parent.parent / ".claude" / "agents"
REQUIRED_SECTIONS = ("## Inputs", "## Outputs", "## Rules", "## Done when")
EXPECTED = {
    "page-summarizer", "timeline-extractor", "scene-extractor",
    "outline-writer", "section-writer", "episode-auditor",
}
# `smoother` and `consistency-checker` were merged into `episode-auditor`: a sliding
# window cannot see a device repeated three sections apart, and a checker that never
# read the chunks could not enforce its own grounding rule.
REPLACED = {"smoother", "consistency-checker"}


def _frontmatter(path: Path) -> dict:
    text = path.read_text()
    assert text.startswith("---\n"), f"{path}: no frontmatter"
    fm = text.split("---\n", 2)[1]
    return yaml.safe_load(fm)


def test_lore_agent_defs_present_and_well_formed():
    for name in ("page-summarizer", "timeline-extractor", "scene-extractor"):
        p = AGENTS / f"{name}.md"
        fm = _frontmatter(p)
        assert fm["name"] == name
        assert fm.get("description")
        body = p.read_text()
        for sec in REQUIRED_SECTIONS:
            assert sec in body, f"{p} missing {sec}"


def test_replaced_agents_are_gone():
    for name in REPLACED:
        assert not (AGENTS / f"{name}.md").exists(), f"{name} was replaced by episode-auditor"


def test_all_generation_agents_present_and_well_formed():
    for name in EXPECTED:
        p = AGENTS / f"{name}.md"
        fm = _frontmatter(p)
        assert fm["name"] == name
        assert fm.get("description")
        body = p.read_text()
        for sec in REQUIRED_SECTIONS:
            assert sec in body, f"{p} missing {sec}"


def test_generation_agents_reference_the_canon_store():
    for name in ("outline-writer", "section-writer"):
        body = (AGENTS / f"{name}.md").read_text()
        assert "config/canon/" in body, f"{name} must list the canon store in Inputs"
        assert "canon" in body.split("## Rules", 1)[1], f"{name} needs a Rules bullet for it"


GENERATION_AGENTS = {"outline-writer", "section-writer"}


def test_generation_agents_declare_content_priority():
    for name in GENERATION_AGENTS:
        text = (AGENTS / f"{name}.md").read_text()
        assert "## Content priority" in text, f"{name}: missing Content priority section"
        low = text.lower()
        start = low.index("## content priority")
        section = low[start:start + 2000]
        # Lore and worldbuilding are a first-class claim on the episode in both agents,
        # ranked above the galaxy events the narrator had no part in.
        assert section.index("lore") < section.index("galaxy"), \
            f"{name}: lore must outrank galaxy events the narrator was not part of"


def test_outline_priority_leads_with_the_forms_spine():
    # Which shape an episode takes is the chosen form's business, not a universal
    # "cover the personal arc across the trilogy" rule — that is the `arc` form.
    section = (AGENTS / "outline-writer.md").read_text().lower()
    start = section.index("## content priority")
    section = section[start:start + 2000]
    assert "spine" in section
    assert section.index("spine") < section.index("lore")


def test_outline_writer_knows_about_forms_scenes_and_pack_keys():
    body = (AGENTS / "outline-writer.md").read_text()
    for needle in ("config/forms.yaml", "form_note", "scripts/scenes.py",
                   "retrieval", "promises"):
        assert needle in body, f"outline-writer must mention {needle}"


def test_scene_extractor_knows_the_scene_schema():
    body = (AGENTS / "scene-extractor.md").read_text()
    # The fields that exist precisely to stop the failures the overhaul was written for.
    for needle in ("scene_id", "participants", "private_to", "heard_by", "requires",
                   "beats", "source_chunks", "variants", "conditional",
                   "scripts/scenes.py", "data/pages/"):
        assert needle in body, f"scene-extractor must mention {needle}"


def test_scene_extractor_never_writes_the_ledger():
    body = (AGENTS / "scene-extractor.md").read_text()
    assert "scenes/.done" in body
    rules = body.split("## Rules", 1)[1]
    assert "never" in rules.lower() and "scenes/.done" in rules, \
        "the controller owns scenes/.done — the agent must be told not to write it"
