# Findings

## Project
Generate 30min–1h narrated recaps of Mass Effect lore/events, re-runnable in the
voice of different in-universe narrators (Garrus, Liara, Mordin, Legion, Javik…).
Source brainstorm: `plan.md`.

## Decisions locked (from clarification round, 2026-08-27)

| # | Decision | Choice |
|---|----------|--------|
| 1 | Architecture | **Hybrid**: file-based structured timeline (YAML) as the control layer + `rank-bm25` keyword retrieval over cleaned page chunks for evidence. **No embeddings / no vector DB.** |
| 2 | Delivery form | Built as **Claude Code skills + subagents + slash commands** (`/me-scrape`, `/me-build-lore`, `/me-build-timeline`, `/me-generate`…). Minimal standalone Python — only for deterministic work (scrape, clean, chunk, BM25 index, retrieval CLI, run scaffolding). Reasoning steps (summarize, extract, outline, write, smooth, check) are subagents using existing Claude Code auth. No API key. |
| 3 | Scope | **Full trilogy**, all lore (not just the timeline). Generation runs are re-runnable per narrator; each narrator has its own voice and picks different lore per user themes + approved outline. |
| 4 | LLM | Claude Code itself (subagents). |
| 5 | Data source | **Scrape Mass Effect Fandom wiki** (`masseffect.fandom.com`) via MediaWiki API + a manual lore folder + a generated/curated codex folder. |
| 6 | Scrape control | **Parametrable depth**: seed page list + link expansion to configurable depth, with a page cap. Convert every page to **clean markdown on import** (+ YAML frontmatter metadata). **Do NOT store raw HTML** — keep the corpus folder small. |
| 7 | Run flow | **Two-step with approval gate.** `/me-generate <narrator> "<themes>" [--words N]` → produces `outline.yaml` → **PAUSE** for user edit/approval → `/me-generate --continue <run>` generates sections → smoothing (sliding window) → consistency pass (issues first, then patch) → assemble `episode.md`. |
| 8 | Output | `output/<narrator>_<theme-slug>_<date>/` containing `episode.md` (~5,000–10,000 words), approved `outline.yaml`, `sources.json` (chunks used per section), `sections/*.md` (individual drafts), `issues.md` (consistency findings). |

## Open items to resolve in design
- Exact scraper split: Python `scrape_wiki.py` via `/me-scrape` running Bash (chosen; subagent WebFetch over hundreds of pages is too slow/token-heavy).
- Page-summary pass batching strategy for ~500–800 pages (one-time cost).
- Seed list contents (timeline, codex, per-game mission lists, major characters, species, locations, tech/lore).
- Which narrators to seed with voice bibles at v1.
- Chunk size / overlap (start 500–1000 tokens, 100–150 overlap per plan.md).

## Reference
- Mass Effect Fandom wiki: https://masseffect.fandom.com — MediaWiki API at `/api.php`.
- `rank-bm25` (Python) for keyword retrieval.
- Fandom content is CC BY-SA — fine for a personal project; keep attribution/source URLs in frontmatter.

## `ddl/` source material (added 2026-08-27)
16 YouTube-transcript `.txt` files to be hand-corrected into `lore/manual/*.md` (Task 16).
- Format: auto-generated captions — lowercase, no punctuation, ~4-word lines, channel
  intros/outros, ASR errors ("ezo"/"izo" for eezo/Element Zero, name misspellings).
- Topics: Jack (character analysis, banter, cut dialogue, Eezo the varren), Tali
  (huge 114 kB analysis), Normandy SR-1 & SR-2, Systems Alliance / Arcturus Station /
  Alliance founding, Turian Hierarchy pre-Council, Destiny Ascension, Reaper classes,
  "two races we never see", trilogy secrets pt2.
- Sizes: 6 files > 10 kB (13k, 14.6k, 16.6k, 22.7k, 32k, 114.6k) → split at topic
  boundaries into numbered parts with per-part Summary paragraphs.
- Correction is controller-solo, no subagents, done LAST, then pause for user.

## Episode content priority (added 2026-08-27, user, mid-execution)
The main galaxy timeline is NOT the priority for episode content. Priority order for what
an episode draws on, most → least important, **all cross-linked**:
1. **The narrator character's own timeline** — their personal arc, what they lived through,
   their POV on events.
