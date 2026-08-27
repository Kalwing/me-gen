---
description: Generate a narrated Mass Effect episode. First run produces an outline for approval; `--continue <run-dir>` writes the full script.
---

Usage:
- `/me-generate <narrator> "<theme1, theme2>" [--words 8000]` — outline phase (stops for approval).
- `/me-generate --continue <run-dir>` — generation phase.

## Outline phase
1. Require `timeline/master_timeline.yaml` and `data/bm25_index.pkl`. If missing, tell the user to run
   `/me-scrape`, `/me-build-lore`, `/me-build-timeline` and stop.
2. Require `config/narrators/<narrator>.yaml`. If missing, list the available bibles and stop.
3. Scaffold the run: `python scripts/new_run.py <narrator> "<themes>" --words <words>` and capture the printed path.
4. Dispatch the `outline-writer` subagent for that run dir.
5. Print the outline path and its section table. Tell the user:
   "Review and edit `output/<run>/outline.yaml`, then delete the first line (`# UNAPPROVED …`)
   and run `/me-generate --continue output/<run>`." STOP here.

## Generation phase (`--continue <run-dir>`)
1. Refuse unless
   `python -c "from pathlib import Path,sys; from scripts import common; sys.exit(0 if common.outline_is_approved(Path('<run-dir>')) else 1)"`
   exits 0. If it fails, tell the user the outline is still unapproved and stop.
2. For each section in `outline.yaml`, in order: dispatch `section-writer` with the run dir, that
   section object, and the narrator. Run sequentially. Retry a failed section once, then log to
   `output/<run>/gen_errors.log` and continue.
3. For each section in order, dispatch `smoother` with the run dir and section id.
4. Dispatch `consistency-checker` for the run dir (it does its own find-then-fix two passes).
5. Assemble: `python scripts/assemble_episode.py <run-dir>`.
6. Print the episode path, its word count vs. `target_words`, and the `issues.md` summary.

## Verify
- `output/<run>/episode.md` exists and is within 15% of `target_words`.
- `output/<run>/sources.json` has a non-empty entry (or an explicit `__warnings__` note) for every section.
- `output/<run>/issues.md` has a `## Fixes applied` section.
- Read the first and last 300 words aloud: the voice matches the narrator bible and nothing invented stands out.
