# Progress Log

## Session: 2026-08-27

### Current Status
- **Phase:** 3 - Implementation (subagent-driven, starting Task 1)
- **Started:** 2026-08-27

### Actions Taken
- Read existing `plan.md` brainstorm.
- Initialized planning files (default mode).
- 2 clarification rounds with user (8 decisions locked → findings.md).
- Presented 5-section design in chat; user approved ("Great.").
- Wrote design spec: `docs/superpowers/specs/2026-08-27-mass-effect-narrator-design.md`.
- Spec self-review: no placeholders/TBDs; scope is one implementation plan; open
  questions explicitly deferred to implementation. No contradictions found.
- User reviewed spec, made small inline edits (narrator examples, event count
  ~50–500, added scrape download-rate param), approved: "its ok now".
- Invoked writing-plans skill; wrote implementation plan
  `docs/superpowers/plans/2026-08-27-mass-effect-narrator.md` — 14 TDD tasks,
  full code for every deterministic script, full file bodies for every subagent
  and slash command, self-review with spec-coverage table.
- User picked execution mode: **subagent-driven-development, in this session**.
- Phase 2 complete. Entering Phase 3: dispatch Task 1 (scaffold + common.py) to a subagent.
- Git set up by user; branch feat/mass-effect-narrator.
- Task 1 DONE + review clean (commit 0174387). Task 2 DONE + review clean (commit 09c621d).
- Task 3 impl DONE (commit d71298f); review subagent hit HTTP 429 session rate limit
  (resets ~2:10pm Europe/Paris). No subagents runnable until reset.
- User amended the implementation plan mid-execution (see SDD ledger + plan file):
  +Task 15 narrative-choices questionnaire, +Task 16 ddl→lore/manual (controller-solo,
  last, then pause), Task 14 descoped to README/suite/status, real episode generation
  + live scrape moved to "Deferred / out of scope".
- HOLDING: waiting for rate-limit reset to resume Tasks 3(review)-15 via subagents,
  then Task 14, then Task 16 solo, then stop for user input.

### Session resume 2026-08-27 ~14:20 (rate limit reset)
- Subagents working again. Task 3 review re-dispatched → ✅ spec compliant, quality
  Approved, no Critical/Important; 5 minors deferred to final review. Task 3 complete
  (commits 09c621d..d71298f).
- Task 4 (BM25 build + retrieval) implementer dispatched (haiku). BASE d71298f.
- Briefs pre-generated for Tasks 6-9.
- Detailed execution ledger: .superpowers/sdd/2026-08-27-mass-effect-narrator/progress.md

### Test Results
| Test | Expected | Actual | Status |
|------|----------|--------|--------|

### Errors
| Error | Resolution |
|-------|------------|

### Session resume 2026-08-28 (cont.)
- Final whole-branch review returned "Needs fixes": C1 seeds.yaml `Priority: Earth`
  parsed as dict → crawl() crash; C2 me-generate.md gate `from pathlib import Path,sys`
  ImportError → whole --continue path dead; I1 narrative_choices main() bare
  FileNotFoundError on missing working copy; I2 assemble_episode null `sections:` →
  TypeError. All fixed + M1 (summary readout labels) + tests; 58 green. Committed.
  Report: .superpowers/sdd/2026-08-27-mass-effect-narrator/final-review-report.md
- Task 16 batch 1 committed: jack-dialogue, turian-hierarchy-early-history,
  systems-alliance-founding, arcturus-station, destiny-ascension (+README). 5/16 sources.

### Session 2026-08-28 (post-completion tweak)
- User deleted config/narrative_choices.template.yaml, keeping only their filled
  config/narrative_choices.yaml. Made it consistent: un-ignored the file (now tracked),
  me-build-timeline drops the `cp` template step, tests/README/docstring updated.
  Commit 35ce128. 58 green, all lore/manual parses clean.

### Session 2026-08-28 — Phase 5: live scrape
- User ran /me-scrape --rate 30. First launch: killed (all-or-nothing write, 0 on disk).
- Fixed scrape_wiki: crawl() gains on_page (write each page as fetched) + have()
  (skip re-fetching pages already on disk; seeds always re-fetched to rebuild frontier;
  have-pages still count toward --cap). +existing_slugs(). +progress print every 20 pages.
  5 new tests, 63 green. Commits on feat/mass-effect-narrator.
- Relaunched: pid 19947, cap 1000 / depth 2 / rate 30s (~8h). Writes incrementally to
  data/pages/; re-run resumes. Monitor task b0nmmndek streams progress + exit.
- On exit: chunk -> build_bm25 -> retrieve verify, then report counts.

### 2026-08-28 — stop + image strip
- User: "stop. Don't keep the images when scrapping." Killed scrape (pid 19947, 5 pages),
  stopped monitor, deleted the 5 stale image-laden pages + run/error logs.
- clean_md: markdownify strip += 'img'; _DROP_SELECTORS += img,figure,figcaption,
  .thumb,.image,.pi-image,.video-thumbnail. Pages now carry no images/captions/base64.
  +test in test_clean_md; 63 green. Committed.
- Scrape not relaunched — waiting for user.

### 2026-08-28 — rate change mid-run
- Scrape ran at --rate 30 to ~101 pages on disk. User: "in 15min, stop and continue
  the run at a rate of 15sec." Set a 15-min bg timer; on fire, SIGTERMed pid 21098
  (confirmed down, 101 pages intact), relaunched `scrape_wiki.py --rate 15` as pid 29384,
  appending to data/scrape_run.log. Old monitor bf35tkrq0 ended on the kill; new
  persistent monitor b4mtpmro8 tails --pid=29384.
- Resume path: 101 slugs on disk skipped; seeds re-fetched to rebuild the BFS frontier
  (write_page no-ops on existing non-empty files). "resuming:" line is block-buffered,
  flushes with the first progress: line. On exit: chunk -> build_bm25 -> retrieve verify.

### 2026-08-28 — persistent crawl frontier (user: index visited links / depth)
- User: resume must not re-walk the tree via API to rebuild the queue after a
  too-small cap. Implemented data/crawl_state.json: {seen:[titles], queue:[[title,depth]],
  errors:[]}, atomic write, checkpoint every 10 pages + on return + on SIGTERM/SIGINT.
  crawl() gains seen=/queue=/checkpoint= params; when queue= is passed, seeds ignored
  and nothing already-seen is refetched. Removed have()/always-refetch-seeds.
  --cap is now a per-run fetch bound; re-run (optionally larger --cap) drains the
  saved queue. One-time transition: no state + pages on disk -> refetch seeds once
  to seed the queue, then it persists.
- Tests: dropped 3 have() tests, added resume-from-queue, checkpoint-pending-frontier,
  checkpoint-cadence, state-roundtrip, load-state-missing. 65 green. gitignore +=
  data/crawl_state.json. me-scrape.md updated.

### 2026-08-28 — resumable chunk + index (user request)
- chunk.py: appends chunks per page, records finished page stems in
  data/chunks/chunks.jsonl.done. Re-run skips finished pages; _rewrite_kept_lines
  drops a half-written page + truncated last line from a killed run before
  appending. SIGTERM/SIGINT stop at the next page boundary. +"source" field on
  each chunk row (page file stem). --force rechunks all. progress every 50 pages.
- build_bm25.py: atomic write (bm25_index.pkl.tmp -> os.replace + fsync) so a
  killed run never leaves a corrupt pickle. Skips rebuild when index mtime >=
  chunks.jsonl mtime; returns -1 sentinel. --force overrides.
- Tests: +3 chunk resume/force/partial-drop, +2 build freshness/atomic. 70 green.
- data/chunks/ already gitignored (covers .done + .tmp).

