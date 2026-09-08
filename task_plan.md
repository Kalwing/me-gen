# Task Plan: Mass Effect Narrator pipeline

## Goal
A Claude Code skill/subagent pipeline that scrapes Mass Effect trilogy lore, builds a
file-based YAML timeline + BM25 evidence index, and generates approved 5–10k-word
narrated recaps in swappable in-universe narrator voices.

## Next Step
2026-09-08 (session N): the timeline sweep is COMPLETE — 1,636/1,636 stems in
`timeline/.done`, 190 event files, master 190 rows, `renumber_timeline.py --check`
clean. The generation overhaul's Phase 1 test run passed ("came out great").

Work now follows `docs/superpowers/specs/2026-09-07-generation-overhaul-design.md`
**Phase 2**, not the wave procedure below (kept for reference):
- [x] Phase 2 item 10 — timeline sweep + renumber.
- [x] Phase 2 item 9 (tooling) — `/me-build-scenes` + `scene-extractor` written,
      mirroring `/me-build-timeline`: alphabetical batches of ~20, `scenes/.done`
      ledger owned by the controller, 4 agents in flight, Haiku default / Sonnet for
      attendance- and branch-heavy batches, pause-and-commit per wave. 169 tests green.
- [ ] Phase 2 item 9 (the sweep) — 1,636 stems pending, un-run. Token-heavy; run in
      waves and `/clear` between them.
- [ ] Phase 2 item 11 — codex correction pass for compressed-causality bullets of the
      Krogan Monument kind.
- [ ] TODO2.md line-level corrections to the test-run output (Jack/Tali/Wrex).

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
Phase 5 — user-initiated live run (deferred items).

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
