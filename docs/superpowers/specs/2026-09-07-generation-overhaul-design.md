# me-gen generation overhaul — design

Date: 2026-09-07
Status: design approved in brainstorm; awaiting spec review
Supersedes: the retrieval and verification halves of `plan.md`

## Why

Three episodes have been generated (Jack, Tali, Wrex). Reviewing them surfaced a class of
failure that is not a prompting problem and cannot be fixed by more rules:

- Canon branches recorded in `narrative_choices.yaml` were ignored (Ashley narrated alive
  when `virmire_survivor: [Kaidan]` is answered).
- Occasions with no timeline event were written from parametric memory (the Citadel DLC
  party section retrieved nine chunks, all about the CAT6 conspiracy, none about the party).
- The narrator repeatedly erased Shepard's agency, narrating in third person to Shepard's face.
- Every episode came out the same shape: chronological personal arc, trilogy-wide.
- Guardrails and codex bullets asserted wrong facts authoritatively.

### Root causes

1. **One index, plot-shaped, queried by guesswork.** `section-writer` composes its own BM25
   query strings. When a section is about an *occasion* rather than a *mission*, those queries
   land on the mission pages next door. Silent retrieval failure is indistinguishable from
   success, and the fallback is the model's own memory of Mass Effect — which is where
   wrong-but-plausible facts live.
2. **The timeline is the only spine.** 190 event files over 1,636 page summaries, all
   mission-shaped. No `event_id` exists for a hangout, a party, a banter beat, or a crew
   relationship. `outline-writer` must anchor every section to a real event id, so it
   *structurally cannot* build a section out of anecdote. The uniform episode shape is the
   shape of the data structure, not a stylistic habit.
3. **Canon is a string, not a constraint.** `narrative_choices.py` emits 55 answers as one
   unpunctuated line. Nothing filters it per section, nothing reconciles a user's shorthand
   against the corpus, and no verification pass ever opens the file.
4. **Facts live in prompts and in lossy codex bullets.** `section-writer.md` is 182 lines and
   contains four wrong Citadel facts, added in good faith from memory. `codex/places.md:176`
   asserts "a drunken Grunt and Aralakh Company climbed [the Krogan Monument] in 2186" with
   the hospital, Utukku and the rope-out-the-window causality compressed out — and a codex
   bullet carries the same authority as a sourced chunk with none of the traceability.
5. **The verification pass never holds the evidence.** `consistency-checker` reads sections,
   the master timeline and the narrator bible. Its own rule — "invented lore = any claim not
   supported by that section's `sources.json` chunks" — is unenforceable, because it never
   reads the chunks.

## Decisions taken (brainstorm, 2026-09-07)

| # | Decision |
|---|---|
| 1 | Add a **scene layer** beside `timeline/events/`, derived from the corpus by the same resumable sweep machinery. Full sweep, but phased (see Phasing). |
| 2 | **Fix retrieval too** — the scene layer alone would leave `page_summaries/citadel-party.md` still unfound. |
| 3 | Episodes get **explicit forms**, a reference set altered by the brief and settled at the outline gate. |
| 4 | The **narrator bible governs excursion within the form** — how far and how often they stray, and how they return. Form is the skeleton; the bible is the gait. |
| 5 | **Split authority on conflicts.** User canon is authoritative for *which branch happened*; the corpus is authoritative for *staging*. Genuine mismatches are surfaced, not silently reconciled. |
| 6 | Canon becomes a **living store that agents write to** — resolved conflicts logged, unanswered lore questions appended for the user to answer. |
| 7 | Canon store laid out as `config/canon/`, **split by who writes each file**, merged by a resolver into the single view agents consume. Documented in the README. |
| 8 | Retrieval is **planned at outline time and executed deterministically** into per-section evidence packs. The writer composes no queries. |
| 9 | A **pack-coverage audit** replaces `consistency-checker`, absorbing `smoother`. It judges richness against the pack as a denominator, and may only swap, never append. |
| 10 | Build the **generation side first** against a targeted scene set; the full sweep follows once the schema is proven by a working run. |

