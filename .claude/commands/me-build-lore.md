---
description: Summarize every in-scope scraped page into page_summaries/ and build the codex/ via the page-summarizer subagent.
---

Turn the raw corpus into factual summaries and a codex.

## Steps
1. Build the source list from both corpora — scraped pages and hand-corrected manual
   lore (`lore/manual/*.md`, excluding `README.md`) — minus pages already summarized
   and minus pages the corpus filter dropped (`data/lore_skipped.txt`, one
   `<slug>\t<reason>\t<size>` row per excluded page: planet-scan stubs,
   Andromeda-specific pages, mineral stubs):

   ```
   comm -23 \
     <( (ls data/pages 2>/dev/null; ls lore/manual 2>/dev/null | grep -v '^README.md$') \
        | sed 's/\.md$//' | sort -u ) \
     <( cat <(ls page_summaries 2>/dev/null | sed 's/\.md$//') \
            <(cut -f1 data/lore_skipped.txt 2>/dev/null | sed 's/\.md$//') \
        | sort -u )
   ```

   With `--force`, drop the `ls page_summaries` line from the second process
   substitution (re-summarize everything in scope) but STILL subtract
   `data/lore_skipped.txt` — that file is a deliberate corpus-quality filter, not a
   done-marker. To re-include a skipped page, delete its row from
   `data/lore_skipped.txt` first.

   Resolve each name to its real path under `data/pages/` or `lore/manual/` when
   handing it to the subagent.
2. Split that list into batches of ~15.
3. For each batch, dispatch the `page-summarizer` subagent with the batch's file paths (and `--force` if given).
   If one fails, retry it once, then log the batch to `data/lore_errors.log` and continue.

   **Sequential** is safe as-is. To run **waves of N batches in parallel** (faster wall
   clock, same token cost), give each parallel agent a unique `WAVE_ID` and tell it to
   write codex bullets to `codex/_inbox/<WAVE_ID>-<group>.md` (plain `- ` lines, no H1)
   instead of appending to `codex/*.md` directly — `page_summaries/<slug>.md` writes are
   already collision-free. After each wave finishes, merge the inbox:
   for each `codex/_inbox/*-<group>.md`, append its lines to `codex/<group>.md` (create
   with `# <Group>` H1 if missing), then de-dupe and alphabetically sort the bullet
   lines under the H1, then `rm codex/_inbox/*`. Recompute the remaining list (step 1)
   before dispatching the next wave.
4. After all batches, report how many summaries exist vs. how many in-scope source pages.

## Verify
- `ls page_summaries | wc -l` ≈ (`ls data/pages | wc -l` + `ls lore/manual | grep -vc '^README.md$'`) − `wc -l < data/lore_skipped.txt` (minus any logged skips).
- `ls codex` shows the group files that apply to the corpus.
- Spot-read 2 summaries against their source pages for accuracy and length (200-500 words).
