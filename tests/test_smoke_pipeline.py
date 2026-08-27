import shutil
from pathlib import Path

import yaml

from scripts import assemble_episode, build_bm25, chunk, common, new_run, retrieve

FIX = Path(__file__).parent / "fixtures"


def test_deterministic_spine(tmp_path):
    # 1. chunk the mini corpus
    chunks_path = tmp_path / "chunks.jsonl"
    n = chunk.chunk_dir(FIX / "mini_corpus", chunks_path, size=120, overlap=20)
    assert n >= 3

    # 2. build the BM25 index
    index = tmp_path / "bm25_index.pkl"
    assert build_bm25.build(chunks_path, index) == n

    # 3. retrieval finds the right page for a lore query
    hits = retrieve.retrieve(index, ["Sovereign Reaper Citadel"], k=3)
    assert hits and hits[0]["page"] == "Sovereign"

    # 4. load the hand-written timeline
    events = common.load_events(FIX / "mini_timeline")
    assert set(events) == {"eden_prime", "virmire_decision"}

    # 5. scaffold a run and hand-approve an outline built from the timeline
    run = new_run.new_run("garrus", ["the cost of war"], 200, tmp_path / "output")
    outline = {
        "narrator": "garrus", "themes": ["the cost of war"], "target_words": 200,
        "sections": [
            {"id": "eden_prime", "title": "Eden Prime", "events": ["eden_prime"], "target_words": 100},
            {"id": "virmire", "title": "Virmire", "events": ["virmire_decision"], "target_words": 100},
        ],
    }
    (run / "outline.yaml").write_text(yaml.safe_dump(outline, sort_keys=False))
    assert common.outline_is_approved(run)

    # 6. stand in for section-writer subagents, then assemble
    for s in outline["sections"]:
        ev = events[s["events"][0]]
        (run / "sections" / f"{s['id']}.md").write_text(ev["summary"].strip() + "\n")
    episode = assemble_episode.assemble(run)
    text = episode.read_text()
    assert text.index("## Eden Prime") < text.index("## Virmire")
    # lower bound relaxed per controller ruling: brief's fixtures yield ~83 words; 120 floor contradicted Step 4
    assert 70 <= common.word_count(text) <= 400
