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
| 3b. Canon | edit `config/canon/choices.yaml` — Shepard build, ME1/2/3 decisions; add `config/canon/overrides.yaml` entries where your memory beats the wiki | — |
| 3c. Scenes | hand-authored `scenes/*.yaml` (targeted set); `/me-build-scenes` for the full sweep | `scenes/`, and `scene` rows in `data/bm25_index.pkl` |
| 4a. Outline | `/me-generate garrus "the cost of war, loyalty" --words 8000` | `output/<run>/outline.yaml` (**stops for approval**) |
| 4b. Approve | edit `outline.yaml` — the `form`, the sections, and especially each section's `promises` and `retrieval` keys — then delete the `# UNAPPROVED` first line | — |
| 4c. Voice check | `/me-generate --continue output/<run>` | `output/<run>/packs/*.json` (**hard-stops on a gap**), then `output/<run>/voice_check.md` — the **first section only** (**stops for approval**) |
| 4d. Approve the voice | read it for voice and lore handling; give feedback (folded into the narrator bible, section rewritten) or delete the `# UNAPPROVED` first line | — |
| 4e. Write | `/me-generate --continue output/<run>` | `output/<run>/episode.md` (+ `sections/`, `sources.json`, `issues.md`) |

Hand-written lore goes in `lore/manual/*.md` with the same frontmatter as
`data/pages/` files; it is picked up by step 2. YouTube-transcript lore in `ddl/`
is converted to `lore/manual/*.md` by Task 16 of the build.

## Configuration

