---
description: Derive timeline/events/*.yaml and master_timeline.yaml from the page summaries via the timeline-extractor subagent.
---

Build the control-layer timeline. Runs in batches and is resumable: stop any
time (Ctrl+C, killed session, rate limit) and re-run — finished summaries
(listed in `timeline/.done`) are skipped, and `master_timeline.yaml` is rebuilt
from whatever event files exist. A batch that was interrupted mid-flight is
simply redone: its stems never reached `timeline/.done`, and the
`timeline-extractor` agent skips event files that already exist, so re-running is
idempotent (no duplicate events).

## Steps
1. Confirm `page_summaries/` is populated and `data/chunks/chunks.jsonl` exists; if not, tell the user to run `/me-build-lore` / `/me-scrape` first and stop.
2. Prepare the timeline dir and clean up after any interrupted run:
   - `mkdir -p timeline/events`
   - `rm -f timeline/events/*.yaml.tmp` — drop atomic-write temp files from a killed agent.
   - Drop any event file that no longer parses (half-written by a hard stop). Its
     summary stems are not in `timeline/.done`, so the next batch rebuilds it:
     ```
     for f in timeline/events/*.yaml; do
       [ -e "$f" ] || continue
       python -c "from pathlib import Path; from scripts import common; common.load_event(Path('$f'))" >/dev/null 2>&1 \
         || { echo "dropped partial $f"; rm -f "$f"; }
     done
     ```
3. Build the to-do list: summary stems in `page_summaries/` not already in `timeline/.done`
   (all of them if `--force` was given — on `--force` also `rm -f timeline/.done`).
   If the list is empty, skip to step 7.
4. Split the list into batches of ~20. Run **at most 2 `timeline-extractor` subagents
   at a time** (disjoint batch paths — no shared writes except append-only
   `timeline/.done`, which the controller writes, never the agents).
5. For each batch, in order (2 in flight max):
   - Dispatch the `timeline-extractor` subagent with that batch's `page_summaries/*.md` paths
     (and `--force` if given).
   - On success, append the batch's stems to `timeline/.done` (one per line). Only the
     controller writes this file, one batch at a time, so the append is never torn.
   - On failure, retry once; then log the batch to `data/timeline_errors.log` and continue.
6. Normalize event filenames to their `event_id` (a subagent may emit
   `foo_bar.yaml` for `event_id: foo-bar`, which breaks the master↔file match):
   ```
   for f in timeline/events/*.yaml; do
     [ -e "$f" ] || continue
     id=$(grep -m1 '^event_id:' "$f" | sed 's/event_id: *//; s/["'"'"']//g' | tr -d '[:space:]')
     [ -n "$id" ] && [ "$id" != "$(basename "$f" .yaml)" ] && mv "$f" "timeline/events/$id.yaml"
   done
   ```
7. **Renumber — only when the whole sweep is done** (the step-3 to-do list came
   back empty): `python scripts/renumber_timeline.py`. Each `timeline-extractor`
   batch guesses a *global* `chronological_order` in isolation, so mid-sweep the
   integers are only locally sorted (ME3 events land in the ME1 range). This
   one-shot deterministic pass re-derives the order from data every event already
   carries — `(year parsed from date, game rank ME1<ME2<ME3, prior order as a
   hint)` — and rewrites `chronological_order` as 10, 20, 30, … It is idempotent,
   touches only the `chronological_order:` line of each file, and also rebuilds
   `master_timeline.yaml` (so step 8 is then a no-op). **Skip it on a partial
   sweep** — run it once, at the very end.
8. Rebuild the master index: `python scripts/rebuild_master_timeline.py`
   (atomic; safe to run repeatedly).
9. Run the load check:
   `python -c "from pathlib import Path; from scripts import common; print(len(common.load_events(Path('timeline/events'))), 'events')"`
10. Check the player's canon file: `test -f config/narrative_choices.yaml`. It is a
   tracked file and should always be present.
11. Backfill the canon catalogue:
   `python scripts/sync_narrative_choices.py config/narrative_choices.yaml`.
   This appends a blank stub (`answer: ""`, `detail: ""`, with `options` pre-filled
   where the outcome is discrete) for every canonical trilogy decision point not
   already in the file — existing questions, answers and ordering are never touched,
   so it is a no-op once the file is complete. Report which ids (if any) it added.
12. Remind the user to review `config/narrative_choices.yaml` and set `answer`/`detail`
   (or narrow `options` to one value) for whatever they remember of their playthrough
   (Shepard background/profile/class, ME1/2/3 decisions), including any stubs step 11
   just added. Anything left blank falls back to default canon.
13. Report the event count and the first/last entries of `timeline/master_timeline.yaml`.

## Verify
- Every `event_id` in `master_timeline.yaml` has a matching `timeline/events/<id>.yaml`.
- `chronological_order` is non-decreasing in `master_timeline.yaml`.
- After a completed sweep, `python scripts/renumber_timeline.py --check` reports
  nothing out of place (events ordered by in-universe year, then game).
- Event count is between 50 and 500.
- Spot-check 3 events: `source_chunks` ids exist in `chunks.jsonl` and are on-topic.
- `config/narrative_choices.yaml` exists and `python scripts/narrative_choices.py config/narrative_choices.yaml` runs clean.
- `python scripts/sync_narrative_choices.py config/narrative_choices.yaml --check` reports nothing missing.
