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


def test_build_skips_when_index_is_fresh(tmp_path):
    import os
    chunks = tmp_path / "chunks.jsonl"
    index = tmp_path / "bm25_index.pkl"
    _write_chunks(chunks)
    assert build_bm25.build(chunks, index) == 3

    # index now newer than chunks -> no rebuild
    assert build_bm25.build(chunks, index) == -1
    # force overrides
    assert build_bm25.build(chunks, index, force=True) == 3

    # chunks touched newer than index -> rebuild
    future = index.stat().st_mtime + 100
    os.utime(chunks, (future, future))
    assert build_bm25.build(chunks, index) == 3


def test_build_is_atomic_no_tmp_left(tmp_path):
    chunks = tmp_path / "chunks.jsonl"
    index = tmp_path / "bm25_index.pkl"
    _write_chunks(chunks)
    build_bm25.build(chunks, index)
    assert not (tmp_path / "bm25_index.pkl.tmp").exists()
    assert index.is_file()


def test_retrieve_no_matches(tmp_path):
    chunks = tmp_path / "chunks.jsonl"
    index = tmp_path / "bm25_index.pkl"
    _write_chunks(chunks)
    build_bm25.build(chunks, index)
    hits = retrieve.retrieve(index, ["xyzabc defgh"], k=10)
    assert hits == []


# --- kind-tagged index ----------------------------------------------------

def _tiny_corpus(tmp_path):
    """A chunks file, a page summary and a scene — one of each kind."""
    chunks = tmp_path / "chunks.jsonl"
    chunks.write_text(
        '{"chunk_id": "party_001", "source": "party", "page": "Citadel: Party", '
        '"section": "", "game": "Mass Effect 3", "text": "Joker suggests throwing a party.", '
        '"url": "u"}\n', encoding="utf-8")

    summaries = tmp_path / "page_summaries"
    summaries.mkdir()
    (summaries / "krogan-monument.md").write_text(
        "---\ntitle: Krogan Monument\nurl: u\ngame: Mass Effect 3\ntype: location\n"
        "characters: [Grunt]\n---\n\nA statue of a krogan warrior in the Presidium lake.\n",
        encoding="utf-8")

    scenes_dir = tmp_path / "scenes"
    scenes_dir.mkdir()
    (scenes_dir / "citadel-grunt-csec.yaml").write_text(
        "scene_id: citadel-grunt-csec\ntitle: Bailing Grunt Out\nkind: hangout\n"
        "game: Mass Effect 3\nwhen: 2186\nwhere: a noodle stand\n"
        "participants: [Shepard, Grunt]\n"
        "beats:\n  - text: Grunt threw a bottle of ryncol at a C-Sec shuttle.\n"
        "    source_chunks: [grunt_005]\n"
        "source_chunks: [grunt_005]\n", encoding="utf-8")
    return chunks, summaries, scenes_dir


def test_build_tags_every_chunk_with_a_kind(tmp_path):
    from scripts import build_bm25, retrieve as r
    chunks, summaries, scenes_dir = _tiny_corpus(tmp_path)
    out = tmp_path / "index.pkl"
    n = build_bm25.build(chunks, out, summaries_dir=summaries, scenes_dir=scenes_dir)
    assert n == 3
    _, rows = r.load_index(out)
    assert {row["kind"] for row in rows} == {"page", "summary", "scene"}


def test_scene_chunks_carry_their_scene_id(tmp_path):
    from scripts import build_bm25, retrieve as r
    chunks, summaries, scenes_dir = _tiny_corpus(tmp_path)
    out = tmp_path / "index.pkl"
    build_bm25.build(chunks, out, summaries_dir=summaries, scenes_dir=scenes_dir)
    _, rows = r.load_index(out)
    scene_rows = [row for row in rows if row["kind"] == "scene"]
    assert scene_rows and scene_rows[0]["scene_id"] == "citadel-grunt-csec"


def test_retrieve_can_demand_a_kind(tmp_path):
    from scripts import build_bm25, retrieve as r
    chunks, summaries, scenes_dir = _tiny_corpus(tmp_path)
    out = tmp_path / "index.pkl"
    build_bm25.build(chunks, out, summaries_dir=summaries, scenes_dir=scenes_dir)
    hits = r.retrieve(out, ["krogan monument statue"], k=5, kinds=["summary"])
    assert hits and all(h["kind"] == "summary" for h in hits)


def test_retrieve_per_kind_k_spreads_the_budget(tmp_path):
    # 6 of whatever scores highest is how a party section ended up with nine chunks
    # about mercenaries. A pack asks for n of each kind instead.
    from scripts import build_bm25, retrieve as r
    chunks, summaries, scenes_dir = _tiny_corpus(tmp_path)
    out = tmp_path / "index.pkl"
    build_bm25.build(chunks, out, summaries_dir=summaries, scenes_dir=scenes_dir)
    hits = r.retrieve_by_kind(out, ["krogan monument ryncol party"],
                              per_kind={"scene": 1, "summary": 1, "page": 1})
    assert {h["kind"] for h in hits} == {"page", "summary", "scene"}


def test_retrieve_without_kinds_is_unchanged(tmp_path):
    from scripts import build_bm25, retrieve as r
    chunks, summaries, scenes_dir = _tiny_corpus(tmp_path)
    out = tmp_path / "index.pkl"
    build_bm25.build(chunks, out, summaries_dir=summaries, scenes_dir=scenes_dir)
    assert len(r.retrieve(out, ["party"], k=5)) >= 1
