# Task Plan: Mass Effect Narrator pipeline

## Goal
A Claude Code skill/subagent pipeline that scrapes Mass Effect trilogy lore, builds a
file-based YAML timeline + BM25 evidence index, and generates approved 5–10k-word
narrated recaps in swappable in-universe narrator voices.

## Next Step
Begin Phase 3 Task 1 (project scaffold + `scripts/common.py`) via a dispatched
subagent, following superpowers:subagent-driven-development.

## Current Phase
Phase 3

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
- [ ] Execute the 14-task plan (Tasks 1-9 Python spine w/ TDD; 10-13 subagents + commands; 14 README + first real run)
  - [ ] Task 1: Project scaffold + `scripts/common.py`
  - [ ] Task 2: HTML → clean markdown (`clean_md.py`)
  - [ ] Task 3: Chunker (`chunk.py`)
  - [ ] Task 4: BM25 build + retrieval (`build_bm25.py`, `retrieve.py`)
  - [ ] Task 5: Wiki scraper (`scrape_wiki.py`)
  - [ ] Task 6: Run scaffolder (`new_run.py`)
  - [ ] Task 7: Episode assembler (`assemble_episode.py`)
  - [ ] Tasks 8-9: remaining Python spine
  - [ ] Tasks 10-13: subagents + slash commands
  - [ ] Task 14: README + first real run
- **Status:** in_progress

### Phase 4: Testing & Verification
- [ ] Unit tests (clean_md, chunk, retrieve, new_run)
- [ ] Integration smoke test on 3-page mini corpus
- [ ] Fact-preservation check
- **Status:** pending

### Phase 5: Delivery
- [ ] Full trilogy scrape + build, 5 narrator bibles, one real 8k-word episode
- **Status:** pending

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Hybrid architecture, no vector DB | User choice; BM25 + explicit event→chunk links give enough grounding, stays inspectable/git-friendly |
| Built as Claude Code skills + subagents | User choice; uses existing auth, no API key; Python only for deterministic work |
| Deterministic (scrape/clean/chunk/index/retrieve) = Python; reasoning = subagents | Scraping hundreds of pages via subagent WebFetch is too slow/token-heavy |
| Full trilogy, re-runnable per narrator | User choice |
| Clean markdown on import, no raw HTML stored | User choice; keeps corpus folder small |
| Two-step generate with outline approval gate | User choice; matches plan.md step 6 |

## Errors Encountered
| Error | Resolution |
|-------|------------|
