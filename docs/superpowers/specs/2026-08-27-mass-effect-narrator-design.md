# Mass Effect Narrator — Design Spec

**Date:** 2026-08-27
**Status:** Implemented (pipeline; first real run deferred)
**Source brainstorm:** `plan.md`

## 1. Goal

Produce a pipeline that generates 30-minute-to-1-hour narrated recaps of Mass
Effect lore and events, covering the full original trilogy. Each recap is written
in the voice of a chosen in-universe narrator (Garrus, Liara, Mordin, Joker,
Jack, …). A run takes a narrator, a set of thematic pointers, and a target word
count; it produces an outline for the user to approve, then generates the full
script grounded in scraped wiki lore.

The end state: from a clean checkout, a user can run four commands
(`/me-scrape`, `/me-build-lore`, `/me-build-timeline`, `/me-generate`) and get an
`episode.md` of 5,000–10,000 words plus its supporting artifacts.

## 2. Non-goals

- No embeddings, no vector database. Retrieval is BM25 keyword search only.
- No standalone API integration. All reasoning runs through Claude Code subagents
  using the user's existing auth.
- No coverage of Andromeda or non-trilogy media at v1.
- No audio / TTS generation at v1 (prose output only).
- No web UI. The interface is Claude Code slash commands + files on disk.

## 3. Architecture

### 3.1 Two kinds of work

| Kind | Mechanism | Steps |
|------|-----------|-------|
| Deterministic | Python scripts in `scripts/`, invoked by slash commands via Bash | scrape, HTML→markdown clean, chunk, build BM25 index, retrieval CLI, run-folder scaffolding |
| Reasoning | Claude Code subagents (`.claude/agents/`), existing auth, no API key | summarize pages, extract timeline events, build outline, write sections, smooth, consistency-check |

### 3.2 Control flow

```
Wiki (MediaWiki API)
  → data/pages/*.md            clean markdown + frontmatter (no raw HTML stored)
  → data/chunks/chunks.jsonl   500–1000 token chunks, 100–150 overlap
  → data/bm25_index.pkl
  → page_summaries/*.md        200–500 words per page  (+ lore/manual/*.md)
  → timeline/events/*.yaml     event summaries, each links source_chunks[]
  → timeline/master_timeline.yaml   ~50–500 ordered trilogy-wide events
  → codex/                     human-readable curated reference

/me-generate <narrator> "<themes>" [--words N]
  → output/<run>/outline.yaml        [PAUSE — user edits / approves]
/me-generate --continue <run>
  → per section: retrieve.py evidence → section-writer subagent → sections/<id>.md
  → smoother subagent (sliding window, continuity only)
  → consistency-checker subagent (issues.md first, then patch pass)
  → output/<run>/episode.md
```

The YAML timeline is the **control layer** (pacing, chronology, event selection).
BM25 supplies **grounding detail**. The narrator voice bible supplies **style**.

## 4. Directory layout

```
mass/
  scripts/
    scrape_wiki.py      MediaWiki API crawl from seeds, depth-limited, capped
    clean_md.py         HTML → clean markdown + frontmatter (shared module)
    chunk.py            pages → chunks.jsonl
    build_bm25.py       chunks.jsonl → bm25_index.pkl
    retrieve.py         CLI: query string → top-k chunks as JSON (used by subagents)
    new_run.py          scaffold output/<narrator>_<theme-slug>_<date>/
  .claude/
    commands/
      me-scrape.md
      me-build-lore.md
      me-build-timeline.md
      me-generate.md
    agents/
      page-summarizer.md
      timeline-extractor.md
      outline-writer.md
      section-writer.md
      smoother.md
      consistency-checker.md
  config/
    seeds.yaml          seed page titles, per-seed expansion depth, global page cap
    narrators/
      garrus.yaml  liara.yaml  mordin.yaml  legion.yaml  javik.yaml
  data/
    pages/<page-slug>.md          frontmatter: title, url, game, type, characters
    chunks/chunks.jsonl           fields: chunk_id, page, section, game, text, url
    bm25_index.pkl
  lore/manual/<name>.md           hand-added lore, same frontmatter shape
  page_summaries/<page-slug>.md
  timeline/
    master_timeline.yaml
    events/<event_id>.yaml        title, date, game, chronological_order, summary,
                                  characters[], consequences[], source_chunks[]
  codex/                          grouped: species / tech / characters / factions / timeline
  output/<narrator>_<theme-slug>_<YYYY-MM-DD>/
    outline.yaml  episode.md  sources.json  sections/*.md  issues.md
```

## 5. Data formats

### 5.1 Page file (`data/pages/<slug>.md`)

