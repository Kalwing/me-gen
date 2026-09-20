---
description: Generate a narrated Mass Effect episode. First run produces an outline for approval; `--continue <run-dir>` writes the full script.
---

Usage:
- `/me-generate <narrator> "<theme1, theme2>" [--brief "<free text>"] [--subject <slug>] [--words N]` — outline phase (stops for approval).
- `/me-generate --continue <run-dir>` — generation phase.

`<narrator>` may be several comma-separated ids (`tali,liara`): the episode is then told in
**alternating voices** — each section is one narrator's turn, speaking to the other(s) and
answering the turn before. The first id is the lead `narrator:`; the list is stored as
`narrators:` and each section carries its own `narrator:`. The `dialogue` form in
`config/forms.yaml` is built for this. A single id is a monologue, exactly as before.
If the user gives no narrator but the brief puts two narrators in conversation, ask
whether to alternate between them or have one narrate.

`--brief` is an optional free-text note that sits alongside the themes — e.g.
`--brief "Tali romance; speaks by phone after a fight, a bit tired"`. It does two
things:
- **Framing** — the occasion, scene, mood, and who the narrator is addressing.
- **Finer canon** — it refines `config/canon/choices.yaml` for this one episode:
  it picks among options the choices file leaves open (e.g. which romance when
  several are recorded), adds playthrough detail not in the file, and where the
  brief and the choices file speak to the same point the **brief wins for this run**.
`--subject <slug>` names **who the episode is about** — the person the narrator is
addressing and characterizing. It defaults to `shepard`, which is what every episode has
been, so leaving it off changes nothing. Pass it **only when the user explicitly asks for
that character**, by name or by an unmistakable brief; never infer it. With
`--subject thomas` the run records `subject: thomas` in `outline.yaml`, and every
downstream agent reads `config/narrators/thomas.notes.md` in Shepard's place. It swaps the
*addressee*, not the world: Shepard still commands the Normandy and `config/canon/` still
decides which branch of the trilogy happened. The subject must have a
`config/narrators/<slug>.notes.md` or `new_run.py` refuses to scaffold the run.

A named subject who is an original character is **not in the corpus** — no scene record
will ever list them, so `build_pack.py` warns on every pack that a record's silence about
them is not absence. Their presence comes from their notes file, read by its timeline
*stretches* rather than its named occasions: where the notes put them with the crew they
were at that period's occasions too (the Citadel DLC shore leave included), and outside
those stretches they were not there. The notes stay binding on the load-bearing facts —
relationships, habits, dates, deaths, deeds.

It invents no world lore, but canon does more than colour the telling: many
timeline events are choice-conditional (a death on Virmire, the Council's fate,
the genophage, the Suicide Mission roster, the ending), and `narrative_choices` —
refined by the brief — decides **which branch is true**, hence which sections
exist and which outcomes are narrated. Non-conditional events, dates, and lore
still come only from the timeline and retrieved evidence.

## Outline phase
1. Require `timeline/master_timeline.yaml` and `data/bm25_index.pkl`. If missing, tell the user to run
   `/me-scrape`, `/me-build-lore`, `/me-build-timeline` and stop.
2. Require `config/narrators/<narrator>.yaml` — for every id when there are several. If one
   is missing, list the available bibles and stop.
3. Scaffold the run: `PYTHONPATH=. .venv/bin/python scripts/new_run.py <narrator> "<themes>" [--words <words>] [--brief "<brief>"] [--form <form>] [--subject <slug>]`
   and capture the printed path. **Pass `--words` only if the user named a length.** Left
   off, the episode is sized from its form — `words_per_section x section count`, clamped
   into that form's `words_clamp` (`config/forms.yaml`) — so a form of many short sections
   and one of few long ones no longer produce the same 8,000 words. With `--form` the size
   is set at scaffold time; without one it lands as `0` and the outline-writer fills it in
   once it has chosen the form and the section count. (Pass `--brief` only if the user gave one; it is stored as
   `brief:` in `outline.yaml`. Pass `--form` only if the user named one from
   `config/forms.yaml`; left blank, `outline-writer` chooses the form and explains the
   choice in `form_note`. Pass `--subject` only if the user explicitly named the character
   the episode is about; left off it is Shepard. If it fails because the notes file is
   missing, list `config/narrators/*.notes.md` and stop.)
4. Load the player's canon: run
   `PYTHONPATH=. .venv/bin/python scripts/canon.py` and print its output.
   If it prints `all questions unanswered`, warn the user that the recap will use default
   trilogy canon (they can edit `config/canon/choices.yaml` and re-run) — do NOT stop.
5. Make sure the index knows about the scene layer:
   `.venv/bin/python scripts/build_bm25.py` (a no-op when it is already newer than its sources).
6. Dispatch the `outline-writer` subagent for that run dir.
7. Print the outline path, the episode's `subject` (say so explicitly when it is not
   Shepard), the chosen `form` and `form_note`, and the section table with
   each section's `promises` (and, with more than one voice, each section's `narrator`). Report any question the outline-writer appended to
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
4. **Voice checkpoint — the first turn of each voice.** List the checkpoint sections:
   `python -c "import yaml; from scripts import common; print(' '.join(common.voice_check_sections(yaml.safe_load(open('<run-dir>/outline.yaml')))))"`.
   For a monologue that is the first section alone; with alternating voices it is each
   narrator's first turn. Dispatch `section-writer` for those sections, in outline order, and
   nothing else. Then write `output/<run>/voice_check.md`:

   ```
   # UNAPPROVED — voice check. Delete this line to approve, then re-run --continue.

   <the full text of each checkpoint section, verbatim — under a `## <narrator>` line
    per section when there is more than one voice>
   ```

   Print the section(s) in the chat too, and ask the user to read them for **voice and lore
   handling, not facts** — and, with more than one voice, whether the voices are
   unmistakably distinct and the reply actually answers the turn before it:
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
   - Fold every correction into `config/narrators/<narrator>.yaml` first (the bible of the
     voice the feedback is about, when there are several) — that is the durable
     fix and it is what the remaining sections will be written against. Feedback about *how*
     they talk belongs in `diction` / `signature` / `avoid`; feedback about *what* they wander
     into and the rhythm of the wandering belongs in `digressions`. Quote the offending phrase
     in the `avoid` entry so the failure is named, not merely described.
   - Re-dispatch `section-writer` for the checkpoint section(s) the feedback touches (with
     two voices, redo a later checkpoint turn whenever an earlier one it answers was
     redone), refresh `voice_check.md` from the new drafts, and STOP again. Repeat until the user clears the marker line.
   If the user has given no feedback, just tell them the checkpoint is still waiting and stop.
6. For each **remaining** section in `outline.yaml`, in order: dispatch `section-writer` with
   the run dir and the section id. It reads that section's pack and the narrator files and
   nothing else — do not hand it retrieval results, event files or codex excerpts. Run
   sequentially (this also lets `output/<run>/used_lines.md` accumulate across sections, so
   a later section knows what stock phrasing an earlier one already used, and each turn in a
   multi-voice episode can read the turn it answers). Retry a failed
   section once, then log to `output/<run>/gen_errors.log` and continue. The approved
   checkpoint sections are not rewritten.
7. Dispatch `episode-auditor` for the run dir. It holds the packs and the whole episode, runs
   its own find-then-fix passes (including a deterministic repetition scan), and absorbs
   what `smoother` used to do. It must run before any tone pass.
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
