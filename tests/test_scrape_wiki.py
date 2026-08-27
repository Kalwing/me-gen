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
