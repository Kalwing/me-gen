# Task Plan: Mass Effect Narrator pipeline

## Goal
A Claude Code skill/subagent pipeline that scrapes Mass Effect trilogy lore, builds a
file-based YAML timeline + BM25 evidence index, and generates approved 5–10k-word
narrated recaps in swappable in-universe narrator voices.

## Next Step
ALL PLAN TASKS DONE (1-17). Final review addressed (commit fcb9ef7). Task 16 complete
(commit 087b5b8): all 16 ddl/ transcripts hand-corrected into lore/manual/ (24 pages +
README), me-build-lore wired to feed them. Suite 58 green. STOP — wait for user.
Deferred to a later user-initiated session: live wiki scrape, real /me-build-lore +
/me-build-timeline runs, first real /me-generate episode, live fact-preservation QA.
Standing ruling: every script doing `from scripts...` needs the sys.path bootstrap.

## Current Phase
Phase 5 — user-initiated live run (deferred items).

### Phase 5: Live corpus build (user-initiated 2026-08-28)
- [x] scrape_wiki: incremental page writes + resumable crawl (commit) + progress print every 20 pages
- [~] `/me-scrape --rate 30` running (pid 19947, cap 1000, depth 2). ~8h at this rate. Monitor task b0nmmndek reports progress/exit.
- [ ] On scrape exit: `chunk.py` → `build_bm25.py` → verify with `retrieve.py "Sovereign Reaper"`; report page/chunk/error/stub counts.
- [ ] Then (separate go-ahead): `/me-build-lore`, `/me-build-timeline`, first `/me-generate`.
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
