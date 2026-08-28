from pathlib import Path

from scripts import clean_md

FIXTURES = Path(__file__).parent / "fixtures"


def test_clean_html_keeps_prose_drops_chrome():
    html = (FIXTURES / "html" / "virmire.html").read_text()
    md = clean_md.clean_html(html)
    assert "Virmire is a planet in the Sentry Omega cluster." in md
    assert "## Mission" in md
    assert "Commander Shepard assaults Saren's base." in md
    assert "- Wrex confronts Shepard." in md
    # chrome removed
    assert "nav junk" not in md
    assert "Planet stats" not in md
    assert "[edit]" not in md
    assert "stat table" not in md
    assert "ref one" not in md
    assert "tracking()" not in md
    assert "Contents" not in md
    # images and their captions dropped entirely
    assert "![" not in md
    assert "data:image" not in md
    assert "Base.png" not in md
    assert "caption text here" not in md
    assert "inline image." in md  # surrounding prose survives


def test_infer_type():
    assert clean_md.infer_type(["Missions", "Mass Effect"]) == "mission"
    assert clean_md.infer_type(["Characters", "Turians"]) == "character"
    assert clean_md.infer_type(["Species"]) == "species"
    assert clean_md.infer_type(["Codex"]) == "lore"
    assert clean_md.infer_type(["Timeline"]) == "timeline"
    assert clean_md.infer_type(["Weapons", "Technology"]) == "tech"
    assert clean_md.infer_type(["Unknown bucket"]) == "lore"
