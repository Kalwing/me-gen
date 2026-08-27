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
| 3. Timeline | `/me-build-timeline` | `timeline/events/*.yaml`, `timeline/master_timeline.yaml`, `config/narrative_choices.yaml` |
| 3b. Canon questionnaire | copy + fill `config/narrative_choices.yaml` — Shepard build, ME1/2/3 decisions | — |
| 4a. Outline | `/me-generate garrus "the cost of war, loyalty" --words 8000` | `output/<run>/outline.yaml` (**stops for approval**) |
| 4b. Approve | edit `outline.yaml`, delete the `# UNAPPROVED` first line | — |
| 4c. Write | `/me-generate --continue output/<run>` | `output/<run>/episode.md` (+ `sections/`, `sources.json`, `issues.md`) |

Hand-written lore goes in `lore/manual/*.md` with the same frontmatter as
`data/pages/` files; it is picked up by step 2. YouTube-transcript lore in `ddl/`
is converted to `lore/manual/*.md` by Task 16 of the build.

## Configuration

- **`config/seeds.yaml`:** Scrape seed URLs and crawl parameters (`depth`, `cap`, `rate`)
- **`config/narrators/<name>.yaml`:** Voice bibles for each narrator (tone, diction, signature phrases, knowledge biases)
- **`config/narrative_choices.template.yaml`:** Structured questionnaire template
  - Copy to `config/narrative_choices.yaml` and fill it out
  - Questions cover Shepard build (background, psych profile, class, gender, romance)
    and trilogy story decisions (ME1, ME2, ME3 — choice points with free-text `detail`)
  - Generation agents read the *answered* subset only; unanswered questions default to canon (with warnings, not errors)
  - `/me-build-timeline` seeds the working copy from the template

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

### The narrative-choices questionnaire

`config/narrative_choices.template.yaml` is a structured questionnaire, not a
configuration file. Users copy it to `config/narrative_choices.yaml`, then fill
in their Shepard's background, class, gender, romance choice, and key trilogy
story decisions (with optional `detail` fields for free-text expansion). When
generation runs, the agents read only the *answered* subset and treat unanswered
questions as defaults (they warn about blanks, but do not block). `/me-build-timeline`
seeds the working copy from the template automatically.

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

The pipeline (scripts, subagents, commands, config templates) is built and
tested. Running it end-to-end against the live wiki to produce a real episode is
done on demand in a later session — give Claude a narrator and a theme prompt.
