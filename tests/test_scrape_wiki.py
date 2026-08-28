from pathlib import Path

from scripts import scrape_wiki
from scripts.scrape_wiki import PageData


def _page(title, links=(), game="Mass Effect"):
    return PageData(title=title, url=f"https://masseffect.fandom.com/wiki/{title}",
                    game=game, type="lore", characters=[], html=f"<p>{title} body text.</p>",
                    links=list(links))


def test_crawl_respects_depth():
    graph = {
        "Virmire": _page("Virmire", links=["Saren", "Sovereign"]),
        "Saren": _page("Saren", links=["Sovereign", "Benezia"]),
        "Sovereign": _page("Sovereign", links=["Reapers"]),
        "Benezia": _page("Benezia"),
        "Reapers": _page("Reapers"),
    }
    errors: list[str] = []
    got = scrape_wiki.crawl(["Virmire"], depth=1, cap=100, fetch=graph.get, errors=errors)
    titles = {p.title for p in got}
    assert titles == {"Virmire", "Saren", "Sovereign"}  # depth 1 = seed + direct links
    assert errors == []


def test_crawl_respects_cap():
    graph = {f"P{i}": _page(f"P{i}", links=[f"P{i+1}"]) for i in range(20)}
    got = scrape_wiki.crawl(["P0"], depth=10, cap=5, fetch=graph.get, errors=[])
    assert len(got) == 5


def test_crawl_records_fetch_failures():
    graph = {"Virmire": _page("Virmire", links=["Missing"])}
    errors: list[str] = []
    got = scrape_wiki.crawl(["Virmire"], depth=1, cap=100, fetch=graph.get, errors=errors)
    assert {p.title for p in got} == {"Virmire"}
    assert errors == ["Missing"]


def test_parse_page_response():
    api = {"parse": {
        "title": "Virmire",
        "text": {"*": "<p>Virmire is a planet.</p>"},
        "links": [{"ns": 0, "*": "Saren", "exists": ""}, {"ns": 14, "*": "Category:Missions"}],
        "categories": [{"*": "Missions"}, {"*": "Mass_Effect_2"}],
    }}
    pd = scrape_wiki.parse_page_response("Virmire", api)
    assert pd.title == "Virmire"
    assert pd.type == "mission"
    assert pd.game == "Mass Effect 2"
    assert pd.links == ["Saren"]  # ns 0 only


def test_write_page_skips_existing(tmp_path):
    pd = _page("Virmire")
    assert scrape_wiki.write_page(pd, tmp_path, force=False) is True
    assert scrape_wiki.write_page(pd, tmp_path, force=False) is False
    assert scrape_wiki.write_page(pd, tmp_path, force=True) is True
    assert (tmp_path / "virmire.md").read_text().startswith("---")


def test_crawl_calls_on_page_as_it_goes():
    graph = {
        "Virmire": _page("Virmire", links=["Saren"]),
        "Saren": _page("Saren"),
    }
    seen_order: list[str] = []
    got = scrape_wiki.crawl(["Virmire"], depth=1, cap=100, fetch=graph.get,
                            errors=[], on_page=lambda p: seen_order.append(p.title))
    assert seen_order == ["Virmire", "Saren"]
    assert [p.title for p in got] == ["Virmire", "Saren"]


def test_crawl_resumes_from_persisted_queue_without_refetching():
    graph = {
        "Virmire": _page("Virmire", links=["Saren", "Sovereign"]),
        "Saren": _page("Saren", links=["Benezia"]),
        "Sovereign": _page("Sovereign"),
        "Benezia": _page("Benezia"),
    }
    fetched: list[str] = []

    def fetch(title):
        fetched.append(title)
        return graph.get(title)

    # A prior run visited Virmire + Saren and stopped with Sovereign, Benezia queued.
    got = scrape_wiki.crawl(
        [], depth=1, cap=100, fetch=fetch, errors=[],
        seen={"Virmire", "Saren"},
        queue=[("Sovereign", 1), ("Benezia", 2)])
    assert fetched == ["Sovereign", "Benezia"]  # seeds/seen never re-fetched
    assert {p.title for p in got} == {"Sovereign", "Benezia"}


def test_crawl_checkpoint_receives_pending_frontier_on_cap():
    graph = {f"P{i}": _page(f"P{i}", links=[f"P{i+1}"]) for i in range(20)}
    snapshots: list[tuple[list, set]] = []
    got = scrape_wiki.crawl(
        ["P0"], depth=10, cap=3, fetch=graph.get, errors=[],
        checkpoint=lambda q, s: snapshots.append(([tuple(x) for x in q], set(s))),
        checkpoint_every=100)
    assert [p.title for p in got] == ["P0", "P1", "P2"]
    # final checkpoint fires on return; P3 was discovered but not visited
    pending, seen = snapshots[-1]
    assert ("P3", 3) in pending
    assert seen == {"P0", "P1", "P2"}


def test_crawl_checkpoint_fires_periodically_and_at_end():
    graph = {f"P{i}": _page(f"P{i}", links=[f"P{i+1}"]) for i in range(10)}
    calls: list[int] = []
    scrape_wiki.crawl(["P0"], depth=20, cap=6, fetch=graph.get, errors=[],
                      checkpoint=lambda q, s: calls.append(len(s)),
                      checkpoint_every=2)
    # every 2 of 6 fetches -> 3, plus the final return checkpoint -> 4
    assert len(calls) == 4


def test_state_roundtrip(tmp_path):
    p = tmp_path / "state.json"
    scrape_wiki.write_state(p, queue=[("Sovereign", 1), ("Benezia", 2)],
                            seen={"Virmire", "Saren"}, errors=["Missing", "Missing"])
    got = scrape_wiki.load_state(p)
    assert set(got["seen"]) == {"Virmire", "Saren"}
    assert [tuple(x) for x in got["queue"]] == [("Sovereign", 1), ("Benezia", 2)]
    assert got["errors"] == ["Missing"]


def test_load_state_missing_returns_none(tmp_path):
    assert scrape_wiki.load_state(tmp_path / "nope.json") is None


def test_pending_pages_counts_distinct_unvisited():
    queue = [("A", 1), ("B", 1), ("A", 2), ("C", 1), ("D", 2)]
    seen = {"C"}  # already crawled
    # A (twice) + B + D  ->  3 distinct pages left; C ignored
    assert scrape_wiki.pending_pages(queue, seen) == 3
    assert scrape_wiki.pending_pages([], set()) == 0


def test_existing_slugs(tmp_path):
    (tmp_path / "virmire.md").write_text("---\n---\nx")
    (tmp_path / "saren-arterius.md").write_text("---\n---\nx")
    (tmp_path / "notes.txt").write_text("ignored")
    assert scrape_wiki.existing_slugs(tmp_path) == {"virmire", "saren-arterius"}
    assert scrape_wiki.existing_slugs(tmp_path / "nope") == set()
