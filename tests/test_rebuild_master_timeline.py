import yaml

from scripts import rebuild_master_timeline as rmt


def _event(path, eid, order, *, game="Mass Effect", title=None):
    path.write_text(yaml.safe_dump({
        "event_id": eid,
        "title": title or eid.replace("-", " ").title(),
        "game": game,
        "chronological_order": order,
        "date": "2183 CE",
        "summary": "x " * 60,
        "characters": ["Shepard"],
        "consequences": ["something happened"],
        "source_chunks": ["c_001"],
    }), encoding="utf-8")


def test_rebuild_sorts_and_dedupes(tmp_path):
    events = tmp_path / "events"
    events.mkdir()
    _event(events / "eden-prime.yaml", "eden-prime", 20)
    _event(events / "citadel.yaml", "citadel", 10)
    _event(events / "virmire.yaml", "virmire", 30)
    out = tmp_path / "master_timeline.yaml"

    n = rmt.rebuild(events, out)
    assert n == 3
    rows = yaml.safe_load(out.read_text())
    assert [r["event_id"] for r in rows] == ["citadel", "eden-prime", "virmire"]
    assert set(rows[0]) == {"event_id", "title", "game", "chronological_order"}


def test_rebuild_skips_malformed_event_file(tmp_path):
    events = tmp_path / "events"
    events.mkdir()
    _event(events / "good.yaml", "good", 10)
    (events / "half-written.yaml").write_text("event_id: half\ntitle: Half\n", encoding="utf-8")
    (events / "not-yaml.yaml").write_text(": : : [", encoding="utf-8")
    out = tmp_path / "master_timeline.yaml"

    n = rmt.rebuild(events, out)
    assert n == 1
    assert yaml.safe_load(out.read_text())[0]["event_id"] == "good"


def test_rebuild_is_atomic_no_tmp_left(tmp_path):
    events = tmp_path / "events"
    events.mkdir()
    _event(events / "a.yaml", "a", 10)
    out = tmp_path / "master_timeline.yaml"
    rmt.rebuild(events, out)
    assert not (tmp_path / "master_timeline.yaml.tmp").exists()
    assert out.is_file()


def test_rebuild_is_rerunnable(tmp_path):
    events = tmp_path / "events"
    events.mkdir()
    _event(events / "a.yaml", "a", 10)
    out = tmp_path / "master_timeline.yaml"
    assert rmt.rebuild(events, out) == 1
    _event(events / "b.yaml", "b", 20)
    assert rmt.rebuild(events, out) == 2  # picks up the new event, no dupes
    ids = [r["event_id"] for r in yaml.safe_load(out.read_text())]
    assert ids == ["a", "b"]
