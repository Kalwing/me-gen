"""Crawl the Mass Effect Fandom wiki into data/pages/*.md via the MediaWiki API."""
from __future__ import annotations

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import argparse
import json
import signal
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
          fetch: Callable[[str], PageData | None], errors: list[str],
          on_page: Callable[[PageData], None] | None = None,
          seen: set[str] | None = None,
          queue: list[tuple[str, int]] | None = None,
          checkpoint: Callable[[list[tuple[str, int]], set[str]], None] | None = None,
          checkpoint_every: int = 10) -> list[PageData]:
    """Breadth-first crawl from ``seeds`` to ``depth`` hops, fetching up to ``cap``
    pages *this run*.

    ``on_page`` fires for every page as soon as it is fetched, so a caller can
    persist incrementally and survive an interrupt.

    The crawl frontier is explicit and resumable. Pass ``seen`` (titles already
    dequeued on a previous run) and ``queue`` (``(title, depth)`` pairs that were
    discovered but not yet visited) to continue exactly where a capped run left
    off — no page or link is fetched twice, and the wiki tree is never re-walked
    just to rebuild the queue. When ``queue`` is given, ``seeds`` is ignored.

    ``checkpoint(pending, seen)`` is called every ``checkpoint_every`` fetches and
    once more when the crawl returns, handing the caller the current pending queue
    and seen set to write to disk.
    """
    seen = set(seen or ())
    q: deque[tuple[str, int]] = deque(
        (str(t), int(d)) for t, d in
        (queue if queue is not None else [(s, 0) for s in seeds]))
    out: list[PageData] = []
    since_ckpt = 0
    while q and len(out) < cap:
        title, d = q.popleft()
        if title in seen:
            continue
        seen.add(title)
        page = fetch(title)
        if page is None:
            errors.append(title)
            continue
        out.append(page)
        if on_page is not None:
            on_page(page)
        if d < depth:
            for link in page.links:
                if link not in seen:
                    q.append((link, d + 1))
        since_ckpt += 1
        if checkpoint is not None and since_ckpt >= checkpoint_every:
            checkpoint(list(q), seen)
            since_ckpt = 0
    if checkpoint is not None:
        checkpoint(list(q), seen)
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


def _write_error_log(log: Path, errors: list[str], short: list[str]) -> None:
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("\n".join(["FETCH FAILED: " + e for e in errors]
                             + ["SHORT/STUB: " + s for s in short]) + "\n")


def existing_slugs(pages_dir: Path) -> set[str]:
    p = Path(pages_dir)
    return {f.stem for f in p.glob("*.md")} if p.is_dir() else set()


def pending_pages(queue: list[tuple[str, int]], seen: set[str]) -> int:
    """How many *distinct* not-yet-visited pages are left in the frontier.

    The raw queue can list the same title several times (many pages link to
    it); this counts each remaining page once and ignores anything already
    crawled. That is the number of pages a bigger ``--cap`` would still fetch.
    """
    return len({t for t, _ in queue if t not in seen})


def load_state(path: Path) -> dict | None:
    """Read the persisted crawl frontier, or None if it is absent/unreadable."""
    p = Path(path)
    if not p.is_file():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None
    if not isinstance(data, dict):
        return None
    data.setdefault("seen", [])
    data.setdefault("queue", [])
    data.setdefault("errors", [])
    return data


