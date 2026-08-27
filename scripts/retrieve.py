"""Query the BM25 index for grounding chunks."""
from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi

from scripts.build_bm25 import tokenize


def load_index(index_path: Path):
    with Path(index_path).open("rb") as fh:
        data = pickle.load(fh)
    return BM25Okapi(data["tokenized"]), data["chunks"]


def retrieve(index_path: Path, queries: list[str], *, k: int = 6) -> list[dict]:
    bm25, chunks = load_index(index_path)
    best: dict[str, dict] = {}
    for q in queries:
        scores = bm25.get_scores(tokenize(q))
        ranked = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)[:k]
        for i in ranked:
            if scores[i] <= 0:
                continue
            row = dict(chunks[i], score=float(scores[i]))
            prev = best.get(row["chunk_id"])
            if prev is None or row["score"] > prev["score"]:
                best[row["chunk_id"]] = row
    return sorted(best.values(), key=lambda r: r["score"], reverse=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Retrieve top chunks for one or more queries")
    ap.add_argument("--index", type=Path, default=Path("data/bm25_index.pkl"))
    ap.add_argument("--k", type=int, default=6)
    ap.add_argument("queries", nargs="+")
    a = ap.parse_args()
    print(json.dumps(retrieve(a.index, a.queries, k=a.k), ensure_ascii=False, indent=2))
