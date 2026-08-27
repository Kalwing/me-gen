"""Split cleaned pages into overlapping, sentence-aware chunks.

Sizes are WORD counts (see plan Global Constraints): ~1 word = ~1.3 tokens,
so the default 800-word chunk is ~1040 tokens, within the spec's 500-1000
token target band.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
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


def chunk_page(path: Path, *, size: int = 800, overlap: int = 120) -> list[dict]:
    fm, body = common.read_frontmatter_md(path)
    slug = common.slugify(fm.get("title", path.stem))
    rows = []
    for i, (section, text) in enumerate(split_into_chunks(body, size=size, overlap=overlap), start=1):
        rows.append({
            "chunk_id": f"{slug}_{i:03d}",
            "page": fm.get("title", path.stem),
            "section": section,
            "game": fm.get("game", ""),
            "text": text,
            "url": fm.get("url", ""),
        })
    return rows


def chunk_dir(pages_dir: Path, out_path: Path, *, size: int = 800, overlap: int = 120) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with out_path.open("w", encoding="utf-8") as fh:
        for p in sorted(Path(pages_dir).glob("*.md")):
            for row in chunk_page(p, size=size, overlap=overlap):
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                total += 1
    return total


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Chunk cleaned pages into chunks.jsonl")
    ap.add_argument("--pages", type=Path, default=Path("data/pages"))
    ap.add_argument("--out", type=Path, default=Path("data/chunks/chunks.jsonl"))
    ap.add_argument("--size", type=int, default=800)
    ap.add_argument("--overlap", type=int, default=120)
    a = ap.parse_args()
    n = chunk_dir(a.pages, a.out, size=a.size, overlap=a.overlap)
    print(f"wrote {n} chunks to {a.out}")
