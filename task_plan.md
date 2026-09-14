# Task Plan: Mass Effect Narrator pipeline

## Goal
A Claude Code skill/subagent pipeline that scrapes Mass Effect trilogy lore, builds a
file-based YAML timeline + BM25 evidence index, and generates approved 5–10k-word
narrated recaps in swappable in-universe narrator voices.

## Next Step
2026-09-14 — Session start (/pwf), user gave 3 notes: (1) `config/narrators/*.mp3`
are final audio output, ignore as input; (2) `mass_effect.json` is a personal quote
collection, user chose "fold matching quotes into narrator .style.md files"; (3) Jack's
last generation overused "Don't make me repeat it"/"I won't say it again" — user chose
"add explicit avoid-note to jack.yaml". Both actioned:
- [x] jack.yaml avoid-list += note naming both phrases, done directly.
- [x] mass_effect.json fold-in: 35 new quotes across 9 of the 10 narrator .style.md
      files (traynor 0 new, all dupes). 169 passed.
- [x] Shepard has no .style.md/.yaml (not a selectable narrator) — only
      `shepard.notes.md`. Its 3 hand-picked lines were already covered by
      mass_effect.json; added the other 22 Shepard-authored lines from that file.
- [x] User dropped a full Shepard AU character profile (backstory, personality,
      appearance, beliefs) + 2 verbatim speeches (crew pre-war address, galaxy
      pre-final-push address) — consistent with existing `config/canon/choices.yaml`
      canon (Earthborn/Anderson-rescue/Akuze-Sole-Survivor/Vanguard/faithful-romance/
      Synthesis), just fleshes it out. Folded into `shepard.notes.md` as new
      "Full character profile" + "Speeches" sections; added Akuze detail to
      choices.yaml's `profile` id (was blank). 169 passed.
- [x] Committed as 4e55525 (jack.yaml avoid-note, 9 narrator style.md fold-ins,
      shepard.notes.md, choices.yaml profile detail).
- [x] Working-tree review (user: "let's review"): found 5 pre-existing uncommitted
      files unrelated to this session (Fish Audio tone-marker rework in progress).
      Fixed 2 real gaps found there: `normandy-hackett-pre-battle-address.yaml`
      grammar + dropped stray "Jack" from `heard_by`; `tone-marker.md`'s onomatopoeia
      table now splits character-sound tags (each with a spelled-out word) from
      crowd/ambient tags (no word) per user direction.
- [x] Cross-section repetition fix (user: "how would you fix it?" -> "Perfect" to
      build both layers). Root cause: `section-writer` dispatch is sequential but
      stateless — no section knows what stock phrasing an earlier section in the
      same episode already used. Built:
      1. Prevention: `section-writer.md` reads `output/<run>/used_lines.md` (stock
         phrases already used this episode) and appends its own to it, excluding a
         narrator's declared `catchphrases`.
      2. Detection backstop: new `scripts/check_repetition.py` (shingle scan, 8
         new tests) + `episode-auditor.md` new `Repetition` heading (runs the
         script, judges flags, fixes by rewriting the *later* occurrence only) +
         `me-generate.md` step 6/7 notes. 177 passed.
- [x] Committed as 62fa684 (repetition fix + shepard.notes.md wiring).
- [x] User: "should all be committed and used" for the rest of the working tree
      (tone-marker.md already committed; overrides.yaml, assemble_performance.py,
      all .pol.md files) + "can be discarded if not relevant anymore" for
      TODO/TODO2.md deletions and mass_effect.json. Actioned:
      - 18 `config/narrators/*.pol.md` (political-philosophy refs, 10 selectable
        narrators + 8 subject-only characters) were on disk but unwired — same
        pattern as shepard.notes.md. Generalized the wiring: section-writer.md /
        episode-auditor.md now read a narrator's own .pol.md as a depth layer,
        plus any *other* character's .pol.md/.notes.md when quoted/addressed in
        a section (shepard.notes.md is now the flagship instance of this general
        rule, not a special case). Renamed thane.md -> thane.pol.md for naming
        consistency.
      - overrides.yaml (Jack N7 tattoo AU) + assemble_performance.py (Fish Audio
        tag support) committed as previously reviewed, no changes needed.
      - TODO/TODO2.md deletions finalized (content superseded — world-texture
        sweep/timeline/choices-verification done; episode-review complaints
        now structural via scene layer + agency-transposition + Phase 8 fixes).
      - mass_effect.json deleted (fully mined into narrator files, commit 4e55525).
      - mp3s under config/narrators/ stay untracked by design (final output).
      Committed as 0059227. 177 passed. Working tree clean except the 3 mp3s.
