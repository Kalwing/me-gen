"""Query the BM25 index for grounding chunks.

Rows are kind-tagged (``page`` / ``summary`` / ``scene``; see ``build_bm25.py``).
``--kind`` restricts a query to one or more kinds, and ``--per-kind`` asks for a fixed
number of each — so a caller can demand, say, 4 scene rows, 4 summary rows and 8 page rows
for a subject rather than 6 of whatever happens to score highest.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import pickle
import sys
from pathlib import Path

from rank_bm25 import BM25Okapi

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from scripts.build_bm25 import tokenize


def load_index(index_path: Path) -> tuple[BM25Okapi, list[dict]]:
    with Path(index_path).open("rb") as fh:
        data = pickle.load(fh)
    return BM25Okapi(data["tokenized"]), data["chunks"]


def _search(bm25, chunks: list[dict], queries: list[str], k: int,
            kinds: list[str] | None) -> dict[str, dict]:
    """Top ``k`` rows per query, restricted to ``kinds`` if given, keyed by chunk id."""
    wanted = set(kinds) if kinds else None
    best: dict[str, dict] = {}
    for q in queries:
        scores = bm25.get_scores(tokenize(q))
        order = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)
        taken = 0
        for i in order:
            if taken >= k or scores[i] <= 0:
                break
            if wanted is not None and chunks[i].get("kind") not in wanted:
                continue
            row = dict(chunks[i], score=float(scores[i]))
            prev = best.get(row["chunk_id"])
            if prev is None or row["score"] > prev["score"]:
                best[row["chunk_id"]] = row
            taken += 1
    return best


def retrieve(index_path: Path, queries: list[str], *, k: int = 6,
             kinds: list[str] | None = None) -> list[dict]:
    bm25, chunks = load_index(index_path)
    best = _search(bm25, chunks, queries, k, kinds)
    return sorted(best.values(), key=lambda r: r["score"], reverse=True)


def retrieve_by_kind(index_path: Path, queries: list[str],
                     *, per_kind: dict[str, int]) -> list[dict]:
    """Run the queries once per kind, with that kind's own budget.

    This is what an evidence pack uses. Asking the index for the top six overall lets one
    loud subject take every slot; asking for n scenes, n summaries and n pages guarantees
    the occasion layer is represented even when the mission pages next door score higher.
    """
    bm25, chunks = load_index(index_path)
    best: dict[str, dict] = {}
    for kind, k in per_kind.items():
        if k > 0:
            best.update(_search(bm25, chunks, queries, k, [kind]))
    return sorted(best.values(), key=lambda r: r["score"], reverse=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Retrieve top chunks for one or more queries")
    ap.add_argument("--index", type=Path, default=Path("data/bm25_index.pkl"))
    ap.add_argument("--k", type=int, default=6)
    ap.add_argument("--kind", action="append", dest="kinds",
                    choices=["page", "summary", "scene"],
                    help="restrict to this kind; repeatable")
    ap.add_argument("--per-kind", metavar="KIND=N", action="append", default=[],
                    help="budget per kind, e.g. --per-kind scene=4 --per-kind page=8; "
                         "repeatable, and overrides --k/--kind")
    ap.add_argument("queries", nargs="+")
    a = ap.parse_args()
    if a.per_kind:
        budget = {}
        for spec in a.per_kind:
            kind, _, n = spec.partition("=")
            budget[kind] = int(n or a.k)
        rows = retrieve_by_kind(a.index, a.queries, per_kind=budget)
    else:
        rows = retrieve(a.index, a.queries, k=a.k, kinds=a.kinds)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
