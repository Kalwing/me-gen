"""Crawl the Mass Effect Fandom wiki into data/pages/*.md via the MediaWiki API."""
from __future__ import annotations

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import argparse
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import requests
import yaml

from scripts import common
from scripts.clean_md import clean_html, infer_type

API = "https://masseffect.fandom.com/api.php"
UA = "mass-effect-narrator/0.1 (personal project)"
_short_pages: list[str] = []


@dataclass
class PageData:
    title: str
    url: str
    game: str
    type: str
    characters: list[str]
    html: str
    links: list[str] = field(default_factory=list)


def game_from_categories(categories: list[str]) -> str:
    joined = " ".join(c.lower().replace("_", " ") for c in categories)
    if "mass effect 3" in joined:
        return "Mass Effect 3"
    if "mass effect 2" in joined:
        return "Mass Effect 2"
    return "Mass Effect"


def characters_from_categories(categories: list[str]) -> list[str]:
    return []


def parse_page_response(title: str, api_json: dict) -> PageData:
    parse = api_json["parse"]
    cats = [c["*"] for c in parse.get("categories", [])]
    links = [l["*"] for l in parse.get("links", []) if l.get("ns") == 0]
    real_title = parse.get("title", title)
    return PageData(
        title=real_title,
        url=f"https://masseffect.fandom.com/wiki/{real_title.replace(' ', '_')}",
        game=game_from_categories(cats),
        type=infer_type(cats),
        characters=characters_from_categories(cats),
        html=parse.get("text", {}).get("*", ""),
        links=links,
    )


def live_fetch(title: str, session: requests.Session, rate: float) -> PageData | None:
    params = {"action": "parse", "page": title, "prop": "text|links|categories",
              "redirects": 1, "format": "json", "formatversion": 1}
    for attempt in range(3):
        try:
            time.sleep(rate)
            r = session.get(API, params=params, headers={"User-Agent": UA}, timeout=30)
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                return None
            return parse_page_response(title, data)
        except (requests.RequestException, ValueError):
            time.sleep(rate * (2 ** attempt))
    return None


def crawl(seeds: list[str], *, depth: int, cap: int,
          fetch: Callable[[str], PageData | None], errors: list[str]) -> list[PageData]:
    seen: set[str] = set()
    out: list[PageData] = []
    queue: deque[tuple[str, int]] = deque((s, 0) for s in seeds)
    while queue and len(out) < cap:
        title, d = queue.popleft()
        if title in seen:
            continue
        seen.add(title)
        page = fetch(title)
        if page is None:
            errors.append(title)
            continue
        out.append(page)
        if d < depth:
            for link in page.links:
                if link not in seen:
                    queue.append((link, d + 1))
    return out


def write_page(page: PageData, pages_dir: Path, *, force: bool) -> bool:
    pages_dir = Path(pages_dir)
    pages_dir.mkdir(parents=True, exist_ok=True)
    dest = pages_dir / f"{common.slugify(page.title)}.md"
    if dest.exists() and dest.stat().st_size > 0 and not force:
        return False
    body = clean_html(page.html)
    if len(body.strip()) < 200:
        _short_pages.append(page.title)
        if not body.strip():
            return False
    common.write_frontmatter_md(dest, {
        "title": page.title, "url": page.url, "game": page.game, "type": page.type,
        "characters": page.characters, "scraped": time.strftime("%Y-%m-%d"),
    }, body)
    return True


def _load_seeds(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Scrape the Mass Effect wiki")
    ap.add_argument("--seeds", type=Path, default=Path("config/seeds.yaml"))
    ap.add_argument("--depth", type=int)
    ap.add_argument("--cap", type=int)
    ap.add_argument("--rate", type=float)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--pages", type=Path, default=Path("data/pages"))
    a = ap.parse_args()

    cfg = _load_seeds(a.seeds)
    depth = a.depth if a.depth is not None else cfg.get("depth", 2)
    cap = a.cap if a.cap is not None else cfg.get("cap", 600)
    rate = a.rate if a.rate is not None else cfg.get("rate", 0.5)
    seeds = cfg.get("seeds", [])

    session = requests.Session()
    errors: list[str] = []
    pages = crawl(seeds, depth=depth, cap=cap,
                  fetch=lambda t: live_fetch(t, session, rate), errors=errors)
    written = sum(write_page(p, a.pages, force=a.force) for p in pages)

    log = Path("data/scrape_errors.log")
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("\n".join(["FETCH FAILED: " + e for e in errors]
                             + ["SHORT/STUB: " + s for s in _short_pages]) + "\n")
    print(f"crawled {len(pages)} pages, wrote {written}, "
          f"{len(errors)} fetch errors, {len(_short_pages)} short pages "
          f"(see {log})")
