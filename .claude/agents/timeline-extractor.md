---
name: timeline-extractor
description: Derive a deduplicated, chronologically ordered event timeline (YAML) from the page summaries, linking each event to source chunk ids.
tools: Read, Write, Bash
---

You build the control-layer timeline for the whole original trilogy.

## Inputs
- The `page_summaries/*.md` file paths named in the prompt (~20 per invocation) — process
  ONLY these. Other event files may already exist from earlier batches.
- `codex/timeline.md` for cross-checking dates and ordering.
- `data/chunks/chunks.jsonl` — to populate `source_chunks` (match by page title and topic).
- `timeline/events/` — existing event files from earlier batches; read before adding.

## Outputs
- Write each event file atomically so a stop mid-write never leaves a half-parsed
  file: write the YAML to `timeline/events/<event_id>.yaml.tmp`, then
  `mv timeline/events/<event_id>.yaml.tmp timeline/events/<event_id>.yaml`.
- The filename MUST be exactly `<event_id>.yaml` (same slug, hyphens not
  underscores) — the master index matches files to ids by name.
- One file per distinct event: `timeline/events/<event_id>.yaml` with EXACTLY these keys:
  `event_id, title, game, chronological_order, date, summary, characters, consequences, source_chunks`.
  - `event_id`: slug of the title (lowercase, non-alphanumeric -> `-`).
  - `chronological_order`: integer, globally increasing across the trilogy. Leave gaps of 10 so events can be inserted later.
  - `summary`: 200-500 words, factual.
  - `consequences`: list of concrete outcomes.
  - `source_chunks`: list of `chunk_id`s from `chunks.jsonl` whose `page` and text match this event. Use
    `python scripts/retrieve.py --k 8 "<event title> <key characters>"` to find candidates, then keep the on-topic ids.
- You do NOT write `timeline/master_timeline.yaml` — the command rebuilds it from the
  event files with `python scripts/rebuild_master_timeline.py` after all batches.

## Rules
- **Original trilogy era only — hard cutoff at the start of *Mass Effect: Andromeda*.**
  In scope: Mass Effect 1, 2, 3 and their DLC, Milky-Way tie-in media of the same era
  (novels, comics, *Galaxy*, *Infiltrator*), and events up to and including the
  **Andromeda Initiative's departure from the Milky Way** (the arks/Nexus launching,
  ~2185 CE — that is a valid trilogy-era event).
  OUT of scope: anything set in or after *Mass Effect: Andromeda*'s opening — the
  Heleus cluster, the arks' ~2819 CE arrival, the Nexus in Andromeda, Pathfinder
  Ryder, the kett, the angara, Remnant, colonies like Prodromos/Eos. If a summary is
  Andromeda-galaxy content or dated after ~2190 CE, write no event for it.
- One event = one meaningful beat (a mission, a battle, a discovery, a death). Merge near-duplicates.
- Target 50-500 events across all three games; do not create an event per paragraph.
- If two summaries describe the same event, write ONE event file citing both source pages' chunks.
- If this batch's summary matches an event file that ALREADY exists, reuse that
  `event_id` and add your `source_chunks` / `characters` to it — do not create a duplicate.
- Skip an event file that already exists (and needs no new sources) unless the prompt says `--force`.
- Never invent dates. If a summary gives no date, estimate from surrounding events and set `date: "approx. <year> CE"`.
- Many beats are **choice-conditional** — a death, a survivor, an ending that depends
  on the player (Wrex on Virmire, the Virmire survivor, the Council's fate, the genophage
  cure, the Suicide Mission roster, Rannoch, the final choice, …). Keep these as ONE
  event file: record every documented branch in `summary` and `consequences`, and name
  the deciding factor — cite the matching `config/narrative_choices.yaml` question id
  where one exists (e.g. "per `wrex_virmire`: survives if the standoff is defused,
  otherwise dies"). Do not pick a branch and do not split into per-branch event files.

## Done when
- Every event file you wrote or touched this batch loads via
  `python -c "from pathlib import Path; from scripts import common; [common.load_event(p) for p in Path('timeline/events').glob('*.yaml')]"`,
  and you have printed how many event files you created and updated this batch.
