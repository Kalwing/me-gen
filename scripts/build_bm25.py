"""Build a BM25 keyword index over chunks.jsonl.

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

_TOKEN = re.compile(r"[a-z0-9']+")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def _is_fresh(chunks_path: Path, index_path: Path) -> bool:
    return (index_path.is_file()
            and index_path.stat().st_mtime >= chunks_path.stat().st_mtime)


def build(chunks_path: Path, index_path: Path, *, force: bool = False) -> int:
    """Return the chunk count, or -1 if a fresh index was left untouched."""
    chunks_path, index_path = Path(chunks_path), Path(index_path)
    if not force and _is_fresh(chunks_path, index_path):
        return -1

    chunks: list[dict] = []
    with chunks_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
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
    ap.add_argument("--out", type=Path, default=Path("data/bm25_index.pkl"))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    n = build(a.chunks, a.out, force=a.force)
    if n < 0:
        print(f"{a.out} is already newer than {a.chunks} — nothing to do (use --force)")
    else:
        print(f"indexed {n} chunks -> {a.out}")