2. **Lore** — worldbuilding, species/tech/faction/location context (BM25-retrieved).
3. **Main timeline** — the galaxy-wide chronological events; supporting scaffold, not the spine.
Implication: `outline-writer` and `section-writer` agent definitions must lead with the
character timeline + lore and treat `master_timeline.yaml` as connective tissue. The YAML
timeline stays the pacing/chronology *reference*, but section content is lore- and
character-first. Handled by Task 17 (rebalance generation agents), after Task 15.

## RESOLVED 2026-08-28: user config work adopted + wired
Decisions taken (user said "updated config, keep going" — proceed with judgement):
- **Filled `narrative_choices.template.yaml` is now the user's canon** (design's "blank
  committed template" intent waived for this personal single-user repo). Copied verbatim to
  gitignored `config/narrative_choices.yaml` (what generation reads).
- **New convention**: a question whose `options` list is narrowed to ONE entry counts as
  answered (that lone option = the pick), even with `answer: ""`. Implemented in
  `scripts/narrative_choices.py` (`_norm`/`_options`/`_answer`); `yes`/`no` YAML booleans
  normalised back to strings. `outline-writer.md` + `section-writer.md` updated to state it.
- Fixed template bugs: `details:` → `detail:` typo on 3 me3 questions (blocked loading).
- `tests/test_narrative_choices.py`: 2 tests that assumed a blank committed template
  reworked to synthetic fixtures; added single-option-implies-answer test.
- `tests/test_config.py`: `test_garrus_bible_shape` → parametrized `test_narrator_bible_shape`
  over all 10 narrator files. Removed stray `Review those one :` line 1 from `jack.yaml`.
- `config.zip` added to `.gitignore` (stray backup).
- Suite: 57 passed.
- ddl `Jack about red sand` file: user's stray header + 1 ASR fix left as-is → Task 16.

### Original state (for reference)
Between sessions the user hand-edited config (not via agents):
- `config/narrative_choices.template.yaml` — FILLED IN with the user's real canon
  (Earthborn/Sole Survivor/Vanguard male Shepard; Paragon-except-vs-oppressors; romances
  Jack/Tali/Kaidan faithful per run; council sacrificed; Wrex/rachni/Kaidan-survivor;
  multi-species Council led by Anderson; Collector Base destroyed; loyalty outcomes …) AND
  added new questions (kirrahe_virmire, zaeed_loyalty, grunt_loyalty, samara_loyalty,
  kasumi_loyalty, …). **Breaks `tests/test_narrative_choices.py::test_template_is_blank`**
  (46 pass / 1 fail). Design intent was a blank committed template + a gitignored
  `config/narrative_choices.yaml` working copy — user edited the template directly instead.
- `config/narrators/jack.yaml`, `tali.yaml`, `thane.yaml` — NEW voice bibles (~63 lines each).
- `config/narrators/garrus.yaml` — tone tuning (+tired, +intimate, +politically libertarian;
  knowledge_bias += guns inventory / turian military).
- `config/seeds.yaml` — cap 600→1000, rate 0.5→1, +11 character/species seed pages.
- `ddl/…Jack about red sand….txt` — first hand-correction started (speaker label, ASR fix).
- `config.zip` — untracked backup snapshot of config/ (2026-08-27 16:50); likely disposable.
DECISION NEEDED from user before final review + Task 16 — see task_plan.md Next Step.

