from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
NARRATOR_KEYS = {"name", "species", "tone", "diction", "signature", "avoid", "knowledge_bias"}

NARRATOR_FILES = sorted((ROOT / "config" / "narrators").glob("*.yaml"))


def test_seeds_yaml_shape():
    cfg = yaml.safe_load((ROOT / "config" / "seeds.yaml").read_text())
    assert isinstance(cfg["seeds"], list) and cfg["seeds"]
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
