"""Split cleaned pages into overlapping, sentence-aware chunks.

Sizes are WORD counts (see plan Global Constraints): ~1 word = ~1.3 tokens,
so the default 800-word chunk is ~1040 tokens, within the spec's 500-1000
token target band.

Resumable: chunks are appended to the output as each page is processed and a
sidecar manifest (``<out>.done``) records which pages are finished. Re-running
skips finished pages and discards any half-written trailing page from a killed
run, so an interrupted chunking job just needs to be run again. ``--force``
rechunks everything.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from scripts import common

_HEADING = re.compile(r"^#{1,3}\s+(.*)$")
_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")


def _sentences(paragraph: str) -> list[str]:
    return [s.strip() for s in _SENT.split(paragraph.strip()) if s.strip()]


def split_into_chunks(body: str, *, size: int = 800, overlap: int = 120):
    out: list[tuple[str, str]] = []
    section = ""
    cur: list[str] = []
    cur_words = 0

    def flush():
        nonlocal cur, cur_words
        if cur:
            out.append((section, " ".join(cur).strip()))
        cur, cur_words = [], 0

    for raw_line in body.splitlines():
        m = _HEADING.match(raw_line.strip())
        if m:
            flush()
            section = m.group(1).strip()
            continue
        if not raw_line.strip():
            continue
        for sent in _sentences(raw_line):
            w = common.word_count(sent)
            if cur_words + w > size and cur:
                out.append((section, " ".join(cur).strip()))
                keep, kept_words = [], 0
                for s in reversed(cur):
                    sw = common.word_count(s)
                    if kept_words + sw > overlap:
                        break
                    keep.insert(0, s)
                    kept_words += sw
                cur, cur_words = keep, kept_words
            cur.append(sent)
            cur_words += w
    flush()
    return out


def chunk_page(path: Path, *, size: int = 800, overlap: int = 120,
               prefix: str = "") -> list[dict]:
    fm, body = common.read_frontmatter_md(path)
    slug = prefix + common.slugify(fm.get("title", path.stem))
    rows = []
    for i, (section, text) in enumerate(split_into_chunks(body, size=size, overlap=overlap), start=1):
        rows.append({
            "chunk_id": f"{slug}_{i:03d}",
            "source": prefix + path.stem,
            "page": fm.get("title", path.stem),
            "section": section,
            "game": fm.get("game", ""),
            "text": text,
            "url": fm.get("url", ""),
        })
    return rows


def _manifest_path(out_path: Path) -> Path:
    return out_path.with_name(out_path.name + ".done")


def _read_manifest(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def _rewrite_kept_lines(out_path: Path, done: set[str]) -> int:
    """Keep only chunk lines whose source page is in ``done``; drop a partial
    trailing page and any truncated final line from a killed run."""
    if not out_path.is_file():
        return 0
    kept: list[str] = []
    with out_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue  # truncated last line
            if row.get("source") in done:
                kept.append(line)
    tmp = out_path.with_name(out_path.name + ".tmp")
    tmp.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
    tmp.replace(out_path)
    return len(kept)


def _iter_sources(pages_dir: Path, manual_dir: Path | None):
    """Yield ``(path, prefix, source_id)`` for every page to chunk.

    Scraped pages keep a bare stem; hand-corrected ``lore/manual`` docs get a
    ``manual-`` prefix on both the chunk id and the manifest key so they never
    collide with a same-named scraped page (arcturus-station, destiny-ascension).
    ``README.md`` in the manual dir is not lore.
    """
    items: list[tuple[Path, str, str]] = []
    for p in sorted(Path(pages_dir).glob("*.md")):
        items.append((p, "", p.stem))
    if manual_dir is not None and Path(manual_dir).is_dir():
        for p in sorted(Path(manual_dir).glob("*.md")):
            if p.name.lower() == "readme.md":
                continue
            items.append((p, "manual-", f"manual-{p.stem}"))
    return items


def chunk_dir(pages_dir: Path, out_path: Path, *, size: int = 800, overlap: int = 120,
              force: bool = False, progress_every: int = 50,
              manual_dir: Path | None = None) -> int:
    """Chunk every ``*.md`` under ``pages_dir`` (and ``manual_dir`` if given)
    into ``out_path`` (JSONL).

    Returns the number of chunks written *this run*. Safe to interrupt and
    re-run: finished pages (tracked in ``<out>.done``) are skipped and a
    half-written page from a previous kill is dropped before appending.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = _manifest_path(out_path)

    all_pages = _iter_sources(pages_dir, manual_dir)
    if force:
        out_path.unlink(missing_ok=True)
        manifest.unlink(missing_ok=True)
        done: set[str] = set()
    else:
        done = set(_read_manifest(manifest))

    pages = [t for t in all_pages if t[2] not in done]
    if not pages:
        return 0
    if not force:
        # drop a half-written page / truncated line from a killed run
        _rewrite_kept_lines(out_path, done)

    written = 0
    stop = {"now": False}

    def _stop(signum, frame):
        stop["now"] = True
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    with out_path.open("a", encoding="utf-8") as fh, \
            manifest.open("a", encoding="utf-8") as mh:
        for n, (p, prefix, source_id) in enumerate(pages, start=1):
            rows = chunk_page(p, size=size, overlap=overlap, prefix=prefix)
            # one write per page keeps a killed run from splitting a line
            fh.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
            fh.flush()
            mh.write(source_id + "\n")
            mh.flush()
            written += len(rows)
            if n % progress_every == 0:
                print(f"chunked {n}/{len(pages)} new pages, {written} chunks "
                      f"this run", flush=True)
            if stop["now"]:
                print(f"signal received: stopped after {n} pages "
                      f"({written} chunks) — re-run to resume", flush=True)
                break
    return written


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Chunk cleaned pages into chunks.jsonl")
    ap.add_argument("--pages", type=Path, default=Path("data/pages"))
    ap.add_argument("--manual", type=Path, default=Path("lore/manual"),
                    help="hand-corrected deep-dive docs; chunked with a manual- prefix")
    ap.add_argument("--out", type=Path, default=Path("data/chunks/chunks.jsonl"))
    ap.add_argument("--size", type=int, default=800)
    ap.add_argument("--overlap", type=int, default=120)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    n = chunk_dir(a.pages, a.out, size=a.size, overlap=a.overlap, force=a.force,
                  manual_dir=a.manual)
    total = sum(1 for _ in a.out.open(encoding="utf-8")) if a.out.is_file() else 0
    print(f"wrote {n} chunks this run; {total} total in {a.out}")
