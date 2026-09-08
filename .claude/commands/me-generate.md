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
- **Finer canon** — it refines `config/canon/choices.yaml` for this one episode:
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
3. Scaffold the run: `PYTHONPATH=. .venv/bin/python scripts/new_run.py <narrator> "<themes>" --words <words> [--brief "<brief>"] [--form <form>]`
   and capture the printed path. (Pass `--brief` only if the user gave one; it is stored as
   `brief:` in `outline.yaml`. Pass `--form` only if the user named one from
   `config/forms.yaml`; left blank, `outline-writer` chooses the form and explains the
   choice in `form_note`.)
4. Load the player's canon: run
   `PYTHONPATH=. .venv/bin/python scripts/canon.py` and print its output.
   If it prints `all questions unanswered`, warn the user that the recap will use default
   trilogy canon (they can edit `config/canon/choices.yaml` and re-run) — do NOT stop.
5. Make sure the index knows about the scene layer:
   `.venv/bin/python scripts/build_bm25.py` (a no-op when it is already newer than its sources).
6. Dispatch the `outline-writer` subagent for that run dir.
7. Print the outline path, the chosen `form` and `form_note`, and the section table with
   each section's `promises`. Report any question the outline-writer appended to
   `config/canon/questions.yaml`. Tell the user:
   "Review and edit `output/<run>/outline.yaml` — the `form`, the section list, and
   especially each section's `promises` and `retrieval` keys, which are what the episode
   will be built and audited against — then delete the first line (`# UNAPPROVED …`) and
   run `/me-generate --continue output/<run>`." STOP here. This gate is where a missing
   beat or a wrong retrieval key is cheap to fix; after it, everything downstream is
   deterministic from what it says.

## Generation phase (`--continue <run-dir>`)
1. Refuse unless
   `python -c "import sys; from pathlib import Path; from scripts import common; sys.exit(0 if common.outline_is_approved(Path('<run-dir>')) else 1)"`
   exits 0. If it fails, tell the user the outline is still unapproved and stop.
2. **Build the evidence packs:** `PYTHONPATH=. .venv/bin/python scripts/build_pack.py <run-dir> --all` (the `PYTHONPATH` is required — the script imports `scripts.canon`).
   This is deterministic and it hard-stops: a section naming a scene or event that does not
   exist, or a retrieval key that returns nothing in any kind, exits non-zero and names the
   gap. If it fails, print the gaps and tell the user to fix those keys in `outline.yaml`
   and re-run — do NOT proceed, and do not pass `--allow-thin` on your own initiative. An
   empty pack is how a section gets written from the model's memory of Mass Effect instead
   of from the corpus. Report every warning it prints, especially a scene the narrator has
   no route to.
3. Read the voice checkpoint state:
   `python -c "from pathlib import Path; from scripts import common; print(common.voice_check_state(Path('<run-dir>')))"`
   and branch on it — `missing` → step 4, `pending` → step 5, `approved` → step 6.
4. **Voice checkpoint — first section only.** Dispatch `section-writer` for the *first* section
   in `outline.yaml` and nothing else. Then write `output/<run>/voice_check.md`:

   ```
   # UNAPPROVED — voice check. Delete this line to approve, then re-run --continue.

   <the full text of the first section, verbatim>
   ```

   Print the section in the chat too, and ask the user to read it for **voice and lore
   handling, not facts**:
   - *Voice* — does the narrator sound like themselves: cadence, register, how they digress,
     how they avoid a subject, what they would never say?
   - *Lore* — is the history and worldbuilding **integrated the way
     `docs/generation-example.md` integrates it**: reached for eagerly, carried by the
     narrator's opinion about it, load-bearing in the scene? Or is it recited — correct facts
     delivered in a neutral register that could belong to any narrator, or hung on the plot as
     garnish? Density without integration is the failure mode; so is a clean plot recap.
   Before writing the file, re-read `docs/generation-example.md` and judge the draft against it
   yourself, and say plainly where the draft falls short of it. STOP here. Fourteen more
   sections written in a voice that is subtly off is the expensive failure this checkpoint
   exists to prevent.
5. **The checkpoint is pending.** If the user has given voice feedback (in chat or as edits to
   `voice_check.md`), act on it before anything else:
   - Fold every correction into `config/narrators/<narrator>.yaml` first — that is the durable
     fix and it is what the remaining sections will be written against. Feedback about *how*
     they talk belongs in `diction` / `signature` / `avoid`; feedback about *what* they wander
     into and the rhythm of the wandering belongs in `digressions`. Quote the offending phrase
     in the `avoid` entry so the failure is named, not merely described.
   - Re-dispatch `section-writer` for the first section, refresh `voice_check.md` from the new
     draft, and STOP again. Repeat until the user clears the marker line.
   If the user has given no feedback, just tell them the checkpoint is still waiting and stop.
6. For each **remaining** section in `outline.yaml`, in order: dispatch `section-writer` with
   the run dir and the section id. It reads that section's pack and the narrator files and
   nothing else — do not hand it retrieval results, event files or codex excerpts. Run
   sequentially. Retry a failed section once, then log to `output/<run>/gen_errors.log` and
   continue. The approved first section is not rewritten.
7. Dispatch `episode-auditor` for the run dir. It holds the packs and the whole episode, runs
   its own find-then-fix passes, and absorbs what `smoother` used to do. It must run before
   any tone pass.
8. Assemble: `PYTHONPATH=. .venv/bin/python scripts/assemble_episode.py <run-dir>`.
9. Print the episode path, its word count vs. `target_words`, the `issues.md` summary, and
   the per-section coverage figures the auditor reported.

## Verify
- `output/<run>/episode.md` exists and is within 15% of `target_words`.
- `output/<run>/sources.json` has a non-empty entry (or an explicit `__warnings__` note) for every section.
- `output/<run>/packs/<id>.json` exists for every section, and none is empty.
- `output/<run>/issues.md` has a `## Fixes applied` section, and its `Coverage` heading
  reports real numbers rather than "none found".
- Read the first and last 300 words aloud: the voice matches the narrator bible and nothing invented stands out.
- `output/<run>/voice_check.md` exists and no longer carries its `# UNAPPROVED` line.

## If voice feedback arrives after the episode is written
The checkpoint has been missed, so the fix is retroactive and has three parts, in order:
1. Fold the feedback into `config/narrators/<narrator>.yaml` as above.
2. Sweep **every** section against the new rules, not only the one that was reviewed — the same
   habit will have recurred. Repair the offending lines in place; do not regenerate a section
   that is otherwise sound. Sweep for lore *integration* in the same pass, against
   `docs/generation-example.md`: a paragraph that recites accurate lore in a neutral register
   is as much a defect as one that invents it.
3. Re-run the tone pass (`tone-marker`) on every section whose prose changed, then
   `PYTHONPATH=. .venv/bin/python scripts/assemble_episode.py <run-dir>` and
   `PYTHONPATH=. .venv/bin/python scripts/assemble_performance.py <run-dir>`. A `.performance.md` left over from the
   old prose fails the assembler's byte-identity check, which is the point.
