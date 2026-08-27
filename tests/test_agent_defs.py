from pathlib import Path

import yaml

AGENTS = Path(__file__).parent.parent / ".claude" / "agents"
REQUIRED_SECTIONS = ("## Inputs", "## Outputs", "## Rules", "## Done when")
EXPECTED = {
    "page-summarizer", "timeline-extractor",
    "outline-writer", "section-writer", "smoother", "consistency-checker",
}


def _frontmatter(path: Path) -> dict:
    text = path.read_text()
    assert text.startswith("---\n"), f"{path}: no frontmatter"
    fm = text.split("---\n", 2)[1]
    return yaml.safe_load(fm)


def test_lore_agent_defs_present_and_well_formed():
    for name in ("page-summarizer", "timeline-extractor"):
        p = AGENTS / f"{name}.md"
        fm = _frontmatter(p)
        assert fm["name"] == name
        assert fm.get("description")
        body = p.read_text()
        for sec in REQUIRED_SECTIONS:
            assert sec in body, f"{p} missing {sec}"


def test_all_six_agents_present_and_well_formed():
    for name in EXPECTED:
        p = AGENTS / f"{name}.md"
        fm = _frontmatter(p)
        assert fm["name"] == name
        assert fm.get("description")
        body = p.read_text()
        for sec in REQUIRED_SECTIONS:
            assert sec in body, f"{p} missing {sec}"


def test_generation_agents_reference_narrative_choices():
    for name in ("outline-writer", "section-writer"):
        body = (AGENTS / f"{name}.md").read_text()
        assert "config/narrative_choices.yaml" in body, f"{name} must list the canon file in Inputs"
        assert "narrative_choices" in body.split("## Rules", 1)[1], f"{name} needs a Rules bullet for it"