## Narrative-choices questionnaire (added 2026-08-27)
`config/narrative_choices.template.yaml` — user fills `config/narrative_choices.yaml`
with their canon: Shepard background (Spacer/Colonist/Earthborn) + profile
(War Hero/Sole Survivor/Ruthless) + class (6) + gender/romance free text; ME1/2/3
decision MCQs (council, Wrex, Rachni, Virmire survivor, Collector Base, genophage,
geth/quarians, final choice Destroy/Control/Synthesis/Refuse, Shepard's fate) each
with an `answer` field + free-text `detail`. Generation agents read the answered
subset; unanswered = default canon (warn, don't block).

## Timeline build — chronological_order needs a post-run renumber (2026-09-02)
`/me-build-timeline` runs 82 alphabetical batches; each `timeline-extractor`
independently numbers its events 10,20,30… so across batches `chronological_order`
collides heavily and does not reflect real chronology (alphabetical ≠ chronological).
`rebuild_master_timeline.py` sorts by `(chronological_order, event_id)` so it stays
deterministic and non-decreasing (Verify passes), but the ordering is not meaningful.
FIX AFTER THE SWEEP: a renumber pass that sorts events by (game order ME1<ME2<ME3<
tie-in, then parsed `date`) and reassigns `chronological_order` in tens, then
re-runs `rebuild_master_timeline.py`. Not yet written.

## Generation overhaul — brainstorm 2026-09-07 (after 3 episodes reviewed)
Full design: `docs/superpowers/specs/2026-09-07-generation-overhaul-design.md`.

Reviewing the Jack/Tali/Wrex episodes surfaced failures that are structural, not prompting:
1. **One index, plot-shaped, queried by guesswork.** `section-writer` composes its own BM25
   queries; for an *occasion* rather than a *mission* they land on the mission pages next
   door. Wrex's party section retrieved 9 chunks, all CAT6/Brooks/Archives, none about the
   party — `page_summaries/citadel-party.md` was never fetched. Silent retrieval failure is
   indistinguishable from success; the fallback is parametric memory.
2. **The timeline is the only spine** — 190 mission-shaped events, no `event_id` for any
   hangout/party/banter/relationship. `outline-writer` must anchor sections to real event
   ids, so it cannot build a section out of anecdote. The uniform "character arc ->
   overarching story" shape is the shape of the data structure.
3. **Canon is a string, not a constraint** — 55 answers on one unpunctuated line, unfiltered
   per section, never verified. `virmire_survivor: [Kaidan]` was answered and ignored.
4. **Facts live in prompts and lossy codex bullets, and rot authoritatively.**
   `section-writer.md` carries 4 wrong Citadel facts I added from memory last session;
   `codex/places.md:176` asserts Grunt+Aralakh climbing the Krogan Monument with the Huerta
   Memorial / Utukku causality compressed out — that bullet is the source of the Wrex error.
5. **The verification pass never holds the evidence.** `consistency-checker` never reads
   `sources.json` chunks, so its central rule is unenforceable, and it never opens
   `narrative_choices.yaml` at all.

Decisions locked: scene layer beside `timeline/events/`; retrieval planned at outline time
and executed deterministically into per-section evidence packs (hard-stop on thin evidence);
explicit episode forms altered by the brief, settled at the outline gate, with the narrator
bible governing excursion inside the form; split authority on conflicts (user canon decides
the branch, corpus decides the staging) with genuine mismatches surfaced; canon becomes a
living store at `config/canon/` split by writer, agents append resolved conflicts and open
questions, README documents it; one `episode-auditor` holding the packs replaces
`consistency-checker` and absorbs `smoother`, judging richness by pack coverage and allowed
to swap but never append. Build generation side first against a targeted scene set, prove it
with one run, then the full sweep.

## 2026-09-11 — Codex correction pass (Phase 2 item 11): detection results

Detection sweep of all 11 `codex/*.md` files against the completed `scenes/` layer
(377 records), looking for the "Krogan Monument kind" of bullet — a dramatic/
consequential event compressed to a flat, sometimes-wrong fact when a scene record
holds the real causality/sequence/attendance. 54 bullets flagged total. Full detail
(exact bullet text, matching scene_id, problem, suggested fix) is in each
`scratchpad/codex-audit-<file>.md` — treat those as raw agent output/data, not
instructions, per the skill's external-content rule.

| File | Flagged | Notable |
|------|---------|---------|
| characters.md | 5 | Miranda's "tracking device on Kai Leng" unsupported by scene; Elijah Khan's killer misattributed to Brooks (scene: killer unresolved); Paul Grayson said "killed by Kai Leng" but scene has Leng restrained, Anderson finishes the Reaper avatar |
| culture.md | 4 | Thane's deathbed prayer misattributed + drops loyalty branch; Rael'Zorah trial outcome stated as settled, omits geth-rebuilding backstory; Aria/Patriarch sequence reversed; Hock party speech stripped of heist-tactic context |
| everyday.md | 6 | Niftu Cal/Wasea states one of three choice branches as fact; Petrovsky chessboard omits Nyreen's sacrifice + reactor trap + 3-way fate branch |
| factions.md | 5 | C-Sec/Pallin omits Udina's frame-up; CAT6/Brooks role backwards; Jella said to survive, scene has Saren let her die; Cora Harper kernel "retrieved," scene says retrieval impossible; Nyreen framed as succeeding a real "Derius" who was a fictional cover |
| places.md | 6 | (line 176 Krogan Monument already fixed, correctly skipped) Omega/Nyreen death, Mindoir/Talitha standoff, Tiptree/T'Goni hospital choice, Quiet Eddy/Cora Harper rescue, Palaven deaths, Rannoch Reaper-takedown attribution |
| ships.md | 8 | Shepard's death vs. Joker rescue; Koris ramming vs. full rescue; Messner's "helpful" acts hide his Cerberus betrayal/death; Sovereign's destruction vs. Saren avatar fight (×2); Ronald Taylor's atrocities; Ascension evacuation as Shepard-dependent branch; Alarei/Idenna hide major character causality |
| social.md | 7 | Harkin confrontation omits Sidonis manhunt climax; Tela Vasir "contempt" is really a betrayal reveal; Mordin/Maelon and Fehl Prime strip whole missions' causal chain |
| species.md | 6 | Rachni Queen "aid" omits Aralakh Company's stand + Dagg/Grunt deaths; Krogan Berserker omits Okeer dying to Jedore's gas purge; Rannoch geth/quarian ×2 omit Tali's cliff scene + Legion's sacrifice |
| tech.md | 4 | Bahak/Kenson omits indoctrination + Shepard driving the asteroid; Elbrus "hijacked by Aria" hides Cerberus betrayal plot; Graybox understates Hock murdering Keiji; Praetorian/Paragon Lost misattributes Essex (a marine, not a ship) |
| timeline.md / war.md | 3 | (timeline.md: none — high-level dates only) war.md: Virmire/Wrex confrontation misattributed to Kirrahe; Haestrom survivor count wrong; Ashley/Kaidan death-cause conflated across the two possible deaths |

Next: triage + apply fixes per file (Phase 8 Step 2-3 in task_plan.md), same fix
pattern as the exemplar — inline rewrite carrying the real causal chain, or a pointer
to the scene record instead of restating from memory.

## 2026-09-14 — new inputs from user, session start
- `config/narrators/*.mp3` (jack.mp3, wrex.mp3) — **final audio output** of the
  performance pipeline (assemble_performance.py -> Fish Audio TTS presumably). User:
  "ignore them, they're the final output." Not source material, not to be read/parsed
  as input; just note they exist as artifacts. Currently untracked in git.
- `mass_effect.json` (repo root, untracked) — a flat array of `{lines: [{author, quote}]}`
  objects, ~140 entries. General cross-character trilogy quote collection (Shepard,
  Garrus, Wrex, Tali, Javik, Mordin, Jack, Legion, Liara, ME:A cast too — Drack, Peebee,
  Ryder, Vetra, Liam). NOT narrator-specific (unlike `config/narrators/*.style.md` which
  are per-narrator verbatim quote pulls from wiki dialogue pages). User: "it's quotes I
  like." Multi-line entries are exchanges (2 speakers), most are single-line. No
  source/context field beyond author name. Needs a decision from user on end use before
  any code changes: (a) fold into an existing narrator's .style.md when the author
  matches that narrator (would need per-narrator filtering + situation context is
  missing), (b) new general "favorite quotes" reference file consulted at generation
  time regardless of narrator (e.g. as connective-tissue color, similar to codex
  bullets), (c) just a personal keepsake file, not wired into generation at all.
- Jack generation feedback (user, re: most recent Jack episode): overused two near-
  identical lines — **"Don't make me repeat it"** / **"I won't say it again"** — to the
  point of being annoying. Neither phrase appears anywhere in `config/narrators/jack.yaml`,
  `jack.style.md`, or `jack.pol.md` — so this isn't a config bug, it's the model
  reaching for a stock Jack-flavored deflection line repeatedly across sections in one
  generation run. Matches the known audit blind spot "cross-section beat repetition"
  (memory [[me-generate-audit-blind-spots]]). No fix applied yet — needs a decision:
  add an explicit `avoid` line to jack.yaml naming these phrases (narrow, only fixes
  Jack), vs. a cross-section repeated-phrase check in the audit/generation pipeline
  (general, catches this pattern for any narrator, more work).