- **`config/seeds.yaml`:** Scrape seed URLs and crawl parameters (`depth`, `cap`, `rate`)
- **`config/narrators/<name>.yaml`:** Voice bibles for each narrator (tone, diction, signature phrases, knowledge biases)
- **`config/canon/`:** The canon store — see [The canon store](#the-canon-store) below.
  Four files, split by who writes each one; `python scripts/canon.py` merges them into the
  single view the agents consume.

## Adding a narrator

Copy `config/narrators/garrus.yaml` to `config/narrators/<name>.yaml` and rewrite
`tone`, `diction`, `signature`, `avoid`, and `knowledge_bias`. No code change.

Optionally add `digressions:` — `style` (how this narrator wanders off-topic and comes
back) and `subjects` (the lore, history and worldbuilding they'd genuinely dwell on).
Both generation agents read it: `outline-writer` builds lore/history sections around
those subjects, `section-writer` uses it to pick what to reach for and how to ramble.
See `config/narrators/jack.yaml` and `traynor.yaml` for worked examples, and
`docs/generation-example.md` for the density aimed for.

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

**Build phase** (`/me-scrape` → `/me-build-lore` → `/me-build-timeline` → `/me-build-scenes`):

| Artifact | Built by | What it is | Consumed by |
|---|---|---|---|
| `data/pages/*.md` | `/me-scrape` | Raw cleaned wiki pages, one per topic | `page-summarizer` only — nothing downstream reads these directly |
| `data/bm25_index.pkl` | `/me-scrape` (via `scripts/build_bm25.py`) | Search index over chunked `data/pages/` + `lore/manual/` text | `scripts/retrieve.py`, called by `section-writer` for per-section grounding chunks |
| `page_summaries/<slug>.md` | `page-summarizer` (via `/me-build-lore`) | 200–500 word factual prose summary of one page | `outline-writer` (background/lore reading); not read section-by-section — it's outline-time context |
| `codex/{characters,factions,places,species,tech,ships,war,timeline,culture,social,everyday}.md` | `page-summarizer`, appending bullets as it summarizes | Deduplicated one-line facts, grouped by subject, each tagged `(source: <page title>)` | `outline-writer` (which lore to prioritize) **and** `section-writer` (culture/social/everyday are grepped live per section as world-texture grounding — see the Rules in `.claude/agents/section-writer.md`) |
| `timeline/events/<event_id>.yaml` + `timeline/master_timeline.yaml` | `timeline-extractor` (via `/me-build-timeline`) | Deduplicated, chronologically ordered events, each with `characters`, `summary`, `consequences`, and source chunk ids | `outline-writer` (picks which events become sections); reaches `section-writer` as a pack's `required_facts` |
| `scenes/<scene_id>.yaml` | hand-authored for the targeted set; `/me-build-scenes` for the full sweep | The **occasion** layer: a bounded thing that happened with people in a room, with `participants` / `private_to` / `heard_by`, per-beat `source_chunks`, and `variants` for branches | `outline-writer` (which occasions a section can be built from) and `build_pack.py` (which computes attendance from it) |

**Config, hand-authored, read at generation time only:**

| File | What it is | Read by |
|---|---|---|
| `config/narrators/<name>.yaml` | The voice bible: `tone`, `diction`, `avoid`, `signature`, `knowledge_bias`, optional `digressions` | `outline-writer` (pacing/weighting, lore sections) and `section-writer` (prose voice, what lore to reach for) |
| `config/narrators/<name>.style.md` | Optional: real verbatim quotes with context + a "how they talk" note, built once per narrator by `narrator-style-extractor` | `section-writer` (cadence bank — lines used verbatim or adapted; the `.yaml` bible still wins on conflicts) |
| `docs/generation-example.md` | Illustration of the lore/worldbuilding density sections aim for (not a template) | `outline-writer`, `section-writer` and `episode-auditor` |
| `config/forms.yaml` | The episode-form reference set: what shape an episode can take (`arc`, `evening`, `one-relationship`, `one-place`, `postmortem`, `argument`) and where its sections come from | `outline-writer`, which records the chosen `form` and a one-line `form_note` in `outline.yaml` |
| `config/canon/choices.yaml` | The player's canon questionnaire (Shepard build, ME1–3 decisions) — a question counts as answered once `answer` is set or `options` narrows to one value | `outline-writer` (which branch of a choice-conditional event exists) and `section-writer` (which branch to narrate); unanswered questions fall back to default canon |
| `config/canon/overrides.yaml` | Canon that beats the corpus: `kind: au` (deliberate divergence) or `kind: correction` (the wiki is wrong or lossy), each scoped to entities/scenes/events | every stage, via `scripts/canon.py`; an override settles staging as well as outcome |
| `config/canon/questions.yaml` | Agent inbox — what an agent could not resolve. The user answers in place; answered entries become canon on the next run | appended by agents (`canon.py --ask`), read by the user |
| `config/canon/resolved.yaml` | Audit log of conflicts settled silently under split authority | appended by agents (`canon.py --log-resolution`), read by the user |

**Generation phase** (`/me-generate <narrator> "<themes>" [--brief ...]` → approve outline → `--continue`):

1. `outline-writer` reads `config/forms.yaml`, the master timeline, the scene layer,
   `page_summaries/`, `codex/*.md`, the narrator's `.yaml`/`.style.md` and the canon store
   (+ optional free-text `brief`), and writes `output/<run>/outline.yaml`: a `form` and
   `form_note`, then sections carrying `events`, `scenes`, **`retrieval` keys** and
   **`promises`** alongside their word targets. Stops for user approval (`# UNAPPROVED`).
2. `scripts/build_pack.py <run> --all` turns each approved section into
   `output/<run>/packs/<id>.json` — required facts, the canon narrowed to that section, the
   scene records, computed attendance, the retrieved evidence tagged with the key that found
   it, codex lines with line numbers, conflicts and warnings. It is deterministic, and it
   **hard-stops**: a scene id that does not exist or a retrieval key that returns nothing
   fails the run and names the gap. That is the point — a silent retrieval failure looks
   exactly like a successful one, and the writer's fallback for missing evidence is its own
   memory of Mass Effect.
3. `section-writer` writes the **first section only** from its pack, and generation stops at
   the voice checkpoint (`voice_check.md`, same `# UNAPPROVED` convention). This is where
   voice and lore-integration feedback is cheapest: corrections go into
   `config/narrators/<narrator>.yaml` first, so every later section is written against the
   corrected bible. Once the marker is cleared, `section-writer` writes each remaining
   section — reading its pack, the narrator files and `generation-example.md`, and nothing
   else.
4. `episode-auditor` holds the packs and the whole episode at once and runs find-then-fix:
   grounding, canon, vantage, agency, recitation, **coverage** (pack items used vs unused,
   promises kept vs dropped), staging and length. It fixes by **swapping**, never appending,
   and only from pack items. It replaces the old `consistency-checker` and absorbs
   `smoother`.

So: **summaries** feed the outline, the **codex** feeds the outline and arrives in packs as
located lines, the **timeline** supplies the required facts, the **scene layer** supplies
occasions and vantage, **BM25** supplies per-section evidence for the keys the outline
named, and the **narrator config + canon store** decide voice and which version of events
actually happened in this playthrough.

### How `outline-writer` actually weighs its inputs

`outline-writer` isn't a sequential pipeline of steps — it's one subagent call
that reads all its inputs at once and reasons over them together. But the
order it's told to *weight* them is fixed, and that fixed order is effectively
the "flow":

1. **Timeline first, as raw material.** It reads `master_timeline.yaml` +
   `timeline/events/*.yaml` — every possible event, tagged with `characters`,
   `event_id`, and (for forked events) multiple branches.
2. **The canon store + `brief` decide which branch is real**, not
   just which sections exist. Many events are choice-conditional (e.g. "Wrex
   dies on Virmire" vs. "Wrex survives"). For any forked event, only the
   branch the answered choices select is real — `brief` wins if it conflicts
   with the canon store; the other branch's sections simply aren't built.
   Unanswered questions are ignored; default canon applies.
3. **The narrator's own arc is the spine.** From the surviving branch of the
   timeline, the agent pulls every event where this narrator is in the
   `characters` list, in chronological order — the backbone of the outline,
   weighted by the narrator's `.yaml` `knowledge_bias` (events they lived get
   more sections/words than ones they only heard about).
4. **`page_summaries/` + `codex/*.md` fill in around that spine.** This
   doesn't add new events — it tells the agent which existing timeline events
   deserve their own section vs. a passing mention, and which lore-heavy
   sections to add alongside plot sections. Lore, history and worldbuilding get
   dedicated sections, not just asides: the narrator's `knowledge_bias` and
   `digressions` name the subjects (an institution's history, a faction, a
   species, a place, a piece of culture), drawn from the codex history files as
   well as culture/social/everyday world-texture.
5. **Non-personal galaxy events split two ways** — history this narrator would
   genuinely dwell on (per `knowledge_bias`/`digressions`) earns real weight and
   its own sections, told from their vantage; galaxy events they don't care about
   stay brief connective/bridging material, never the bulk.
6. **`brief`, if given, sets the frame on top of all that** — occasion, mood,
   who's addressed — and can pin an otherwise-unanswered canon choice for
   just this episode.
7. **The narrator's `.style.md`** (quotes + "how they talk") barely affects
   section *selection* — mainly it judges how much room this narrator's voice
   needs per beat, though strong quotes on a subject signal one they'd dwell on.

`section-writer` then works section by section using the same priority order
(narrator's lived experience → their own lore told as story → the galaxy history
and worldbuilding they care about → required timeline facts as the skeleton the
first three hang on) — see its Content priority in
`.claude/agents/section-writer.md`. Two things worth knowing about it:

- It runs a **second retrieval pass** for the subjects a section runs through
  (institutions, factions, species, places, history) on top of the plot-shaped
  first pass — that pass is where the worldbuilding comes from.
- Facts stay strictly grounded, but the narrator may voice **connective tissue**:
  their own plausible in-universe inferences and opinions linking grounded facts,
  clearly marked as their read ("the way I figure it"). It connects lore; it never
  adds canon.

### The canon store

`config/canon/` holds everything that makes this *your* playthrough rather than the
wiki's. It is four files rather than one because they have different writers, and a
YAML round-trip write destroys comments and reflows a hand-formatted file — so the
files you live in are never machine-rewritten.

| File | Writer | Holds |
|---|---|---|
| `choices.yaml` | you | The questionnaire: Shepard build and the ME1–3 decision points |
| `overrides.yaml` | you | Canon that beats the corpus, marked deliberate |
| `questions.yaml` | agents append, you answer | What an agent could not resolve |
| `resolved.yaml` | agents append | Conflicts settled on your behalf |

**Split authority.** An answered choice settles *which branch happened*; the corpus
still owns *how it was staged*. If you wrote "I let Garrus win the sniper contest",
the outcome is yours — but the scene record says a Presidium rooftop and beverage
cans, so that is where it is narrated, and the reconciliation is logged to
`resolved.yaml` rather than argued about. An entry in `overrides.yaml` settles both,
which is what makes a divergence deliberate instead of shorthand accidentally promoted
into staging. A genuine contradiction is appended to `questions.yaml` and surfaced at
the outline gate; it never blocks a run.

A question is answered when `answer` is set or its `options` are narrowed to one
value. Unanswered questions and open questions warn; default canon applies.

```
python scripts/canon.py                          # human summary, authority marked
python scripts/canon.py --json                   # machine view
python scripts/canon.py --for 'Wrex,Grunt' --json  # just the canon touching a section
python scripts/canon.py --ask 'question: ...'    # append to questions.yaml
python scripts/canon.py --log-resolution '...'   # append to resolved.yaml
```

`--for` is what fills an evidence pack's `canon` field, so a section carries the five
facts that bear on it rather than all sixty.

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