def write_state(path: Path, *, queue: list[tuple[str, int]], seen: set[str],
                errors: list[str]) -> None:
    """Atomically persist the crawl frontier so a later run can resume it."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({
        "seen": sorted(seen),
        "queue": [[str(t), int(d)] for t, d in queue],
        "errors": sorted(set(errors)),
    })
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    tmp.replace(p)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Scrape the Mass Effect wiki")
    ap.add_argument("--seeds", type=Path, default=Path("config/seeds.yaml"))
    ap.add_argument("--depth", type=int)
    ap.add_argument("--cap", type=int)
    ap.add_argument("--rate", type=float)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--pages", type=Path, default=Path("data/pages"))
    ap.add_argument("--state", type=Path, default=Path("data/crawl_state.json"))
    a = ap.parse_args()

    cfg = _load_seeds(a.seeds)
    depth = a.depth if a.depth is not None else cfg.get("depth", 2)
    cap = a.cap if a.cap is not None else cfg.get("cap", 600)
    rate = a.rate if a.rate is not None else cfg.get("rate", 0.5)
    seeds = cfg.get("seeds", [])

    session = requests.Session()
    errors: list[str] = []
    log = Path("data/scrape_errors.log")

    existing = existing_slugs(a.pages)
    state = None if a.force else load_state(a.state)

    if state is not None:
        # Resume from the persisted frontier — no API re-walk.
        seen0: set[str] = set(state["seen"])
        queue0: list[tuple[str, int]] | None = [
            (t, d) for t, d in state["queue"] if t not in seen0]
        errors.extend(e for e in state["errors"] if e not in errors)
        print(f"resuming from {a.state}: {len(queue0)} queued, "
              f"{len(seen0)} seen, {len(existing)} pages on disk", flush=True)
    elif existing and not a.force:
        # First run under state-file support with pages already on disk: fetch the
        # seeds once to rebuild the frontier; from the first checkpoint on, the
        # state file carries it and this branch is never taken again.
        seen0, queue0 = set(), None
        print(f"no crawl state at {a.state}; {len(existing)} pages on disk — "
              f"re-fetching seeds once to rebuild the frontier, then it persists",
              flush=True)
    else:
        seen0, queue0 = set(), None
        if a.force:
            print("--force: ignoring existing pages and crawl state", flush=True)

    # `cap` bounds pages fetched *this run* (a batch bound). Progress across runs
    # comes from the persisted queue draining, so re-running always advances.
    if state is not None and not queue0:
        print(f"crawl state at {a.state} has an empty queue — crawl is complete "
              f"({len(existing)} pages). Use --force to start over.")
        _write_error_log(log, errors, _short_pages)
        sys.exit(0)

    stats = {"written": 0, "fetched": 0}
    every = 20  # progress cadence, in pages
    frontier: dict = {"queue": [], "seen": set()}

    def checkpoint(pending: list[tuple[str, int]], seen: set[str]) -> None:
        frontier["queue"], frontier["seen"] = pending, seen
        write_state(a.state, queue=pending, seen=seen, errors=errors)

    def _flush_and_exit(signum, frame) -> None:
        write_state(a.state, queue=frontier["queue"], seen=frontier["seen"],
                    errors=errors)
        _write_error_log(log, errors, _short_pages)
        n_left = pending_pages(frontier["queue"], frontier["seen"])
        print(f"\nsignal {signum}: frontier saved to {a.state} — "
              f"{n_left} distinct pages still to crawl. Re-run to resume "
              f"(raise --cap for a bigger batch).", flush=True)
        sys.exit(0)

    signal.signal(signal.SIGTERM, _flush_and_exit)
    signal.signal(signal.SIGINT, _flush_and_exit)

    def on_page(p: PageData) -> None:
        # Persist each page (and refresh the error log) as we go, so an
        # interrupted run keeps everything fetched so far.
        if write_page(p, a.pages, force=a.force):
            stats["written"] += 1
        stats["fetched"] += 1
        _write_error_log(log, errors, _short_pages)
        if stats["fetched"] % every == 0:
            done = len(existing) + stats["written"]
            left = pending_pages(frontier["queue"], frontier["seen"])
            print(f"progress: {done} pages on disk, {stats['fetched']}/{cap} "
                  f"fetched this run ({len(errors)} fetch errors, "
                  f"{left} distinct pages still to crawl)", flush=True)

    pages = crawl(seeds, depth=depth, cap=cap,
                  fetch=lambda t: live_fetch(t, session, rate), errors=errors,
                  on_page=on_page, seen=seen0, queue=queue0,
                  checkpoint=checkpoint, checkpoint_every=10)

    _write_error_log(log, errors, _short_pages)
    left = pending_pages(frontier["queue"], frontier["seen"])
    print(f"crawled {len(pages)} new pages, wrote {stats['written']}, "
          f"{len(existing)} already on disk, {len(errors)} fetch errors, "
          f"{len(_short_pages)} short pages (see {log}).")
    if left:
        print(f"{left} distinct pages still to crawl (frontier saved to "
              f"{a.state}). Re-run to fetch the next batch, or raise --cap "
              f"for a bigger one.")
    else:
        print(f"frontier drained — corpus is complete at "
              f"{len(existing) + stats['written']} pages.")
