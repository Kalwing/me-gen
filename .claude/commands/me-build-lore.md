---
description: Summarize every scraped page into page_summaries/ and build the codex/ via the page-summarizer subagent.
---

Turn the raw corpus into factual summaries and a codex.

## Steps
1. List pages needing summaries:
   `comm -23 <(ls data/pages | sed 's/.md$//' | sort) <(ls page_summaries 2>/dev/null | sed 's/.md$//' | sort)`
   (all pages if `--force` was given).
2. Split that list into batches of ~15.
3. For each batch, dispatch the `page-summarizer` subagent with the batch's file paths (and `--force` if given).
   Run batches sequentially; if one fails, retry it once, then log the batch to `data/lore_errors.log` and continue.
4. After all batches, report how many summaries exist vs. how many pages.

## Verify
- `ls page_summaries | wc -l` ≈ `ls data/pages | wc -l` (minus logged skips).
- `ls codex` shows the group files that apply to the corpus.
- Spot-read 2 summaries against their source pages for accuracy and length (200-500 words).
