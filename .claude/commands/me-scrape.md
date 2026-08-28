---
description: Scrape the Mass Effect wiki into data/pages, then chunk and build the BM25 index.
---

Build or refresh the local lore corpus.

## Steps
1. Read `config/seeds.yaml` so you can report the depth/cap/rate that will be used.
2. Run the scraper (pass through any `--depth`, `--cap`, `--rate`, `--force` the user gave):
   `python scripts/scrape_wiki.py --seeds config/seeds.yaml $ARGUMENTS`
   Pages are written to `data/pages/` as they are fetched. The crawl frontier
   (pending `[title, depth]` queue + seen set) is persisted to
   `data/crawl_state.json` every 10 pages, on clean exit, and on SIGTERM/SIGINT.
   A re-run loads that file and continues draining the saved queue — no wiki
   re-walk. When it stops (cap hit or signal) it prints how many **distinct
   pages are still to crawl**; if the user wants them, re-run to fetch the next
   batch or raise `--cap` for a bigger one. `--force` ignores existing pages and
   state and starts fresh.
3. Show the summary line and the tail of `data/scrape_errors.log`.
4. Chunk the pages: `python scripts/chunk.py --pages data/pages --out data/chunks/chunks.jsonl`
   Chunks are appended per page and finished pages are tracked in
   `data/chunks/chunks.jsonl.done`, so an interrupted run resumes on re-run
   (a half-written page from a kill is discarded). `--force` rechunks all.
5. Build the index: `python scripts/build_bm25.py --chunks data/chunks/chunks.jsonl --out data/bm25_index.pkl`
   Written atomically (temp + rename) — a killed run never corrupts the index.
   A re-run is a no-op when the index is already newer than chunks.jsonl;
   `--force` rebuilds anyway.

## Verify
- `ls data/pages | wc -l` is non-trivial (dozens+).
- `wc -l data/chunks/chunks.jsonl` > page count.
- `python scripts/retrieve.py --k 3 "Sovereign Reaper"` returns Sovereign-related chunks.
- Report counts for pages, chunks, fetch errors, and short/stub pages.
