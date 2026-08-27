---
description: Derive timeline/events/*.yaml and master_timeline.yaml from the page summaries via the timeline-extractor subagent.
---

Build the control-layer timeline.

## Steps
1. Confirm `page_summaries/` is populated and `data/chunks/chunks.jsonl` exists; if not, tell the user to run `/me-build-lore` / `/me-scrape` first and stop.
2. Dispatch the `timeline-extractor` subagent (pass `--force` through if given).
3. When it returns, run the load check:
   `python -c "from pathlib import Path; from scripts import common; print(len(common.load_events(Path('timeline/events'))), 'events')"`
4. Seed the player's canon file if absent:
   `if [ ! -f config/narrative_choices.yaml ]; then cp config/narrative_choices.template.yaml config/narrative_choices.yaml; fi`
   Then tell the user to open `config/narrative_choices.yaml` and fill in `answer`/`detail`
   for whatever they remember of their playthrough (Shepard background/profile/class, ME1/2/3
   decisions). Anything left blank falls back to default canon.
5. Report the event count and the first/last entries of `timeline/master_timeline.yaml`.

## Verify
- Every `event_id` in `master_timeline.yaml` has a matching `timeline/events/<id>.yaml`.
- `chronological_order` is strictly increasing in `master_timeline.yaml`.
- Event count is between 50 and 500.
- Spot-check 3 events: `source_chunks` ids exist in `chunks.jsonl` and are on-topic.
- `config/narrative_choices.yaml` exists and `python scripts/narrative_choices.py config/narrative_choices.yaml` runs clean.
