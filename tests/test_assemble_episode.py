import pytest
import yaml

from scripts import assemble_episode


def _run(tmp_path, approved=True):
    run = tmp_path / "garrus_war_2026-08-27"
    (run / "sections").mkdir(parents=True)
    marker = "" if approved else "# UNAPPROVED\n"
    (run / "outline.yaml").write_text(marker + yaml.safe_dump({
        "narrator": "garrus", "themes": ["war"], "target_words": 20,
        "sections": [
            {"id": "intro", "title": "The Beginning", "events": [], "target_words": 10},
            {"id": "end", "title": "The End", "events": [], "target_words": 10},
        ],
    }, sort_keys=False))
    return run


def test_assemble_orders_sections_and_adds_header(tmp_path):
    run = _run(tmp_path)
    (run / "sections" / "intro.md").write_text("Humanity found the relay and everything changed forever.\n")
    (run / "sections" / "end.md").write_text("The Reapers fell and the galaxy exhaled at last.\n")
    ep = assemble_episode.assemble(run)
    text = ep.read_text()
    assert ep.name == "episode.md"
    assert text.index("## The Beginning") < text.index("## The End")
    assert "Garrus" in text.splitlines()[0]
    assert "Humanity found the relay" in text


def test_assemble_rejects_unapproved(tmp_path):
    run = _run(tmp_path, approved=False)
    (run / "sections" / "intro.md").write_text("x\n")
    (run / "sections" / "end.md").write_text("y\n")
    with pytest.raises(RuntimeError):
        assemble_episode.assemble(run)


def test_assemble_reports_missing_sections(tmp_path):
    run = _run(tmp_path)
    (run / "sections" / "intro.md").write_text("only intro here\n")
    with pytest.raises(FileNotFoundError) as exc:
        assemble_episode.assemble(run)
    assert "end" in str(exc.value)