## Architecture

```
config/canon/          user + agent canon store  ──┐
config/forms.yaml      episode form reference       │
timeline/events/       mission spine  ──────────────┤
scenes/                occasion spine  ─────────────┼──> build_pack.py ──> output/<run>/packs/<id>.json
page_summaries/        prose summaries  ────────────┤                              │
codex/                 world texture  ──────────────┤                              v
data/bm25_index.pkl    kind-tagged chunk index  ────┘                       section-writer
                                                                                   │
                                                                                   v
                                                                          episode-auditor ──> tone-marker ──> assemble
```

Pipeline after this change:

```
/me-generate            outline-writer  → outline.yaml (form, scenes, retrieval keys, promises)
                        [USER GATE]
/me-generate --continue build_pack.py   → packs/*.json      (deterministic, hard-stops on thin evidence)
                        section-writer  → sections/*.md     (first section only, then voice gate)
                        [VOICE GATE]
                        section-writer  → remaining sections
                        episode-auditor → issues.md + patched sections
                        tone-marker     → sections/*.performance.md
                        assemble_episode.py + assemble_performance.py
```

---

## 1. Canon store — `config/canon/`

Split by writer, so the file the user lives in is never machine-rewritten (YAML round-trip
writes destroy comments and reflow hand-formatted files).

### `choices.yaml` — user-owned, agents never write

The existing `narrative_choices.yaml`, migrated unchanged in content. Keeps the
single-narrowed-option-implies-answered convention already implemented in
`scripts/narrative_choices.py`.

### `overrides.yaml` — authoritative over the corpus

The category where the user's memory beats the wiki, *because it is explicitly marked so*.
This is what distinguishes a deliberate divergence from shorthand accidentally promoted
into staging.

```yaml
overrides:
  - id: shepard-born-on-the-normandy
    kind: au                      # au | correction
    scope: [Shepard]              # entities, scene ids or event ids this governs
    statement: >
      Shepard was born aboard a ship called the Normandy, parentless, ran with a gang
      as a child and had a drug problem before Anderson pulled him into N7.
    overrides: "Earthborn background as the wiki describes it"
    added: 2026-09-07
  - id: aralakh-company-died-at-utukku
    kind: correction
    scope: [Grunt, Aralakh Company, citadel-grunt-csec]
    statement: >
      Aralakh Company was wiped out holding the tunnel at Utukku. Grunt survived alone and
      was recovering in Huerta Memorial during shore leave. Any source showing the company
      alive on the Citadel is wrong for this playthrough.
    overrides: "codex/places.md Krogan Monument bullet; Citadel DLC 'his men' framing"
    added: 2026-09-07
```

`kind: au` — deliberate divergence from canon. `kind: correction` — the corpus is wrong or
incomplete and the user is fixing it. Both beat evidence; the distinction is for the user's
own bookkeeping and for how the auditor phrases a conflict.

### `questions.yaml` — agent-appended inbox

Where an agent raises something it could not resolve. The user answers in place; answered
entries become part of the resolved canon on the next run.

```yaml
questions:
  - id: q-2026-09-07-001
    raised_by: wrex_.../one-last-party-on-the-citadel
    question: Did Wrex attend the Armax Arsenal Arena with Shepard, or only hear about it?
    context: >
      scenes/citadel-armax-arena.yaml lists Wrex as an available ally but the party scene
      does not place him there. choices.yaml citadel_dlc says "Did all the missions".
    options: [attended, heard about it, did not come up]
    answer: ""
    status: open
```

### `resolved.yaml` — agent-appended audit log

Conflicts settled silently under split authority, so the user can review what was decided
on their behalf rather than discovering it in the prose.

