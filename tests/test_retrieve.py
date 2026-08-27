import json
from pathlib import Path

from scripts import build_bm25, retrieve


def _write_chunks(path: Path):
    rows = [
        {"chunk_id": "sovereign_001", "page": "Sovereign", "section": "History",
         "game": "Mass Effect", "url": "u", "text": "Sovereign is a Reaper that manipulated Saren."},
        {"chunk_id": "virmire_003", "page": "Virmire", "section": "Mission",
         "game": "Mass Effect", "url": "u", "text": "On Virmire Wrex confronts Shepard about the genophage cure."},
        {"chunk_id": "rachni_001", "page": "Rachni", "section": "Overview",
         "game": "Mass Effect", "url": "u", "text": "The rachni queen speaks through an asari body."},
    ]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def test_build_then_retrieve_known_query(tmp_path):
    chunks = tmp_path / "chunks.jsonl"
    index = tmp_path / "bm25_index.pkl"
    _write_chunks(chunks)
    assert build_bm25.build(chunks, index) == 3

    hits = retrieve.retrieve(index, ["Sovereign Reaper"], k=1)
    assert hits[0]["chunk_id"] == "sovereign_001"
    assert "score" in hits[0]


def test_retrieve_dedups_across_queries(tmp_path):
    chunks = tmp_path / "chunks.jsonl"
    index = tmp_path / "bm25_index.pkl"
    _write_chunks(chunks)
    build_bm25.build(chunks, index)
    hits = retrieve.retrieve(index, ["Virmire Wrex", "Wrex genophage"], k=2)
    ids = [h["chunk_id"] for h in hits]
    assert ids.count("virmire_003") == 1
    assert ids == sorted(set(ids), key=lambda i: -[h for h in hits if h["chunk_id"] == i][0]["score"])


def test_tokenize():
    assert build_bm25.tokenize("Sovereign's Reaper-tech!") == ["sovereign's", "reaper", "tech"]
