---
description: Derive timeline/events/*.yaml and master_timeline.yaml from the page summaries via the timeline-extractor subagent.
---

Build the control-layer timeline. Runs in batches and is resumable: stop any
time between batches and re-run — finished summaries (listed in `timeline/.done`)
are skipped, and `master_timeline.yaml` is rebuilt from whatever event files exist.

## Steps
1. Confirm `page_summaries/` is populated and `data/chunks/chunks.jsonl` exists; if not, tell the user to run `/me-build-lore` / `/me-scrape` first and stop.
2. Build the to-do list: summary stems in `page_summaries/` not already in `timeline/.done`
   (all of them if `--force` was given — on `--force` also `rm -f timeline/.done`).
   If the list is empty, skip to step 5.
3. Split the list into batches of ~20.
4. For each batch, in order:
   - Dispatch the `timeline-extractor` subagent with that batch's `page_summaries/*.md` paths
     (and `--force` if given).
   - On success, append the batch's stems to `timeline/.done` (one per line).
   - On failure, retry once; then log the batch to `data/timeline_errors.log` and continue.
5. Rebuild the master index: `python scripts/rebuild_master_timeline.py`
   (atomic; safe to run repeatedly).
6. Run the load check:
   `python -c "from pathlib import Path; from scripts import common; print(len(common.load_events(Path('timeline/events'))), 'events')"`
7. Check the player's canon file: `test -f config/narrative_choices.yaml`. It is a
   tracked file and should always be present.
8. Backfill the canon catalogue:
   `python scripts/sync_narrative_choices.py config/narrative_choices.yaml`.
   This appends a blank stub (`answer: ""`, `detail: ""`, with `options` pre-filled
   where the outcome is discrete) for every canonical trilogy decision point not
   already in the file — existing questions, answers and ordering are never touched,
   so it is a no-op once the file is complete. Report which ids (if any) it added.
9. Remind the user to review `config/narrative_choices.yaml` and set `answer`/`detail`
   (or narrow `options` to one value) for whatever they remember of their playthrough
   (Shepard background/profile/class, ME1/2/3 decisions), including any stubs step 8
   just added. Anything left blank falls back to default canon.
10. Report the event count and the first/last entries of `timeline/master_timeline.yaml`.

## Verify
- Every `event_id` in `master_timeline.yaml` has a matching `timeline/events/<id>.yaml`.
- `chronological_order` is non-decreasing in `master_timeline.yaml`.
- Event count is between 50 and 500.
- Spot-check 3 events: `source_chunks` ids exist in `chunks.jsonl` and are on-topic.
- `config/narrative_choices.yaml` exists and `python scripts/narrative_choices.py config/narrative_choices.yaml` runs clean.
- `python scripts/sync_narrative_choices.py config/narrative_choices.yaml --check` reports nothing missing.