```yaml
resolved:
  - id: r-2026-09-07-001
    run: wrex_...
    section: one-last-party-on-the-citadel
    config_said: "I let Garrus win the sniper contest"
    evidence_said: >
      scenes/citadel-garrus-presidium.yaml — skycar to the top of the Presidium, beverage
      cans, sniper rifles, deliberate miss on the second shot.
    resolution: >
      Outcome taken from config (Garrus won, Shepard threw it); staging taken from the
      scene record. "Arcade" was never asserted by the user and is not written.
    date: 2026-09-07
```

### `scripts/canon.py` — the resolver

Replaces `scripts/narrative_choices.py` (which is kept as an internal loader for
`choices.yaml`). Merges all four files into one structured view.

- `python scripts/canon.py` — human-readable summary, grouped by game, one line per answer.
  Not the 55-item wall: structured, with `authority` marked on override-backed entries.
- `python scripts/canon.py --json` — machine view, keyed by id.
- `python scripts/canon.py --for '<entity>,<entity>,...' --json` — the subset relevant to a
  section's entities. **This is what goes into an evidence pack**, so a section carries the
  five canon facts that bear on it rather than all fifty-five.
- `python scripts/canon.py --ask <yaml-fragment>` — append a question to `questions.yaml`.
- `python scripts/canon.py --log-resolution <yaml-fragment>` — append to `resolved.yaml`.

Open questions and unanswered choices **warn, never block** — unchanged from today.

### Migration

`config/narrative_choices.yaml` moves to `config/canon/choices.yaml`. A shim in
`scripts/narrative_choices.py` keeps the old path working for one release and prints a
deprecation line, so an interrupted migration cannot break a run mid-flight.

---

## 2. Scene layer — `scenes/`

An **occasion**: a bounded thing that happened, with people in a room. Where
`timeline/events/` answers *what happened to the galaxy*, `scenes/` answers *what happened
between these people, and who was there to see it*.

### Schema — `scenes/<scene_id>.yaml`

```yaml
scene_id: citadel-garrus-presidium
title: Shooting Cans off the Presidium with Garrus
kind: hangout            # hangout | party | banter | downtime | ceremony | mission-aside | argument
game: Mass Effect 3
when: 2186, Citadel shore leave, after the clone conspiracy
where: top of the Presidium, reached by skycar from Docking Bay D24

participants: [Shepard, Garrus Vakarian]
private_to: [Shepard, Garrus Vakarian]     # ONLY these witnessed it
heard_by: [Normandy crew]                  # who could plausibly have heard afterwards

requires:                                  # canon conditions for this scene to exist
  - garrus_alive: true
  - citadel_dlc: any

beats:
  - text: >
      Garrus messages Shepard to meet at docking bay D24; they take a skycar to the top of
      the Presidium and shoot beverage cans with sniper rifles.
    source_chunks: [garrus-vakarian_014]
  - text: >
      If Shepard misses the second shot on purpose, Garrus declares "I'm Garrus Vakarian,
      and this is now my favorite spot on the Citadel."
    source_chunks: [garrus-vakarian_014]
    conditional: {let_garrus_win: true}
  - text: >
      If Shepard does not miss, Garrus jokes about adding rampaging klixen next time to
      separate the rookies from the pros.
    source_chunks: [garrus-vakarian_014]
    conditional: {let_garrus_win: false}

variants:
  - condition: {romance: Garrus}
    text: The same outing is played as a first date, ending in a tango on the casino floor.
    source_chunks: [garrus-vakarian_016]

related_scenes: [citadel-garrus-casino-wingman]
related_events: [citadel-dlc-archives]
source_chunks: [garrus-vakarian_014, garrus-vakarian_016]
```

The fields that kill our specific failures:

| Field | Failure it prevents |
|---|---|
| `participants` / `private_to` / `heard_by` | narrators witnessing scenes they weren't in — replaces the hand-typed Citadel rule in `section-writer.md`, which encoded four wrong facts |
| `requires` | scenes narrated in playthroughs where they can't have happened (Aralakh Company alive after Utukku) |
| `beats[].source_chunks` | per-beat traceability, so compression can't quietly drop causality the way the codex bullet did |
| `beats[].conditional` / `variants` | one occasion, several branches, only the canon-selected one narrated |

