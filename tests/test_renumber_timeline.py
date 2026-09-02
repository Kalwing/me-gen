import yaml

from scripts import renumber_timeline as rt


def _event(path, eid, order, *, game="Mass Effect", date="2183 CE"):
    path.write_text(yaml.safe_dump({
        "event_id": eid,
        "title": eid.replace("-", " ").title(),
        "game": game,
        "chronological_order": order,
        "date": date,
        "summary": "x " * 60,
        "characters": ["Shepard"],
        "consequences": ["something happened"],
        "source_chunks": ["c_001"],
    }, sort_keys=False), encoding="utf-8")


def test_parse_year_variants():
    assert rt.parse_year("2157 CE") == 2157
    assert rt.parse_year("2157-2158 CE") == 2157
    assert rt.parse_year("approx. 1980s CE") == 1980
    assert rt.parse_year("710 CE") == 710
    assert rt.parse_year(None) == 9999


def test_game_rank():
    assert rt.game_rank("Mass Effect") == 1
    assert rt.game_rank("Mass Effect 1") == 1
    assert rt.game_rank("Mass Effect 2") == 2
    assert rt.game_rank("Mass Effect 3") == 3
    assert rt.game_rank("") == 1


def test_renumber_orders_by_year_then_game(tmp_path):
    events = tmp_path / "events"
    events.mkdir()
    # deliberately scrambled stored orders
    _event(events / "me3-early.yaml", "me3-early", 40, game="Mass Effect 3", date="2186 CE")
    _event(events / "me1-late.yaml", "me1-late", 300, game="Mass Effect", date="2183 CE")
    _event(events / "prehistory.yaml", "prehistory", 999, game="Mass Effect", date="1895 CE")
    _event(events / "me2-mid.yaml", "me2-mid", 10, game="Mass Effect 2", date="2185 CE")

    # me3-early already sits at 40 and stays there, so only 3 files rewrite
    changed = rt.renumber(events, dry_run=False)
    assert changed == 3

    got = {p.stem: yaml.safe_load(p.read_text())["chronological_order"]
           for p in events.glob("*.yaml")}
    assert got == {"prehistory": 10, "me1-late": 20, "me2-mid": 30, "me3-early": 40}


def test_renumber_is_idempotent_and_surgical(tmp_path):
    events = tmp_path / "events"
    events.mkdir()
    _event(events / "b.yaml", "b", 5, date="2186 CE")
    _event(events / "a.yaml", "a", 5, date="2183 CE")

    rt.renumber(events, dry_run=False)
    first = {p.stem: p.read_text() for p in events.glob("*.yaml")}
    assert rt.renumber(events, dry_run=False) == 0  # no-op second run
    second = {p.stem: p.read_text() for p in events.glob("*.yaml")}
    assert first == second
    # only the chronological_order line changed; every other key is intact
    ev = yaml.safe_load(first["a"])
    assert ev["event_id"] == "a" and ev["summary"].strip() and ev["source_chunks"] == ["c_001"]


def test_check_reports_drift_then_clean(tmp_path):
    events = tmp_path / "events"
    events.mkdir()
    _event(events / "future.yaml", "future", 10, game="Mass Effect 3", date="2186 CE")
    _event(events / "past.yaml", "past", 20, game="Mass Effect", date="2183 CE")
    assert rt.check(events)  # 'future' stored before 'past' but dated later
    rt.renumber(events, dry_run=False)
    assert rt.check(events) == []


def test_dry_run_writes_nothing(tmp_path):
    events = tmp_path / "events"
    events.mkdir()
    _event(events / "x.yaml", "x", 777, date="2186 CE")
    before = (events / "x.yaml").read_text()
    assert rt.renumber(events, dry_run=True) == 1
    assert (events / "x.yaml").read_text() == before
