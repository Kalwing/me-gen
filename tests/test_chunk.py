import json
from pathlib import Path

from scripts import chunk, common


def _make_page(tmp_path, sentences, heading="Mission", name="virmire", title="Virmire"):
    body = f"## {heading}\n\n" + " ".join(sentences) + "\n"
    p = tmp_path / f"{name}.md"
    common.write_frontmatter_md(
        p,
        {"title": title, "game": "Mass Effect",
         "url": f"https://masseffect.fandom.com/wiki/{title}"},
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
    assert rows[0]["source"] == "virmire"
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


def test_chunk_dir_resumes_only_new_pages(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    _make_page(pages, [f"Alpha {i}." for i in range(40)], name="a", title="A")
    _make_page(pages, [f"Bravo {i}." for i in range(40)], name="b", title="B")
    out = tmp_path / "chunks.jsonl"

    first = chunk.chunk_dir(pages, out, size=30, overlap=5)
    assert first > 0
    manifest = (tmp_path / "chunks.jsonl.done").read_text().split()
    assert set(manifest) == {"a", "b"}

    _make_page(pages, [f"Charlie {i}." for i in range(40)], name="c", title="C")
    second = chunk.chunk_dir(pages, out, size=30, overlap=5)
    sources = {json.loads(ln)["source"] for ln in out.read_text().splitlines()}
    assert sources == {"a", "b", "c"}
    # only C was chunked the second time
    assert second > 0
    c_lines = sum(1 for ln in out.read_text().splitlines()
                  if json.loads(ln)["source"] == "c")
    assert second == c_lines


def test_chunk_dir_drops_partial_page_from_killed_run(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    _make_page(pages, [f"Alpha {i}." for i in range(40)], name="a", title="A")
    out = tmp_path / "chunks.jsonl"
    chunk.chunk_dir(pages, out, size=30, overlap=5)

    # simulate a crash mid-way through page "b": some b-rows + a truncated line,
    # with "b" never recorded in the manifest
    with out.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"chunk_id": "b_001", "source": "b", "text": "x"}) + "\n")
        fh.write('{"chunk_id": "b_002", "source": "b", "tex')  # truncated
    _make_page(pages, [f"Bravo {i}." for i in range(40)], name="b", title="B")

    chunk.chunk_dir(pages, out, size=30, overlap=5)
    rows = [json.loads(ln) for ln in out.read_text().splitlines()]
    assert all(len(r) > 3 for r in rows if r["source"] == "b")  # real rows, not the stub
    assert not any(r.get("text") == "x" for r in rows)


def test_chunk_dir_includes_manual_dir_with_prefix(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    manual = tmp_path / "manual"
    manual.mkdir()
    _make_page(pages, [f"Alpha {i}." for i in range(40)], name="a", title="A")
    _make_page(manual, [f"Deep {i}." for i in range(40)], name="b", title="B")
    (manual / "README.md").write_text("# not lore\n", encoding="utf-8")
    out = tmp_path / "chunks.jsonl"

    chunk.chunk_dir(pages, out, size=30, overlap=5, manual_dir=manual)
    rows = [json.loads(ln) for ln in out.read_text().splitlines()]
    sources = {r["source"] for r in rows}
    assert sources == {"a", "manual-b"}  # README.md excluded
    assert all(r["chunk_id"].startswith("manual-b_")
               for r in rows if r["source"] == "manual-b")
    assert (tmp_path / "chunks.jsonl.done").read_text().split() == ["a", "manual-b"] \
        or set((tmp_path / "chunks.jsonl.done").read_text().split()) == {"a", "manual-b"}


def test_chunk_dir_manual_stem_collision_keeps_both(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    manual = tmp_path / "manual"
    manual.mkdir()
    _make_page(pages, [f"Wiki {i}." for i in range(40)],
               name="arcturus-station", title="Arcturus Station")
    _make_page(manual, [f"Transcript {i}." for i in range(40)],
               name="arcturus-station", title="Arcturus Station")
    out = tmp_path / "chunks.jsonl"

    chunk.chunk_dir(pages, out, size=30, overlap=5, manual_dir=manual)
    rows = [json.loads(ln) for ln in out.read_text().splitlines()]
    sources = {r["source"] for r in rows}
    assert sources == {"arcturus-station", "manual-arcturus-station"}
    wiki_text = " ".join(r["text"] for r in rows if r["source"] == "arcturus-station")
    manual_text = " ".join(r["text"] for r in rows
                           if r["source"] == "manual-arcturus-station")
    assert "Wiki 0" in wiki_text and "Transcript 0" in manual_text


def test_chunk_dir_resumes_new_manual_file_only(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    manual = tmp_path / "manual"
    manual.mkdir()
    _make_page(pages, [f"Alpha {i}." for i in range(40)], name="a", title="A")
    _make_page(manual, [f"Deep {i}." for i in range(40)], name="m1", title="M1")
    out = tmp_path / "chunks.jsonl"
    chunk.chunk_dir(pages, out, size=30, overlap=5, manual_dir=manual)

    _make_page(manual, [f"More {i}." for i in range(40)], name="m2", title="M2")
    second = chunk.chunk_dir(pages, out, size=30, overlap=5, manual_dir=manual)
    assert second > 0
    m2_lines = sum(1 for ln in out.read_text().splitlines()
                   if json.loads(ln)["source"] == "manual-m2")
    assert second == m2_lines  # only the new manual file was chunked


def test_chunk_dir_force_rechunks_all(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    _make_page(pages, [f"Alpha {i}." for i in range(40)], name="a", title="A")
    out = tmp_path / "chunks.jsonl"
    chunk.chunk_dir(pages, out, size=30, overlap=5)
    again = chunk.chunk_dir(pages, out, size=30, overlap=5, force=True)
    assert again > 0  # force ignores the manifest