### Build — `/me-build-scenes` + `scene-extractor` subagent

Same shape as `/me-build-timeline`: alphabetical batches over `page_summaries/`, a
`scenes/.done` ledger, resumable, wave-based, Haiku by default and Sonnet for
attendance-heavy or branch-heavy batches (per the standing subagent-model policy).

Crucially, the extractor works from `page_summaries/` **and** the corresponding
`data/pages/` source when the summary is thin — the Grunt C-Sec detail exists in
`data/pages/grunt.md` and was compressed out of the codex. Scene beats cite chunk ids so
this is checkable.

---

## 3. Indices and the evidence pack

### Kind-tagged index

`scripts/build_bm25.py` gains a `kind` field on every chunk: `page` (existing raw-page
chunks), `summary` (one chunk per `page_summaries/*.md`), `scene` (one chunk per scene
beat, carrying `scene_id`). One index, three kinds — simpler than three indices and lets a
single query see all of them.

`scripts/retrieve.py` gains `--kind` (repeatable) and per-kind `k`, so a pack can demand,
say, 4 scene chunks, 4 summary chunks and 8 page chunks for a subject rather than 6 of
whatever scores highest — which is how the party section ended up with nine chunks about
mercenaries.

### `scripts/build_pack.py <run-dir> <section-id>`

Deterministic. Reads the approved `outline.yaml` and writes
`output/<run>/packs/<section-id>.json` plus a human-readable `.md` beside it.

```json
{
  "section": {"id": "...", "title": "...", "target_words": 700, "form": "evening"},
  "promises": ["Wrex's read on the Krogan Monument", "what the apartment drinks were"],
  "required_facts": [{"event_id": "...", "fact": "...", "actor": "Shepard"}],
  "canon": [{"id": "grunt_fate", "answer": "...", "authority": "choices"}],
  "scenes": [{"scene_id": "citadel-party-apartment", "...": "full record"}],
  "attendance": {"citadel-party-apartment": "witnessed",
                 "citadel-garrus-presidium": "heard"},
  "evidence": [{"chunk_id": "...", "kind": "summary", "text": "...", "for_key": "krogan monument"}],
  "codex": [{"file": "codex/culture.md", "line": 35, "text": "..."}],
  "conflicts": [{"config_said": "...", "evidence_said": "...", "resolution": "..."}],
  "warnings": ["thin subject: 'aralakh company' returned no scene or summary chunks"]
}
```

`attendance` is computed, not written by hand: the narrator's name against each scene's
`participants` / `private_to` / `heard_by`.

**Hard stop.** If a section names a scene id that does not exist, or a retrieval key that
returns nothing in any kind, `build_pack.py` exits non-zero and names the gap. The
generation phase refuses to run until the outline's keys are fixed or the user explicitly
waives with `--allow-thin`. This is the single change that would have prevented the party
section: an empty pack becomes a visible file and a failed exit, not silent improvisation.

**Conflict detection.** Where a canon entry and a scene record describe the same occasion:
shorthand resolves silently under split authority and is logged to `resolved.yaml`; a
genuine mismatch (an outcome the scene record cannot produce, or a flat contradiction) is
appended to `questions.yaml` and reported at the gate.

---

## 4. Episode forms — `config/forms.yaml`

A reference set, not a straitjacket. The brief alters the chosen form; the narrator bible
governs how far the narration strays inside it and how it returns.

```yaml
forms:
  - id: arc
    description: Chronological personal arc across the trilogy. The current default.
    spine: events
    section_count: [12, 20]
  - id: evening
    description: >
      One occasion, one night. Anecdote-driven, small-scale, digressive. Sections are
      subjects raised in conversation rather than chapters of a life.
    spine: scenes
    section_count: [8, 14]
  - id: one-relationship
    description: One other person, start to finish, through the narrator's eyes.
    spine: mixed
  - id: one-place
    description: A world, station or ship — its history, its people, what it did to them.
    spine: mixed
  - id: postmortem
    description: After the fact. What it cost, who is missing, what it was for.
    spine: events
  - id: argument
    description: A position the narrator is defending, evidence marshalled from their life.
    spine: mixed
```