```markdown
---
title: Virmire
url: https://masseffect.fandom.com/wiki/Virmire
game: Mass Effect
type: mission          # mission | character | species | location | tech | lore | faction | timeline
characters: [Shepard, Saren, Ashley, Kaidan, Wrex]
scraped: 2026-08-27
---

<clean prose markdown, nav/infobox/gameplay-table noise removed>
```

### 5.2 Chunk (`data/chunks/chunks.jsonl`, one JSON object per line)

```json
{"chunk_id": "virmire_004", "page": "Virmire", "section": "Mission",
 "game": "Mass Effect", "text": "...", "url": "https://..."}
```

### 5.3 Timeline event (`timeline/events/<event_id>.yaml`)

```yaml
event_id: virmire_decision
title: The Virmire mission
game: Mass Effect
chronological_order: 42
date: "2183 CE"
summary: >
  Shepard leads a strike on Saren's cloning and research facility...
characters: [Shepard, Saren, Ashley, Kaidan, Wrex]
consequences:
  - Saren's research base is destroyed
  - One squadmate is left behind and killed
  - Sovereign is revealed as a Reaper
source_chunks: [virmire_003, virmire_004, sovereign_002]
```

### 5.4 Narrator voice bible (`config/narrators/<name>.yaml`)

```yaml
name: Garrus Vakarian
species: Turian
tone: [dry humor, tactical, understated, loyal to Shepard, exasperated by bureaucracy]
diction: [military metaphors, blunt sentences, occasional self-deprecation]
signature: ["calibrations"]
avoid: [purple prose, parody catchphrase spam, breaking the fourth wall]
knowledge_bias: >
  Weights combat, C-Sec / Archangel history, squad relationships. Light on
  politics he was not present for; flags secondhand knowledge as hearsay.
```

`knowledge_bias` is what lets each narrator legitimately select different lore for
the same themes.

### 5.5 Run outline (`output/<run>/outline.yaml`)

```yaml
narrator: garrus
themes: [the cost of war, loyalty]
target_words: 8000
sections:
  - id: humanity_enters
    title: Humanity enters the galactic stage
    events: [mars_discovery, charon_relay, first_contact_war]
    target_words: 500
  - id: eden_prime
    title: Eden Prime and the hunt for Saren
    events: [eden_prime, spectre_induction]
    target_words: 600
```

### 5.6 Sources record (`output/<run>/sources.json`)

```json
{"eden_prime": ["eden_prime_001", "eden_prime_004", "prothean_beacon_002"],
 "virmire":    ["virmire_003", "virmire_004", "sovereign_002"]}
```

## 6. Pipeline stages

### Stage 0 — `/me-scrape [--depth N] [--cap M] [--seeds config/seeds.yaml]`

1. `scrape_wiki.py` reads `seeds.yaml`, walks the MediaWiki API (`action=parse`
   / `action=query`) from each seed title, following in-page links to depth `N`
   (default 2), stopping at `M` total pages (default from seeds.yaml), with `T` download rate.
2. Each page is converted to clean markdown via `clean_md.py` (drop nav, infobox
   templates, gameplay stat tables, edit links, references section; keep prose,
   headings, lists). Frontmatter is populated; `type` inferred from wiki
   categories with a fallback of `lore`.
3. Rate-limited, polite User-Agent, incremental: a page already present with a
   recent `scraped` date is skipped unless `--force`.
4. `chunk.py` → `chunks.jsonl` (500–1000 tokens, 100–150 overlap, never split
   mid-sentence where avoidable).
5. `build_bm25.py` → `bm25_index.pkl`.

**Output:** `data/pages/`, `data/chunks/chunks.jsonl`, `data/bm25_index.pkl`.

### Stage 1 — `/me-build-lore`

`page-summarizer` subagent processes `data/pages/` + `lore/manual/` in batches of
~15 pages per call → `page_summaries/<slug>.md` (200–500 words, prose, facts
only). After all batches, it assembles `codex/` files grouped by
species / tech / characters / factions / timeline, each entry citing its source
page. Rerunnable; existing summaries skipped unless `--force`.

**Output:** `page_summaries/`, `codex/`.

### Stage 2 — `/me-build-timeline`

`timeline-extractor` subagent reads `page_summaries/` (and `codex/` for
cross-checking) → writes one `timeline/events/<event_id>.yaml` per distinct
event, each with `source_chunks` populated by matching event content to chunk IDs
in `chunks.jsonl`. Then produces `master_timeline.yaml` — every event ordered by
`chronological_order`, deduplicated, ~50–500 entries across the trilogy.

**Output:** `timeline/events/*.yaml`, `timeline/master_timeline.yaml`.

### Stage 3 — `/me-generate <narrator> "<themes>" [--words 8000]`

