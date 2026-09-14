from pathlib import Path

from scripts import check_repetition as cr


def test_shingles_basic():
    assert cr.shingles("Don't make me repeat it.", 3) == [
        "don't make me", "make me repeat", "me repeat it",
    ]


def test_is_flaggable_drops_stopword_heavy_shingle():
    assert not cr.is_flaggable("of the it and so")
    assert cr.is_flaggable("don't make me repeat it")


def test_find_repeats_flags_phrase_in_two_or_more_sections():
    sections = {
        "one": "She looked at him. \"Don't make me repeat it,\" she said.",
        "two": "Later, tired, she said, \"Don't make me repeat it.\"",
        "three": "A completely different line about biotics and prison.",
    }
    flags = cr.find_repeats(sections, n=4)
    assert any("repeat it" in sh for sh in flags)
    hit = next(sh for sh in flags if "repeat it" in sh)
    assert flags[hit] == ["one", "two"]


def test_find_repeats_ignores_single_occurrence():
    sections = {
        "one": "Don't make me repeat it, she snapped.",
        "two": "A totally unrelated section about varren and mercenaries.",
    }
    assert cr.find_repeats(sections, n=4) == {}


def test_find_repeats_excludes_declared_catchphrase():
    sections = {
        "one": "Keelah se'lai, she whispered.",
        "two": "Keelah se'lai, she said again at the end.",
    }
    assert cr.find_repeats(sections, n=2, catchphrases=["Keelah se'lai"]) == {}


def test_check_writes_report_and_returns_flags(tmp_path: Path):
    run_dir = tmp_path / "run"
    (run_dir / "sections").mkdir(parents=True)
    (run_dir / "sections" / "one.md").write_text(
        "Don't make me repeat it, she snapped at him.", encoding="utf-8")
    (run_dir / "sections" / "two.md").write_text(
        "Don't make me repeat it, she said again, tired.", encoding="utf-8")
    (run_dir / "sections" / "one.performance.md").write_text(
        "[flat] Don't make me repeat it, she snapped at him.", encoding="utf-8")

    flags = cr.check(run_dir, narrator=None, n=4)

    assert flags
    report = (run_dir / "repetition_flags.md").read_text(encoding="utf-8")
    assert "repeat it" in report
    assert "one" in report and "two" in report


def test_check_writes_none_found_when_clean(tmp_path: Path):
    run_dir = tmp_path / "run"
    (run_dir / "sections").mkdir(parents=True)
    (run_dir / "sections" / "one.md").write_text("Nothing repeats here at all.", encoding="utf-8")
    (run_dir / "sections" / "two.md").write_text("A wholly different set of words entirely.", encoding="utf-8")

    flags = cr.check(run_dir, narrator=None, n=4)

    assert flags == {}
    report = (run_dir / "repetition_flags.md").read_text(encoding="utf-8")
    assert "none found" in report


def test_check_reads_narrator_from_outline_for_catchphrases(tmp_path: Path):
    narrators_dir = Path("config/narrators")
    slug = "__test_repetition_narrator__"
    bible = narrators_dir / f"{slug}.yaml"
    bible.write_text("name: Test\ncatchphrases:\n  - \"Keelah se'lai\"\n", encoding="utf-8")
    try:
        run_dir = tmp_path / "run"
        (run_dir / "sections").mkdir(parents=True)
        (run_dir / "sections" / "one.md").write_text("Keelah se'lai, she whispered softly.", encoding="utf-8")
        (run_dir / "sections" / "two.md").write_text("Keelah se'lai, she said once more.", encoding="utf-8")
        (run_dir / "outline.yaml").write_text(f"narrator: {slug}\n", encoding="utf-8")

        flags = cr.check(run_dir, n=2)

        assert flags == {}
    finally:
        bible.unlink()
