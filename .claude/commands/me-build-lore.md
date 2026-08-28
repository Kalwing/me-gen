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
   pg=$(mktemp); man=$(mktemp)
   ls data/pages 2>/dev/null | sed 's/\.md$//' | sort -u > "$pg"
   # manual doc slugs (README excluded); any that ALSO exist as a scraped page get a
   # `manual-` prefix so the collision is not silently deduped (arcturus-station,
   # destiny-ascension). `manual-<slug>` resolves to lore/manual/<slug>.md and its
   # summary checkpoint is page_summaries/manual-<slug>.md.
   ls lore/manual 2>/dev/null | grep -v '^README\.md$' | sed 's/\.md$//' | sort -u \
     | while read -r s; do
         grep -qxF "$s" "$pg" && echo "manual-$s" || echo "$s"
       done > "$man"
   comm -23 \
     <( cat "$pg" "$man" | sort -u ) \
     <( cat <(ls page_summaries 2>/dev/null | sed 's/\.md$//') \
            <(cut -f1 data/lore_skipped.txt 2>/dev/null | sed 's/\.md$//') \
        | sort -u )
   rm -f "$pg" "$man"
   ```

   With `--force`, drop the `ls page_summaries` line from the second process
   substitution (re-summarize everything in scope) but STILL subtract
   `data/lore_skipped.txt` — that file is a deliberate corpus-quality filter, not a
   done-marker. To re-include a skipped page, delete its row from
   `data/lore_skipped.txt` first.

   Resolve each name to its real path when handing it to the subagent: a
   `manual-<slug>` name is `lore/manual/<slug>.md` (and must be passed ALONGSIDE
   `data/pages/<slug>.md` so the summarizer can merge them — see page-summarizer
   "Colliding slug"); a bare `<slug>` is `data/pages/<slug>.md`, or
   `lore/manual/<slug>.md` when no scraped page of that name exists.
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
5. **Narrator style references** (post-sweep — needs the corpus and summaries present).
   For each `config/narrators/<slug>.yaml` (not `.style.md`), resolve the narrator's
   source files:
   - their character page: `data/pages/*<name>*.md` (the wiki page for the person,
     e.g. `tali-zorah-nar-rayya.md`, `urdnot-wrex.md`);
   - dialogue/quote pages that include them: `data/pages/*<name>*-unique-dialogue.md`,
     and any `*-battle-quotes` / cut-content `*-voicelines` pages where they speak;
   - `lore/manual/*<name>*.md` deep-dive analyses.
   Dispatch the `narrator-style-extractor` subagent once per narrator with that list;
   it writes `config/narrators/<slug>.style.md`. Narrators with no source material get
   no file (that is fine). Safe to run in a parallel wave — one output file per narrator.

## Verify
- `ls page_summaries | wc -l` ≈ (`ls data/pages | wc -l` + `ls lore/manual | grep -vc '^README.md$'`) − `wc -l < data/lore_skipped.txt` (minus any logged skips).
- `ls codex` shows the group files that apply to the corpus.
- Spot-read 2 summaries against their source pages for accuracy and length (200-500 words).
