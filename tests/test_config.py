from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
NARRATOR_KEYS = {"name", "species", "tone", "diction", "signature", "avoid", "knowledge_bias"}

NARRATOR_FILES = sorted((ROOT / "config" / "narrators").glob("*.yaml"))


def test_seeds_yaml_shape():
    cfg = yaml.safe_load((ROOT / "config" / "seeds.yaml").read_text())
    assert isinstance(cfg["seeds"], list) and cfg["seeds"]
    assert all(isinstance(s, str) and s.strip() for s in cfg["seeds"]), (
        "every seed must be a plain string — an unquoted 'Key: Value' entry parses as a dict"
    )
    assert isinstance(cfg["depth"], int)
    assert isinstance(cfg["cap"], int)
    assert isinstance(cfg["rate"], (int, float))


@pytest.mark.parametrize("path", NARRATOR_FILES, ids=lambda p: p.stem)
def test_narrator_bible_shape(path):
    bible = yaml.safe_load(path.read_text())
    assert isinstance(bible, dict), f"{path.name} is not a mapping"
    assert NARRATOR_KEYS <= set(bible), f"{path.name} missing {NARRATOR_KEYS - set(bible)}"
    for k in ("tone", "diction", "signature", "avoid"):
        assert isinstance(bible[k], list) and bible[k], f"{path.name}: {k} must be a non-empty list"
    assert isinstance(bible["knowledge_bias"], str) and bible["knowledge_bias"].strip()


# --- episode forms --------------------------------------------------------

def test_forms_file_loads_and_is_well_formed():
    from scripts import common
    forms = common.load_forms()
    assert "arc" in forms and "evening" in forms
    for fid, form in forms.items():
        assert form["id"] == fid
        assert form["description"].strip()
        assert form["spine"] in ("events", "scenes", "mixed"), fid
        lo, hi = form["section_count"]
        assert 1 <= lo <= hi


def test_load_forms_rejects_an_unknown_spine(tmp_path):
    from scripts import common
    p = tmp_path / "forms.yaml"
    p.write_text("forms:\n  - id: x\n    description: y\n    spine: vibes\n    section_count: [1, 2]\n")
    import pytest
    with pytest.raises(ValueError):
        common.load_forms(p)


def test_load_forms_rejects_duplicate_ids(tmp_path):
    from scripts import common
    p = tmp_path / "forms.yaml"
    p.write_text(
        "forms:\n"
        "  - id: x\n    description: y\n    spine: mixed\n    section_count: [1, 2]\n"
        "  - id: x\n    description: z\n    spine: mixed\n    section_count: [1, 2]\n"
    )
    import pytest
    with pytest.raises(ValueError):
        common.load_forms(p)
