from pathlib import Path

import pytest
import yaml

from scripts import scenes

SCENES_DIR = Path(__file__).parent.parent / "scenes"

MINIMAL = {
    "scene_id": "citadel-garrus-presidium",
    "title": "Shooting Cans off the Presidium",
    "kind": "hangout",
    "game": "Mass Effect 3",
    "when": "2186, Citadel shore leave",
    "where": "top of the Presidium",
    "participants": ["Shepard", "Garrus Vakarian"],
    "private_to": ["Shepard", "Garrus Vakarian"],
    "heard_by": ["Normandy crew"],
    "beats": [{"text": "They shoot cans.", "source_chunks": ["garrus-vakarian_014"]}],
    "source_chunks": ["garrus-vakarian_014"],
}


def _write(tmp_path, data, name=None):
    d = tmp_path / "scenes"
    d.mkdir(exist_ok=True)
    p = d / f"{name or data['scene_id']}.yaml"
    p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
    return p


# --- schema ---------------------------------------------------------------

def test_load_scene_accepts_a_minimal_record(tmp_path):
    scene = scenes.load_scene(_write(tmp_path, MINIMAL))
    assert scene["scene_id"] == "citadel-garrus-presidium"
    assert scene["heard_by"] == ["Normandy crew"]


@pytest.mark.parametrize("key", ["scene_id", "title", "kind", "game", "when", "where",
                                 "participants", "beats", "source_chunks"])
def test_load_scene_rejects_a_missing_required_key(tmp_path, key):
    data = {k: v for k, v in MINIMAL.items() if k != key}
    data.setdefault("scene_id", "x")
    with pytest.raises(ValueError):
        scenes.load_scene(_write(tmp_path, data, name=MINIMAL["scene_id"]))


def test_load_scene_rejects_an_unknown_kind(tmp_path):
    with pytest.raises(ValueError, match="kind"):
        scenes.load_scene(_write(tmp_path, {**MINIMAL, "kind": "vibes"}))


def test_load_scene_rejects_a_filename_that_disagrees_with_the_id(tmp_path):
    with pytest.raises(ValueError, match="filename"):
        scenes.load_scene(_write(tmp_path, MINIMAL, name="something-else"))


def test_load_scene_rejects_a_beat_without_sources(tmp_path):
    # Per-beat traceability is the whole point: a beat nobody can check is how
    # compressed causality gets asserted authoritatively.
    data = {**MINIMAL, "beats": [{"text": "They shoot cans.", "source_chunks": []}]}
    with pytest.raises(ValueError, match="source_chunks"):
        scenes.load_scene(_write(tmp_path, data))


def test_load_scene_rejects_private_to_outside_participants(tmp_path):
    data = {**MINIMAL, "private_to": ["Shepard", "Wrex"]}
    with pytest.raises(ValueError, match="private_to"):
        scenes.load_scene(_write(tmp_path, data))


def test_load_scenes_rejects_duplicate_ids(tmp_path):
    d = tmp_path / "scenes"
    d.mkdir()
    _write(tmp_path, MINIMAL)
    (d / "dupe.yaml").write_text(yaml.safe_dump({**MINIMAL, "scene_id": "dupe"}))
    scenes.load_scenes(d)  # distinct ids load fine
    (d / "dupe.yaml").write_text(yaml.safe_dump(MINIMAL))
    with pytest.raises(ValueError):
        scenes.load_scenes(d)


# --- attendance -----------------------------------------------------------

def test_attendance_witnessed_for_a_participant(tmp_path):
    scene = scenes.load_scene(_write(tmp_path, MINIMAL))
    assert scenes.attendance(scene, "garrus") == "witnessed"
    assert scenes.attendance(scene, "Garrus Vakarian") == "witnessed"


def test_attendance_heard_for_someone_who_was_only_told(tmp_path):
    data = {**MINIMAL, "heard_by": ["Urdnot Wrex", "Tali'Zorah"]}
    scene = scenes.load_scene(_write(tmp_path, data))
    assert scenes.attendance(scene, "wrex") == "heard"
    assert scenes.attendance(scene, "tali") == "heard"


def test_attendance_crew_group_covers_the_whole_normandy(tmp_path):
    scene = scenes.load_scene(_write(tmp_path, MINIMAL))
    assert scenes.attendance(scene, "jack") == "heard"


def test_attendance_absent_when_private_and_not_named(tmp_path):
    data = {**MINIMAL, "heard_by": []}
    scene = scenes.load_scene(_write(tmp_path, data))
    assert scenes.attendance(scene, "jack") == "absent"


# --- the real scene set ---------------------------------------------------

def test_every_scene_on_disk_is_valid():
    loaded = scenes.load_scenes(SCENES_DIR)
    assert loaded, "the targeted scene set should not be empty"


def test_every_scene_beat_cites_a_real_chunk():
    known = scenes.known_chunk_ids()
    if not known:
        pytest.skip("no chunk index built")
    for scene in scenes.load_scenes(SCENES_DIR).values():
        for cid in scenes.cited_chunks(scene):
            assert cid in known, f"{scene['scene_id']}: unknown chunk {cid}"


def test_related_events_resolve():
    from scripts import common
    events_dir = Path(__file__).parent.parent / "timeline" / "events"
    if not events_dir.is_dir():
        pytest.skip("no timeline")
    known = set(common.load_events(events_dir))
    for scene in scenes.load_scenes(SCENES_DIR).values():
        for eid in scene.get("related_events") or []:
            assert eid in known, f"{scene['scene_id']}: unknown event {eid}"


def test_related_scenes_resolve():
    loaded = scenes.load_scenes(SCENES_DIR)
    for scene in loaded.values():
        for sid in scene.get("related_scenes") or []:
            assert sid in loaded, f"{scene['scene_id']}: unknown related scene {sid}"


# --- CLI ------------------------------------------------------------------

def test_cli_list_prints_one_line_per_scene(tmp_path, capsys):
    _write(tmp_path, MINIMAL)
    assert scenes.main(["--scenes-dir", str(tmp_path / "scenes"), "--list"]) == 0
    out = capsys.readouterr().out
    assert "citadel-garrus-presidium" in out and "hangout" in out


def test_cli_show_prints_the_record(tmp_path, capsys):
    _write(tmp_path, MINIMAL)
    assert scenes.main(["--scenes-dir", str(tmp_path / "scenes"),
                        "--show", "citadel-garrus-presidium"]) == 0
    assert "top of the Presidium" in capsys.readouterr().out


def test_cli_show_unknown_id_fails(tmp_path, capsys):
    _write(tmp_path, MINIMAL)
    assert scenes.main(["--scenes-dir", str(tmp_path / "scenes"), "--show", "nope"]) == 1


def test_cli_for_narrator_marks_attendance(tmp_path, capsys):
    _write(tmp_path, MINIMAL)
    assert scenes.main(["--scenes-dir", str(tmp_path / "scenes"),
                        "--list", "--for", "wrex"]) == 0
    assert "heard" in capsys.readouterr().out
