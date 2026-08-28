---
description: Generate a narrated Mass Effect episode. First run produces an outline for approval; `--continue <run-dir>` writes the full script.
---

Usage:
- `/me-generate <narrator> "<theme1, theme2>" [--brief "<free text>"] [--words 8000]` — outline phase (stops for approval).
- `/me-generate --continue <run-dir>` — generation phase.

`--brief` is an optional free-text note that sits alongside the themes — e.g.
`--brief "Tali romance; speaks by phone after a fight, a bit tired"`. It does two
things:
- **Framing** — the occasion, scene, mood, and who the narrator is addressing.
- **Finer canon** — it refines `config/narrative_choices.yaml` for this one episode:
  it picks among options the choices file leaves open (e.g. which romance when
  several are recorded), adds playthrough detail not in the file, and where the
  brief and the choices file speak to the same point the **brief wins for this run**.
It invents no world lore, but canon does more than colour the telling: many
timeline events are choice-conditional (a death on Virmire, the Council's fate,
the genophage, the Suicide Mission roster, the ending), and `narrative_choices` —
refined by the brief — decides **which branch is true**, hence which sections
exist and which outcomes are narrated. Non-conditional events, dates, and lore
still come only from the timeline and retrieved evidence.

## Outline phase
1. Require `timeline/master_timeline.yaml` and `data/bm25_index.pkl`. If missing, tell the user to run
   `/me-scrape`, `/me-build-lore`, `/me-build-timeline` and stop.
2. Require `config/narrators/<narrator>.yaml`. If missing, list the available bibles and stop.
3. Scaffold the run: `python scripts/new_run.py <narrator> "<themes>" --words <words> [--brief "<brief>"]`
   and capture the printed path. (Pass `--brief` only if the user gave one; it is stored as
   `brief:` in `outline.yaml`.)
4. Load the player's canon: run
   `python scripts/narrative_choices.py config/narrative_choices.yaml` and print its output.
   If it prints `all questions unanswered`, warn the user that the recap will use default
   trilogy canon (they can edit `config/narrative_choices.yaml` and re-run) — do NOT stop.
5. Dispatch the `outline-writer` subagent for that run dir.
6. Print the outline path and its section table. Tell the user:
   "Review and edit `output/<run>/outline.yaml`, then delete the first line (`# UNAPPROVED …`)
   and run `/me-generate --continue output/<run>`." STOP here.

## Generation phase (`--continue <run-dir>`)
1. Refuse unless
   `python -c "import sys; from pathlib import Path; from scripts import common; sys.exit(0 if common.outline_is_approved(Path('<run-dir>')) else 1)"`
   exits 0. If it fails, tell the user the outline is still unapproved and stop.
2. For each section in `outline.yaml`, in order: dispatch `section-writer` with the run dir, that
   section object, the narrator, and the outline's `brief` (if non-empty). Run sequentially.
   Retry a failed section once, then log to `output/<run>/gen_errors.log` and continue.
3. For each section in order, dispatch `smoother` with the run dir and section id.
4. Dispatch `consistency-checker` for the run dir (it does its own find-then-fix two passes).
5. Assemble: `python scripts/assemble_episode.py <run-dir>`.
6. Print the episode path, its word count vs. `target_words`, and the `issues.md` summary.

## Verify
- `output/<run>/episode.md` exists and is within 15% of `target_words`.
- `output/<run>/sources.json` has a non-empty entry (or an explicit `__warnings__` note) for every section.
- `output/<run>/issues.md` has a `## Fixes applied` section.
- Read the first and last 300 words aloud: the voice matches the narrator bible and nothing invented stands out.
