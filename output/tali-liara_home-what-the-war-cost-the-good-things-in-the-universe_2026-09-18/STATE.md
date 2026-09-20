# Run state: episode assembled 2026-09-20

First multi-voice episode: Tali and Liara alternate turns, form `reminiscing`, 12 sections.

## Done
- The outline is approved. You edited it: §11 got a new promise and a 1000-word target, §12 got a 1000-word target, and the run's `target_words` is 11000.
- All 12 packs are built. §4–§12 were rebuilt after the ceremony was added to the `shepard-death-unconfirmed` override. §9 and §10 were rebuilt after their grief promises were amended.
- The voice checkpoint is approved (`voice_check.md` holds §1 and §2).
- All 12 sections are written. The coordinator fixed some by hand:
  - §1: helmet, vantage, the gut-lining invention, "not tonight", the Mako quote, the memorial weld line.
  - §3: cut the retelling of §1.
  - §4: removed the mission walkthrough and mechanics (fixed by its writer).
  - §6: age now "a hundred and some", "Keelah" changed to "Goddess", "off the Normandy", trims.
  - §9: compressed the run paragraph.
  - §10: "two years" changed to "years".

## Audit and assembly (2026-09-20)
- `episode-auditor` re-ran over the whole episode, including the three sections the interrupted pass of 2026-09-19 had edited without logging. It found 2 real issues and fixed both:
  1. A vantage error in `two-years-and-after`: Liara claimed to have stood at the memorial wall with Garrus after Thessia. She was with Javik and then shut in her quarters, and Garrus's wall moment was after the Cerberus coup.
  2. Liara's "I am not going to" tic, in 4 of her 6 turns. The later three were rewritten.
- Everything else came back clean: grounding, canon, foreknowledge, agency, recitation, mechanics, form, rhythm, memory, staging, voices, length. `issues.md` holds the checklist, coverage table and fixes; `## Left unfixed` is None.
- Every section keeps all its promises, citing 7–27 pack chunks each.
- `episode.md` assembled: 10,645 words against 11,000, 12 speaker-labelled sections, word share Tali 5,380 / Liara 5,153.

## Remaining, optional
- `tone-marker` per section, then `PYTHONPATH=. .venv/bin/python scripts/assemble_performance.py <run-dir>` for the Fish Audio performance script. Each section heading names its speaker, so the voice switches there.

## Uncommitted repo changes from this session (not committed)
- Multi-voice support in `scripts/common.py`, `new_run.py`, `build_pack.py`, `check_repetition.py` and both assemblers, plus `tests/test_multi_voice.py` (194 tests pass).
- The `dialogue` form in `config/forms.yaml`.
- Agent and command docs, including the "crew are friends" and "whole crew" rules.
- `config/narrators/tali.yaml` and `liara.yaml`: the crew-friends register.
- `config/canon/overrides.yaml`, `shepard-death-unconfirmed`: amended by Claude at your request (after a few months he is held dead, and the ceremony).
