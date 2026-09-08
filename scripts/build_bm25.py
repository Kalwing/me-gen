"""Build a BM25 keyword index over the corpus.

Every row carries a ``kind``:

``page``     one chunk of a scraped wiki page (from ``chunks.jsonl``)
``summary``  one chunk per ``page_summaries/*.md`` — the prose summary of a whole page
``scene``    one chunk per scene beat, carrying its ``scene_id``

One index with three kinds beats three indices: a single query sees all of them, and
``retrieve.py --kind`` lets a caller demand a spread rather than taking six of whatever
scores highest — which is how a section about a party ended up holding nine chunks about
mercenaries.

The index is written atomically (temp file + rename), so a run that is killed
mid-write never leaves a corrupt pickle behind — the previous good index stays
in place. A re-run is a no-op when the index is already newer than
chunks.jsonl; pass ``--force`` to rebuild regardless.
"""
from __future__ import annotations

import argparse
import json
import os
import pickle
import re
from pathlib import Path

import yaml

_TOKEN = re.compile(r"[a-z0-9']+")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def _newest(paths: list[Path]) -> float:
    times = [p.stat().st_mtime for p in paths if p.exists()]
    for d in [p for p in paths if p.is_dir()]:
        times += [f.stat().st_mtime for f in d.rglob("*") if f.is_file()]
    return max(times, default=0.0)


def _is_fresh(sources: list[Path], index_path: Path) -> bool:
    return index_path.is_file() and index_path.stat().st_mtime >= _newest(sources)


def _page_chunks(chunks_path: Path) -> list[dict]:
    out: list[dict] = []
    with Path(chunks_path).open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(dict(json.loads(line), kind="page"))
    return out


def _summary_chunks(summaries_dir: Path) -> list[dict]:
    """One row per page summary — the whole-page prose an occasion is usually described in."""
    import sys

    from scripts.common import read_frontmatter_md
    out: list[dict] = []
    for path in sorted(Path(summaries_dir).glob("*.md")):
        try:
            fm, body = read_frontmatter_md(path)
        except Exception as exc:
            # A malformed summary must not take the whole index down with it — say which
            # file, skip it, and keep going.
            print(f"warning: skipping {path}: {exc.__class__.__name__}", file=sys.stderr)
            continue
        out.append({
            "chunk_id": f"summary:{path.stem}",
            "source": path.stem,
            "page": fm.get("title", path.stem),
            "section": "",
            "game": fm.get("game", ""),
            "text": body.strip(),
            "url": fm.get("url", ""),
            "kind": "summary",
        })
    return out


def _scene_chunks(scenes_dir: Path) -> list[dict]:
    """One row per scene beat, so an occasion is findable by what happened in it."""
    out: list[dict] = []
    for path in sorted(Path(scenes_dir).glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = data.get("scene_id") or path.stem
        blocks = list(data.get("beats") or []) + list(data.get("variants") or [])
        header = f"{data.get('title', '')}. {data.get('when', '')} {data.get('where', '')}"
        for i, block in enumerate(blocks, start=1):
            out.append({
                "chunk_id": f"scene:{sid}#{i:02d}",
                "source": sid,
                "scene_id": sid,
                "page": data.get("title", sid),
                "section": data.get("kind", ""),
                "game": data.get("game", ""),
                "text": f"{header} {block.get('text', '')}".strip(),
                "url": "",
                "kind": "scene",
            })
    return out


def build(chunks_path: Path, index_path: Path, *, force: bool = False,
          summaries_dir: Path | None = None, scenes_dir: Path | None = None) -> int:
    """Return the row count, or -1 if a fresh index was left untouched."""
    chunks_path, index_path = Path(chunks_path), Path(index_path)
    sources = [chunks_path]
    if summaries_dir:
        sources.append(Path(summaries_dir))
    if scenes_dir:
        sources.append(Path(scenes_dir))
    if not force and _is_fresh(sources, index_path):
        return -1

    chunks = _page_chunks(chunks_path)
    if summaries_dir and Path(summaries_dir).is_dir():
        chunks += _summary_chunks(summaries_dir)
    if scenes_dir and Path(scenes_dir).is_dir():
        chunks += _scene_chunks(scenes_dir)
    tokenized = [tokenize(c["text"]) for c in chunks]

    index_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = index_path.with_name(index_path.name + ".tmp")
    with tmp.open("wb") as fh:
        pickle.dump({"chunks": chunks, "tokenized": tokenized}, fh)
        fh.flush()
        os.fsync(fh.fileno())
    tmp.replace(index_path)
    return len(chunks)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build BM25 index from chunks.jsonl")
    ap.add_argument("--chunks", type=Path, default=Path("data/chunks/chunks.jsonl"))
    ap.add_argument("--summaries", type=Path, default=Path("page_summaries"))
    ap.add_argument("--scenes", type=Path, default=Path("scenes"))
    ap.add_argument("--out", type=Path, default=Path("data/bm25_index.pkl"))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    n = build(a.chunks, a.out, force=a.force,
              summaries_dir=a.summaries, scenes_dir=a.scenes)
    if n < 0:
        print(f"{a.out} is already newer than its sources — nothing to do (use --force)")
    else:
        print(f"indexed {n} rows -> {a.out}")
