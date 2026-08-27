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
| 3b. Canon | edit `config/narrative_choices.yaml` — pick your trilogy decisions, Shepard background/profile/class | — |
| 4a. Outline | `/me-generate garrus "the cost of war, loyalty" --words 8000` | `output/<run>/outline.yaml` (**stops for approval**) |
| 4b. Approve | edit `outline.yaml`, delete the `# UNAPPROVED` first line | — |
| 4c. Write | `/me-generate --continue output/<run>` | `output/<run>/episode.md` (+ `sections/`, `sources.json`, `issues.md`) |

Hand-written lore goes in `lore/manual/*.md` with the same frontmatter as
`data/pages/` files; it is picked up by step 2. YouTube-transcript lore in `ddl/`
is converted to `lore/manual/*.md` by Task 16 of the build.

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

## Status

The pipeline (scripts, subagents, commands, config templates) is built and
tested. Running it end-to-end against the live wiki to produce a real episode is
done on demand in a later session — give Claude a narrator and a theme prompt.
