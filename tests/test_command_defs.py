from pathlib import Path

import yaml

CMDS = Path(__file__).parent.parent / ".claude" / "commands"
EXPECTED = {"me-scrape", "me-build-lore", "me-build-timeline", "me-generate"}


def _frontmatter(path: Path) -> dict:
    text = path.read_text()
    assert text.startswith("---\n"), f"{path}: no frontmatter"
    return yaml.safe_load(text.split("---\n", 2)[1])


def test_lore_commands_present_and_reference_their_tools():
    checks = {
        "me-scrape": ["scripts/scrape_wiki.py", "scripts/chunk.py", "scripts/build_bm25.py"],
        "me-build-lore": ["page-summarizer"],
        "me-build-timeline": ["timeline-extractor"],
    }
    for name, needles in checks.items():
        p = CMDS / f"{name}.md"
        fm = _frontmatter(p)
        assert fm.get("description")
        body = p.read_text()
        assert "## Verify" in body
        for needle in needles:
            assert needle in body, f"{p} should mention {needle}"