`outline-writer` picks a form (or takes one named in the brief), records it in
`outline.yaml` as `form:` with a one-line `form_note:` explaining the choice, and shapes
sections accordingly. The user overrides it at the same gate where they already approve
section titles.

The mandate in `outline-writer.md` to "cover the narrator's personal arc start to finish
across the trilogy" becomes a property of the `arc` form rather than a universal rule.

### New `outline.yaml` shape

```yaml
# UNAPPROVED — edit, then delete this line
narrator: wrex
themes: [...]
brief: "..."
form: evening
form_note: "Brief puts them drinking on the eve of the battle; scenes, not chapters."
target_words: 9000
sections:
  - id: one-last-party-on-the-citadel
    title: One Last Party on the Citadel
    events: [citadel-dlc-archives]
    scenes: [citadel-party-apartment, citadel-grunt-csec-noodles]
    retrieval: ["krogan monument", "aralakh company utukku", "apartment cocktails"]
    promises:
      - "Wrex on what the Monument means to krogan"
      - "Grunt at the party, and why he was on the Citadel at all"
    target_words: 800
```

`promises` is what the section is *supposed* to carry. It is the denominator the auditor
checks coverage against, and it is editable by the user at the gate — which is where a
missing beat is cheap to add.

---

## 5. `section-writer` rewrite

**Reads:** the pack (one `Read`), the narrator `.yaml` and `.style.md`,
`docs/generation-example.md`. Nothing else. No Bash, no greps, no retrieval, no codex
walking, no event files. This is the token saving: one pack read replaces two retrieval
passes, four or five greps and a dozen file reads per section.

**Removed from `section-writer.md`:**
- the entire Inputs retrieval apparatus (both passes, the codex grep instructions)
- the hardcoded Citadel shore-leave rule — attendance now arrives as pack data with sources,
  and the rule as written contains four wrong facts
- branch-selection reasoning — the pack carries only the canon-selected branch
- the Bash-vs-Read admonitions, which exist only because the agent used to shell out

**Added:**
- **Agency transposition.** Required facts arrive as third-person prose from event
  summaries (`"Shepard leaned on Victus"`). The narrator must re-attribute every deed to
  the person who did it, and address the listener in second person where the listener is
  the one who did it. A narrator saying "Shepard's call alone" to Shepard's face is the
  `summary:` field leaking through unmodified, and it is a defect.
- **Vantage discipline from data.** Write `attendance: witnessed` scenes as seen,
  `heard` scenes as gossip/inference/teasing, and never claim presence at a scene marked
  `private_to` others.
- **Promises.** The section's `promises` are commitments, not suggestions.

**Kept:** integration-not-recitation against `generation-example.md`, `digressions` for
excursion and return, `signature`/`avoid`, length discipline.

Target: `section-writer.md` under 90 lines, down from 182. Rules that data now enforces
are deleted rather than restated — the Citadel rule is the proof that a fact in a prompt
rots authoritatively.

---

## 6. `episode-auditor` — replaces `consistency-checker` and `smoother`

One pass that holds the evidence packs, with the whole episode in view rather than a
sliding window. Find, then fix.

**Checks:**

| Check | Method |
|---|---|
| Grounding | every concrete claim traces to a pack item; flag the rest |
| Canon | every section against the resolved canon; branch violations |
| Vantage | witnessed claims against `attendance` |
| Agency | third-person references to the addressee; deeds attributed to nobody |
| Recitation | against `generation-example.md` — a sentence whose only job is to state a fact |
| **Coverage** | pack items used vs unused; `promises` kept vs dropped |
| Staging | contradicted physical state across a section boundary; repeated opening devices |
| Length | within 15% of target |

Coverage is the richness check, and the pack makes it arithmetic rather than opinion:

> `wrex/one-last-party`: 9 of 34 pack items used. Unused and relevant to this narrator's
> `digressions`: the apartment cocktail menu, Grunt vs. Wrex on the balcony, the Krogan
> Monument's meaning to Wrex. Promise "why Grunt was on the Citadel at all" — not kept.

**Fix pass constraints:**
- **Swaps, not appends.** Trade a thin or recited passage for a richer one within the
  section's word target. Unconstrained enrichment is a padding machine — a model asked
  whether prose could be richer always says yes, and always answers by adding.
- **Pack items only.** Anything it adds is already sourced. No new retrieval, no reaching.
- Runs **before** `tone-marker`, which hard-fails on any prose change after it.

Absorbing `smoother` is deliberate: the two continuity bugs found by hand (a section
ending mid-task while the next contradicts it; two consecutive sections opening with the
same "put it down, come here" device) are exactly `smoother`'s remit and it missed both,
because a sliding window cannot see a repeated device three sections apart.

---

## 7. Corrections to existing artifacts

Not optional, and not deferred — these are actively wrong on disk and will poison the next run:

- `.claude/agents/section-writer.md` — delete the Citadel shore-leave rule (states "Garrus
  at the sniping arcade", "Traynor at space chess", "Garrus's date on the Presidium").
- `codex/places.md:176` — the Krogan Monument bullet, corrected to carry the Huerta
  Memorial / Utukku causality, or a pointer to the scene record.
- The `citadel-dlc-scene-attendance` memory file — rewritten to describe the *mechanism*
  (attendance is data, read the scene record) rather than restating facts from memory.

## Phasing

**Phase 1 — generation side, proven by one run.**
1. `config/canon/` + `scripts/canon.py` + README section + migration shim.
2. `config/forms.yaml` + `outline-writer` rewrite (form, scenes, retrieval keys, promises).
3. Scene schema + a **targeted** set: the Citadel DLC first (the proven failure), then
   ship banter and crew relationships, loyalty-mission character moments, shore leave.
   Roughly 40–60 scenes, hand-checked against `data/pages/`.
4. Kind-tagged index + `build_pack.py` with hard-stop and conflict detection.
5. `section-writer` rewrite.
6. `episode-auditor`, absorbing `smoother`.
7. Corrections above.
8. **Test run**, `evening` form, end to end. — DONE 2026-09-08, user: "came out great".

**Phase 2 — fill the layer in behind a proven interface.**
9. `/me-build-scenes` full sweep over 1,636 summaries, wave-based and resumable.
   Tooling built 2026-09-08 (`.claude/commands/me-build-scenes.md` +
   `.claude/agents/scene-extractor.md`, 169 tests green); the sweep itself is
   un-run — 1,636 stems pending, `scenes/.done` not yet created.
10. ~~Finish the timeline sweep (2 batches) and run `renumber_timeline.py`~~ — DONE:
    page_summaries 1,636 == timeline/.done 1,636, 190 events, master 190 rows,
    `renumber_timeline.py --check` clean.
11. Codex correction pass for compressed-causality bullets of the Krogan Monument kind.

Sweeping now would mean discovering at generation time that scenes needed a field they
don't have, and re-sweeping 1,636 pages to add it.

## Risks

- **Front-loading the outline.** `outline-writer` gets heavier and the gate slower to
  produce. Accepted: the gate is where corrections are cheap.
- **Packs can't react mid-section.** A writer that discovers it needs something else is
  stuck. Accepted, and arguably a feature — "the writer went looking for something else"
  is how the arcade happened. Escape hatch: fix the outline keys and rebuild the pack.
- **Scene extraction inherits summarizer compression.** The very failure mode that produced
  the bad codex bullet. Mitigated by per-beat `source_chunks` and by extracting from
  `data/pages/` when the summary is thin — but it is the main quality risk in Phase 2.
- **The auditor is now load-bearing.** Merging three passes into one means a bug there has
  wider blast radius. Mitigated by its find-pass writing `issues.md` before it fixes
  anything, which is already the existing two-pass shape.