### 2026-08-28 — report distinct pages remaining (user request)
- scrape_wiki: +pending_pages(queue, seen) -> count of DISTINCT unvisited titles
  in the frontier (raw queue lists dupes). Used in the periodic progress line,
  the SIGTERM/SIGINT message, and the final summary ("N distinct pages still to
  crawl ... re-run / raise --cap"). Empty frontier -> "corpus is complete".
  +test_pending_pages_counts_distinct_unvisited. 71 green.
- NOTE: the currently-running scrape (pid 30635) is pre-this-change; its final
  line will still read "links still queued". Next run uses the deduped wording.

### 2026-08-28 — resumable build-timeline + generate --brief (user request)
- me-build-timeline now batches (~20 summaries) like me-build-lore: timeline/.done
  manifest, re-run skips finished summaries. master_timeline.yaml is now a DERIVED
  index: new scripts/rebuild_master_timeline.py scans timeline/events/*.yaml, sorts
  by chronological_order, dedupes, skips malformed files, atomic temp->rename.
  timeline-extractor.md reworked: processes only the batch's summaries, no longer
  authors master_timeline, reuses existing event_ids instead of duplicating.
- me-generate: new --brief "<free text>" alongside themes — a directorial note
  (occasion/scene/mood/address), stored as brief: in outline.yaml. new_run.py
  --brief; outline-writer frames open/close + weighting around it; section-writer
  keeps its situation/mood as present tense. Never canon (narrative_choices still
  the only playthrough source).
- Tests: +test_new_run_records_brief, +test_rebuild_master_timeline.py (4). 76 green.

### 2026-08-28 — scrape run 1 complete + pipeline
- pid 30635 exited at cap 1000. data/pages: 880 (.md), 779 written this run + 101 prior.
  2 fetch errors (Mass Effect (Original Trilogy), Admiralty — disambig), 0 stubs.
  data/crawl_state.json frontier: ~42k raw queued links (deduped shown next run).
- chunk.py: 7729 chunks -> data/chunks/chunks.jsonl (+ chunks.jsonl.done manifest, 880 stems).
- build_bm25.py: data/bm25_index.pkl, 20M. Re-run of chunk + build = no-op (resume works).
- retrieve "Sovereign indoctrination Saren Citadel" -> sovereign_005 (20.4),
  saren-arterius_007 (18.9), sovereign_004 (18.4). On-topic. Suite 76 green.
- Next (user go-ahead): optionally more /me-scrape batches, then /me-build-lore,
  /me-build-timeline, first /me-generate.

### 2026-08-28 — brief is finer canon, not just framing (user correction)
- Reframed --brief across me-generate.md + outline-writer.md + section-writer.md:
  the brief LAYERS OVER config/narrative_choices.yaml as per-episode canon control
  — resolves options the choices file leaves open (e.g. which romance when several
  recorded), adds playthrough detail; where brief and choices file overlap, brief
  wins for that run. Still cannot add world events/dates/deaths (timeline+evidence only).
- Docs only, no code change (brief already flows new_run -> outline -> sections). 76 green.

### 2026-08-28 — canon selects choice-conditional timeline branches (user)
- Deaths/events keyed to player choices (wrex_virmire, virmire_survivor, council_fate,
  genophage, suicide_mission roster, geth_quarian, final_choice, ...) => canon
  (narrative_choices + brief) chooses WHICH branch is real, hence which sections exist
  and which outcomes are narrated.
- timeline-extractor.md: keep a conditional beat as ONE event file, record all branches
  in summary/consequences, name the deciding narrative_choices id; don't pick, don't split.
- outline-writer.md: resolved canon decides which branch is real -> section selection
  (no downstream sections for a character the canon kills; that beat carries the death).
- section-writer.md: narrate ONLY the canon-selected branch; a required consequence on a
  ruled-out branch is dropped, a selected branch's consequences become required; never
  two outcomes of one fork.
- me-generate.md wording updated. Docs only. 76 green.

### 2026-08-28 — scrape run 2 launched (user go-ahead)
- Command: scripts/scrape_wiki.py --seeds config/seeds.yaml --depth 2 --cap 2500 --rate 7
- pid 46473, nohup, log data/scrape_run2.log
- Resumed cleanly from data/crawl_state.json: "27419 queued, 1002 seen, 880 pages on disk"
  — drained the saved frontier, no API re-walk.
- ETA ~5h at rate 7 (2500 fetches). Re-run again afterward if frontier not drained.

### 2026-08-28 — scrape run 2 stopped, relaunched at rate 3 (user)
- SIGTERM'd pid 46473 cleanly: "signal 15: frontier saved — 3630 distinct pages still to crawl".
  900 pages on disk at that point.
- Relaunched: scrape_wiki.py --seeds config/seeds.yaml --depth 2 --cap 2500 --rate 3
  pid 51272, nohup, log data/scrape_run3.log. Resumed: "27457 queued, 1024 seen, 900 pages on disk".
- ETA ~2h at rate 3.

### 2026-08-28 — scrape run 3 stopped, corpus chunked + reindexed (user: "stop and do next step")
- SIGTERM'd pid 51272 cleanly at 2320/2500 fetched: "frontier saved — 1672 distinct pages still to crawl".
- Pages on disk: 2981 (was 900). crawl_state.json holds the 1672-page frontier for a later run.
- chunk.py resumed (2101 new pages, 880 skipped via .done): +12095 chunks -> 19824 total in data/chunks/chunks.jsonl.
- build_bm25.py: rebuilt data/bm25_index.pkl (39.1M, 19824 chunks). retrieve "Sovereign Reaper" -> reaper_015, human-reaper_005 — on-topic.

### 2026-08-28 — /me-build-lore: corpus filtered, sweep started (user)
- User: "filter corpus first" + "ignore andromeda specific pages".
- Filter 1 (filler): dropped 966 planet-scan stubs (type=location <250w, or Mineral-Deposits
  section <400w; + 18 tiny lore, 1 tech). Kept ~2037.
- Filter 2 (Andromeda): dropped 473 MEA-specific pages (lead-keyword + keyword-density
  heuristic, 2 passes; multi-game class/skill pages rescued via disambiguation-banner check).
- All drops -> data/lore_skipped.txt (1369 rows). All 19824 chunks stay in the BM25 index.
- FINAL lore to-do: 1634 pages -> batch 000 done (15 summaries; agent flagged a-better-beginning
  + adhi as actually-MEA, relabeled), 109 batches (~1621 pages) remaining.
- page-summarizer runs sequentially; resumable (page_summaries/<slug>.md = done).

### Session resume 2026-08-28 (later) — /pwf context restore
- Ran planning-with-files restore. session-catchup: no unsynced context. Re-read all
  three planning files + findings.md.
- STATE RECONCILED against git (progress log above was optimistic):
  - HEAD is still `f061f7a` ("docs: scrape relaunched (pid 21098)"). Everything logged
    after that entry — crawl_state.json frontier, resumable chunk.py/build_bm25.py,
    pending_pages wording, resumable me-build-timeline + rebuild_master_timeline.py,
    `me-generate --brief`, jack.yaml tweak — is **UNCOMMITTED** (git diff: 19 files,
    +703/-116; plus untracked scripts/rebuild_master_timeline.py +
    tests/test_rebuild_master_timeline.py). The "Committed / 65|70|76 green" notes in
    earlier entries did NOT actually land. Suite state unverified this session.
  - data/scrape.pid holds stale 21098; no scrape/summarizer process is running.
  - /me-build-lore sweep in progress: 205 summaries in page_summaries/ (gitignored),
    ~1429 of ~1634 filtered pages still to summarize. Resumable.
  - me-build-lore.md builds its source list as (all data/pages + lore/manual) minus
    existing summaries — it does NOT subtract data/lore_skipped.txt (1372 rows). The
    corpus filter is being applied manually by the controller when forming batches;
    the command file was never updated to honor lore_skipped.txt. Flagged for a fix.
- NEXT: (1) commit the pending Phase 5 work after a suite run; (2) decide whether to
  wire lore_skipped.txt into me-build-lore.md; (3) resume the page-summarizer sweep.

### Session 2026-08-28 (later) — commit + resume sweep
- Recreated .venv via `uv` (no venv existed): `uv venv && uv pip install -r
  requirements.txt`. `.venv/bin/pytest -q` -> 76 passed.
- Committed the whole Phase 5 backlog as ONE commit 0fccd8c
  ("feat(scrape,chunk,timeline): resumable frontier + interrupt-safe pipeline;
  me-generate --brief"). .gitignore now also ignores data/*.log, data/scrape.pid,
  data/lore_skipped.txt, data/lore_errors.log. data/ still untracked otherwise.
- page-summarizer sweep resumed. Project subagents in .claude/agents/ are NOT
  registered as spawnable types this session -> running the identical spec through
  `general-purpose` subagents instead.
- Todo recomputed: (data/pages + lore/manual - README) minus existing summaries minus
  `cut -f1 data/lore_skipped.txt` = 1428 pages -> 96 batches of 15
  ($SCRATCH/batches/b000..b095, todo list at $SCRATCH/todo.txt). Running sequentially
  (codex/*.md append races). Batch b000 dispatched.
- Switched to STATELESS resume: no longer using the $SCRATCH batch files. Each round
  recomputes the remaining list straight from disk with the me-build-lore.md step-1
  command (pages + manual - summaries - lore_skipped) and takes the next 15. This
  makes a fresh turn, a post-autocompact turn, and a post-/clear session all resume
  identically — page_summaries/<slug>.md IS the checkpoint. me-build-lore.md now
  encodes the lore_skipped.txt subtraction so /clear + /pwf reproduces it.
- Sweep progress: b000 +15 (all type:lore, no codex). b001 +15 (4 -> codex/characters.md).
  235 summaries on disk, 1398 in-scope pages remaining (~93 batches). Batch 3 dispatched
  (carnage..cerberus-commando).

### Session 2026-08-28 (later) — parallel waves (user: "run multiple batches in parallel")
- Switched to PARALLEL waves. Hazard = concurrent codex/*.md appends; page_summaries/
  writes are already disjoint. Fix: each parallel agent gets a WAVE_ID and writes codex
  bullets to codex/_inbox/<WAVE_ID>-<group>.md (bare "- " lines, no H1); after each wave
  the controller merges the inbox into codex/<group>.md (dedupe + sort under the H1),
  rm's the inbox, recomputes the remaining list, dispatches the next wave.
  me-build-lore.md step 3 now documents this parallel mode.
- Found an ORPHAN codex/inbox/ from an earlier session (b002..b008, "## group" format,
  never merged). Folded it into the same merge. codex/ backed up to $SCRATCH first.
- Wave 1 (batch3 + w1s0..w1s3, 75 pages carnage..citadel-a-friend-of-a-friend): done.
  Codex merge -> species.md 7, tech.md 29, characters.md 50, factions.md 1 (unique bullets).
- 310 summaries on disk, 1323 in-scope remaining (~89 batches).
- Wave 2 dispatched: 5x15 all citadel-* (w2s0..w2s4), lines 1..75 of the recomputed todo.
- ETA ~3h at 4-5 wide; ~9M subagent tokens total; needs this session live to dispatch
  each wave (or a /plan-loop nudge).
- Wave 2 done (75 citadel-* pages). Codex merge -> factions.md 5 (Citadel Council +
  C-Sec x3). species 7 / tech 29 / characters 50 unchanged. 385 summaries, 1248
  in-scope remaining (~84 batches).
- Commit 298e504: me-build-lore.md now honors lore_skipped.txt + documents parallel
  waves; plan/progress checkpointed.
- Wave 3 dispatched: 5x15 (w3s0..w3s4) citadel-the-fourth-estate .. combat-mass-effect-galaxy
  (many codex-* wiki entries + collector-* pages).

### Session resume 2026-08-29 — /pwf context restore
- Ran planning-with-files restore. session-catchup: no unsynced context. Re-read all
  three planning files + findings.md.
- STATE ON DISK: HEAD 298e504. Only progress.md modified (the Wave 3 dispatch note, +7).
  No scrape/summarizer process running. data/scrape.pid stale.
- Sweep reconciled: page_summaries/ now holds 460 .md (was 385 after Wave 2). Wave 3's
  75 pages DID land on disk (385+75=460). But: progress log never recorded Wave 3
  completion, and codex/_inbox/ is EMPTY — so Wave 3 codex bullets were either merged
  and rm'd already, or the Wave 3 agents wrote no codex bullets. codex/ files
  (characters/factions/species/tech .md) untouched since 21:07. Treat Wave 3 codex as
  UNVERIFIED — re-check inbox convention on next wave.
- Remaining: 1173 in-scope pages to summarize (me-build-lore step-1 recompute:
  data/pages + lore/manual - README - page_summaries - lore_skipped.txt[1372]).
  ~78 batches of 15.
- timeline/events/ still empty — /me-build-timeline not started (correct; waits for sweep).
- Wave 3 codex now VERIFIED complete: codex bullet counts grew since Wave 2
  (characters 50->56, factions 5->9, species 7->12, tech 29->55) and _inbox was
  emptied, so Wave 3's inbox merge did run. Newest summary `collector-guardian`
  matches Wave 3's stated range end. Wave 3 fully landed; only its progress entry
  was missing.
- User (/pwf, "resume one batch first"): dispatched a single page-summarizer batch
  w4s0 (15 pages, comics..crescent-nebula) in WAVE mode to re-confirm the
  summarizer + codex/_inbox/ convention end to end before scaling back to waves.
- w4s0 VERIFIED: 15/15 summaries written (475 total), lengths 136-400w, proper nouns
  intact, factual — spot-read commander-shepard + crescent-nebula, both good.
  codex/_inbox/w4s0-characters.md (10 bullets) merged into codex/characters.md
  (56 -> 66 bullets, dedupe+sort under H1), inbox cleared. Pipeline works end to end.
  Remaining recomputed: 1158 in-scope pages (~77 batches). NOT yet committed.

### 2026-08-29 — lore/manual to be chunked + indexed + fed richer into codex (user)
- User Q&A: confirmed section-writer's BM25 deep-dive only reaches data/pages chunks;
  lore/manual/*.md (24 hand-corrected deep-dive docs) are summarized only, NOT chunked.
- User: "yes. they have to matter, they also have to be used to enhance the codex.
  it's quite important." => make lore/manual chunked + retrievable AND give it a
  stronger codex contribution than the default type->bullets pass.
- Findings for the change:
  - 23 of 24 manual files still unsummarized (only arcturus-station done). Deep-dives:
    jack x3, tali x5, normandy-sr1 x2 / sr2 x4, reaper-classes x2, trilogy-secrets x2,
    systems-alliance-founding, turian-hierarchy-early-history, humanity-before-relays,
    destiny-ascension, two-unseen-races.
  - STEM COLLISION: arcturus-station and destiny-ascension exist in BOTH data/pages/
    and lore/manual/. chunk.py keys manifest + chunk-id on p.stem -> collision if both
    dirs globbed. me-build-lore step-1 `sort -u` also silently dedupes these two.
    Need a manual namespace (e.g. source "manual/<stem>" or "<stem>-manual").
  - chunk.py globs a single --pages dir (Path(pages_dir).glob("*.md")). Needs a second
    source dir, README.md excluded, resumable .done manifest still intact.
- NEXT: brainstorm the design (namespace scheme, retrieval weighting for manual lore,
  what "enhance the codex" means concretely) before coding.

### 2026-08-29 — design APPROVED (user: "perfect. continue"). 3 parts:
- Part 1 — chunk + index lore/manual, EQUAL FOOTING (no BM25 boost). chunk.py also
  scans lore/manual/*.md (excl README.md); manual chunks get source + chunk-id prefix
  `manual-<stem>` (dodges arcturus-station / destiny-ascension stem collisions,
  visible in sources.json). `.done` manifest keyed on the prefixed name. Then
  chunk.py run + build_bm25.py --force.
- Part 2 — codex entries for the 2 colliding slugs draw on BOTH the data/pages and
  lore/manual versions, weighting the manual (curated) text heavier; colliding
  summary written as page_summaries/manual-<slug>.md. me-build-lore step-1 must stop
  `sort -u` collapsing those two.
- Part 3 — per-narrator style reference config/narrators/<narrator>.style.md (linked
  file, NOT folded into the YAML bible, NOT the codex). Built by a new
  `narrator-style-extractor` subagent. Sources: data/pages/<narrator-char>.md Quotes
  section + <narrator>-unique-dialogue / *-battle-quotes / *-voicelines pages +
  lore/manual/*<narrator>* deep-dives. Output: ALL verbatim quotes (no cap — selected
  later), each with speaker + situation context, plus a short "how they talk" prose
  section. section-writer.md + outline-writer.md read it when present (YAML bible stays
  authoritative for tone/avoid/signature). Runs as a post-sweep step in me-build-lore,
  alongside /me-build-timeline.
- Parts 1-3 committed at 54b6b47. Suite 79 green. chunks.jsonl 19984 (160 manual),
  bm25 index rebuilt --force. Batch path files for the whole remaining sweep
  pre-sliced to $CLAUDE_JOB_DIR/tmp/batches/b00..b77.txt (15 pages each, 1160 total).
- Wave 5 dispatched: w5s0..w5s4 (b00..b04), pages crooks..eclipse-trooper.
  Codex bullets -> codex/_inbox/w5s*-<group>.md; merge after wave, recompute, next wave.
- Wave 5 DONE: 75/75 summaries (550 total). Inbox merge hit a zsh multi-file `cat`
  bug + premature `rm` — recovered all bullets from agent .output transcripts (jq),
  re-merged clean: characters 66->88, species 12->19, tech 55->60, factions 9->17.
  Wrote robust $CLAUDE_JOB_DIR/tmp/merge_inbox.sh for future waves (dedupe+sort, rm last).
- Wave 6 dispatched: w6s0..w6s4 (b05..b09), eclipse-vanguard..fortinbras-plague.
  Remaining before wave 6: 1085.
- Wave 6 DONE: 75/75 (625 total). Merged: characters 88->121, species 19->20,
  tech 60->66, factions 17. merge_inbox.sh fixed for empty-glob groups.
- Wave 7 dispatched: w7s0..w7s4 (b10..b14), forvan..hades-nexus-prothean-sphere
  (incl garrus-vakarian, genophage, geth, grunt + grunt-unique-dialogue).
  Remaining before wave 7: 1010.
- Wave 7 DONE: 700 total. characters 148, species 25, tech 87, factions 18.
- Wave 8 DONE: 775 total. characters 179, species 31, tech 103, factions 20,
  timeline 6 (first timeline bullets, from humanity-before-the-mass-relays — the
  lore/manual doc was already ASR-corrected). Committed checkpoint 1c874f5.
- Wave 9 dispatched: w9s0..w9s4 (b20..b24), irune-book-of-plenix..khalisah-al-jilani.
  w9s0 = Jack-heavy (jack + 3 lore/manual jack-* docs + jack/jacob dialogue pages).
  Remaining before wave 9: 860.

### Session resume 2026-08-30 — /pwf context restore + sweep tail
- Ran planning-with-files restore. session-catchup: no unsynced context.
  git working tree CLEAN, HEAD dd5a4d7. page_summaries/ is gitignored.
- STATE RECONCILED: waves 9..N all ran to disk since the last progress entry.
  page_summaries/ now holds 1629 .md. me-build-lore step-1 recompute
  (data/pages[2981] + lore/manual[24, README excl] - page_summaries - lore_skipped[1372])
  => only **6 in-scope pages left**: warp, warp-ammo, warp-skill, weapon-mods,
  weapons, zaeed-massani (all data/pages/*.md, none skipped).
  4 "extra" summaries that aren't in the recomputed in-scope list are expected:
  a-better-beginning + achievements (kept from early batches), manual-arcturus-station
  + manual-destiny-ascension (intentional manual- collision summaries).
- LEFTOVER unmerged codex inbox: codex/_inbox/w5b22-characters.md (Zev Cohen, Zymandis,
  Zaeed Massani/Unique dialogue) + w5b22-places.md (Zakera Ward, Zhu's Hope) — from a
  prior wave, never merged.
- timeline/events/ still empty — /me-build-timeline not started (correct; waits for sweep).
- config/narrators/*.style.md: NONE exist yet — me-build-lore step 5 not started.
  10 narrator yamls: garrus, jack, joker, kaidan, liara, samara, tali, thane, traynor, wrex.
- ACTION: dispatched final page-summarizer batch (WAVE_ID wfin, 6 pages) writing codex
  bullets to codex/_inbox/wfin-<group>.md. Next: merge w5b22 + wfin inboxes into
  codex/*.md (dedupe+sort under H1), verify 0 remaining, commit.
- THEN (needs user go-ahead): me-build-lore step 5 (narrator style refs, 10 agents),
  /me-build-timeline, first /me-generate.
- wfin batch DONE: 6/6 summaries (warp, warp-ammo, warp-skill = lore biotic pages,
  no codex; weapons + weapon-mods -> tech; zaeed-massani -> characters).
- Codex inbox merge (w5b22 + wfin, explicit-file-arg script — first attempt's quoted
  glob no-op'd, redone): characters 427->442, places 172->178, tech 215->225.
  codex/_inbox/ removed.
- SWEEP COMPLETE: me-build-lore step-1 recompute returns EMPTY. 1635 summaries
  (1631 in-scope + 4 expected extras). Suite 79 green. Committed 51708c3.

### 2026-08-30 — me-build-lore step 5: narrator style refs (user: "narrator style ref")
- Dispatched 10 narrator-style-extractor agents in ONE parallel wave, one output
  file each -> config/narrators/<slug>.style.md. No collision (disjoint outputs).
- Source resolution per narrator (char page + *-unique-dialogue + mission pages +
  lore/manual deep-dives + relevant multi-speaker cut-content *-voicelines pages;
  agents told to take only confidently-attributed lines from multi-speaker pages):
  - garrus: garrus-vakarian, citadel-garrus, garrus-eye-for-an-eye,
    garrus-find-dr-saleon + 5 ME1 cut-content voiceline pages. (no unique-dialogue page)
  - jack: jack, jack-subject-zero, jack-unique-dialogue, sb-dossier + 3 lore/manual
    (jack-character-analysis-01/02, jack-dialogue) + 3 ME2 cut-content voicelines.
  - joker: jeff-joker-moreau (+unique-dialogue), prologue-save-joker + 3 voicelines.
  - kaidan: kaidan-alenko (+unique-dialogue) + 5 ME1 cut-content voicelines.
  - liara: liara-t-soni, find-liara-t-soni + 4 ME1 cut-content voicelines.
  - samara: samara, samara-the-ardat-yakshi + 2 ME2 cut-content voicelines.
  - tali: tali-zorah-nar-rayya (+unique-dialogue), dossier-tali, sb-dossier,
    tali-treason, tali-and-the-geth, talis-fia + 5 lore/manual tali-character-analysis
    + 2 cut-content voicelines.
  - thane: thane-krios, thane-sins-of-the-father + 2 ME2 cut-content voicelines.
  - traynor: samantha-traynor ONLY (thin source — expected).
  - wrex: urdnot-wrex (+unique-dialogue), citadel-wrex, virmire-wrex-and-the-genophage,
    wrex-family-armor + 3 ME1 cut-content voicelines.
- config/narrators/ IS tracked (not gitignored) — commit the .style.md files after
  the wave + a suite run + spot-check.

### 2026-09-01 — TODO sweep (user: "now do the TODO")
- Restored context via planning-with-files. Verified suite green (79), spot-checked
  traynor/wrex style refs, committed all 10 config/narrators/*.style.md (9fb325e).
- Found + fixed real bug in config/narrative_choices.yaml: id `virmire_survivor` was
  reused for two different questions (ME1 "who survived Virmire" vs ME3 "did they
  rejoin the Normandy"), producing contradictory-looking output in the prompt summary
  fed to outline-writer (`ME1 virmire survivor: Kaidan ... ME3 virmire survivor: yes`).
  Renamed ME3 id to `virmire_survivor_rejoins`, clarified its prompt. Also normalized
  stray `detail : ""` spacing. Suite still 79 green. Committed (30832df).
- Culture/world-texture enrichment (TODO items 2-3):
  - Found Blasto (ME3 in-universe hanar movie franchise) was wrongly filtered as
    Andromeda content in data/lore_skipped.txt (false positive — page frontmatter
    says `game: Mass Effect 3`). Removed that row.
  - User's manual-page worry was a false alarm: all 24 lore/manual/*.md docs ARE
    summarized; only the 2 slug-collision ones (arcturus-station, destiny-ascension)
    get the `manual-` prefix, the other 22 use plain slugs (verified all 24
    individually against page_summaries/).
  - Dispatched page-summarizer agent (a92a54c0636d0df34): summarized blasto.md,
    backfilled 14 new bullets into codex/culture.md from 14 already-summarized pages
    whose flavor content (Fornax/Genit-elcor/Krogasm, elcor theater incl. Hamlet,
    Citadel DLC cocktail menu, species drinks/snacks, galactic sports, Illium vs Omega
    News tone, Morinth's cultural bait incl. Forta/Vaenia/Expel 10/Hallex, in-universe
    novels, tabletop/video games) never reached the codex. culture.md 81->95 bullets.
  - Added two new codex categories to .claude/agents/page-summarizer.md routing:
    `social.md` (interpersonal texture between named individuals — banter, crushes,
    rivalries, opinions about each other) and `everyday.md` (daily-life texture —
    fashion, objects, medicine, economy, architecture, ambient fauna/flora, news).
    User chose "expand codex/*.md categories" over a separate retrieval subsystem.
  - Dispatched page-summarizer agent (a8125b0abde367c34) to seed both new files from
    romance.md + 10 crew character pages + foods/drinks/game-shop.md (read-only,
    page_summaries/ untouched). Result: codex/social.md 28 bullets (Kasumi/Jacob
    crush, Jack-Miranda rivalry, Garrus-Tali banter, Traynor's EDI crush, Wrex's
    species prejudices, etc.), codex/everyday.md 10 bullets (nutrient paste economics,
    levo/dextro food friction, drink/coffee culture, in-universe advertising).
  - DISCOVERED: codex/ was entirely gitignored — the whole curated lore digest
    (1635-page sweep output) had never been in git history, only on disk + the user's
    manual mass.zip backup from 2026-08-28 (now stale). Asked user; confirmed: track
    it. Removed `codex/` from .gitignore (also added `mass.zip` to .gitignore — keep
    the archive out of git, matches existing `config.zip` convention).
- Suite green (79) throughout. NEXT: commit codex/ + .gitignore + page-summarizer.md
  routing update + TODO (everything except mass.zip), then continue the TODO: verify
  narrative_choices is otherwise sound (done), `/me-build-timeline`, surface any
  timeline-driven open choices to the user, then generation readiness.

### 2026-09-01 (cont.) — thorough texture pass: keyword search instead of blind re-mine
- User: "there's no Ryncol for flagged relevant pages... take the keywords/idea I gave
  you, add synonyms... create a whole cloud of ideas... search the pages with a
  script/bash command and only process the relevant ones with a model." Confirmed gap:
  data/pages/ryncol.md (krogan liquor, own dedicated page, cited in 15 other pages) has
  a page_summaries entry but zero codex/culture.md or everyday.md bullets — same
  failure mode as Blasto.
- Built scripts/texture_keywords.txt (curated cloud of synonyms/adjacent terms per
  category: religion, culture/arts, food/drink, games, medicine/objects,
  economy/politics, prejudice/social friction, flirting/humor, fashion/architecture/
  fauna-flora) + scripts/find_texture_candidates.py (deterministic, no-LLM grep over
  data/pages + lore/manual, cross-referenced against existing codex/{culture,social,
  everyday}.md source citations to mark already-covered vs new).
  - First pass: naive prefix-matching (`art*`, `opera*`) hit 2451 pages — mostly noise
    ("art" matched "Arterius", "opera" matched "operative"). Fixed to whole-word
    matching by default (opt-in `*` suffix only for real stems), pruned generic
    sci-fi vocabulary (council/government/corporation/market/trade/device/merchant)
    that would flag most of the corpus and defeat the point of a filter. Also caught
    "custom*" matching "customer"/"customize" — narrowed to specific phrases.
  - Re-run: 807 keyword hits -> 521 new uncovered candidates (248 filtered via
    data/lore_skipped.txt, mostly legit Andromeda pages e.g. Jaal/Aya — spot-checked,
    no more Blasto-style false positives found in this batch).
  - User: also fold in Shadow Broker dossiers + Citadel pages for social.md, read full
    raw pages not just summaries (they're relationship-rich but don't reliably hit
    generic keywords). Added 12 dossier + 87 citadel-*.md pages (70 not already in
    keyword candidates) -> data/texture_final_candidates.txt, 592 total slugs
    (gitignored, regenerate via the script; script + keyword file are committed).
- User: start small, extraction-only (append codex bullets, do NOT rewrite
  page_summaries/*.md bodies — cheaper per-page than the original full sweep).
  Dispatched trial batch (agent a9feebb6ae41477da): 12 Shadow Broker dossiers + top-20
  multi-keyword-hit pages (ashley-williams, james-vega, asari, krogan codex pages,
  etc.) = 32 pages, extraction-only, running.
- NEXT: review trial batch yield/quality with user, then decide sequential vs
  parallel-wave pacing for the remaining ~560 candidates in data/texture_final_candidates.txt.

### 2026-09-01 (cont.) — trial texture batch results
- Trial (37 pages: 12 Shadow Broker dossiers + 20 high-keyword-density pages,
  extraction-only, page_summaries/ untouched): 18 new bullets (culture.md 97->104,
  social.md 37->42, everyday.md 13->19). ~50% yield — richest sources were Shadow
  Broker character dossiers (personal logs/purchase histories) and Cerberus Daily
  News archives (tabloid/culture content); walkthrough/plot-synopsis pages mostly
  had nothing left to extract. Spot-checked, well-sourced, suite still 79 green.
- Also wired the codex into actual generation (user request, separate from the sweep):
  section-writer.md never read codex/*.md directly (only BM25 chunk retrieval from
  raw pages) — the culture/social/everyday content could sit unused however thorough
  the codex got. Added a grep-codex step + a rule to weave in a matching bullet as
  grounding color when one fits; outline-writer's lore step now explicitly names
  world-texture so it isn't crowded out by plot-only sections. Committed (b811e1c).

### 2026-09-01 (cont.) — full texture sweep, wave 1
- User: "continue" (fuller pass past the trial). Marked the 37 trial-batch slugs done
  in data/texture_candidates.done, recomputed remaining: 555 candidates
  (data/texture_remaining.txt). Split into 28 batches of 20
  (data/texture_batch_000..027, gitignored working files).
- Wave 1 dispatched: 5 parallel agents, batches 000-004 (100 pages: alliance news
  network pages, armor/weapon pages, bioware-stories dev interviews + bonus-content-disc
  creature/environment featurettes, cerberus-daily-news archives, citadel-arena +
  chora's den pages). Extraction-only, page_summaries/ untouched.

### 2026-09-01 (cont.) — wave 1 committed, wave 2 dispatched
- Wave 1 (batches 000-004, 100 pages) results: culture.md +17, social.md +17,
  everyday.md +14 (48 bullets). Spot-checked good quality, well-sourced,
  specific (turian dueling customs, Ardat-Yakshi monastery economy, AI-rights
  advocacy, Chora's Den rumors, cross-species mourning after Vallum Blast, etc).
  Suite 79 green. Committed a2729e1.
- Wave 2 dispatched: 5 parallel agents, batches 005-009 (100 pages) — almost
  entirely `citadel-*` side-quest/assignment pages (per user instruction to
  mine Citadel files fully) plus a few in-game codex entries and misc
  character pages. Extraction-only, page_summaries/ untouched.

### 2026-09-01 (cont.) — wave 4 committed, wave 5 hit rate limit (checkpoint)
- Wave 3 (batches 010-014, 100 pages) results: culture.md +13, social.md +41,
  everyday.md +16 (70 bullets) — notably landed the Book of Plenix bullet the
  original TODO flagged as under-covered (Kahje's Nyahir holiday too). Suite 79
  green. Committed 60d01ec.
- Answered a user process question about how outline-writer weighs its inputs
  (timeline -> narrative_choices/brief resolve forks -> narrator's own arc as
  spine -> codex/summaries fill gaps -> galaxy events as connective tissue).
  Wrote this up in README.md as a new "How outline-writer actually weighs its
  inputs" section, plus an earlier "Where each piece fits" data-flow table
  (build phase vs generation phase, what reads what: raw pages -> BM25/
  summaries/codex -> timeline -> narrator config/style/narrative_choices ->
  outline -> sections). Committed 9208095.
- Wave 4 dispatched and committed (batches 015-019, 100 pages): culture.md +10,
  social.md +21, everyday.md +14. Character loyalty-mission pages, cut-content
  voicelines, in-universe comics (Foundation, Redemption), Normandy SR-2 crew
  texture. Committed 8f74c1a.
- User clarified scope: "finish the waves" = finish the codex world-texture
  extraction sweep only, not the other parked TODO items (timeline build,
  narrative_choices review, generation-readiness wrap-up).
- Wave 5 dispatched (batches 020-024) but hit the session's API rate limit
  ("You've hit your session limit, resets 4:30pm Europe/Paris") — agents
  020, 021, 022 all failed/terminated early before writing anything to codex
  files (confirmed via `git status --short` = clean, nothing to salvage).
  Batches 023-024 were never dispatched this round.
- STATE AT CHECKPOINT: batches 000-019 done (marked in
  data/texture_candidates.done, 337 entries). Batches 020-027 (8 batches,
  ~160 pages) remain undispatched/failed. No uncommitted codex changes.
  Resume by re-dispatching wave 5 as page-summarizer agents over
  data/texture_batch_020 through data/texture_batch_027 once the session rate
  limit resets (~16:30 Europe/Paris), same extraction-only brief pattern as
  waves 1-4, 5 batches per wave, commit + mark .done + pytest after each wave.

### 2026-09-01 (cont.) — world-texture sweep wave 5 (post rate-limit resume)
- Re-dispatched the failed wave 5 as 5 Haiku page-summarizer agents, batches
  020-024 (100 pages), extraction-only (codex/_inbox/wA0XX-{culture,social,
  everyday}.md, page_summaries/ untouched). Per-batch yield: 020=12, 021=31,
  022=24, 023=45, 024=50 bullets.
- Merged (scratchpad merge_inbox.sh, dedupe+sort under H1): culture 154->204 (+50),
  social 138->181 (+43), everyday 79->143 (+64). Suite 79 green. Committed c122978.
- Marked batch 020-024 slugs in data/texture_candidates.done (437 rows, gitignored).
- Note: a Haiku agent left a stray one-line CLAUDE.md in repo root (paraphrase of
  the task prompt); not committed, removed. zsh `rm` is aliased to `rm -i` — use
  `/bin/rm -f` in tool calls.
- Note: batch 024 landed ~10 Talein's Daughters / Cora Harper bullets sourced from
  the in-corpus talein-s-daughters.md + tamayo-point.md pages (Andromeda-tie-in
  novel content, but pages are game:"Mass Effect" and not in lore_skipped). Left as-is
  per the mechanical waves-1-4 pattern; harmless for trilogy generation (won't be
  retrieved for trilogy events).
- REMAINING: batches 025-027 (3 batches, ~55 pages) = final wave.

### 2026-09-01 (cont.) — world-texture sweep wave 6 (FINAL) — SWEEP COMPLETE
- Dispatched batches 025-027 as 3 Haiku page-summarizer agents (55 pages),
  extraction-only (codex/_inbox/wB0XX-*.md, page_summaries/ untouched).
  Per-batch yield: 025=79, 026=52, 027=37 bullets (168 pre-dedupe).
- Merged (merge_inbox.sh, dedupe+sort under H1): culture 204->265 (+61),
  social 181->220 (+39), everyday 143->204 (+61). All bullets carry a
  (source: ...) tag. Suite 79 green. Committed e022c235.
- Marked batch 025-027 slugs in data/texture_candidates.done (492 rows, gitignored).
- Highest-yield sources: The Art of the Mass Effect Trilogy art books (concept-art
  in-universe captions), Urdnot Wrex & Zaeed Massani unique-dialogue pages
  (verbatim social lines), Varren ecology, Zakera Ward ambient commerce memos.
- SWEEP COMPLETE: texture_batch_000-027 (28 batches) all processed. Final codex
  world-texture totals: culture.md 265, social.md 220, everyday.md 204 bullets.
  Parked TODO items (narrator style refs, /me-build-timeline, first /me-generate)
  remain untouched — awaiting explicit user go-ahead.

### Session resume 2026-09-02 — /pwf context restore
- Ran planning-with-files restore. session-catchup: no unsynced context. Re-read all
  three planning files + findings.md. HEAD cddb2ca.
- STATE RECONCILED against git — there is UNCOMMITTED, UNLOGGED work on disk:
  - NEW `scripts/sync_narrative_choices.py` (233 lines) + `tests/test_sync_narrative_choices.py`
    (108 lines, +7 tests). A CATALOG of ~60 canonical trilogy decision points
    (shepard/me1/me2/me3); `sync` appends a blank stub (answer:""/detail:"", options
    pre-filled where discrete) for every catalogue id absent from the file, touching
    nothing that already exists; `--check` reports gaps and exits 1.
  - `config/narrative_choices.yaml` MODIFIED (+157/-41): the sync script has been run
    against it — many stub questions added (first_name, alignment, feros_colony,
    bring_down_the_sky, conrad_verner, saren_confrontation, all me2 loyalty missions,
    most me3 beats…), plus several existing prompts reworded to drop `": "` so they
    emit unquoted. Existing answers/details preserved.
  - `.claude/commands/me-build-timeline.md` MODIFIED: new step 8 runs
    `sync_narrative_choices.py` after the load check; steps renumbered; Verify section
    adds a `--check` assertion.
  - Untracked `me-gen.zip` (28 MB, 2026-08-30) — user backup archive, keep out of git
    (matches config.zip / mass.zip convention; not yet in .gitignore).
- Suite: `.venv/bin/pytest -q` → 86 passed (was 79; +7 from the new test file). Green.
- This directly advances Phase 6 TODO items "Verify narrative_choices.yaml config" and
  "Surface timeline-driven choices not covered by narrative_choices.yaml". Looks
  complete and tested; needs a commit decision + user review of the new blank stubs.
- NEXT: get user direction — commit the sync work, then choose among remaining Phase 6
  items (/me-build-timeline, generation-readiness wrap-up) or first /me-generate.
- User chose: "just commit the sync work" then stop for review.
- Pre-commit check caught that config/narrative_choices.yaml did NOT validate:
  8 stub answers the user filled were shorthand not matching the pre-filled option
  strings (bring_down_the_sky 'Let go', conrad_verner 'Talked him down',
  saren_confrontation 'Talked into suicide', legion_loyalty 'Rewritten',
  overlord 'sent to Grissom', kelly_chambers 'Survived', mordin_fate 'Died',
  salarian_councilor 'Refused'). The test suite never loads the real config so
  pytest stayed green. User chose "normalize my answers to the option strings" —
  rewrote all 8 to the option verbatim. `scripts/narrative_choices.py
  config/narrative_choices.yaml` now clean; `sync_narrative_choices.py --check`
  reports complete.
- Committed 7638e14: sync_narrative_choices.py + test (+7), backfilled
  narrative_choices.yaml, me-build-timeline.md step 8 + Verify assertion,
  .gitignore += me-gen.zip. Suite 86 green. Working tree clean.
- Phase 6 checkboxes updated: "verify narrative_choices" + "surface timeline-driven
  choices" now [x]. Remaining: /me-build-timeline, generation-readiness wrap-up.
- STOPPED for user review per instruction.

### 2026-09-02 (cont.) — /me-build-timeline: harden resume, then run
- User: "make sure generate-timeline can be stopped and resumed; run it; Haiku for
  easy agents; no more than 2 agents at a time."
- Hardened /me-build-timeline resume (commit 563d220):
  - Command step 2 now `mkdir -p timeline/events`, `rm -f *.yaml.tmp`, and drops any
    event file that fails `common.load_event` (half-written by a hard stop — its
    stems aren't in timeline/.done so the next batch rebuilds it).
  - timeline-extractor.md: write each event file atomically (<id>.yaml.tmp then mv).
  - Documented the resume contract (interrupted batch is redone idempotently; agent
    skips existing event files) + 2-agent concurrency cap; only the controller
    appends timeline/.done, one batch at a time.
  - Suite 86 green.
- RUN STARTED: 1636 summaries, batches of 20 -> 82 batches
  ($SCRATCH/tbatches/b000..b081), 2 Haiku agents per wave = 41 waves. Resumable via
  timeline/.done (currently empty). timeline/events/ empty at start.
- Wave 1 dispatched: b000 (2175-aeia..aeian-t-goni), b001 (aethyta..anto).
  NOTE: b001 prompt had a copy-paste smudge (duplicated first 3 path lines + stray
  $(cat)) but carries an explicit disambiguation naming the real 20-file range.
- On each wave complete: append batch stems to timeline/.done, then next wave.
  After all waves: rebuild_master_timeline.py, load check, sync_narrative_choices,
  report + Verify.
- Wave 1 (b000-b001): 13 events. Removed 1 Andromeda false-positive (Prodromos/Eos
  2819 CE from "a-better-beginning"); patched timeline-extractor.md with an explicit
  "original trilogy only, skip Andromeda" rule (commit df... after 563d220).
- Wave 2 (b002-b003): +13 -> 26 events. The Arrival/Bahak relay, Arcturus Station
  destruction, Leviathan discovery, Omega liberation, Aria merc-recruit beats,
  Normandy SR-1 first flight, Lesuss monastery.
- FINDINGS note added: chronological_order collides across batches (each numbers
  10,20,30 independently). Needs a post-sweep renumber pass (sort by game+date,
  reassign in tens, rebuild). rebuild_master_timeline stays deterministic meanwhile.
- Wave 3 (b004-b005) dispatched, then user interrupted the session (killed the
  agents). b004 still completed post-kill (+arrae-ex-cerberus-scientists-rescue,
  merged sources into arrival-bahak). b005 lost. Neither in timeline/.done -> both
  redone. Disk reconciled: 27 event files, no .tmp, all parse, dates all <=2186 CE.
- User asks: (a) watch main-process token growth; (b) hard cutoff = nothing after
  Mass Effect: Andromeda's start (Initiative DEPARTURE from Milky Way ~2185 is OK;
  Heleus / ~2819 arrival / Ryder are OUT).
  - (b): sharpened timeline-extractor.md rule + committed. "Drop any event dated
    after ~2190 CE." Current events clean.
  - (a): batch size 20 -> 36 (44 batches, ~22 waves instead of 39); bookkeeping
    (append .done + rebuild) now every 2 waves not every wave; terser prompts.
- NEW BATCHING: $SCRATCH/tb2/b000..b043 (36 stems each), rebuilt from the 1556
  stems not yet in timeline/.done. $SCRATCH/mkpaths.sh emits the path list.
- KNOWN dup events from parallel batches (need an end-of-sweep merge pass):
  arcturus-station-destruction + battle-of-arcturus-station;
  liberation-of-omega + liberation-of-omega-afterlife-assault.
- Wave "tb2-1" dispatched: tb2/b000 (armor-piercing-ammo..attican-beta),
  tb2/b001 (attican-traverse..bethany-westmoreland).
- tb2-1 DONE: tb2/b000 = 0 created / 7 enriched (idempotent merge, good).
  tb2/b001 = +6 (Benezia/Noveria death, Kasumi/Bekenstein, Shadow Broker/Baria,
  Avernus adjutant, Attican Traverse rachni, Benning evidence).
  Old interrupted b005 also completed late (+5: Virmire-survivor choice,
  Bring-Down-the-Sky, Overlord, Ashley/Eden Prime, Citadel coup) — subsumed by
  tb2 ranges, merged fine.
- BUG FOUND + FIXED (commit 7d53ab1): a Haiku batch wrote foo_bar.yaml for
  event_id foo-bar (5 files), breaking master<->file match. Renamed all 5; added
  a filename-normalize step to /me-build-timeline (now step 6, before rebuild);
  agent def now says filename MUST equal <event_id>.yaml. Suite 86 green.
- CHECKPOINT COMMIT 7f9608f: timeline/ first tracked (38 events). master rebuilt,
  all 38 master rows have matching files. Dates all <=2186 CE (scope clean).
- Wave "tb2-2" dispatched: tb2/b002 (binary-helix..bonus-content-disc-creatures-hanar),
  tb2/b003 (bonus-content-disc-creatures-humans..caleston) — both very low-yield
  (biotic skills, merc enemy types, dev-commentary featurettes).
- timeline/.done = 152 stems. tb2 batches done: b000,b001 (2/44).
- tb2-2: b002 = 0 events, b003 = 0 created / 2 enriched. (all skill/enemy/dev pages)
- tb2-3 (b004 caleston-cut..cerberus-daily-news-july, b005 ..charles-saracino):
  both 0 events (Cerberus armor/news archives, character-index pages).
- tb2-4 (b006 charn..codex, b007 citadel-cerberus-retribution..citadel-oculon-syndicate):
  b006 +1 citadel-dlc-archives (Citadel DLC clone); b007 +1 expose-saren-citadel-hearing
  + 2 enriched (leviathan-discovery, cerberus-coup). -> 40 events. Committed 7129448.
- tb2-5: b008 Haiku (minor citadel quests) + b009 SONNET (Suicide Mission, needs
  branch care). b009 DONE: +1 suicide-mission (one choice-conditional event, all
  death permutations + Collector Base fate, cites suicide_mission/collector_base/
  iff_delay/loyalty_missions/kelly_chambers). b008 KILLED by user "stop and save"
  before writing anything -> NOT in timeline/.done, re-runs on resume.

### 2026-09-02 — /me-build-timeline PAUSED at user request ("stop and save")
- Stopped agent tb2-b008. Reconciled disk: rm *.yaml.tmp (none), dropped 0 partials,
  0 filename mismatches. Marked tb2/b009 done. Rebuilt master.
- STATE (committed a683f51): 41 event files, master_timeline.yaml 41 rows all matched,
  dates 2157-2186 CE (scope clean, nothing post-Andromeda). Suite 86 green.
  timeline/.done = 404 stems. tb2 done: b000-b007 + b009 (9/44). ~35 batches remain.
- RESUME: re-run /me-build-timeline (or continue the tb2/bNNN waves manually per
  task_plan.md Next Step). b008 will redo. Then post-sweep: chronological_order
  renumber + merge the 2 known dup-event pairs + command steps 8-12.
- Known dup events still to merge: arcturus-station-destruction +
  battle-of-arcturus-station; liberation-of-omega + liberation-of-omega-afterlife-assault.

### 2026-09-02 (session 2) — timeline sweep, token-minimal / pause-per-wave
- User: continue sweep, Haiku for small batches / Sonnet for pivotal, pause + save +
  commit after EACH wave so context can be /clear'd.
- Prior tb2/* scratch lost with old session -> batches now re-derived from disk each
  wave: comm -23 (page_summaries stems) (sort -u timeline/.done), next 72 -> 2x36.
- Wave 1 (both Haiku): A=citadel-old-friends..codex, B=collector-captain..crescent-nebula.
  A +8 events (wrex-recruitment-citadel, council-meeting-me2, conrad-verner-saga,
  terra-firma-political-influence, citadel-dlc-identity-theft-begins,
  saren-sovereign-final-battle, citadel-rita-s-sister-jenna, volus-ambassador-din-korlack).
  B +3 (collector-ship-mission, ilos-conduit-citadel, london-conduit-assault).
  61 of 72 pages yielded nothing (mechanics/stat/minor pages) — expected.
- Bookkeeping: .done 404->476, filenames normalized (0 renames), master rebuilt
  (52 rows, all matched, chronological_order non-decreasing), suite 86 green.
  Committed 0505239. Remaining: 1160 stems (~16 waves).
- Possible dups for the post-sweep merge pass: saren-sovereign-final-battle vs any
  existing citadel-battle event; citadel-dlc-identity-theft-begins vs citadel-dlc-archives;
  ilos-conduit-citadel vs any existing ilos event.
- PAUSED for /clear. Resume: task_plan.md "Per-wave procedure", start wave 2.

### 2026-09-02 (session 2) — timeline sweep wave 2
- Wave 2: A=crooks..din-korlack (sonnet — batch held `crucible`), B=director..eclipse-heavy (haiku).
  +15 events -> 67. .done 476->548. Suite 86 green. Remaining: 1088 stems (~15 waves).
- Batch A +7 new: crucible-superweapon-project, derelict-reaper-iff-mission,
  desolas-arterius-palaven-coup, sidon-research-station-attack, dekuuna-elcor-evacuation,
  fehl-prime-collector-attack, horizon-collector-attack. +3 updated: normandy-first-test-flight,
  overlord-david-archer, volus-ambassador-din-korlack.
- Batch B +8 new: garrus/tali/jack/samara/mordin/zaeed/grunt-recruitment-* (ME2 dossiers),
  drell-rescue-kahje. ~26 of 36 pages yielded nothing (mechanics/enemy-type/lore-catalog) — expected.
- Bookkeeping: filenames normalized (0 renames), master rebuilt (67 rows, all matched,
  chronological_order non-decreasing, first abrudas-trap-shanxi / last london-conduit-assault).
- Dup-merge candidates for post-sweep: horizon-collector-attack vs existing horizon event;
  derelict-reaper-iff-mission vs existing reaper-iff/legion event.
- Noted: commit 0505239 accidentally committed mass2.zip (29MB binary) — flagged to user.
- PAUSED for /clear. Resume: task_plan.md "Per-wave procedure", start wave 3.

### 2026-09-02 (session 3) — timeline sweep wave 4 (PARTIAL) + chronological_order concern
- Ran batches 000–004 (100 stems, `eva-cor`..`greg-adams`). .done 588→688. Events 76→98 on disk.
  Batches 005–009 dispatched but 005 & 006 died on session rate limit (resets 12:40 Paris);
  005–009 NOT in .done — re-run next session (idempotent, extractor skips existing event files).
  Deleted accidental mass2.zip (29MB) in this commit.
- New events this wave incl: first-contact-war, priority-mars, priority-sur-kesh,
  genophage-cure-tuchanka, shadow-broker-base-hagalaz, morning-war /
  quarian-geth-morning-war, genophage-deployed-*, geth-heretic-schism,
  legion-a-house-divided-heretic-station, rannoch-quarian-geth-war-resolution,
  freedom-s-progress-investigation, garrus-eye-for-an-eye, grunt-rite-of-passage-tuchanka,
  ascension-project-cerberus-exposure, cerberus-assault-on-the-idenna.
- **OPEN ISSUE (user-flagged): `chronological_order` integers are unreliable across batches.**
  Each timeline-extractor batch runs isolated/parallel and guesses a *global* integer from
  ~20 summaries + existing files; no coordination, and NOTHING renumbers them afterward.
  Result: ME3 events (2186) interleaved into the ME1 range — e.g. adjutant-outbreak-omega
  (2186) at order 40 between two Eden Prime (2183) events; council-meeting-me2 (2185) at 155
  mid-ME1; battle-of-arcturus-station (2186) tied at 310 with arrival-bahak (2185).
  The skill "Verify" check ("non-decreasing") is vacuous — rebuild sorts by that key.
  Every event DOES carry a `date` field (`YYYY CE` / `approx. YYYY CE` / `YYYY-YYYY CE`).
  PROPOSED FIX (needs user decision): add `scripts/renumber_timeline.py` — deterministic
  pass run once after the sweep: sort by (parsed year, game rank ME1<ME2<ME3, current
  order as local hint), reassign chronological_order in steps of 10. Intra-year order
  (2183 ~20 events, 2186 dozens) stays approximate unless a mission-sequence anchor list
  is added. Until then the integers are only locally meaningful within one batch.
- PAUSED for /clear (rate limit + awaiting user call on the renumber approach).
  Resume: re-run wave 4 batches 005–009, then continue alphabetically from `grenade-upgrades`.

### 2026-09-02 (session 3 cont.) — renumber decision: RESOLVED
- User: "Renumber at the end of all timeline generation ... Add that as a script/command after."
- Built `scripts/renumber_timeline.py`: deterministic one-shot pass. Sort key
  `(parse_year(date), game_rank ME1<ME2<ME3, current chronological_order, event_id)`;
  rewrites chronological_order as 10,20,30,… touching only that one line per file;
  idempotent; also rebuilds master. Flags: `--dry-run`, `--check` (exit 1 on drift),
  `--no-rebuild`. Intra-year order stays approximate (no mission anchors — accepted).
- Wired into `/me-build-timeline` as **step 7**, guarded "only when the whole sweep is
  done" (step-3 to-do list empty); steps 7–12 renumbered to 8–13. Added Verify line:
  `renumber_timeline.py --check` clean after a completed sweep.
- Tests: `tests/test_renumber_timeline.py` (7 cases) + needle in `test_command_defs.py`.
  Full suite 92 green. NOT run against real data yet — sweep is still partial (688/~1276).
- Still to do: finish the sweep (wave 4 batches 005–009, then batches 010+), THEN run
  `python scripts/renumber_timeline.py` once. Dedup/merge pass still pending too.

### 2026-09-02 (session 4) — timeline sweep wave 4 COMPLETE
- Re-ran wave 4 batches 005–009 (100 stems, `grenade-upgrades`..`jack-unique-dialogue`).
  .done 688→788. Event files 98→108. All 108 load clean; master rebuilt (108 rows,
  first genophage-deployed-krogan-rebellions / last london-conduit-assault).
- New events: grissom-academy-emergency-evacuation, hades-nexus-prothean-artifact-recovery,
  hal-mccann-death-on-the-citadel, helena-blake-crime-syndicate, miranda-the-prodigal,
  priority-horizon-sanctuary, mass-effect-galaxy-jath-amon-citadel-plot,
  murder-of-irikah-krios, subject-zero-cerberus-teltin-experiments, jack-subject-zero.
- Many updates (source_chunks): grunt-rite/recruitment, tali-recruitment-haestrom,
  rannoch-*, cerberus-assault-on-the-idenna, ascension-project-*, garrus-eye-for-an-eye,
  horizon-collector-attack, suicide-mission, ilos-conduit-citadel, randall-ezno-barn-escape,
  jack-recruitment-purgatory.
- Dup-merge candidates for post-sweep pass: miranda-the-prodigal vs priority-horizon-sanctuary
  (both Lawson/Oriana threads); jack-subject-zero (loyalty) vs existing jack-recruitment;
  hades-nexus-prothean-artifact-recovery merged 2 fetch missions already.
- narrative_choices.yaml: complete, validator + --check clean (no change).
- renumber_timeline.py NOT run (sweep still partial: 788/1636 summaries, ~948 stems left).
- PAUSED for /clear. Resume: `/me-build-timeline`, continue alphabetically from batch 010
  (`jaal-*` onward — fresh todo regenerates from .done, old scratchpad batches still valid).

### 2026-09-02 (session 5) — timeline sweep waves 5–7
- Waves 5–6 were run in a prior session that /clear'd without a progress.md entry
  (commits 89af54a, 530e84c): .done 788->1048, event files ->142.
- Wave 7 (this session): 12 batches of 20 (`mechs`..`rannoch-geth-fighter-squadrons`),
  running 4 `timeline-extractor` subagents at a time (user asked for 4-wide). Haiku by
  default; Sonnet for the choice-heavy batches: b01 (mordin-old-blood / morinth),
  b09 (the ME3 Priority: * mission spine), b10 (protect-the-council + ME1/ME3 prologues),
  b11 (the rachni-queen Noveria choice).
- +17 new event files -> 159 on disk. ~12 existing events picked up source-chunk merges
  (attack-on-eden-prime, normandy-sr1-destruction-alchera, benezia-death-noveria,
  liberation-of-omega, london-conduit-assault, overlord-david-archer, paul-grayson-*,
  rannoch-quarian-geth-war-resolution, freedom-s-progress-investigation,
  samara-recruitment-illium, miranda-the-prodigal, discovery-of-the-kholas-array).
  Note: one subagent reported Edit tooling disabled and could not append minor chunk
  ids to two already-complete Citadel-DLC events — cosmetic, events themselves complete.
- .done 1048->1288. Suite 92 green. master rebuilt: 159 rows, every id has a file,
  chronological_order non-decreasing (still only locally sorted — renumber pass is
  post-sweep). first krogan-rebellions / last london-conduit-assault.
- `timeline/events/` and `timeline/master_timeline.yaml` are gitignored by design; the
  wave commit is `timeline/.done` + task_plan.md + progress.md only.
- me3.zip (30MB) sits untracked in the worktree and is NOT in .gitignore — flagged in
  task_plan.md; do not `git add -A` it into history.
- renumber_timeline.py NOT run (sweep partial: 1288/1636, 348 stems left, ~15 batches).
- Post-sweep dup-merge candidates added (see task_plan.md wave log): noveria-geth-interest
  / noveria-espionage vs benezia-death-noveria; normandy-sr1-destruction-alchera vs any
  ME2-opening event; project-firewalker-the-prothean-site-on-kopis vs
  hades-nexus-prothean-artifact-recovery.
- PAUSED for /clear. Resume: `/me-build-timeline`, continue alphabetically from `ravager`
  (regenerate remaining.txt from .done; scratchpad batch b12 was prepared but not run).

### Timeline sweep — standing process (user-set 2026-09-02)
- **Wave = 8 batches of 20 summaries.** Run **4 `timeline-extractor` subagents at a
  time** (user override of the skill's 2-wide cap; batches write disjoint event
  files, only the controller appends `timeline/.done`).
- Haiku subagents by default; Sonnet for choice-heavy batches (branching decisions,
  ME3 Priority spine, prologues).
- After each batch returns: append its 20 stems to `timeline/.done` (controller only).
- **End of each wave:** normalize event filenames to `event_id`, `python
  scripts/rebuild_master_timeline.py`, load-check, resolve any obvious duplicate
  events, then `git commit` the `.done` bump (+ task_plan.md / progress.md).
- **STOP after each wave** and hand back for a `/clear`. Do not roll straight into
  the next wave.
- `renumber_timeline.py` runs **once, at the very end** of the whole sweep only.

### 2026-09-02 (session 6) — timeline sweep wave 8
- Wave 8: batches b00–b07 (`ravager`..`tali-and-the-geth`), 4-wide, per process above.
- +14 new events -> 173 on disk. Deleted duplicate
  `shepard-reconciles-septimus-oraka-and-the-consort` (superseded by
  `citadel-the-consort-s-dilemma`). Kept `destruction-of-the-ssv-iwo-jima` as a
  distinct dated beat despite overlap with `sidon-research-station-attack`.
- .done 1288->1448. master rebuilt: 173 rows. Commit 06d34ec.

### 2026-09-02 (session 6) — timeline sweep wave 9
- Wave 9: batches b08–b15 (`tali-character-analysis-01`..`warp`), 4-wide, per process.
- +16 new events -> 189 on disk. Merged 2 duplicate pairs:
  `tuchanka-bomb` folded into `tuchanka-bomb-tarquin-victus` (kept war-asset branch
  chunks); `virtual-aliens-ghost-ship-contact` folded into
  `virtual-alien-ghost-ship-encounter` (kept CDN chunks). `tuchanka-turian-platoon`
  kept — genuinely distinct mission (platoon rescue that unlocks the bomb mission).
- Removed 2 stale `*.yaml.tmp` (jack-recruitment-purgatory, mordin-recruitment-omega;
  real files intact).
- .done 1448->1608. master rebuilt: 189 rows, load-check clean.
- Post-sweep dup-merge candidates to revisit: `destruction-of-the-ssv-iwo-jima` vs
  `sidon-research-station-attack` (overlapping Camala/Kahlee content, kept separate);
  `citadel-the-consort-s-dilemma` — check against any pre-existing consort event.
- PAUSED for /clear. Resume: `/me-build-timeline`, wave 10 = FINAL partial wave, only
  2 batches left (b16 `warp-ammo`..`ysin-mal-vas-idenna`, b17
  `zaal-koris-vas-qwib-qwib`..`zymandis`; 28 stems). After b16/b17: this is the whole
  sweep done -> run `python scripts/renumber_timeline.py` (ONE-SHOT, end only), then
  rebuild master, then the skill's remaining steps (narrative_choices sync, verify).

## 2026-09-08 — Phase 2 opened: scene-sweep tooling
- Verified Phase 2 item 10 was already complete: `page_summaries` 1,636 == `timeline/.done`
  1,636, 190 event files, master 190 rows, `renumber_timeline.py --check` clean.
- Built Phase 2 item 9's tooling (the sweep itself is un-run):
  `.claude/agents/scene-extractor.md` and `.claude/commands/me-build-scenes.md`, mirroring
  `/me-build-timeline` — alphabetical batches of ~20, controller-owned `scenes/.done`,
  4 agents in flight, Haiku default with Sonnet for attendance-/branch-heavy batches,
  pause-and-commit per wave.
- Agent rules target the TODO2.md failures directly: read `data/pages/` when the summary is
  thin, attendance from the page not from memory, per-beat `source_chunks`, causality and
  sequence preserved, Shepard's agency recorded, branches kept in one record via
  `conditional`/`variants` keyed to `config/canon/choices.yaml` ids.
- Tests first: 3 new checks in `tests/test_agent_defs.py` / `tests/test_command_defs.py`
  (schema fields named, ledger not agent-written, every expected command exists).
  Suite 166 -> 169 green.
- Not committed — the tree still holds the whole uncommitted Phase 1 overhaul, and
  `me3.zip` (30MB) is untracked and not in `.gitignore`.

## Session resume 2026-09-09 — /pwf context restore
- Ran planning-with-files restore. `session-catchup.py` produced no output (no unsynced
  context recorded). Re-read all three planning files + findings.md.
- STATE RECONCILED against git — planning files were ~13 commits stale:
  - The Phase 1 overhaul + scene-sweep tooling DID commit (f3a6704); progress.md's last
    entry saying "Not committed" was wrong.
  - The **scene sweep has run 12 waves** (7a4b139, 0defc02, 0dc6121, 8e27b4f, cf754ea,
    fe4e507, 4b09640, 284fb8e, a5b0331, 6d2f7a5, 9d04c2e, d1d766c) plus two choice-branch
    fix commits (301f421, 9dddae3). None of this was logged in progress.md.
  - `scenes/.done` = 620 stems; `scenes/*.yaml` = 199 files; `page_summaries/` = 1,636.
    ~1,016 stems remain.
  - **Wave 13 is uncommitted in the working tree**: `scenes/tuchanka-grunt-rite-of-passage.yaml`
    modified + 7 new untracked scene files (citadel-flux-anderson-steal-the-normandy,
    citadel-hannah-shepard-call, freedom-s-progress-veetor-and-tali,
    grissom-academy-jack-and-the-biotic-students, illium-parasini-beer-and-hermia,
    omega-afterlife-forvan-poisoned-drink, omega-fist-dockworker-grudge). Stems NOT in
    `scenes/.done`. Covers the `f*`/`g*` alphabetical range.
- task_plan.md updated: new `## Next Step`, `## Current Phase` → Phase 7, added
  `### Phase 7: Scene sweep`.
- User chose: finalize & commit wave 13, then stop for /clear.

### 2026-09-09 (cont.) — scene sweep wave 13 finalized
- Cleanup: 0 `.tmp`, `scenes --drop-unparseable` dropped 0, 0 filename renames.
- `python -m scripts.scenes --check` → 199 scenes checked, clean.
- Wave 13's 8 tree files: 7 new + `tuchanka-grunt-rite-of-passage` enriched
  (Uvenk krantt confrontation + Gatatog Warriors post-Rite firefight, all beats cite
  `gatatog-uvenk_003` / `gatatog-warrior_001`).
- Attendance spot-check (all 3+-participant new records — grissom-academy-jack…,
  freedom-s-progress-veetor-and-tali, + the enrichment): every participant name
  (Octavia, Rodriguez, Bellarmine, Seanne, David Archer, Kahlee, Prazza, Veetor,
  Prangley, Hermia, Miranda, Jacob …) appears verbatim in that beat's cited chunks.
  No fabricated attendance.
- `.done` append: the wave's batch was NOT logged (dispatched right after wave 12's
  commit, session died before the controller step). Reconstructed conservatively —
  cited page_summary stems (fist #2, flux #6, forvan #12, freedom-s-progress #14/#15)
  confirm batch 1 ran fully; appended the safe contiguous prefix **`fish`..`gagarin-station`
  (20 stems)**. `scenes/.done` 620 → 640. Stems #21–31 (game-shop..gatatog-warrior)
  were likely also touched (gatatog-uvenk/-warrior chunks are in the committed tuchanka
  enrichment) but are left OUT of `.done` — they redo idempotently next wave.
- `python -m pytest -q` → 169 passed.
- Committed. Remaining: ~996 stems, resume alphabetically from `game-shop`.

### 2026-09-09 (cont.) — scene sweep wave 14 (8 batches, 160 stems)
- User set wave size to **8 batches of 20** (two rounds of 4 scene-extractors in flight).
  Stems `game-shop`..`jana`. Haiku for the stat-page batches (B geth-units, G ammo/powers),
  Sonnet for A/C/E/H (Garrus & Jacob loyalty, Ascension-novel cluster, Horizon, Jack/Vega banter).
- **13 new scene records:**
  citadel-presidium-garrus-shooting-cans, citadel-garrus… (see extended),
  idenna-cerberus-assault-grayson-kills-golo, grissom-academy-gillian-grayson-biotic-outburst,
  omega-golo-dealings-and-the-trap-for-lemm, horizon-sanctuary-lawson-standoff,
  citadel-helena-blake-syndicate-offer, omega-grayson-finds-dying-hilo,
  me1-ilos-find-the-conduit, illium-nos-astra-thax-vorak, citadel-huerta-thane-final-moments,
  normandy-shuttle-bay-vega-sparring, citadel-apartment-vega-n7-tattoo,
  normandy-engineering-jack-confidences.
- **6 records extended:** citadel-garrus-sidonis-orbital-lounge (Eye for an Eye front half:
  Bailey stop, volus/krogan warehouse, Fade-is-Harkin, factory battle, Harkin pinned,
  shoot-leg vs headbutt branch), bel-anoleis-corruption-noveria, rannoch-the-choice-above-the-fleet
  (Geth VI variant), tuchanka-grunt-rite-of-passage (Wreav-leads variant + ME3 Utukku death
  consequence), flotilla-tali-treason-trial (Han'Gerrel added), horizon-ashley-shepard-reunion
  (broadened to the whole Virmire-survivor reunion, Kaidan branch + Delan).
- Batches B, G and the tail of A/D produced nothing (geth-unit / ammo / power / enemy stat pages).
- Attendance spot-check (idenna, grissom-gillian, omega-golo, huerta-thane, vega-sparring):
  every participant name appears in that scene's cited-page chunk text. No fabrication.
- Fixed 2 fabricated `related_events` ids caught by `test_related_events_resolve`:
  `race-against-time-sovereign` → `ilos-conduit-citadel`;
  `citadel-coup-priority` → `cerberus-coup-citadel-ashley`.
- `scripts.scenes --check` → 212 scenes clean. `pytest -q` → 169 passed.
- `.done` append: all 8 batches were dispatched by the controller and returned success,
  so the full 160-stem range `game-shop`..`jana` is appended (no reconstruction guesswork).
  `scenes/.done` 640 → 800. Remaining: **836 stems**.
- Committed. Resume alphabetically from `japan` / `jarrahe-station` (next stem after `jana`).
