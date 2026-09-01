# Mass Effect Narrator

Generate 30-minute-to-1-hour narrated recaps of the Mass Effect trilogy in the
voice of an in-universe narrator (Garrus, Liara, Mordin, …).

## Setup

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m pytest        # all green
```

## Workflow (run inside Claude Code)

| Step | Command | Produces |
|------|---------|----------|
| 1. Scrape lore | `/me-scrape` (opt. `--depth 2 --cap 600 --rate 0.5`) | `data/pages/`, `data/chunks/chunks.jsonl`, `data/bm25_index.pkl` |
| 2. Summarize | `/me-build-lore` | `page_summaries/`, `codex/` |
| 3. Timeline | `/me-build-timeline` | `timeline/events/*.yaml`, `timeline/master_timeline.yaml` |
| 3b. Canon questionnaire | edit `config/narrative_choices.yaml` — Shepard build, ME1/2/3 decisions | — |
| 4a. Outline | `/me-generate garrus "the cost of war, loyalty" --words 8000` | `output/<run>/outline.yaml` (**stops for approval**) |
| 4b. Approve | edit `outline.yaml`, delete the `# UNAPPROVED` first line | — |
| 4c. Write | `/me-generate --continue output/<run>` | `output/<run>/episode.md` (+ `sections/`, `sources.json`, `issues.md`) |

Hand-written lore goes in `lore/manual/*.md` with the same frontmatter as
`data/pages/` files; it is picked up by step 2. YouTube-transcript lore in `ddl/`
is converted to `lore/manual/*.md` by Task 16 of the build.

## Configuration

- **`config/seeds.yaml`:** Scrape seed URLs and crawl parameters (`depth`, `cap`, `rate`)
- **`config/narrators/<name>.yaml`:** Voice bibles for each narrator (tone, diction, signature phrases, knowledge biases)
- **`config/narrative_choices.yaml`:** Structured questionnaire holding the player's canon
  - Questions cover Shepard build (background, psych profile, class, gender, romance)
    and trilogy story decisions (ME1, ME2, ME3 — choice points with free-text `detail`)
  - A question counts as answered when `answer` is set **or** its `options` list is
    narrowed to a single value
  - Generation agents read the *answered* subset only; unanswered questions default to canon (with warnings, not errors)

## Adding a narrator

Copy `config/narrators/garrus.yaml` to `config/narrators/<name>.yaml` and rewrite
`tone`, `diction`, `signature`, `avoid`, and `knowledge_bias`. No code change.

## How it works

`docs/superpowers/specs/2026-08-27-mass-effect-narrator-design.md` has the full
design. Short version: the YAML timeline controls pacing and chronology, the
narrative-choices file pins the user's canon, BM25 retrieval supplies grounding
detail per section, and the narrator bible supplies style. Deterministic steps
are Python scripts in `scripts/`; reasoning steps are Claude Code subagents in
`.claude/agents/`.

### Where each piece fits, build time vs. generation time

The pipeline has a **build phase** (run once against the scraped corpus,
produces reusable artifacts) and a **generation phase** (run per episode,
consumes those artifacts). Nothing in the generation phase re-reads the raw
scraped pages — everything a narrator agent sees was distilled during the
build phase.

**Build phase** (`/me-scrape` → `/me-build-lore` → `/me-build-timeline`):

| Artifact | Built by | What it is | Consumed by |
|---|---|---|---|
| `data/pages/*.md` | `/me-scrape` | Raw cleaned wiki pages, one per topic | `page-summarizer` only — nothing downstream reads these directly |
| `data/bm25_index.pkl` | `/me-scrape` (via `scripts/build_bm25.py`) | Search index over chunked `data/pages/` + `lore/manual/` text | `scripts/retrieve.py`, called by `section-writer` for per-section grounding chunks |
| `page_summaries/<slug>.md` | `page-summarizer` (via `/me-build-lore`) | 200–500 word factual prose summary of one page | `outline-writer` (background/lore reading); not read section-by-section — it's outline-time context |
| `codex/{characters,factions,places,species,tech,ships,war,timeline,culture,social,everyday}.md` | `page-summarizer`, appending bullets as it summarizes | Deduplicated one-line facts, grouped by subject, each tagged `(source: <page title>)` | `outline-writer` (which lore to prioritize) **and** `section-writer` (culture/social/everyday are grepped live per section as world-texture grounding — see the Rules in `.claude/agents/section-writer.md`) |
| `timeline/events/<event_id>.yaml` + `timeline/master_timeline.yaml` | `timeline-extractor` (via `/me-build-timeline`) | Deduplicated, chronologically ordered events, each with `characters`, `summary`, `consequences`, and source chunk ids | `outline-writer` (picks which events become sections) **and** `section-writer` (each section's required facts) |

**Config, hand-authored, read at generation time only:**

| File | What it is | Read by |
|---|---|---|
| `config/narrators/<name>.yaml` | The voice bible: `tone`, `diction`, `avoid`, `signature`, `knowledge_bias` | `outline-writer` (pacing/weighting) and `section-writer` (prose voice) |
| `config/narrators/<name>.style.md` | Optional: real verbatim quotes with context + a "how they talk" note, built once per narrator by `narrator-style-extractor` | `section-writer` (cadence/word choice reference; the `.yaml` bible still wins on conflicts) |
| `config/narrative_choices.yaml` | The player's canon questionnaire (Shepard build, ME1–3 decisions) — a question counts as answered once `answer` is set or `options` narrows to one value | `outline-writer` (which branch of a choice-conditional event exists) and `section-writer` (which branch to narrate); unanswered questions fall back to default canon |

**Generation phase** (`/me-generate <narrator> "<themes>" [--brief ...]` → approve outline → `--continue`):

1. `outline-writer` reads the master timeline + `page_summaries/` + `codex/*.md` + the narrator's `.yaml`/`.style.md` + `narrative_choices.yaml` (+ optional free-text `brief`) and writes `output/<run>/outline.yaml` — section list with event ids and word targets. Stops for user approval (`# UNAPPROVED` marker).
2. Once approved, `section-writer` writes each section: pulls that section's `timeline/events/*.yaml` for required facts, runs `scripts/retrieve.py` (BM25 over the scraped corpus) for supporting detail, greps `codex/culture.md` / `social.md` / `everyday.md` for texture bullets touching the section's people/places/species, and writes prose in the narrator's voice — required to weave in at least one texture bullet when one genuinely fits.
3. `consistency-checker` and `smoother` pass over the assembled `output/<run>/sections/` afterward for continuity, without touching facts or voice.

So: **summaries** feed the outline (big-picture judgment of what matters), the
**codex** feeds both the outline (what lore to prioritize) and every section
(live grounding detail, including the culture/social/everyday world-texture),
the **timeline** is the chronological skeleton and the required-facts source,
**BM25** is per-section supporting detail pulled from the raw corpus, and the
**narrator config + narrative choices** decide voice and which version of
events actually happened in this playthrough.

### How `outline-writer` actually weighs its inputs

`outline-writer` isn't a sequential pipeline of steps — it's one subagent call
that reads all its inputs at once and reasons over them together. But the
order it's told to *weight* them is fixed, and that fixed order is effectively
the "flow":

1. **Timeline first, as raw material.** It reads `master_timeline.yaml` +
   `timeline/events/*.yaml` — every possible event, tagged with `characters`,
   `event_id`, and (for forked events) multiple branches.
2. **`narrative_choices.yaml` + `brief` decide which branch is real**, not
   just which sections exist. Many events are choice-conditional (e.g. "Wrex
   dies on Virmire" vs. "Wrex survives"). For any forked event, only the
   branch the answered choices select is real — `brief` wins if it conflicts
   with `narrative_choices`; the other branch's sections simply aren't built.
   Unanswered questions are ignored; default canon applies.
3. **The narrator's own arc is the spine.** From the surviving branch of the
   timeline, the agent pulls every event where this narrator is in the
   `characters` list, in chronological order — the backbone of the outline,
   weighted by the narrator's `.yaml` `knowledge_bias` (events they lived get
   more sections/words than ones they only heard about).
4. **`page_summaries/` + `codex/*.md` fill in around that spine.** This
   doesn't add new events — it tells the agent which existing timeline events
   deserve their own section vs. a passing mention, and which lore-heavy
   sections (including culture/social/everyday world-texture) to add
   alongside plot sections.
5. **Non-personal galaxy events are last resort** — brief connective/bridging
   sections only, never the bulk.
6. **`brief`, if given, sets the frame on top of all that** — occasion, mood,
   who's addressed — and can pin an otherwise-unanswered canon choice for
   just this episode.
7. **The narrator's `.style.md`** (quotes + "how they talk") isn't used for
   section *selection* at all — only to judge how much room this narrator's
   voice needs per beat.

`section-writer` then works section by section using the same priority order
(narrator's lived experience → lore/texture → required timeline facts as the
skeleton the first two hang on) — see its Content priority in
`.claude/agents/section-writer.md`.

### The narrative-choices questionnaire

`config/narrative_choices.yaml` is a structured questionnaire, not a
configuration file. It holds the player's Shepard background, class, gender,
romance choice, and key trilogy story decisions (with optional `detail` fields
for free-text expansion). A question is answered when `answer` is set or its
`options` are narrowed to one value. When generation runs, the agents read only
the *answered* subset and treat unanswered questions as defaults (they warn about
blanks, but do not block).

### How episodes are prioritized

Each episode draws on, in order, all cross-linked:

1. **The narrator character's own timeline** — events from the master timeline
   where that narrator appears in the event's `characters` field
2. **Lore** — the narrator's background, the species/tech/factions/places their
   story runs through, and surrounding context
3. **The main galaxy timeline** — as connective tissue only, to bridge the narrator's
   events and ground the pacing

The YAML timeline is the chronological skeleton; the narrator's personal events are
the content spine.

## Status

The pipeline (scripts, subagents, commands, config) is built and
tested. Running it end-to-end against the live wiki to produce a real episode is
done on demand in a later session — give Claude a narrator and a theme prompt.
