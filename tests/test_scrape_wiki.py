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


def test_crawl_skips_pages_already_have():
    graph = {
        "Virmire": _page("Virmire", links=["Saren", "Sovereign"]),
        "Saren": _page("Saren"),
        "Sovereign": _page("Sovereign"),
    }
    fetched: list[str] = []

    def fetch(title):
        fetched.append(title)
        return graph.get(title)

    got = scrape_wiki.crawl(["Virmire"], depth=1, cap=100, fetch=fetch, errors=[],
                            have=lambda t: t == "Saren")
    # Saren is reported as already-on-disk: never fetched, not returned...
    assert "Saren" not in fetched
    assert {p.title for p in got} == {"Virmire", "Sovereign"}


def test_crawl_have_pages_count_toward_cap():
    graph = {
        "Root": _page("Root", links=["A", "B", "C", "D", "E"]),
        "A": _page("A"), "B": _page("B"), "C": _page("C"),
        "D": _page("D"), "E": _page("E"),
    }
    # A and B are already on disk; cap 4 = 2 fetched (Root, C) + 2 skipped (A, B)
    got = scrape_wiki.crawl(["Root"], depth=1, cap=4, fetch=graph.get, errors=[],
                            have=lambda t: t in {"A", "B"})
    assert [p.title for p in got] == ["Root", "C"]


def test_crawl_always_fetches_seeds_even_if_have():
    graph = {"Virmire": _page("Virmire", links=["Saren"]), "Saren": _page("Saren")}
    fetched: list[str] = []

    def fetch(title):
        fetched.append(title)
        return graph.get(title)

    # Virmire is a seed and already on disk, but must still be fetched so its
    # links rebuild the crawl frontier on resume.
    got = scrape_wiki.crawl(["Virmire"], depth=1, cap=100, fetch=fetch, errors=[],
                            have=lambda t: t == "Virmire")
    assert "Virmire" in fetched
    assert {p.title for p in got} == {"Virmire", "Saren"}


def test_existing_slugs(tmp_path):
    (tmp_path / "virmire.md").write_text("---\n---\nx")
    (tmp_path / "saren-arterius.md").write_text("---\n---\nx")
    (tmp_path / "notes.txt").write_text("ignored")
    assert scrape_wiki.existing_slugs(tmp_path) == {"virmire", "saren-arterius"}
    assert scrape_wiki.existing_slugs(tmp_path / "nope") == set()
