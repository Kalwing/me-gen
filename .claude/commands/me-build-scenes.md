---
description: Build scenes/*.yaml — the occasion layer, with attendance — from the page summaries via the scene-extractor subagent.
---

Build the scene layer: occasions, and who was in the room. Runs in waves and is
resumable — stop any time (Ctrl+C, killed session, rate limit) and re-run. Summary
stems listed in `scenes/.done` are skipped, and a batch interrupted mid-flight is simply
redone: its stems never reached the ledger, and `scene-extractor` extends records that
already exist rather than duplicating them, so re-running is idempotent.

The ~43 hand-checked records already in `scenes/` (Citadel DLC, ship banter, crew
relationships, loyalty missions, shore leave) were built against the proven generation
interface. This sweep fills the layer in behind that interface; it must not degrade it.

## Steps
1. Confirm `page_summaries/` is populated and `data/chunks/chunks.jsonl` exists; if not,
   tell the user to run `/me-build-lore` / `/me-scrape` first and stop.
2. Clean up after any interrupted run:
   - `find scenes -maxdepth 1 -name '*.yaml.tmp' -delete` — atomic-write temp files
     from a killed agent (a bare `rm -f scenes/*.yaml.tmp` glob errors under zsh when
     there's nothing to match, so use `find -delete`, which doesn't).
   - Drop any scene file that no longer parses (half-written by a hard stop). Its summary
     stems are not in `scenes/.done`, so the next batch rebuilds it:
     `python -m scripts.scenes --drop-unparseable`
   - `touch scenes/.done`.
3. Build the to-do list — summary stems in `page_summaries/` not already in
   `scenes/.done`, alphabetical so it is deterministic across sessions:
   ```
   comm -23 <(ls page_summaries/*.md | xargs -n1 basename | sed 's/\.md$//' | sort) \
            <(sort -u scenes/.done)
   ```
   On `--force`, `rm -f scenes/.done` first and take every stem. If the list is empty,
   skip to step 7.
4. Split it into batches of ~20 and run them in waves. **At most 4 `scene-extractor`
   subagents in flight**, on disjoint batches — no shared writes, since the controller
   owns `scenes/.done` and each record belongs to one occasion.
   Model: **haiku** by default; **sonnet** for a batch that is attendance-heavy or
   branch-heavy — the Citadel DLC and shore-leave pages, party and squadmate-banter
   pages, loyalty missions, and the choice-conditional spine (Virmire, Tuchanka,
   Rannoch, the Suicide Mission, the Citadel coup).
5. For each batch:
   - Dispatch `scene-extractor` with that batch's `page_summaries/*.md` paths (and
     `--force` if given).
   - On success, append the batch's stems to `scenes/.done`, one per line. Only the
     controller writes this file, one batch at a time, so the append is never torn.
     Append the stems that held no occasion too — they are done, not pending.
   - On failure, retry once; then log the batch to `data/scene_errors.log` and continue.
6. Normalize scene filenames to their `scene_id` (an agent may emit `foo_bar.yaml` for
   `scene_id: foo-bar`, which the validator rejects):
   ```
   for f in scenes/*.yaml; do
     [ -e "$f" ] || continue
     id=$(grep -m1 '^scene_id:' "$f" | sed 's/scene_id: *//; s/["'"'"']//g' | tr -d '[:space:]')
     [ -n "$id" ] && [ "$id" != "$(basename "$f" .yaml)" ] && mv "$f" "scenes/$id.yaml"
   done
   ```
7. Validate the whole set against `scripts/scenes.py`, the schema's only authority:
   `python -m scripts.scenes --check`. Fix or drop what it
   names — an unparseable or unreferenced record breaks every later `build_pack.py`.
   The validator does not (and cannot) check that a `participants` name is actually
   *evidenced* in the record's cited chunks — an agent can invent attendance from a
   general association with the location or topic. Spot-check the wave's new files
   this way: for each participant name, grep the text of that beat's/record's
   `source_chunks` in `data/chunks/chunks.jsonl` for the name; if it never appears,
   the attendance is fabricated and the name must be dropped or re-sourced. Do this
   for at least the new records with 3+ participants each wave; a single ungrounded
   name here is exactly the failure the scene layer exists to prevent.
8. **Pause at the end of each wave**: commit (`scenes/` + `scenes/.done`), report the
   wave's counts and how many stems remain, and stop. The sweep spans 1,600+ summaries;
   waves are the resume points, and context can be cleared between them.
9. When the to-do list finally comes back empty, report the total scene count by `kind`
   and by `game`:
   `python -m scripts.scenes --list | sed -n 's/.*(\(.*\))/\1/p' | sort | uniq -c`

## Verify
- `python -m scripts.scenes --check` runs clean.
- `python -m pytest -q` is green.
- Every stem in `scenes/.done` is a real `page_summaries/<stem>.md`, and no stem
  appears twice.
- Spot-check 3 new records against `data/pages/`: `participants` / `private_to` /
  `heard_by` match who the page says was present, beats are in causal order, and their
  `source_chunks` ids exist in `chunks.jsonl` and are on-topic.
- Attendance still resolves per narrator:
  `python -m scripts.scenes --list --for wrex` marks scenes witnessed / heard / absent.
- The hand-checked records are untouched unless a batch legitimately extended one:
  `git diff --stat scenes/` should show new files, not rewrites of the original 43.
