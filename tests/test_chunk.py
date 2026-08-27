import json
from pathlib import Path

from scripts import chunk, common


def _make_page(tmp_path, sentences, heading="Mission"):
    body = f"## {heading}\n\n" + " ".join(sentences) + "\n"
    p = tmp_path / "virmire.md"
    common.write_frontmatter_md(
        p,
        {"title": "Virmire", "game": "Mass Effect",
         "url": "https://masseffect.fandom.com/wiki/Virmire"},
        body,
    )
    return p


def test_split_respects_size_and_overlap():
    sentences = [f"Sentence number {i} about Virmire." for i in range(200)]
    body = "## Mission\n\n" + " ".join(sentences)
    chunks = chunk.split_into_chunks(body, size=50, overlap=10)
    assert len(chunks) > 1
    for _, text in chunks:
        assert common.word_count(text) <= 50 + 12  # size + one sentence slack
    # consecutive chunks share overlap text
    first_tail = chunks[0][1].split()[-5:]
    assert any(w in chunks[1][1] for w in first_tail)
    # every chunk carries the section heading
    assert all(h == "Mission" for h, _ in chunks)


def test_split_drops_no_text():
    body = "## A\n\n" + " ".join(f"Word{i} here now." for i in range(120))
    joined = " ".join(t for _, t in chunk.split_into_chunks(body, size=30, overlap=0))
    for i in range(120):
        assert f"Word{i}" in joined


def test_chunk_page_ids_and_metadata(tmp_path):
    p = _make_page(tmp_path, [f"Fact {i} about the mission." for i in range(90)])
    rows = chunk.chunk_page(p, size=40, overlap=8)
    assert rows[0]["chunk_id"] == "virmire_001"
    assert rows[1]["chunk_id"] == "virmire_002"
    assert rows[0]["page"] == "Virmire"
    assert rows[0]["game"] == "Mass Effect"
    assert rows[0]["section"] == "Mission"
    assert rows[0]["url"].endswith("/Virmire")


def test_chunk_dir_writes_jsonl(tmp_path):
    _make_page(tmp_path, [f"Sentence {i}." for i in range(60)])
    out = tmp_path / "chunks.jsonl"
    n = chunk.chunk_dir(tmp_path, out, size=40, overlap=8)
    lines = out.read_text().strip().splitlines()
    assert n == len(lines) >= 1
    assert json.loads(lines[0])["chunk_id"].startswith("virmire_")
