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
