from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
NARRATOR_KEYS = {"name", "species", "tone", "diction", "signature", "avoid", "knowledge_bias"}


def test_seeds_yaml_shape():
    cfg = yaml.safe_load((ROOT / "config" / "seeds.yaml").read_text())
    assert isinstance(cfg["seeds"], list) and cfg["seeds"]
    assert isinstance(cfg["depth"], int)
    assert isinstance(cfg["cap"], int)
    assert isinstance(cfg["rate"], (int, float))


def test_garrus_bible_shape():
    bible = yaml.safe_load((ROOT / "config" / "narrators" / "garrus.yaml").read_text())
    assert NARRATOR_KEYS <= set(bible)
    for k in ("tone", "diction", "signature", "avoid"):
        assert isinstance(bible[k], list) and bible[k]
    assert isinstance(bible["knowledge_bias"], str) and bible["knowledge_bias"].strip()
