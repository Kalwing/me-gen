# Task Plan: Mass Effect Narrator pipeline

## Goal
A Claude Code skill/subagent pipeline that scrapes Mass Effect trilogy lore, builds a
file-based YAML timeline + BM25 evidence index, and generates approved 5–10k-word
narrated recaps in swappable in-universe narrator voices.

## Next Step
2026-09-01: world-texture codex extraction sweep is COMPLETE. All 28 batches
(texture_batch_000-027, ~560 pages) processed across waves 1-6; 492 slugs in
data/texture_candidates.done. Final codex world-texture totals: culture.md 265,
social.md 220, everyday.md 204 bullets (all source-tagged). Last commit e022c235.
See progress.md for per-wave bullet counts and commit hashes.
The parked TODO items below stay parked until the user explicitly asks for them.
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
- [ ] Verify narrative_choices.yaml config is functional/well-written.
- [ ] `/me-build-timeline` (timeline/events/ still empty).
- [ ] Surface any timeline-driven choices not covered by narrative_choices.yaml, ask user.
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