- [x] User: broaden the "other character" rule further — several characters who might
      appear as dialogue in someone else's section are themselves selectable narrators
      with a full `.yaml`/`.style.md` bible (e.g. Garrus quoted inside Jack's episode),
      richer than `.pol.md`/`.notes.md` alone. section-writer.md/episode-auditor.md now
      say to check all four `config/narrators/<slug>.*` kinds for any other character,
      not just the two. 177 passed.
- Everything below this point (Phase 7/8 status, deferred generation-overhaul items)
  is carried over unmodified from the 2026-09-11 reconciliation — not re-verified
  this session.

2026-09-11 — RECONCILED against git (planning files were ~7 commits stale, same
drift pattern as the 2026-09-09 resume). Actual state, verified this session:
- **Scene sweep is COMPLETE**: `scenes/.done` 1,636 / `page_summaries` 1,636 (0 remaining),
  377 scene files, waves 15-20 committed (748ce42..ee3efb8) since the plan file's last
  entry (which stopped at wave 14 / 800 done). `scripts.scenes --check` clean.
- **Choice backfill is COMPLETE**: 3 commits (ccc9654, deb8c75, 5985e10) — scene-derived
  decision points backfilled as stubs, then Thomas filled in playthrough answers and
  loosened 16 stubs to free text. `config/canon/choices.yaml` now holds real canon
  (background/profile/class/gender/romance/first_name all answered).
- **Suite**: 169 passed (`.venv/bin/python -m pytest -q`).
- **New, not tracked in this file at all**: commit 376cce3 "narrator(wrex): widen Shepard
  address terms; drop two style-avoid notes" — looks like a first pass addressing the
  Wrex feedback in TODO2.md (see below).
- Deferred generation-overhaul items below are UNVERIFIED against current state — need
  a fresh check before treating any as still open.

Awaiting user direction on what to plan/work on next (see options offered in chat).

Deferred generation-overhaul items (spec `docs/superpowers/specs/2026-09-07-generation-overhaul-design.md`) —
status as of last known write, recheck before acting:
- [ ] Phase 2 item 11 — codex correction pass for compressed-causality bullets of the
      Krogan Monument kind (TODO2.md Wrex section names this explicitly).
- [~] TODO2.md line-level corrections to generated-episode output (Jack/Tali/Wrex) —
      Wrex commit 376cce3 suggests partial progress; Jack/Tali sections' status unknown.
- [x] Scene-sweep → backfill scene choice-branches into `config/canon/choices.yaml` —
      DONE (ccc9654, deb8c75, 5985e10), per memory [[scene-sweep-then-backfill-choices]].

Wave procedure below is the timeline sweep's (kept for reference); the scene sweep's is
in `.claude/commands/me-build-scenes.md`.

### Per-wave procedure (repeat until remaining == 0)
1. Regenerate the to-do list (order = alphabetical, deterministic):
   `comm -23 <(ls page_summaries/*.md | xargs -n1 basename | sed 's/\.md$//' | sort) <(sort -u timeline/.done) > $SCRATCH/remaining.txt`
   (SCRATCH = this session's scratchpad dir.)
2. Take the next 72 → two batches of 36 (`head -36` / `sed -n '37,72p'`), map to
   `page_summaries/<stem>.md` path lists.
3. Dispatch 2 `timeline-extractor` subagents (max 2 in flight), one per batch.
   Model: **haiku** by default. Use **sonnet** for a batch containing a pivotal
   choice-conditional mission (Virmire, genophage/Tuchanka, Rannoch/geth-quarian,
   Crucible endings, Citadel coup, Suicide Mission) or a dense endings/lore page
   (e.g. `crucible`, `catalyst`, `reaper`).
4. On success: append both batches' stems to `timeline/.done` (controller writes only).
5. Normalize filenames (command step 6), rebuild master (`python scripts/rebuild_master_timeline.py`).
6. `python -m pytest -q` — expect green.
7. `git add -A && git commit` with a wave-N checkpoint message.
8. Update this file (remaining count, wave number) + append a progress.md entry.
9. STOP. Tell the user the wave is done and they may /clear.

### Wave log
- Wave 1 DONE (commit 0505239): A=citadel-old-friends..codex, B=collector-captain..crescent-nebula. Both Haiku. +11 events -> 52. .done 404->476. Suite 86. Remaining: 1160.
- Wave 2 DONE (commit PENDING): A=crooks..din-korlack (sonnet, had `crucible`), B=director..eclipse-heavy (haiku).
  +15 events -> 67. .done 476->548. Suite 86 green. Remaining: 1088 (~15 waves).
  A: crucible-superweapon-project, derelict-reaper-iff-mission, desolas-arterius-palaven-coup,
  sidon-research-station-attack, dekuuna-elcor-evacuation, fehl-prime-collector-attack,
  horizon-collector-attack (+3 updated: normandy-first-test-flight, overlord-david-archer,
  volus-ambassador-din-korlack). B: 8 ME2 recruitment dossiers (garrus/tali/jack/samara/
  mordin/zaeed/grunt-recruitment-*, drell-rescue-kahje).
- Waves 3–6 DONE (commits 92e0cf2, e8a316c, cb3ad0a..f8769e4, 89af54a, 530e84c). .done 548->1048.
- Wave 7 DONE (this commit): 12 batches of 20 (b00..b11), stems `mechs`..`rannoch-geth-fighter-squadrons`,
  4 subagents in flight at a time. Haiku default; Sonnet for b01 (mordin/morinth), b09 (ME3
  priority spine), b10 (protect-the-council / prologues), b11 (rachni queen choice).
  +17 new events -> 159 on disk; ~12 existing events got source-chunk merges. .done 1048->1288.
  Suite 92 green. master rebuilt (159 rows, all files present, non-decreasing). Remaining: 348 (~15 batches).
  New: mindoir-raid, priority-palaven, tali-treason-trial-alarei, samara-the-ardat-yakshi,
  nassana-dantius-assassination, noveria-geth-interest, noveria-espionage,
  normandy-sr1-destruction-alchera, normandy-crash-site-memorial, priority-the-citadel-i,
  priority-perseus-veil, priority-the-citadel-iii, rachni-wars, rachni-queen-noveria-choice,
  rannoch-admiral-koris, reaper-invasion-of-earth-shepard-flees-vancouver,
  project-firewalker-the-prothean-site-on-kopis.
- Wave 8 next: re-derive remaining.txt (step 1), continue alphabetically from `ravager`
  (batch b12 was prepared but NOT run). Run pytest via `.venv/bin/python -m pytest -q`.
- Dup-merge candidates for post-sweep: horizon-collector-attack vs any existing horizon event;
  derelict-reaper-iff-mission vs any existing reaper-iff/legion event;
  noveria-geth-interest / noveria-espionage vs benezia-death-noveria (all ME1 Noveria);
  normandy-sr1-destruction-alchera vs any existing ME2-opening / Collector-ambush event;
  project-firewalker-the-prothean-site-on-kopis vs hades-nexus-prothean-artifact-recovery.
- NOTE: `git add -A` will stage `me3.zip` (30MB backup archive, like me-gen.zip) — it is NOT
  in .gitignore. Keep it untracked; add it to .gitignore or delete it.
- NOTE: commit 0505239 accidentally added mass2.zip (29MB binary). Flag to user for history cleanup.

POST-SWEEP (still TODO): (1) chronological_order renumber pass — batches each number
10/20/30 independently so master ordering is not truly chronological (see findings.md);
(2) merge parallel-batch dup events: arcturus-station-destruction + battle-of-arcturus-station,
liberation-of-omega + liberation-of-omega-afterlife-assault;
(3) command steps 8-12 (load check, sync_narrative_choices, report, Verify).

POST-SWEEP (still TODO): (1) chronological_order renumber pass — batches each number
10/20/30 independently so master ordering is not truly chronological (see findings.md);
(2) merge parallel-batch dup events: arcturus-station-destruction + battle-of-arcturus-station,
liberation-of-omega + liberation-of-omega-afterlife-assault; (3) command steps 8-12
(load check, sync_narrative_choices, report, Verify).

Earlier this session (committed): sync_narrative_choices work (7638e14); timeline
resume hardening (563d220); Andromeda cutoff rules (df.., timeline-extractor.md);
filename==event_id fix (7d53ab1).
World-texture codex sweep remains COMPLETE (28 batches, culture 265 / social 220 /
everyday 204). Other parked TODO: narrator style refs (DONE, committed 9fb325e),
first `/me-generate <narrator> "<themes>"`.
  1. me-build-lore step 5 — narrator style references. Dispatch narrator-style-extractor
     once per config/narrators/<slug>.yaml (garrus, jack, joker, kaidan, liara, samara,
     tali, thane, traynor, wrex) -> config/narrators/<slug>.style.md. None exist yet.
     Safe as a parallel wave (one output file per narrator).
  2. `/me-build-timeline` — timeline/events/ is empty. Resumable batches of ~20
     summaries + timeline/.done manifest; rebuild_master_timeline.py derives
     master_timeline.yaml.
  3. First `/me-generate <narrator> "<themes>" [--brief ...]` — outline gate, then
     --continue.
me-build-lore.md subtracts data/lore_skipped.txt (1372 rows) in its step-1 source
list — corpus filter is wired into the command, not applied by hand.
Standing ruling: every script doing `from scripts...` needs the sys.path bootstrap.

## Current Phase
Phase 7 — scene sweep (generation-overhaul Phase 2 item 9). 620/1,636 done, wave 13
uncommitted in the tree. See `## Next Step`.

### Phase 7: Scene sweep (generation-overhaul design, item 9)
Wave = **8 batches of ~20** (user-set 2026-09-09), run 4 scene-extractors in flight
(two rounds of 4). Haiku default; Sonnet for loyalty/branch/banter-heavy batches.
Finalize the whole 160-stem wave together: `.done` append, filename normalize,
`scripts.scenes --check`, attendance spot-check, pytest, commit, pause for /clear.

- [x] Tooling: `/me-build-scenes` + `scene-extractor` (committed f3a6704).
- [~] The sweep — 800/1,636 stems in `scenes/.done`, 212 scene files. Waves 1–14
      committed (7a4b139 … this session).
- [ ] Post-sweep: reconcile scene choice-branches → `config/canon/choices.yaml` blank
      stubs (memory [[scene-sweep-then-backfill-choices]]).
- **Status:** complete (verified 2026-09-11: 1,636/1,636 stems, 377 scene files, `--check` clean)

### Phase 5 (superseded): user-initiated live run

### Phase 5: Live corpus build (user-initiated 2026-08-28)
- [x] scrape_wiki: incremental page writes + resumable crawl (commit) + progress print every 20 pages
- [x] scrape_wiki: drop images (no ![](), no data:image base64, no figure captions)
- [x] scrape_wiki: persist the crawl frontier to `data/crawl_state.json` (pending
      [title,depth] queue + seen set), checkpointed every 10 pages / on exit /
      on SIGTERM+SIGINT. Resume loads it and drains the saved queue — no API
      re-walk. `--cap` is now a per-run fetch bound; re-run to fetch more.
      Dropped the have()/re-fetch-seeds mechanism. 65 green (3 tests swapped).
- [x] scrape run 1 done (pid 30635, --rate 7, cap 1000, depth 2): 880 pages on disk
      (779 new + 101 prior), 2 fetch errors (disambig titles), 0 stubs. crawl_state.json
      holds the frontier; ~42k raw links queued (dedup count shows next run). Re-run
      `/me-scrape --rate 7` (raise --cap) to fetch the next batch.
- [x] chunk.py + build_bm25.py made interrupt-safe/resumable (user request):
      chunk appends per page + `.done` manifest + drops partial page on resume;
      build_bm25 atomic temp-rename + skip-if-fresh. 70 green.
- [x] scrape stop message: report DISTINCT pages left to crawl (pending_pages), not
      the dup-inflated raw queue len. 71 green.
- [x] me-build-timeline resumable: batches of ~20 + `timeline/.done` manifest;
      master_timeline.yaml now derived by scripts/rebuild_master_timeline.py
      (atomic, skips malformed). timeline-extractor.md batch-scoped. 76 green.
- [x] me-generate `--brief "<free text>"`: directorial note beside themes, stored
      as `brief:` in outline.yaml; new_run/outline-writer/section-writer wired.
- [x] Pipeline built: chunk.py → 7729 chunks (data/chunks/chunks.jsonl + .done manifest);
      build_bm25.py → data/bm25_index.pkl (20M). retrieve "Sovereign …" → sovereign_005
      (20.4), saren-arterius_007, sovereign_004 — on-topic. Re-run of both = no-op. 76 green.
- [x] lore/manual into the retrieval + voice pipeline (user-approved 2026-08-29):
      chunk.py `manual-` namespace + index rebuild (79 green); page-summarizer /
      me-build-lore merge colliding slugs, manual weighted; narrator-style-extractor
      subagent + config/narrators/*.style.md wired into section-/outline-writer and
      me-build-lore step 5.
- [x] `/me-build-lore` summary sweep COMPLETE (2026-08-30): 1635 summaries, 0 in-scope
      remaining, all codex/_inbox/ merged, suite 79 green. Committed.
- [ ] Then (separate go-ahead): me-build-lore step 5 (narrator style refs),
      `/me-build-timeline`, first `/me-generate`. Optionally more `/me-scrape` batches
      (crawl_state.json frontier still has ~1600 distinct pages).
- **Status:** in_progress

## Phases

### Phase 1: Requirements & Discovery
- [x] Understand user intent
- [x] Identify constraints (2 clarification rounds)
- [x] Document in findings.md
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Define approach (hybrid: YAML timeline control layer + BM25 evidence)
- [x] Present design, get approval
- [x] Write design spec
- [x] Spec self-review
- [x] User reviews written spec (made small inline edits, approved: "its ok now")
- [x] Invoke writing-plans skill for implementation plan
- [x] Implementation plan written: `docs/superpowers/plans/2026-08-27-mass-effect-narrator.md` (14 tasks)
- [x] User picks execution mode (subagent-driven, this session)
- **Status:** complete

### Phase 3: Implementation
Plan amended mid-execution (2026-08-27, user): +Task 15 (narrative-choices
questionnaire), +Task 16 (ddl→lore/manual, controller-solo, LAST), Task 14
descoped to README/suite/status, live run + real episode generation moved to
"Deferred / out of scope" (later user-initiated session). Plan file has details.
- [x] Execute the amended plan (Tasks 1-9 Python spine w/ TDD; 10-13 subagents + commands; 15 questionnaire; 14 README; 16 manual lore; 17 rebalance)
  - [x] Task 1: Project scaffold + `scripts/common.py` (commit 0174387, review clean)
  - [x] Task 2: HTML → clean markdown (`clean_md.py`) (commit 09c621d, review clean)
  - [x] Task 3: Chunker (`chunk.py`) (commit d71298f, review clean, 5 minors deferred)
  - [x] Task 4: BM25 build + retrieval (`build_bm25.py`, `retrieve.py`) (commits ..7168e3f, 1 fix round: path bootstrap; chunk.py fixed too)
  - [x] Task 5: Wiki scraper (`scrape_wiki.py`) (commit b7fade2, review clean, 5 minors deferred; report reconstructed after accidental kill)
  - [x] Task 6: Run scaffolder (`new_run.py`) (commit de07a21, review clean, 1 minor deferred)
  - [x] Task 7: Episode assembler (`assemble_episode.py`) (commit 16ba475, review clean, 2 minors deferred)
  - [x] Task 8: Starter config (seeds + Garrus bible) (commit 6daa886, review clean)
  - [x] Task 9: Deterministic-spine smoke test (commit a8c9ef8, review clean; ruling: word-count floor 120→70)
  - [x] Task 10: Lore subagents (page-summarizer, timeline-extractor) (commit f7c6f2a, review clean)
  - [x] Task 11: Lore commands (/me-scrape, /me-build-lore, /me-build-timeline) (commit 3463cf6, review clean)
  - [x] Task 12: Generation subagents (outline-writer, section-writer, smoother, consistency-checker) (commit 300afac, review clean)
  - [x] Task 13: /me-generate command (commit 6041403, review clean)
  - [x] Task 15: Narrative-choices questionnaire + generation wiring (commit c51b661, review clean, 4 minors deferred)
  - [x] Task 14: README + full-suite + spec status (commit d18003c, review clean after 1 fix round)
  - [x] Task 17: Rebalance generation agents to character-arc/lore-first priority (commit 8fb37dc, review adjudicated: 2 brief-prose deviations parked, semantically equivalent) — user amendment. See findings.md "Episode content priority".
  - [x] Task 16: ddl → lore/manual manual ingestion (controller solo) — all 16 sources → 24 lore pages + README (commits 8882007..087b5b8); me-build-lore wired to include lore/manual/
- **Status:** complete

### Phase 4: Testing & Verification
- [x] Unit tests (common, clean_md, chunk, retrieve, new_run, assemble_episode, config) — 31 green through Task 9
- [x] Integration smoke test on 3-page mini corpus (Task 9)
- [ ] narrative_choices unit test (Task 15)
- [x] Full-suite green (58 passed)
- [x] Final whole-branch review (SDD) — Needs fixes: 2 Critical + 2 Important + M1, all fixed & verified
- Fact-preservation check: moved to Deferred (first real generation session)
- **Status:** complete

### Phase 6: TODO sweep (2026-09-01, user: "now do the TODO")
- [x] Narrator style refs: verified suite green (79) + spot-checked traynor/wrex, committed (9fb325e).
- [ ] Culture/codex enrichment: fixed Blasto false-positive Andromeda filter (removed from
      data/lore_skipped.txt). Dispatched page-summarizer to summarize blasto.md + backfill
      codex/culture.md from 14 already-summarized flavor pages whose content never reached
      the codex (fornax, fortack, game-shop, drinks, foods, elcor, entertainment,
      codex-publications, news-stories, silversun-strip, samara-the-ardat-yakshi,
      kite-s-nest-pillars-of-strength, irune-book-of-plenix, mass-effect-blasto-eternity-is-forever).
      Agent a92a54c0636d0df34 running.
- [ ] World-texture grounding system (TODO item 3) — user flagged this as genuinely
      open-ended ("I don't know where all that should be kept"). NOT started; needs a
      design decision (where retrievable, keyword-search shape, resumability) before
      building. Asking user for direction rather than guessing.
- [x] Verify narrative_choices.yaml config is functional/well-written — validator clean
      after 8 answer normalizations; committed 7638e14.
- [x] Surface timeline-driven choices not covered by narrative_choices.yaml — done via
      scripts/sync_narrative_choices.py CATALOG (~60 decision points, --check gate);
      user filled canon for the new stubs. Committed 7638e14.
- [ ] `/me-build-timeline` (timeline/events/ still empty).
- [ ] Final process/system wrap-up for generation readiness.
- **Status:** in_progress

### Phase 8: Codex correction pass (generation-overhaul Phase 2 item 11)
Goal: find and fix codex bullets that compress away real causality — the "Krogan
Monument kind" (`codex/places.md:176`, already fixed as the exemplar: a dramatic,
multi-beat event stated as a flat fact, when a full `scenes/*.yaml` record now exists
with the real sequence/attendance/causality). The fix pattern per the exemplar: either
rewrite the bullet to carry the real causal chain, or replace it with a pointer to the
scene record (`scenes/<scene_id>.yaml`) rather than restating facts from memory — same
principle as memory [[citadel-dlc-scene-attendance]].

Scope: 11 files, `codex/{characters,culture,everyday,factions,places,ships,social,
species,tech,timeline,war}.md`, ~1,986 lines total. Now that the scene sweep is
complete (377 scene records), every codex bullet whose `(source: ...)` page has a
matching scene record is a candidate — the scene record may hold causality the bullet
never had room for.

- [x] Step 1 — Detection: COMPLETE. All 10 subagents finished. **54 bullets flagged**
      across 11 files (see findings.md table): characters 5, culture 4, everyday 6,
      factions 5, places 6, ships 8, social 7, species 6, tech 4, timeline+war 3
      (timeline.md: 0). Full detail in `scratchpad/codex-audit-<file>.md`.
- [x] Step 2/3 — COMPLETE. All 10 fix subagents finished; **54/54 flagged bullets
      fixed** (characters 5, culture 4, everyday 6, factions 5, places 6, ships 8,
      social 7, species 6, tech 4, war 3). Each agent re-verified against the scene
      record itself before fixing — species.md and war.md agents both explicitly
      double-checked rather than trusting the audit/controller instructions; war.md's
      agent caught and corrected a wrong assumption in my own dispatch instructions
      about which squadmate dies where at Virmire, using `config/canon/choices.yaml`
      + the scene record as ground truth.
- [x] Step 4 — Verify: `pytest -q` → 169 passed. `git diff --stat codex/` → exactly
      54 insertions/54 deletions across 10 files (matches fix count 1:1). Spot-checked
      species.md + war.md diffs — accurate, terse, matches exemplar style.
- **Status:** complete (pending commit)

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Hybrid architecture, no vector DB | User choice; BM25 + explicit event→chunk links give enough grounding, stays inspectable/git-friendly |
| Built as Claude Code skills + subagents | User choice; uses existing auth, no API key; Python only for deterministic work |
| Deterministic (scrape/clean/chunk/index/retrieve) = Python; reasoning = subagents | Scraping hundreds of pages via subagent WebFetch is too slow/token-heavy |
| Full trilogy, re-runnable per narrator | User choice |
| Clean markdown on import, no raw HTML stored | User choice; keeps corpus folder small |
| Two-step generate with outline approval gate | User choice; matches plan.md step 6 |
| `ddl/` YouTube transcripts hand-corrected by controller, not a subagent | User instruction; ASR cleanup needs care and full-file context; done solo, last, then pause |
| Narrative-choices questionnaire pins user canon before generation | User instruction; recap must match their playthrough (decisions + Shepard background/class) |
| Real episode generation is out of this plan | User instruction; done later on demand with a named character + prompt |

## Errors Encountered
| Error | Resolution |
|-------|------------|
| Task 3 review subagent: HTTP 429 session rate limit (resets ~2:10pm Paris) | Wait for reset; impl commit d71298f stands; re-dispatch review on resume |
| Task 4 review: `python scripts/retrieve.py` broke (ModuleNotFoundError) — plan ref code omits path bootstrap | Ruling: bootstrap all `from scripts...` scripts; fixed retrieve.py + chunk.py in Task 4 fix round |
| Task 9 smoke test: brief asserts word_count 120..400 but its own fixtures yield ~83 | Ruling: lower floor 120→70 (un-speced sanity bound, contradicted brief Step 4) |
