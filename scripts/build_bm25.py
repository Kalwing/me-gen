"""Build a BM25 keyword index over chunks.jsonl."""
from __future__ import annotations

import argparse
import json
import pickle
import re
from pathlib import Path

_TOKEN = re.compile(r"[a-z0-9']+")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def build(chunks_path: Path, index_path: Path) -> int:
    chunks: list[dict] = []
    with Path(chunks_path).open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    tokenized = [tokenize(c["text"]) for c in chunks]
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with Path(index_path).open("wb") as fh:
        pickle.dump({"chunks": chunks, "tokenized": tokenized}, fh)
    return len(chunks)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build BM25 index from chunks.jsonl")
    ap.add_argument("--chunks", type=Path, default=Path("data/chunks/chunks.jsonl"))
    ap.add_argument("--out", type=Path, default=Path("data/bm25_index.pkl"))
    a = ap.parse_args()
    n = build(a.chunks, a.out)
    print(f"indexed {n} chunks -> {a.out}")
