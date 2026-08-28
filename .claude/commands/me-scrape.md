---
description: Scrape the Mass Effect wiki into data/pages, then chunk and build the BM25 index.
---

Build or refresh the local lore corpus.

## Steps
1. Read `config/seeds.yaml` so you can report the depth/cap/rate that will be used.
2. Run the scraper (pass through any `--depth`, `--cap`, `--rate`, `--force` the user gave):
   `python scripts/scrape_wiki.py --seeds config/seeds.yaml $ARGUMENTS`
   Pages are written to `data/pages/` as they are fetched, and a re-run skips any
   page already on disk (re-fetching only the seeds to rebuild the frontier), so an
   interrupted crawl can just be run again to resume. `--force` re-fetches everything.
3. Show the summary line and the tail of `data/scrape_errors.log`.
4. Chunk the pages: `python scripts/chunk.py --pages data/pages --out data/chunks/chunks.jsonl`
5. Build the index: `python scripts/build_bm25.py --chunks data/chunks/chunks.jsonl --out data/bm25_index.pkl`

## Verify
- `ls data/pages | wc -l` is non-trivial (dozens+).
- `wc -l data/chunks/chunks.jsonl` > page count.
- `python scripts/retrieve.py --k 3 "Sovereign Reaper"` returns Sovereign-related chunks.
- Report counts for pages, chunks, fetch errors, and short/stub pages.