1. `new_run.py` scaffolds `output/<narrator>_<theme-slug>_<date>/`.
2. `outline-writer` subagent: `master_timeline.yaml` + themes +
   `config/narrators/<narrator>.yaml` → `outline.yaml`. Sections cover the arc,
   weighted toward the themes and the narrator's `knowledge_bias`; word targets
   sum to `--words` (±10%). **The command stops here and tells the user to review
   `outline.yaml`.**
3. User edits / approves `outline.yaml`.
4. `/me-generate --continue <run-folder>`:
   - For each section: `retrieve.py` is called with the section's event names,
     characters, and consequence phrases; returns top-k chunks; results are
     deduplicated across the query set.
   - `section-writer` subagent receives the narrator bible, the section's
     required facts (from its events' `summary` + `consequences`), and the
     retrieved chunks. Writes `sections/<id>.md` to the section's word target.
     Prompt constraints: preserve every required fact, invent no events, use the
     voice without parodying it. Used chunk IDs recorded in `sources.json`.
5. `smoother` subagent: sliding window (previous section ending / current section
   / next section beginning). Revises **only** the current section for continuity
   and transitions. No factual edits.
6. `consistency-checker` subagent: first pass emits `issues.md` only —
   chronology errors, repeated explanations, missing major events, narrator voice
   drift, invented lore, overlong sections. Second pass patches the offending
   sections.
7. Sections concatenated in outline order → `episode.md`, with a short header
   block (narrator, themes, word count, generation date).

**Output:** a populated `output/<run>/` folder.

## 7. Error handling

- **Scrape:** network errors retried with backoff (3 attempts); a page that
  still fails is logged to `data/scrape_errors.log` and skipped, not fatal.
  Redirect pages resolved to their target. Missing seed titles reported at the
  end, run continues.
- **Clean:** a page that produces < 200 chars of prose after cleaning is flagged
  in the error log (likely a disambiguation or stub) and kept only if non-empty.
- **Chunking / BM25:** deterministic; failure here is a bug, surfaced loudly.
- **Subagent stages:** each writes files incrementally, so a re-run resumes from
  what is already on disk. A subagent that returns malformed YAML/JSON for an
  item is retried once; persistent failure logs the item and continues.
- **`/me-generate` without approved outline:** `--continue` refuses to run if
  `outline.yaml` is missing or still has the `# UNAPPROVED` marker `new_run.py`
  writes at the top; the user removes that line to approve.
- **retrieve.py empty result** for a section: section-writer proceeds on the
  timeline summary/consequences alone and notes the thin sourcing in
  `sources.json` (`"__warnings__": [...]`).

## 8. Testing

- **Unit (pytest):**
  - `clean_md.py` strips nav / infobox / gameplay tables, keeps prose headings
    and lists.
  - `chunk.py` respects size bounds and overlap, does not drop text.
  - `retrieve.py` returns the expected chunk for a known query
    (`"Sovereign"` → Sovereign chunks) against a fixture index.
  - `new_run.py` produces the documented folder shape and the `# UNAPPROVED`
    marker.
- **Integration smoke test:** a committed 3-page mini-corpus (Eden Prime,
  Virmire, Sovereign) → `chunk` → `build_bm25` → hand-written 2-event timeline →
  `/me-generate` outline → approve → `--continue` with `--words 800`. Asserts:
  run folder shape, `episode.md` within ±15% of 800 words, `sources.json`
  non-empty for every section.
- **Fact-preservation check:** run `consistency-checker` against a section with a
  deliberately injected contradiction (wrong squadmate dies on Virmire); the
  injected error must appear in `issues.md`.

## 9. Milestones

1. **Scaffold + scripts:** repo layout, `clean_md.py`, `scrape_wiki.py`,
   `chunk.py`, `build_bm25.py`, `retrieve.py`, `new_run.py`, unit tests, mini
   corpus fixture.
2. **Lore extraction:** `me-scrape` command, `me-build-lore` command +
   `page-summarizer` agent, `me-build-timeline` command + `timeline-extractor`
   agent. Run against a small real seed set, inspect output.
3. **Generation:** `me-generate` command, `outline-writer` / `section-writer` /
   `smoother` / `consistency-checker` agents, `config/narrators/garrus.yaml`.
   End-to-end smoke test passes.
4. **Full corpus + narrators:** finalize `seeds.yaml` for the trilogy, run the
   full scrape + build, author the remaining four narrator bibles, generate one
   real 8,000-word episode and review quality.

## 10. Open questions deferred to implementation

- Final contents of `config/seeds.yaml` (seed titles + depths).
- Exact batch size for `page-summarizer` (start at 15, tune for context limits).
- `retrieve.py` `k` per query and dedup strategy (start k=6, dedup by chunk_id).
- Whether `codex/` generation stays in `me-build-lore` or moves to its own
  command if it proves slow (default: keep it in `me-build-lore`).
