---
description: Summarize every scraped page into page_summaries/ and build the codex/ via the page-summarizer subagent.
---

Turn the raw corpus into factual summaries and a codex.

## Steps
1. Build the source list from both corpora — scraped pages and hand-corrected manual
   lore (`lore/manual/*.md`, excluding `README.md`):
   `comm -23 <( (ls data/pages 2>/dev/null; ls lore/manual 2>/dev/null | grep -v '^README.md$') | sed 's/.md$//' | sort -u) <(ls page_summaries 2>/dev/null | sed 's/.md$//' | sort)`
   (all pages if `--force` was given). Resolve each name to its real path under
   `data/pages/` or `lore/manual/` when handing it to the subagent.
2. Split that list into batches of ~15.
3. For each batch, dispatch the `page-summarizer` subagent with the batch's file paths (and `--force` if given).
   Run batches sequentially; if one fails, retry it once, then log the batch to `data/lore_errors.log` and continue.
4. After all batches, report how many summaries exist vs. how many source pages.

## Verify
- `ls page_summaries | wc -l` ≈ `ls data/pages | wc -l` + `ls lore/manual | grep -vc '^README.md$'` (minus logged skips).
- `ls codex` shows the group files that apply to the corpus.
- Spot-read 2 summaries against their source pages for accuracy and length (200-500 words).
