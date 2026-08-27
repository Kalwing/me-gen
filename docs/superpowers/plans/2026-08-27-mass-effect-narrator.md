# Mass Effect Narrator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code slash-command + subagent pipeline that scrapes Mass Effect trilogy lore into a clean local corpus, derives a file-based YAML timeline plus a BM25 evidence index, and generates approved 5,000–10,000-word narrated recaps in swappable in-universe narrator voices.

**Architecture:** Deterministic work (scrape, HTML→markdown clean, chunk, BM25 index build, retrieval, run scaffolding, episode assembly) is plain Python CLI scripts under `scripts/`, driven by Bash from four slash commands. Reasoning work (summarize pages, extract timeline events, write the outline, write/smooth/consistency-check sections) is Claude Code subagents defined under `.claude/agents/`, using the user's existing Claude Code auth — no API key, no external LLM SDK. The YAML timeline is the control layer for pacing and chronology; BM25 supplies grounding detail; the narrator voice bible supplies style.

**Tech Stack:** Python 3.11+, `pytest`, `requests`, `beautifulsoup4`, `markdownify`, `rank-bm25`, `PyYAML`. Claude Code slash commands (`.claude/commands/*.md`) and subagents (`.claude/agents/*.md`).

**Spec:** `docs/superpowers/specs/2026-08-27-mass-effect-narrator-design.md`

## Global Constraints

- **Python 3.11+.** Every script runs as `python scripts/<name>.py [...]` and supports `--help`.
- **Dependencies** are exactly: `requests`, `beautifulsoup4`, `markdownify`, `rank-bm25`, `PyYAML`, `pytest`. Pinned in `requirements.txt`. No other runtime deps. No embeddings library, no vector DB, no LLM SDK.
- **No network in unit tests.** Anything that hits HTTP takes an injected fetcher/callable so tests pass a fake.
- **Every script is importable without side effects** — all CLI behavior sits behind `if __name__ == "__main__":`.
- **Chunk sizes are word counts**, not tokenizer tokens: `--size` default `800` words, `--overlap` default `120` words. Roughly 1 word ≈ 1.3 tokens, so 800 words ≈ ~1040 tokens, inside the spec's 500–1000 token band. Document this in `chunk.py`'s module docstring.
- **Frontmatter** is a YAML block delimited by `---` fences at the very top of a markdown file.
- **Slug rule:** lowercase; every run of characters not in `[a-z0-9]` becomes a single `-`; strip leading/trailing `-`. Used for page filenames, event ids, run-folder theme slugs.
- **chunk_id format:** `<page-slug>_<NNN>` where `NNN` is a zero-padded 3-digit counter per page starting at `001`.
- **Wiki host:** `https://masseffect.fandom.com`, MediaWiki API at `/api.php`. Requests send `User-Agent: mass-effect-narrator/0.1 (personal project)`.
- **Frequent commits:** one commit per task minimum, conventional-commit style (`feat:`, `test:`, `chore:`, `docs:`).
- **The repo is not yet under git.** Task 1 runs `git init`.
- **Directory layout is fixed by the spec §4.** Do not rename paths.

---

### Task 1: Project scaffold and shared helpers (`scripts/common.py`)

**Files:**
- Create: `.gitignore`
- Create: `requirements.txt`
- Create: `pyproject.toml`
- Create: `scripts/__init__.py` (empty)
- Create: `scripts/common.py`
- Create: `tests/__init__.py` (empty)
- Create: `tests/conftest.py`
- Create: `tests/test_common.py`
- Create: `tests/fixtures/events/virmire_decision.yaml`

**Interfaces:**
- Consumes: nothing (first task).
- Produces:
  - `slugify(text: str) -> str`
  - `read_frontmatter_md(path: pathlib.Path) -> tuple[dict, str]` — returns `(frontmatter_dict, body_str)`; raises `ValueError` if no leading `---` block.
  - `write_frontmatter_md(path: pathlib.Path, frontmatter: dict, body: str) -> None`
  - `load_event(path: pathlib.Path) -> dict` — parse one `timeline/events/*.yaml`; raise `ValueError` if any of the required keys `event_id, title, game, chronological_order, summary, characters, consequences, source_chunks` is missing.
  - `load_events(events_dir: pathlib.Path) -> dict[str, dict]` — map `event_id -> event dict` for every `*.yaml` in the dir.
  - `outline_is_approved(run_dir: pathlib.Path) -> bool` — `False` if `outline.yaml` missing or its first non-blank line starts with `# UNAPPROVED`.
  - `word_count(text: str) -> int` — `len(re.findall(r"\S+", text))`.
  - Module constant `REPO_ROOT: pathlib.Path` (parent of `scripts/`).

- [ ] **Step 1: Initialize git and Python project files**

Run:
```bash
cd /home/thomas/Documents/mass
git init
```

Create `.gitignore`:
```gitignore
__pycache__/
*.pyc
.pytest_cache/
data/pages/
data/chunks/
data/bm25_index.pkl
data/scrape_errors.log
page_summaries/
timeline/events/
timeline/master_timeline.yaml
codex/
output/
!tests/fixtures/**
```

Create `requirements.txt`:
```text
requests==2.32.3
beautifulsoup4==4.12.3
markdownify==0.13.1
rank-bm25==0.2.2
PyYAML==6.0.2
pytest==8.3.3
```

Create `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
```

Run:
```bash
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
```
Add `.venv/` to `.gitignore`.

- [ ] **Step 2: Write the failing test for `scripts/common.py`**

Create `tests/conftest.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
```

Create `tests/fixtures/events/virmire_decision.yaml`:
```yaml
event_id: virmire_decision
title: The Virmire mission
game: Mass Effect
chronological_order: 42
date: "2183 CE"
summary: >
  Shepard leads a strike on Saren's cloning and research facility on Virmire.
characters: [Shepard, Saren, Ashley, Kaidan, Wrex]
consequences:
  - Saren's research base is destroyed
  - One squadmate is left behind and killed
  - Sovereign is revealed as a Reaper
source_chunks: [virmire_003, virmire_004, sovereign_002]
```

Create `tests/test_common.py`:
```python
from pathlib import Path

import pytest

from scripts import common

FIXTURES = Path(__file__).parent / "fixtures"


def test_slugify_basic():
    assert common.slugify("The Virmire Mission!") == "the-virmire-mission"
    assert common.slugify("Mass Effect 2  (game)") == "mass-effect-2-game"
    assert common.slugify("--already-slug--") == "already-slug"


def test_frontmatter_roundtrip(tmp_path):
    p = tmp_path / "page.md"
    fm = {"title": "Virmire", "characters": ["Shepard", "Wrex"]}
    common.write_frontmatter_md(p, fm, "Body text here.\n")
    got_fm, body = common.read_frontmatter_md(p)
    assert got_fm == fm
    assert body.strip() == "Body text here."


def test_read_frontmatter_md_requires_block(tmp_path):
    p = tmp_path / "bad.md"
    p.write_text("no frontmatter here\n")
    with pytest.raises(ValueError):
        common.read_frontmatter_md(p)


def test_load_event_ok():
    ev = common.load_event(FIXTURES / "events" / "virmire_decision.yaml")
    assert ev["event_id"] == "virmire_decision"
    assert ev["chronological_order"] == 42
    assert "Shepard" in ev["characters"]


def test_load_event_missing_key(tmp_path):
    p = tmp_path / "broken.yaml"
    p.write_text("event_id: x\ntitle: y\n")
    with pytest.raises(ValueError):
        common.load_event(p)


def test_load_events_maps_by_id():
    events = common.load_events(FIXTURES / "events")
    assert set(events) == {"virmire_decision"}


def test_outline_is_approved(tmp_path):
    run = tmp_path / "run"
    run.mkdir()
    assert common.outline_is_approved(run) is False  # missing file
    (run / "outline.yaml").write_text("# UNAPPROVED — remove this line to approve\nnarrator: garrus\n")
    assert common.outline_is_approved(run) is False
    (run / "outline.yaml").write_text("narrator: garrus\nsections: []\n")
    assert common.outline_is_approved(run) is True


def test_word_count():
    assert common.word_count("one two   three\nfour") == 4
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python -m pytest tests/test_common.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.common'`.

- [ ] **Step 4: Implement `scripts/common.py`**

```python
"""Shared helpers for the Mass Effect narrator pipeline."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

_EVENT_REQUIRED = (
    "event_id", "title", "game", "chronological_order",
    "summary", "characters", "consequences", "source_chunks",
)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def read_frontmatter_md(path: Path) -> tuple[dict, str]:
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path}: no frontmatter block")
    _, _, rest = text.partition("---\n")
    fm_text, sep, body = rest.partition("\n---\n")
    if not sep:
        raise ValueError(f"{path}: unterminated frontmatter block")
    return yaml.safe_load(fm_text) or {}, body


def write_frontmatter_md(path: Path, frontmatter: dict, body: str) -> None:
    fm_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).rstrip("\n")
    Path(path).write_text(f"---\n{fm_text}\n---\n\n{body.lstrip()}", encoding="utf-8")


def load_event(path: Path) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    missing = [k for k in _EVENT_REQUIRED if k not in data]
    if missing:
        raise ValueError(f"{path}: missing event keys: {missing}")
    return data


def load_events(events_dir: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(Path(events_dir).glob("*.yaml")):
        ev = load_event(p)
        out[ev["event_id"]] = ev
    return out


def outline_is_approved(run_dir: Path) -> bool:
    p = Path(run_dir) / "outline.yaml"
    if not p.exists():
        return False
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            return not line.strip().startswith("# UNAPPROVED")
    return False


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python -m pytest tests/test_common.py -v`
Expected: PASS (8 passed).

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: scaffold project and shared helpers"
```

---

### Task 2: HTML → clean markdown (`scripts/clean_md.py`)

**Files:**
- Create: `scripts/clean_md.py`
- Create: `tests/test_clean_md.py`
- Create: `tests/fixtures/html/virmire.html`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces:
  - `clean_html(html: str) -> str` — strip chrome, return prose markdown (headings, paragraphs, lists preserved).
  - `infer_type(categories: list[str]) -> str` — one of `mission | character | species | location | tech | lore | faction | timeline`; default `lore`.
  - CLI: `python scripts/clean_md.py <input.html>` prints cleaned markdown to stdout.

- [ ] **Step 1: Write the failing test**

Create `tests/fixtures/html/virmire.html`:
```html
<div class="mw-parser-output">
  <div class="navbox">nav junk</div>
  <aside class="portable-infobox"><h2>Virmire</h2><div>Planet stats</div></aside>
  <div class="toc">Contents</div>
  <p>Virmire is a <a href="/wiki/planet">planet</a> in the Sentry Omega cluster.</p>
  <h2><span class="mw-headline" id="Mission">Mission</span><span class="mw-editsection">[edit]</span></h2>
  <p>Commander Shepard assaults Saren's base.</p>
  <ul><li>Wrex confronts Shepard.</li><li>Sovereign is revealed as a Reaper.</li></ul>
  <table class="wikitable infobox">stat table</table>
  <div id="References"><ol class="references"><li>ref one</li></ol></div>
  <script>tracking()</script>
</div>
```

Create `tests/test_clean_md.py`:
```python
from pathlib import Path

from scripts import clean_md

FIXTURES = Path(__file__).parent / "fixtures"


def test_clean_html_keeps_prose_drops_chrome():
    html = (FIXTURES / "html" / "virmire.html").read_text()
    md = clean_md.clean_html(html)
    assert "Virmire is a planet in the Sentry Omega cluster." in md
    assert "## Mission" in md
    assert "Commander Shepard assaults Saren's base." in md
    assert "- Wrex confronts Shepard." in md
    # chrome removed
    assert "nav junk" not in md
    assert "Planet stats" not in md
    assert "[edit]" not in md
    assert "stat table" not in md
    assert "ref one" not in md
    assert "tracking()" not in md
    assert "Contents" not in md


def test_infer_type():
    assert clean_md.infer_type(["Missions", "Mass Effect"]) == "mission"
    assert clean_md.infer_type(["Characters", "Turians"]) == "character"
    assert clean_md.infer_type(["Species"]) == "species"
    assert clean_md.infer_type(["Codex"]) == "lore"
    assert clean_md.infer_type(["Timeline"]) == "timeline"
    assert clean_md.infer_type(["Weapons", "Technology"]) == "tech"
    assert clean_md.infer_type(["Unknown bucket"]) == "lore"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_clean_md.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.clean_md'`.

- [ ] **Step 3: Implement `scripts/clean_md.py`**

```python
"""HTML -> clean markdown for wiki pages.

Chunk/quantity note lives in chunk.py; this module only strips page chrome
(navboxes, infoboxes, TOC, edit links, reference lists, scripts/styles) and
converts the remaining prose, headings, and lists to markdown.
"""
from __future__ import annotations

import sys

from bs4 import BeautifulSoup
from markdownify import markdownify as _md

_DROP_SELECTORS = [
    "script", "style", "sup.reference", ".mw-editsection", ".navbox", ".toc",
    ".portable-infobox", ".infobox", "aside", ".noprint", ".navigation-not-searchable",
    "table.wikitable", "table.infobox", "#References", "#Notes", ".references",
    ".reference", ".mw-empty-elt", ".gallery",
]

_TYPE_RULES = [
    ("mission", {"mission", "missions", "assignments"}),
    ("character", {"characters", "squad members", "individuals"}),
    ("species", {"species", "races"}),
    ("location", {"locations", "planets", "star systems", "clusters"}),
    ("tech", {"technology", "weapons", "armor", "equipment", "starships"}),
    ("faction", {"factions", "organizations", "governments", "military"}),
    ("timeline", {"timeline", "history"}),
    ("lore", {"codex", "lore"}),
]


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for sel in _DROP_SELECTORS:
        for node in soup.select(sel):
            node.decompose()
    md = _md(str(soup), heading_style="ATX", strip=["a"])
    lines = [ln.rstrip() for ln in md.splitlines()]
    out: list[str] = []
    for ln in lines:
        if not ln and out and not out[-1]:
            continue
        out.append(ln)
    return "\n".join(out).strip() + "\n"


def infer_type(categories: list[str]) -> str:
    lowered = {c.strip().lower() for c in categories}
    for type_name, keys in _TYPE_RULES:
        if lowered & keys:
            return type_name
    return "lore"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python scripts/clean_md.py <input.html>")
    print(clean_html(open(sys.argv[1], encoding="utf-8").read()))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_clean_md.py -v`
Expected: PASS (2 passed). If `markdownify` renders a list item as `* ` instead of `- `, add `bullets="-"` to the `_md(...)` call and re-run.

- [ ] **Step 5: Commit**

```bash
git add scripts/clean_md.py tests/test_clean_md.py tests/fixtures/html/virmire.html
git commit -m "feat: HTML to clean markdown converter"
```

---

### Task 3: Chunker (`scripts/chunk.py`)

**Files:**
- Create: `scripts/chunk.py`
- Create: `tests/test_chunk.py`

**Interfaces:**
- Consumes: `scripts.common.read_frontmatter_md`, `scripts.common.slugify`.
- Produces:
  - `split_into_chunks(body: str, *, size: int = 800, overlap: int = 120) -> list[tuple[str, str]]` — returns `(section_heading, chunk_text)` pairs; `section_heading` is the nearest preceding `#`/`##`/`###` heading text or `""`.
  - `chunk_page(path: pathlib.Path, *, size: int = 800, overlap: int = 120) -> list[dict]` — dicts with keys `chunk_id, page, section, game, text, url`.
  - `chunk_dir(pages_dir: pathlib.Path, out_path: pathlib.Path, *, size=800, overlap=120) -> int` — writes JSONL, returns chunk count.
  - CLI: `python scripts/chunk.py --pages data/pages --out data/chunks/chunks.jsonl [--size 800] [--overlap 120]`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_chunk.py`:
```python
import json
from pathlib import Path

from scripts import chunk, common


def _make_page(tmp_path, sentences, heading="Mission"):
    body = f"## {heading}\n\n" + " ".join(sentences) + "\n"
    p = tmp_path / "virmire.md"
    common.write_frontmatter_md(
        p,
        {"title": "Virmire", "game": "Mass Effect",
         "url": "https://masseffect.fandom.com/wiki/Virmire"},
        body,
    )
    return p


def test_split_respects_size_and_overlap():
    sentences = [f"Sentence number {i} about Virmire." for i in range(200)]
    body = "## Mission\n\n" + " ".join(sentences)
    chunks = chunk.split_into_chunks(body, size=50, overlap=10)
    assert len(chunks) > 1
    for _, text in chunks:
        assert common.word_count(text) <= 50 + 12  # size + one sentence slack
    # consecutive chunks share overlap text
    first_tail = chunks[0][1].split()[-5:]
    assert any(w in chunks[1][1] for w in first_tail)
    # every chunk carries the section heading
    assert all(h == "Mission" for h, _ in chunks)


def test_split_drops_no_text():
    body = "## A\n\n" + " ".join(f"Word{i} here now." for i in range(120))
    joined = " ".join(t for _, t in chunk.split_into_chunks(body, size=30, overlap=0))
    for i in range(120):
        assert f"Word{i}" in joined


def test_chunk_page_ids_and_metadata(tmp_path):
    p = _make_page(tmp_path, [f"Fact {i} about the mission." for i in range(90)])
    rows = chunk.chunk_page(p, size=40, overlap=8)
    assert rows[0]["chunk_id"] == "virmire_001"
    assert rows[1]["chunk_id"] == "virmire_002"
    assert rows[0]["page"] == "Virmire"
    assert rows[0]["game"] == "Mass Effect"
    assert rows[0]["section"] == "Mission"
    assert rows[0]["url"].endswith("/Virmire")


def test_chunk_dir_writes_jsonl(tmp_path):
    _make_page(tmp_path, [f"Sentence {i}." for i in range(60)])
    out = tmp_path / "chunks.jsonl"
    n = chunk.chunk_dir(tmp_path, out, size=40, overlap=8)
    lines = out.read_text().strip().splitlines()
    assert n == len(lines) >= 1
    assert json.loads(lines[0])["chunk_id"].startswith("virmire_")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_chunk.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.chunk'`.

- [ ] **Step 3: Implement `scripts/chunk.py`**

```python
"""Split cleaned pages into overlapping, sentence-aware chunks.

Sizes are WORD counts (see plan Global Constraints): ~1 word = ~1.3 tokens,
so the default 800-word chunk is ~1040 tokens, within the spec's 500-1000
token target band.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from scripts import common

_HEADING = re.compile(r"^#{1,3}\s+(.*)$")
_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")


def _sentences(paragraph: str) -> list[str]:
    return [s.strip() for s in _SENT.split(paragraph.strip()) if s.strip()]


def split_into_chunks(body: str, *, size: int = 800, overlap: int = 120):
    out: list[tuple[str, str]] = []
    section = ""
    cur: list[str] = []
    cur_words = 0

    def flush():
        nonlocal cur, cur_words
        if cur:
            out.append((section, " ".join(cur).strip()))
        cur, cur_words = [], 0

    for raw_line in body.splitlines():
        m = _HEADING.match(raw_line.strip())
        if m:
            flush()
            section = m.group(1).strip()
            continue
        if not raw_line.strip():
            continue
        for sent in _sentences(raw_line):
            w = common.word_count(sent)
            if cur_words + w > size and cur:
                out.append((section, " ".join(cur).strip()))
                keep, kept_words = [], 0
                for s in reversed(cur):
                    sw = common.word_count(s)
                    if kept_words + sw > overlap:
                        break
                    keep.insert(0, s)
                    kept_words += sw
                cur, cur_words = keep, kept_words
            cur.append(sent)
            cur_words += w
    flush()
    return out


def chunk_page(path: Path, *, size: int = 800, overlap: int = 120) -> list[dict]:
    fm, body = common.read_frontmatter_md(path)
    slug = common.slugify(fm.get("title", path.stem))
    rows = []
    for i, (section, text) in enumerate(split_into_chunks(body, size=size, overlap=overlap), start=1):
        rows.append({
            "chunk_id": f"{slug}_{i:03d}",
            "page": fm.get("title", path.stem),
            "section": section,
            "game": fm.get("game", ""),
            "text": text,
            "url": fm.get("url", ""),
        })
    return rows


def chunk_dir(pages_dir: Path, out_path: Path, *, size: int = 800, overlap: int = 120) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with out_path.open("w", encoding="utf-8") as fh:
        for p in sorted(Path(pages_dir).glob("*.md")):
            for row in chunk_page(p, size=size, overlap=overlap):
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                total += 1
    return total


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Chunk cleaned pages into chunks.jsonl")
    ap.add_argument("--pages", type=Path, default=Path("data/pages"))
    ap.add_argument("--out", type=Path, default=Path("data/chunks/chunks.jsonl"))
    ap.add_argument("--size", type=int, default=800)
    ap.add_argument("--overlap", type=int, default=120)
    a = ap.parse_args()
    n = chunk_dir(a.pages, a.out, size=a.size, overlap=a.overlap)
    print(f"wrote {n} chunks to {a.out}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_chunk.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add scripts/chunk.py tests/test_chunk.py
git commit -m "feat: sentence-aware page chunker"
```

---

### Task 4: BM25 index build and retrieval (`scripts/build_bm25.py`, `scripts/retrieve.py`)

**Files:**
- Create: `scripts/build_bm25.py`
- Create: `scripts/retrieve.py`
- Create: `tests/test_retrieve.py`

**Interfaces:**
- Consumes: `chunks.jsonl` produced by Task 3.
- Produces:
  - `build_bm25.build(chunks_path: pathlib.Path, index_path: pathlib.Path) -> int` — writes a pickle `{"chunks": [chunk dict, ...], "tokenized": [[str, ...], ...]}`, returns chunk count.
  - `build_bm25.tokenize(text: str) -> list[str]` — `re.findall(r"[a-z0-9']+", text.lower())`.
  - `retrieve.load_index(index_path: pathlib.Path) -> tuple[BM25Okapi, list[dict]]`.
  - `retrieve.retrieve(index_path: pathlib.Path, queries: list[str], *, k: int = 6) -> list[dict]` — per query take top `k` by score; union across queries; dedup by `chunk_id` keeping max score; each returned dict is the chunk dict plus `"score": float`; sorted by score desc.
  - CLI: `python scripts/retrieve.py --index data/bm25_index.pkl --k 6 "query one" "query two"` prints a JSON array to stdout.

- [ ] **Step 1: Write the failing test**

Create `tests/test_retrieve.py`:
```python
import json
from pathlib import Path

from scripts import build_bm25, retrieve


def _write_chunks(path: Path):
    rows = [
        {"chunk_id": "sovereign_001", "page": "Sovereign", "section": "History",
         "game": "Mass Effect", "url": "u", "text": "Sovereign is a Reaper that manipulated Saren."},
        {"chunk_id": "virmire_003", "page": "Virmire", "section": "Mission",
         "game": "Mass Effect", "url": "u", "text": "On Virmire Wrex confronts Shepard about the genophage cure."},
        {"chunk_id": "rachni_001", "page": "Rachni", "section": "Overview",
         "game": "Mass Effect", "url": "u", "text": "The rachni queen speaks through an asari body."},
    ]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def test_build_then_retrieve_known_query(tmp_path):
    chunks = tmp_path / "chunks.jsonl"
    index = tmp_path / "bm25_index.pkl"
    _write_chunks(chunks)
    assert build_bm25.build(chunks, index) == 3

    hits = retrieve.retrieve(index, ["Sovereign Reaper"], k=1)
    assert hits[0]["chunk_id"] == "sovereign_001"
    assert "score" in hits[0]


def test_retrieve_dedups_across_queries(tmp_path):
    chunks = tmp_path / "chunks.jsonl"
    index = tmp_path / "bm25_index.pkl"
    _write_chunks(chunks)
    build_bm25.build(chunks, index)
    hits = retrieve.retrieve(index, ["Virmire Wrex", "Wrex genophage"], k=2)
    ids = [h["chunk_id"] for h in hits]
    assert ids.count("virmire_003") == 1
    assert ids == sorted(set(ids), key=lambda i: -[h for h in hits if h["chunk_id"] == i][0]["score"])


def test_tokenize():
    assert build_bm25.tokenize("Sovereign's Reaper-tech!") == ["sovereign's", "reaper", "tech"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_retrieve.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.build_bm25'`.

- [ ] **Step 3: Implement `scripts/build_bm25.py`**

```python
"""Build a BM25 keyword index over chunks.jsonl."""
from __future__ import annotations

import argparse
import json
import pickle
import re
from pathlib import Path

_TOKEN = re.compile(r"[a-z0-9']+")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def build(chunks_path: Path, index_path: Path) -> int:
    chunks: list[dict] = []
    with Path(chunks_path).open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    tokenized = [tokenize(c["text"]) for c in chunks]
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with Path(index_path).open("wb") as fh:
        pickle.dump({"chunks": chunks, "tokenized": tokenized}, fh)
    return len(chunks)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build BM25 index from chunks.jsonl")
    ap.add_argument("--chunks", type=Path, default=Path("data/chunks/chunks.jsonl"))
    ap.add_argument("--out", type=Path, default=Path("data/bm25_index.pkl"))
    a = ap.parse_args()
    n = build(a.chunks, a.out)
    print(f"indexed {n} chunks -> {a.out}")
```

- [ ] **Step 4: Implement `scripts/retrieve.py`**

```python
"""Query the BM25 index for grounding chunks."""
from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi

from scripts.build_bm25 import tokenize


def load_index(index_path: Path):
    with Path(index_path).open("rb") as fh:
        data = pickle.load(fh)
    return BM25Okapi(data["tokenized"]), data["chunks"]


def retrieve(index_path: Path, queries: list[str], *, k: int = 6) -> list[dict]:
    bm25, chunks = load_index(index_path)
    best: dict[str, dict] = {}
    for q in queries:
        scores = bm25.get_scores(tokenize(q))
        ranked = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)[:k]
        for i in ranked:
            if scores[i] <= 0:
                continue
            row = dict(chunks[i], score=float(scores[i]))
            prev = best.get(row["chunk_id"])
            if prev is None or row["score"] > prev["score"]:
                best[row["chunk_id"]] = row
    return sorted(best.values(), key=lambda r: r["score"], reverse=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Retrieve top chunks for one or more queries")
    ap.add_argument("--index", type=Path, default=Path("data/bm25_index.pkl"))
    ap.add_argument("--k", type=int, default=6)
    ap.add_argument("queries", nargs="+")
    a = ap.parse_args()
    print(json.dumps(retrieve(a.index, a.queries, k=a.k), ensure_ascii=False, indent=2))
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/test_retrieve.py -v`
Expected: PASS (3 passed).

- [ ] **Step 6: Commit**

```bash
git add scripts/build_bm25.py scripts/retrieve.py tests/test_retrieve.py
git commit -m "feat: BM25 index build and retrieval CLI"
```

---

### Task 5: Wiki scraper (`scripts/scrape_wiki.py`)

**Files:**
- Create: `scripts/scrape_wiki.py`
- Create: `tests/test_scrape_wiki.py`

**Interfaces:**
- Consumes: `scripts.clean_md.clean_html`, `scripts.clean_md.infer_type`, `scripts.common.slugify`, `scripts.common.write_frontmatter_md`.
- Produces:
  - `PageData` dataclass: `title: str`, `url: str`, `game: str`, `type: str`, `characters: list[str]`, `html: str`, `links: list[str]`.
  - `crawl(seeds: list[str], *, depth: int, cap: int, fetch: Callable[[str], PageData | None], errors: list[str]) -> list[PageData]` — breadth-first from seeds, following `.links`, dedup by title, stop at `cap` pages; a seed/title whose `fetch` returns `None` is appended to `errors` and skipped.
  - `parse_page_response(title: str, api_json: dict) -> PageData` — build `PageData` from a MediaWiki `action=parse` response (`parse.text["*"]`, `parse.links`, `parse.categories`); resolves nothing (redirects handled by the live fetcher via `redirects=1`).
  - `game_from_categories(categories: list[str]) -> str` — `"Mass Effect 2"` / `"Mass Effect 3"` / `"Mass Effect"` (default).
  - `characters_from_categories(categories: list[str]) -> list[str]` — currently returns `[]`; placeholder kept so the frontmatter key always exists. (Character extraction is the summarizer subagent's job in Task 10.)
  - `write_page(page: PageData, pages_dir: pathlib.Path, *, force: bool) -> bool` — write cleaned markdown + frontmatter to `pages_dir/<slug>.md`; return `False` (skipped) if file exists, is non-empty, and `not force`; flag `< 200` chars of cleaned prose by appending to a module-level warning list and skip writing empty output.
  - `live_fetch(title: str, session, rate: float) -> PageData | None` — real HTTP fetcher; sleeps `rate` seconds, 3 retries with exponential backoff, returns `None` on final failure.
  - CLI: `python scripts/scrape_wiki.py [--seeds config/seeds.yaml] [--depth 2] [--cap 600] [--rate 0.5] [--force] [--pages data/pages]`. Reads `seeds.yaml` shape `{cap: int, depth: int, rate: float, seeds: [str, ...]}` (CLI flags override file values). Writes `data/scrape_errors.log`. Prints a summary line.

- [ ] **Step 1: Write the failing test**

Create `tests/test_scrape_wiki.py`:
```python
from pathlib import Path

from scripts import scrape_wiki
from scripts.scrape_wiki import PageData


def _page(title, links=(), game="Mass Effect"):
    return PageData(title=title, url=f"https://masseffect.fandom.com/wiki/{title}",
                    game=game, type="lore", characters=[], html=f"<p>{title} body text.</p>",
                    links=list(links))


def test_crawl_respects_depth():
    graph = {
        "Virmire": _page("Virmire", links=["Saren", "Sovereign"]),
        "Saren": _page("Saren", links=["Sovereign", "Benezia"]),
        "Sovereign": _page("Sovereign", links=["Reapers"]),
        "Benezia": _page("Benezia"),
        "Reapers": _page("Reapers"),
    }
    errors: list[str] = []
    got = scrape_wiki.crawl(["Virmire"], depth=1, cap=100, fetch=graph.get, errors=errors)
    titles = {p.title for p in got}
    assert titles == {"Virmire", "Saren", "Sovereign"}  # depth 1 = seed + direct links
    assert errors == []


def test_crawl_respects_cap():
    graph = {f"P{i}": _page(f"P{i}", links=[f"P{i+1}"]) for i in range(20)}
    got = scrape_wiki.crawl(["P0"], depth=10, cap=5, fetch=graph.get, errors=[])
    assert len(got) == 5


def test_crawl_records_fetch_failures():
    graph = {"Virmire": _page("Virmire", links=["Missing"])}
    errors: list[str] = []
    got = scrape_wiki.crawl(["Virmire"], depth=1, cap=100, fetch=graph.get, errors=errors)
    assert {p.title for p in got} == {"Virmire"}
    assert errors == ["Missing"]


def test_parse_page_response():
    api = {"parse": {
        "title": "Virmire",
        "text": {"*": "<p>Virmire is a planet.</p>"},
        "links": [{"ns": 0, "*": "Saren", "exists": ""}, {"ns": 14, "*": "Category:Missions"}],
        "categories": [{"*": "Missions"}, {"*": "Mass_Effect_2"}],
    }}
    pd = scrape_wiki.parse_page_response("Virmire", api)
    assert pd.title == "Virmire"
    assert pd.type == "mission"
    assert pd.game == "Mass Effect 2"
    assert pd.links == ["Saren"]  # ns 0 only


def test_write_page_skips_existing(tmp_path):
    pd = _page("Virmire")
    assert scrape_wiki.write_page(pd, tmp_path, force=False) is True
    assert scrape_wiki.write_page(pd, tmp_path, force=False) is False
    assert scrape_wiki.write_page(pd, tmp_path, force=True) is True
    assert (tmp_path / "virmire.md").read_text().startswith("---")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_scrape_wiki.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.scrape_wiki'`.

- [ ] **Step 3: Implement `scripts/scrape_wiki.py`**

```python
"""Crawl the Mass Effect Fandom wiki into data/pages/*.md via the MediaWiki API."""
from __future__ import annotations

import argparse
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import requests
import yaml

from scripts import common
from scripts.clean_md import clean_html, infer_type

API = "https://masseffect.fandom.com/api.php"
UA = "mass-effect-narrator/0.1 (personal project)"
_short_pages: list[str] = []


@dataclass
class PageData:
    title: str
    url: str
    game: str
    type: str
    characters: list[str]
    html: str
    links: list[str] = field(default_factory=list)


def game_from_categories(categories: list[str]) -> str:
    joined = " ".join(c.lower().replace("_", " ") for c in categories)
    if "mass effect 3" in joined:
        return "Mass Effect 3"
    if "mass effect 2" in joined:
        return "Mass Effect 2"
    return "Mass Effect"


def characters_from_categories(categories: list[str]) -> list[str]:
    return []


def parse_page_response(title: str, api_json: dict) -> PageData:
    parse = api_json["parse"]
    cats = [c["*"] for c in parse.get("categories", [])]
    links = [l["*"] for l in parse.get("links", []) if l.get("ns") == 0]
    real_title = parse.get("title", title)
    return PageData(
        title=real_title,
        url=f"https://masseffect.fandom.com/wiki/{real_title.replace(' ', '_')}",
        game=game_from_categories(cats),
        type=infer_type(cats),
        characters=characters_from_categories(cats),
        html=parse.get("text", {}).get("*", ""),
        links=links,
    )


def live_fetch(title: str, session: requests.Session, rate: float) -> PageData | None:
    params = {"action": "parse", "page": title, "prop": "text|links|categories",
              "redirects": 1, "format": "json", "formatversion": 1}
    for attempt in range(3):
        try:
            time.sleep(rate)
            r = session.get(API, params=params, headers={"User-Agent": UA}, timeout=30)
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                return None
            return parse_page_response(title, data)
        except (requests.RequestException, ValueError):
            time.sleep(rate * (2 ** attempt))
    return None


def crawl(seeds: list[str], *, depth: int, cap: int,
          fetch: Callable[[str], PageData | None], errors: list[str]) -> list[PageData]:
    seen: set[str] = set()
    out: list[PageData] = []
    queue: deque[tuple[str, int]] = deque((s, 0) for s in seeds)
    while queue and len(out) < cap:
        title, d = queue.popleft()
        if title in seen:
            continue
        seen.add(title)
        page = fetch(title)
        if page is None:
            errors.append(title)
            continue
        out.append(page)
        if d < depth:
            for link in page.links:
                if link not in seen:
                    queue.append((link, d + 1))
    return out


def write_page(page: PageData, pages_dir: Path, *, force: bool) -> bool:
    pages_dir = Path(pages_dir)
    pages_dir.mkdir(parents=True, exist_ok=True)
    dest = pages_dir / f"{common.slugify(page.title)}.md"
    if dest.exists() and dest.stat().st_size > 0 and not force:
        return False
    body = clean_html(page.html)
    if len(body.strip()) < 200:
        _short_pages.append(page.title)
        if not body.strip():
            return False
    common.write_frontmatter_md(dest, {
        "title": page.title, "url": page.url, "game": page.game, "type": page.type,
        "characters": page.characters, "scraped": time.strftime("%Y-%m-%d"),
    }, body)
    return True


def _load_seeds(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Scrape the Mass Effect wiki")
    ap.add_argument("--seeds", type=Path, default=Path("config/seeds.yaml"))
    ap.add_argument("--depth", type=int)
    ap.add_argument("--cap", type=int)
    ap.add_argument("--rate", type=float)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--pages", type=Path, default=Path("data/pages"))
    a = ap.parse_args()

    cfg = _load_seeds(a.seeds)
    depth = a.depth if a.depth is not None else cfg.get("depth", 2)
    cap = a.cap if a.cap is not None else cfg.get("cap", 600)
    rate = a.rate if a.rate is not None else cfg.get("rate", 0.5)
    seeds = cfg.get("seeds", [])

    session = requests.Session()
    errors: list[str] = []
    pages = crawl(seeds, depth=depth, cap=cap,
                  fetch=lambda t: live_fetch(t, session, rate), errors=errors)
    written = sum(write_page(p, a.pages, force=a.force) for p in pages)

    log = Path("data/scrape_errors.log")
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("\n".join(["FETCH FAILED: " + e for e in errors]
                             + ["SHORT/STUB: " + s for s in _short_pages]) + "\n")
    print(f"crawled {len(pages)} pages, wrote {written}, "
          f"{len(errors)} fetch errors, {len(_short_pages)} short pages "
          f"(see {log})")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_scrape_wiki.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add scripts/scrape_wiki.py tests/test_scrape_wiki.py
git commit -m "feat: MediaWiki wiki scraper with depth/cap crawl"
```

---

### Task 6: Run scaffolder (`scripts/new_run.py`)

**Files:**
- Create: `scripts/new_run.py`
- Create: `tests/test_new_run.py`

**Interfaces:**
- Consumes: `scripts.common.slugify`.
- Produces:
  - `new_run(narrator: str, themes: list[str], words: int, out_root: pathlib.Path) -> pathlib.Path` — creates `out_root/<narrator>_<theme-slug>_<YYYY-MM-DD>[_N]/` containing `outline.yaml` (first line the `# UNAPPROVED` marker, then `narrator`, `themes`, `target_words`, `sections: []`), an empty `sections/` dir, and `sources.json` with `{}`. Returns the run dir. If the base name exists, append `_2`, `_3`, …
  - CLI: `python scripts/new_run.py <narrator> "<themes>" [--words 8000] [--out output]` — prints the created path. `<themes>` is a comma-separated string.

- [ ] **Step 1: Write the failing test**

Create `tests/test_new_run.py`:
```python
import json

import yaml

from scripts import common, new_run


def test_new_run_creates_expected_shape(tmp_path):
    run = new_run.new_run("garrus", ["the cost of war", "loyalty"], 8000, tmp_path)
    assert run.parent == tmp_path
    assert run.name.startswith("garrus_the-cost-of-war-loyalty_")
    assert (run / "sections").is_dir()
    assert json.loads((run / "sources.json").read_text()) == {}

    text = (run / "outline.yaml").read_text()
    assert text.splitlines()[0].startswith("# UNAPPROVED")
    assert common.outline_is_approved(run) is False

    data = yaml.safe_load(text)
    assert data["narrator"] == "garrus"
    assert data["themes"] == ["the cost of war", "loyalty"]
    assert data["target_words"] == 8000
    assert data["sections"] == []


def test_new_run_disambiguates(tmp_path):
    a = new_run.new_run("garrus", ["war"], 8000, tmp_path)
    b = new_run.new_run("garrus", ["war"], 8000, tmp_path)
    assert a != b
    assert b.name.endswith("_2")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_new_run.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.new_run'`.

- [ ] **Step 3: Implement `scripts/new_run.py`**

```python
"""Scaffold an output/<run>/ folder for a generation run."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import yaml

from scripts import common

MARKER = "# UNAPPROVED — remove this line to approve the outline"


def new_run(narrator: str, themes: list[str], words: int, out_root: Path) -> Path:
    out_root = Path(out_root)
    base = f"{common.slugify(narrator)}_{common.slugify('-'.join(themes))}_{time.strftime('%Y-%m-%d')}"
    run = out_root / base
    n = 2
    while run.exists():
        run = out_root / f"{base}_{n}"
        n += 1
    (run / "sections").mkdir(parents=True)
    body = yaml.safe_dump(
        {"narrator": narrator, "themes": themes, "target_words": words, "sections": []},
        sort_keys=False, allow_unicode=True,
    )
    (run / "outline.yaml").write_text(f"{MARKER}\n{body}", encoding="utf-8")
    (run / "sources.json").write_text("{}\n", encoding="utf-8")
    return run


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Scaffold a generation run folder")
    ap.add_argument("narrator")
    ap.add_argument("themes", help="comma-separated theme list")
    ap.add_argument("--words", type=int, default=8000)
    ap.add_argument("--out", type=Path, default=Path("output"))
    a = ap.parse_args()
    themes = [t.strip() for t in a.themes.split(",") if t.strip()]
    print(new_run(a.narrator, themes, a.words, a.out))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_new_run.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add scripts/new_run.py tests/test_new_run.py
git commit -m "feat: generation run scaffolder"
```

---

### Task 7: Episode assembler (`scripts/assemble_episode.py`)

**Files:**
- Create: `scripts/assemble_episode.py`
- Create: `tests/test_assemble_episode.py`

**Interfaces:**
- Consumes: `scripts.common.outline_is_approved`, `scripts.common.word_count`; reads `outline.yaml` and `sections/<id>.md` in a run dir.
- Produces:
  - `assemble(run_dir: pathlib.Path) -> pathlib.Path` — raises `RuntimeError` if `not outline_is_approved(run_dir)`; raises `FileNotFoundError` listing every `outline.yaml` section id that has no `sections/<id>.md`; otherwise writes `episode.md` (header block + each section as `## <title>` followed by its file body, in outline order) and returns its path.
  - `header_block(outline: dict, total_words: int) -> str`.
  - CLI: `python scripts/assemble_episode.py <run_dir>` — prints the episode path and its word count.

- [ ] **Step 1: Write the failing test**

Create `tests/test_assemble_episode.py`:
```python
import pytest
import yaml

from scripts import assemble_episode


def _run(tmp_path, approved=True):
    run = tmp_path / "garrus_war_2026-08-27"
    (run / "sections").mkdir(parents=True)
    marker = "" if approved else "# UNAPPROVED\n"
    (run / "outline.yaml").write_text(marker + yaml.safe_dump({
        "narrator": "garrus", "themes": ["war"], "target_words": 20,
        "sections": [
            {"id": "intro", "title": "The Beginning", "events": [], "target_words": 10},
            {"id": "end", "title": "The End", "events": [], "target_words": 10},
        ],
    }, sort_keys=False))
    return run


def test_assemble_orders_sections_and_adds_header(tmp_path):
    run = _run(tmp_path)
    (run / "sections" / "intro.md").write_text("Humanity found the relay and everything changed forever.\n")
    (run / "sections" / "end.md").write_text("The Reapers fell and the galaxy exhaled at last.\n")
    ep = assemble_episode.assemble(run)
    text = ep.read_text()
    assert ep.name == "episode.md"
    assert text.index("## The Beginning") < text.index("## The End")
    assert "Garrus" in text.splitlines()[0]
    assert "Humanity found the relay" in text


def test_assemble_rejects_unapproved(tmp_path):
    run = _run(tmp_path, approved=False)
    (run / "sections" / "intro.md").write_text("x\n")
    (run / "sections" / "end.md").write_text("y\n")
    with pytest.raises(RuntimeError):
        assemble_episode.assemble(run)


def test_assemble_reports_missing_sections(tmp_path):
    run = _run(tmp_path)
    (run / "sections" / "intro.md").write_text("only intro here\n")
    with pytest.raises(FileNotFoundError) as exc:
        assemble_episode.assemble(run)
    assert "end" in str(exc.value)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_assemble_episode.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.assemble_episode'`.

- [ ] **Step 3: Implement `scripts/assemble_episode.py`**

```python
"""Concatenate approved section drafts into episode.md."""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import yaml

from scripts import common


def header_block(outline: dict, total_words: int) -> str:
    narrator = str(outline.get("narrator", "")).replace("_", " ").title()
    themes = ", ".join(outline.get("themes", []))
    return (f"# {narrator} — Mass Effect\n\n"
            f"_Themes: {themes} · ~{total_words} words · generated {time.strftime('%Y-%m-%d')}_\n")


def assemble(run_dir: Path) -> Path:
    run_dir = Path(run_dir)
    if not common.outline_is_approved(run_dir):
        raise RuntimeError(f"{run_dir}: outline.yaml is missing or still marked UNAPPROVED")
    outline = yaml.safe_load((run_dir / "outline.yaml").read_text(encoding="utf-8"))
    sections = outline.get("sections", [])
    missing = [s["id"] for s in sections if not (run_dir / "sections" / f"{s['id']}.md").exists()]
    if missing:
        raise FileNotFoundError(f"{run_dir}: missing section drafts: {missing}")

    bodies, total = [], 0
    for s in sections:
        text = (run_dir / "sections" / f"{s['id']}.md").read_text(encoding="utf-8").strip()
        total += common.word_count(text)
        bodies.append(f"## {s['title']}\n\n{text}\n")

    episode = run_dir / "episode.md"
    episode.write_text(header_block(outline, total) + "\n" + "\n".join(bodies), encoding="utf-8")
    return episode


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Assemble episode.md from section drafts")
    ap.add_argument("run_dir", type=Path)
    a = ap.parse_args()
    ep = assemble(a.run_dir)
    print(f"{ep} ({common.word_count(ep.read_text())} words)")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_assemble_episode.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add scripts/assemble_episode.py tests/test_assemble_episode.py
git commit -m "feat: episode assembler"
```

---

### Task 8: Starter config — seeds and the Garrus voice bible

**Files:**
- Create: `config/seeds.yaml`
- Create: `config/narrators/garrus.yaml`
- Create: `tests/test_config.py`

**Interfaces:**
- Consumes: nothing.
- Produces: two config files the commands and the smoke test read. Schema for a narrator bible: required keys `name, species, tone, diction, signature, avoid, knowledge_bias`; `tone`, `diction`, `signature`, `avoid` are lists; `knowledge_bias` is a non-empty string.

- [ ] **Step 1: Write the failing test**

Create `tests/test_config.py`:
```python
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
NARRATOR_KEYS = {"name", "species", "tone", "diction", "signature", "avoid", "knowledge_bias"}


def test_seeds_yaml_shape():
    cfg = yaml.safe_load((ROOT / "config" / "seeds.yaml").read_text())
    assert isinstance(cfg["seeds"], list) and cfg["seeds"]
    assert isinstance(cfg["depth"], int)
    assert isinstance(cfg["cap"], int)
    assert isinstance(cfg["rate"], (int, float))


def test_garrus_bible_shape():
    bible = yaml.safe_load((ROOT / "config" / "narrators" / "garrus.yaml").read_text())
    assert NARRATOR_KEYS <= set(bible)
    for k in ("tone", "diction", "signature", "avoid"):
        assert isinstance(bible[k], list) and bible[k]
    assert isinstance(bible["knowledge_bias"], str) and bible["knowledge_bias"].strip()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_config.py -v`
Expected: FAIL — `FileNotFoundError` for `config/seeds.yaml`.

- [ ] **Step 3: Create `config/seeds.yaml`**

```yaml
# Crawl parameters for scrape_wiki.py. CLI flags override these.
depth: 2
cap: 600
rate: 0.5   # seconds between requests

# Seed page titles. The crawler follows in-page links from these to `depth` hops.
seeds:
  - Timeline
  - Mass Effect (Original Trilogy)
  - Mass Effect
  - Mass Effect 2
  - Mass Effect 3
  - Commander Shepard
  - Reapers
  - Saren Arterius
  - Sovereign
  - Citadel
  - Systems Alliance
  - Council
  - Protheans
  - Mass Relay
  - Element Zero
  - Eden Prime
  - Virmire
  - Ilos
  - Battle of the Citadel
  - Collectors
  - Normandy SR-2
  - Lazarus Project
  - Omega
  - Suicide Mission
  - Genophage
  - Krogan
  - Turians
  - Asari
  - Salarians
  - Quarians
  - Geth
  - Rachni
  - Prothean
  - Crucible
  - Catalyst
  - Priority: Earth
  - Cerberus
  - The Illusive Man
```

- [ ] **Step 4: Create `config/narrators/garrus.yaml`**

```yaml
name: Garrus Vakarian
species: Turian
tone:
  - dry humor
  - tactical and precise
  - understated, never melodramatic
  - fiercely loyal to Shepard
  - visibly exasperated by bureaucracy and Council politics
diction:
  - military and marksman metaphors
  - short declarative sentences
  - occasional self-deprecation about his own choices
  - refers to Shepard by rank or name, never "the hero"
signature:
  - calibrations
avoid:
  - purple prose and sweeping cosmic narration
  - repeating "calibrations" more than once or twice in the whole script
  - breaking the fourth wall or addressing the audience as a podcast host
  - parody or exaggerated gruffness
knowledge_bias: >
  Weights front-line combat, C-Sec investigative work, his Archangel campaign on
  Omega, and the personal dynamics of the Normandy crew. Speaks with authority
  about things he witnessed; when covering galactic politics or events he was not
  present for, he frames them as secondhand ("the way I heard it") rather than
  narrating them as settled fact.
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/test_config.py -v`
Expected: PASS (2 passed).

- [ ] **Step 6: Commit**

```bash
git add config tests/test_config.py
git commit -m "feat: starter seeds and Garrus voice bible"
```

---

### Task 9: Deterministic-spine integration smoke test

**Files:**
- Create: `tests/fixtures/mini_corpus/eden-prime.md`
- Create: `tests/fixtures/mini_corpus/virmire.md`
- Create: `tests/fixtures/mini_corpus/sovereign.md`
- Create: `tests/fixtures/mini_timeline/eden_prime.yaml`
- Create: `tests/fixtures/mini_timeline/virmire_decision.yaml`
- Create: `tests/test_smoke_pipeline.py`

**Interfaces:**
- Consumes: `chunk`, `build_bm25`, `retrieve`, `new_run`, `assemble_episode`, `common` from Tasks 1–7.
- Produces: one end-to-end test proving the deterministic spine (chunk → index → retrieve → scaffold → assemble) works together on a realistic mini corpus. The subagent stages are exercised in Tasks 10–13; this test stands in for them by writing section files directly.

- [ ] **Step 1: Create the mini corpus fixtures**

`tests/fixtures/mini_corpus/eden-prime.md`:
```markdown
---
title: Eden Prime
url: https://masseffect.fandom.com/wiki/Eden_Prime
game: Mass Effect
type: mission
characters: [Shepard, Nihlus, Saren, Ashley]
scraped: 2026-08-27
---

## Attack

Eden Prime was a quiet human colony until the geth attacked without warning.
Commander Shepard was sent aboard the Normandy to recover a Prothean beacon.
Nihlus Kryik, a turian Spectre, was killed by Saren Arterius during the raid.
Ashley Williams, the sole survivor of her marine unit, joined Shepard on the ground.

## The Beacon

The Prothean beacon activated and forced a violent vision into Shepard's mind.
The vision showed synthetic machines harvesting organic civilizations.
This warning set Shepard on the hunt for Saren and the truth about the Reapers.
```

`tests/fixtures/mini_corpus/virmire.md`:
```markdown
---
title: Virmire
url: https://masseffect.fandom.com/wiki/Virmire
game: Mass Effect
type: mission
characters: [Shepard, Saren, Wrex, Ashley, Kaidan]
scraped: 2026-08-27
---

## Saren's Base

On Virmire, Shepard discovered that Saren had built a facility to cure the genophage
and breed a loyal krogan army. Urdnot Wrex confronted Shepard on the beach, furious
that the cure would be destroyed. The argument nearly turned lethal before Wrex stood down.

## The Bomb

The team armed a makeshift nuclear device to destroy the base. Holding the line cost
a life: one of Shepard's squadmates stayed behind and died in the blast. Sovereign
arrived during the escape, and it became clear the ship was itself a living Reaper.
```

`tests/fixtures/mini_corpus/sovereign.md`:
```markdown
---
title: Sovereign
url: https://masseffect.fandom.com/wiki/Sovereign
game: Mass Effect
type: tech
characters: [Saren, Shepard]
scraped: 2026-08-27
---

## Nature

Sovereign claimed to be a Reaper, a sentient starship the size of a dreadnought.
It described itself as the vanguard of a civilization that predates organic memory.
Saren believed he was Sovereign's partner; in truth he was being indoctrinated.

## The Battle of the Citadel

Sovereign seized the Citadel to open a relay for the waiting Reaper fleet.
Alliance forces destroyed Sovereign above the station, ending its assault
but proving to a skeptical Council that the Reaper threat was real.
```

- [ ] **Step 2: Create the mini timeline fixtures**

`tests/fixtures/mini_timeline/eden_prime.yaml`:
```yaml
event_id: eden_prime
title: The attack on Eden Prime
game: Mass Effect
chronological_order: 10
date: "2183 CE"
summary: >
  The geth attack Eden Prime. Shepard recovers a Prothean beacon, Nihlus is
  killed by Saren, and Ashley Williams joins the crew. The beacon's vision of
  machines harvesting organics begins the hunt for Saren.
characters: [Shepard, Nihlus, Saren, Ashley]
consequences:
  - Nihlus is killed by Saren
  - Shepard receives the Prothean warning vision
  - Ashley Williams joins the Normandy
source_chunks: []
```

`tests/fixtures/mini_timeline/virmire_decision.yaml`:
```yaml
event_id: virmire_decision
title: The Virmire mission
game: Mass Effect
chronological_order: 42
date: "2183 CE"
summary: >
  Shepard destroys Saren's genophage-cure and krogan-breeding facility on Virmire.
  Wrex confronts Shepard over the cure. One squadmate dies covering the bomb.
  Sovereign is revealed to be a living Reaper.
characters: [Shepard, Saren, Wrex, Ashley, Kaidan]
consequences:
  - Saren's research base is destroyed
  - One squadmate is left behind and killed
  - Sovereign is revealed as a Reaper
source_chunks: []
```

- [ ] **Step 3: Write the smoke test**

Create `tests/test_smoke_pipeline.py`:
```python
import shutil
from pathlib import Path

import yaml

from scripts import assemble_episode, build_bm25, chunk, common, new_run, retrieve

FIX = Path(__file__).parent / "fixtures"


def test_deterministic_spine(tmp_path):
    # 1. chunk the mini corpus
    chunks_path = tmp_path / "chunks.jsonl"
    n = chunk.chunk_dir(FIX / "mini_corpus", chunks_path, size=120, overlap=20)
    assert n >= 3

    # 2. build the BM25 index
    index = tmp_path / "bm25_index.pkl"
    assert build_bm25.build(chunks_path, index) == n

    # 3. retrieval finds the right page for a lore query
    hits = retrieve.retrieve(index, ["Sovereign Reaper Citadel"], k=3)
    assert hits and hits[0]["page"] == "Sovereign"

    # 4. load the hand-written timeline
    events = common.load_events(FIX / "mini_timeline")
    assert set(events) == {"eden_prime", "virmire_decision"}

    # 5. scaffold a run and hand-approve an outline built from the timeline
    run = new_run.new_run("garrus", ["the cost of war"], 200, tmp_path / "output")
    outline = {
        "narrator": "garrus", "themes": ["the cost of war"], "target_words": 200,
        "sections": [
            {"id": "eden_prime", "title": "Eden Prime", "events": ["eden_prime"], "target_words": 100},
            {"id": "virmire", "title": "Virmire", "events": ["virmire_decision"], "target_words": 100},
        ],
    }
    (run / "outline.yaml").write_text(yaml.safe_dump(outline, sort_keys=False))
    assert common.outline_is_approved(run)

    # 6. stand in for section-writer subagents, then assemble
    for s in outline["sections"]:
        ev = events[s["events"][0]]
        (run / "sections" / f"{s['id']}.md").write_text(ev["summary"].strip() + "\n")
    episode = assemble_episode.assemble(run)
    text = episode.read_text()
    assert text.index("## Eden Prime") < text.index("## Virmire")
    assert 120 <= common.word_count(text) <= 400
```

- [ ] **Step 4: Run the whole test suite**

Run: `python -m pytest -v`
Expected: PASS — every test from Tasks 1–9 green.

- [ ] **Step 5: Commit**

```bash
git add tests/fixtures/mini_corpus tests/fixtures/mini_timeline tests/test_smoke_pipeline.py
git commit -m "test: deterministic-spine integration smoke test"
```

---

### Task 10: Lore subagents — `page-summarizer` and `timeline-extractor`

**Files:**
- Create: `.claude/agents/page-summarizer.md`
- Create: `.claude/agents/timeline-extractor.md`
- Create: `tests/test_agent_defs.py`

**Interfaces:**
- Consumes: `data/pages/*.md`, `lore/manual/*.md`, `data/chunks/chunks.jsonl`.
- Produces: `page_summaries/<slug>.md`, `codex/*.md`, `timeline/events/<event_id>.yaml`, `timeline/master_timeline.yaml`. These agents are invoked by the commands in Task 11.
- Agent-definition contract: each file has YAML frontmatter with `name:` and `description:`, and a body containing the sections `## Inputs`, `## Outputs`, `## Rules`, `## Done when`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_agent_defs.py`:
```python
from pathlib import Path

import yaml

AGENTS = Path(__file__).parent.parent / ".claude" / "agents"
REQUIRED_SECTIONS = ("## Inputs", "## Outputs", "## Rules", "## Done when")
EXPECTED = {
    "page-summarizer", "timeline-extractor",
    "outline-writer", "section-writer", "smoother", "consistency-checker",
}


def _frontmatter(path: Path) -> dict:
    text = path.read_text()
    assert text.startswith("---\n"), f"{path}: no frontmatter"
    fm = text.split("---\n", 2)[1]
    return yaml.safe_load(fm)


def test_lore_agent_defs_present_and_well_formed():
    for name in ("page-summarizer", "timeline-extractor"):
        p = AGENTS / f"{name}.md"
        fm = _frontmatter(p)
        assert fm["name"] == name
        assert fm.get("description")
        body = p.read_text()
        for sec in REQUIRED_SECTIONS:
            assert sec in body, f"{p} missing {sec}"
```

(The `EXPECTED` set is used by the Task 12 test; leaving it here keeps one list of agent names.)

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_agent_defs.py -v`
Expected: FAIL — `AssertionError` / `FileNotFoundError` for `.claude/agents/page-summarizer.md`.

- [ ] **Step 3: Write `.claude/agents/page-summarizer.md`**

```markdown
---
name: page-summarizer
description: Summarize a batch of cleaned Mass Effect wiki pages into 200-500 word factual prose summaries, and contribute codex entries.
tools: Read, Write, Bash
---

You condense Mass Effect lore pages. You do not narrate, editorialize, or invent.

## Inputs
- A list of file paths under `data/pages/` and/or `lore/manual/` (given in the prompt, ~15 per invocation).
- Each file has YAML frontmatter (`title`, `url`, `game`, `type`, `characters`) and cleaned markdown prose.

## Outputs
- For each input page `data/pages/<slug>.md`, write `page_summaries/<slug>.md`:
  - Keep the same frontmatter keys (`title`, `url`, `game`, `type`), plus `characters:` — the actual named individuals you find in the prose.
  - Body: 200-500 words, plain prose, past tense, facts only. Cover who/what/when/where and consequences. No section headers.
- Append codex bullet points to the matching file in `codex/` — one of
  `species.md`, `tech.md`, `characters.md`, `factions.md`, `timeline.md` — chosen from the page `type`
  (`species`->species, `tech`->tech, `character`->characters, `faction`->factions,
  `timeline`->timeline, everything else->skip codex). Each bullet ends with `(source: <title>)`.
  Create the codex file with an `# <Group>` H1 if it does not exist.

## Rules
- Never state anything not supported by the page text.
- If a page is a disambiguation page or under ~150 words of real prose, write a one-line
  summary noting that and move on — do not pad.
- Skip a page that already has `page_summaries/<slug>.md` unless the prompt says `--force`.
- Preserve proper nouns exactly (Saren Arterius, Urdnot Wrex, Sovereign).

## Done when
- Every input page has a summary file (or a logged skip), the codex files have been
  appended to, and you have printed a one-line count of summaries written and skipped.
```

- [ ] **Step 4: Write `.claude/agents/timeline-extractor.md`**

```markdown
---
name: timeline-extractor
description: Derive a deduplicated, chronologically ordered event timeline (YAML) from the page summaries, linking each event to source chunk ids.
tools: Read, Write, Bash
---

You build the control-layer timeline for the whole original trilogy.

## Inputs
- All files in `page_summaries/`.
- `codex/timeline.md` for cross-checking dates and ordering.
- `data/chunks/chunks.jsonl` — to populate `source_chunks` (match by page title and topic).

## Outputs
- One file per distinct event: `timeline/events/<event_id>.yaml` with EXACTLY these keys:
  `event_id, title, game, chronological_order, date, summary, characters, consequences, source_chunks`.
  - `event_id`: slug of the title (lowercase, non-alphanumeric -> `-`).
  - `chronological_order`: integer, globally increasing across the trilogy. Leave gaps of 10 so events can be inserted later.
  - `summary`: 200-500 words, factual.
  - `consequences`: list of concrete outcomes.
  - `source_chunks`: list of `chunk_id`s from `chunks.jsonl` whose `page` and text match this event. Use
    `python scripts/retrieve.py --k 8 "<event title> <key characters>"` to find candidates, then keep the on-topic ids.
- `timeline/master_timeline.yaml`: a list of `{event_id, title, game, chronological_order}` sorted by `chronological_order`, no duplicates.

## Rules
- One event = one meaningful beat (a mission, a battle, a discovery, a death). Merge near-duplicates.
- Target 50-500 events across all three games; do not create an event per paragraph.
- If two summaries describe the same event, write ONE event file citing both source pages' chunks.
- Skip an event file that already exists unless the prompt says `--force`.
- Never invent dates. If a summary gives no date, estimate from surrounding events and set `date: "approx. <year> CE"`.

## Done when
- `timeline/master_timeline.yaml` exists, every id in it has an event file, `python -c "from scripts import common; common.load_events(__import__('pathlib').Path('timeline/events'))"` runs without error, and you have printed the event count.
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/test_agent_defs.py -v`
Expected: PASS (1 passed).

- [ ] **Step 6: Commit**

```bash
git add .claude/agents/page-summarizer.md .claude/agents/timeline-extractor.md tests/test_agent_defs.py
git commit -m "feat: page-summarizer and timeline-extractor subagents"
```

---

### Task 11: Lore commands — `/me-scrape`, `/me-build-lore`, `/me-build-timeline`

**Files:**
- Create: `.claude/commands/me-scrape.md`
- Create: `.claude/commands/me-build-lore.md`
- Create: `.claude/commands/me-build-timeline.md`
- Create: `tests/test_command_defs.py`

**Interfaces:**
- Consumes: the scripts from Tasks 3–5 and the subagents from Task 10.
- Produces: three slash commands. Contract: each file has YAML frontmatter with `description:`, and a body with numbered steps that a) run named scripts via Bash and/or b) dispatch a named subagent, plus a `## Verify` section.

- [ ] **Step 1: Write the failing test**

Create `tests/test_command_defs.py`:
```python
from pathlib import Path

import yaml

CMDS = Path(__file__).parent.parent / ".claude" / "commands"
EXPECTED = {"me-scrape", "me-build-lore", "me-build-timeline", "me-generate"}


def _frontmatter(path: Path) -> dict:
    text = path.read_text()
    assert text.startswith("---\n"), f"{path}: no frontmatter"
    return yaml.safe_load(text.split("---\n", 2)[1])


def test_lore_commands_present_and_reference_their_tools():
    checks = {
        "me-scrape": ["scripts/scrape_wiki.py", "scripts/chunk.py", "scripts/build_bm25.py"],
        "me-build-lore": ["page-summarizer"],
        "me-build-timeline": ["timeline-extractor"],
    }
    for name, needles in checks.items():
        p = CMDS / f"{name}.md"
        fm = _frontmatter(p)
        assert fm.get("description")
        body = p.read_text()
        assert "## Verify" in body
        for needle in needles:
            assert needle in body, f"{p} should mention {needle}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_command_defs.py -v`
Expected: FAIL — `FileNotFoundError` for `.claude/commands/me-scrape.md`.

- [ ] **Step 3: Write `.claude/commands/me-scrape.md`**

```markdown
---
description: Scrape the Mass Effect wiki into data/pages, then chunk and build the BM25 index.
---

Build or refresh the local lore corpus.

## Steps
1. Read `config/seeds.yaml` so you can report the depth/cap/rate that will be used.
2. Run the scraper (pass through any `--depth`, `--cap`, `--rate`, `--force` the user gave):
   `python scripts/scrape_wiki.py --seeds config/seeds.yaml $ARGUMENTS`
3. Show the summary line and the tail of `data/scrape_errors.log`.
4. Chunk the pages: `python scripts/chunk.py --pages data/pages --out data/chunks/chunks.jsonl`
5. Build the index: `python scripts/build_bm25.py --chunks data/chunks/chunks.jsonl --out data/bm25_index.pkl`

## Verify
- `ls data/pages | wc -l` is non-trivial (dozens+).
- `wc -l data/chunks/chunks.jsonl` > page count.
- `python scripts/retrieve.py --k 3 "Sovereign Reaper"` returns Sovereign-related chunks.
- Report counts for pages, chunks, fetch errors, and short/stub pages.
```

- [ ] **Step 4: Write `.claude/commands/me-build-lore.md`**

```markdown
---
description: Summarize every scraped page into page_summaries/ and build the codex/ via the page-summarizer subagent.
---

Turn the raw corpus into factual summaries and a codex.

## Steps
1. List pages needing summaries:
   `comm -23 <(ls data/pages | sed 's/.md$//' | sort) <(ls page_summaries 2>/dev/null | sed 's/.md$//' | sort)`
   (all pages if `--force` was given).
2. Split that list into batches of ~15.
3. For each batch, dispatch the `page-summarizer` subagent with the batch's file paths (and `--force` if given).
   Run batches sequentially; if one fails, retry it once, then log the batch to `data/lore_errors.log` and continue.
4. After all batches, report how many summaries exist vs. how many pages.

## Verify
- `ls page_summaries | wc -l` ≈ `ls data/pages | wc -l` (minus logged skips).
- `ls codex` shows the group files that apply to the corpus.
- Spot-read 2 summaries against their source pages for accuracy and length (200-500 words).
```

- [ ] **Step 5: Write `.claude/commands/me-build-timeline.md`**

```markdown
---
description: Derive timeline/events/*.yaml and master_timeline.yaml from the page summaries via the timeline-extractor subagent.
---

Build the control-layer timeline.

## Steps
1. Confirm `page_summaries/` is populated and `data/chunks/chunks.jsonl` exists; if not, tell the user to run `/me-build-lore` / `/me-scrape` first and stop.
2. Dispatch the `timeline-extractor` subagent (pass `--force` through if given).
3. When it returns, run the load check:
   `python -c "from pathlib import Path; from scripts import common; print(len(common.load_events(Path('timeline/events'))), 'events')"`
4. Report the event count and the first/last entries of `timeline/master_timeline.yaml`.

## Verify
- Every `event_id` in `master_timeline.yaml` has a matching `timeline/events/<id>.yaml`.
- `chronological_order` is strictly increasing in `master_timeline.yaml`.
- Event count is between 50 and 500.
- Spot-check 3 events: `source_chunks` ids exist in `chunks.jsonl` and are on-topic.
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python -m pytest tests/test_command_defs.py -v`
Expected: FAIL still — the test also expects `me-generate.md` (Task 13). Confirm the failure message names only `me-generate.md`. That is expected; proceed.

Then run: `python -m pytest tests/test_command_defs.py::test_lore_commands_present_and_reference_their_tools -v`
Expected: PASS (this subtest covers only the three lore commands).

- [ ] **Step 7: Commit**

```bash
git add .claude/commands/me-scrape.md .claude/commands/me-build-lore.md .claude/commands/me-build-timeline.md tests/test_command_defs.py
git commit -m "feat: me-scrape, me-build-lore, me-build-timeline commands"
```

---

### Task 12: Generation subagents — `outline-writer`, `section-writer`, `smoother`, `consistency-checker`

**Files:**
- Create: `.claude/agents/outline-writer.md`
- Create: `.claude/agents/section-writer.md`
- Create: `.claude/agents/smoother.md`
- Create: `.claude/agents/consistency-checker.md`
- Modify: `tests/test_agent_defs.py` (add a test that all six expected agents exist)

**Interfaces:**
- Consumes: `timeline/master_timeline.yaml`, `timeline/events/*.yaml`, `config/narrators/<narrator>.yaml`, `scripts/retrieve.py`, and a run dir under `output/`.
- Produces:
  - `outline-writer` → fills `output/<run>/outline.yaml` `sections:` list (each `{id, title, events, target_words}`), leaving the `# UNAPPROVED` marker in place.
  - `section-writer` → `output/<run>/sections/<id>.md` (prose only, no header) and updates `output/<run>/sources.json` with `{ "<id>": [chunk_id, ...] }` (and `"__warnings__": [...]` when retrieval was thin).
  - `smoother` → rewrites individual `sections/<id>.md` in place for continuity only.
  - `consistency-checker` → `output/<run>/issues.md` on the first pass, then patches offending `sections/<id>.md` files on the second.

- [ ] **Step 1: Write the failing test (extend `tests/test_agent_defs.py`)**

Append to `tests/test_agent_defs.py`:
```python
def test_all_six_agents_present_and_well_formed():
    for name in EXPECTED:
        p = AGENTS / f"{name}.md"
        fm = _frontmatter(p)
        assert fm["name"] == name
        assert fm.get("description")
        body = p.read_text()
        for sec in REQUIRED_SECTIONS:
            assert sec in body, f"{p} missing {sec}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_agent_defs.py::test_all_six_agents_present_and_well_formed -v`
Expected: FAIL — `FileNotFoundError` for `.claude/agents/outline-writer.md`.

- [ ] **Step 3: Write `.claude/agents/outline-writer.md`**

```markdown
---
name: outline-writer
description: Turn the master timeline plus user themes and a narrator voice bible into a section outline with word targets, for user approval.
tools: Read, Write, Bash
---

You plan the episode. You do not write prose.

## Inputs
- `timeline/master_timeline.yaml` and the referenced `timeline/events/*.yaml`.
- The run's `output/<run>/outline.yaml` (has `narrator`, `themes`, `target_words`; `sections: []`).
- `config/narrators/<narrator>.yaml` — especially `knowledge_bias`.

## Outputs
- Rewrite `output/<run>/outline.yaml` keeping the `# UNAPPROVED` first line, `narrator`, `themes`,
  `target_words`, and replacing `sections:` with an ordered list of
  `{id, title, events: [event_id, ...], target_words}`.

## Rules
- Cover the trilogy arc start to finish; do not stop at game 1.
- Choose and weight sections toward the `themes` and the narrator's `knowledge_bias`
  (a section the narrator would dwell on gets more words; one they'd gloss gets less or is cut).
- Every `events` entry must be a real `event_id` from `master_timeline.yaml`.
- `target_words` across all sections must sum to within 10% of `target_words`.
- 8-20 sections. Each `id` is a slug, unique within the outline.
- Do NOT remove the `# UNAPPROVED` line — the user removes it to approve.

## Done when
- `output/<run>/outline.yaml` parses as YAML, section word targets sum within 10% of target,
  every event id resolves, and you have printed the section count and the summed word target.
```

- [ ] **Step 4: Write `.claude/agents/section-writer.md`**

```markdown
---
name: section-writer
description: Write one narrated episode section in a specific narrator's voice, grounded strictly in the retrieved evidence and the section's timeline events.
tools: Read, Write, Bash
---

You write one section of the episode.

## Inputs
- The prompt names: the run dir, the section object (`id`, `title`, `events`, `target_words`), and the narrator.
- `config/narrators/<narrator>.yaml` — the voice bible.
- The section's events from `timeline/events/<event_id>.yaml` (use `summary` + `consequences` as the REQUIRED FACTS).
- Evidence: run
  `python scripts/retrieve.py --index data/bm25_index.pkl --k 6 "<title>" "<each character>" "<each consequence phrase>"`
  and use the returned chunk texts as your only source of detail beyond the event summaries.

## Outputs
- `output/<run>/sections/<id>.md` — prose only. No markdown headers, no "Narrator:" label, no bullet lists.
  Length within 15% of `target_words`.
- Update `output/<run>/sources.json`: set key `<id>` to the list of `chunk_id`s you actually used.
  If retrieval returned nothing usable, set `<id>` to `[]` and append a note to the `"__warnings__"` list
  ("thin sourcing: wrote from timeline summary only").

## Rules
- Include EVERY required fact from the section's events' `summary` and `consequences`.
- Invent no events, characters, dates, or outcomes. If the evidence is silent, stay silent.
- Use the narrator's `tone`/`diction`; honor `avoid`; use `signature` phrases at most once or twice per section.
- Respect `knowledge_bias`: frame events the narrator did not witness as secondhand.
- Write continuous narration a voice actor could read aloud.

## Done when
- `sections/<id>.md` exists at the right length, `sources.json` has an entry for `<id>`,
  and you have printed the word count and the chunk ids used.
```

- [ ] **Step 5: Write `.claude/agents/smoother.md`**

```markdown
---
name: smoother
description: Revise one episode section for continuity and transitions with its neighbors, without changing any facts or the narrator voice.
tools: Read, Write
---

You smooth transitions with a sliding window. You never restructure content.

## Inputs
- The prompt names the run dir and the section `id`.
- Read the previous section's last ~150 words, the full current section, and the next section's first ~150 words
  from `output/<run>/sections/`.

## Outputs
- Overwrite `output/<run>/sections/<id>.md` with a lightly revised version.

## Rules
- Only adjust the opening and closing sentences and obvious hard cuts so the section flows from the previous
  one and into the next.
- Do NOT add, remove, or alter facts, events, names, dates, or consequences.
- Do NOT change the narrator's voice or the section's length by more than ~5%.
- If the section already reads smoothly in context, leave it unchanged and say so.

## Done when
- The file is written (or explicitly left as-is) and you have printed a one-line note on what changed.
```

- [ ] **Step 6: Write `.claude/agents/consistency-checker.md`**

```markdown
---
name: consistency-checker
description: Audit the assembled sections for chronology errors, repetition, missing major events, voice drift, invented lore, and overlong sections; then patch the offenders.
tools: Read, Write, Bash
---

You run two passes: find, then fix.

## Inputs
- `output/<run>/outline.yaml`, all `output/<run>/sections/*.md`, `output/<run>/sources.json`.
- `timeline/master_timeline.yaml` and `config/narrators/<narrator>.yaml` for ground truth.

## Outputs
- Pass 1: write `output/<run>/issues.md` — a checklist grouped under the headings
  `Chronology`, `Repetition`, `Missing events`, `Voice drift`, `Invented lore`, `Length`.
  Each item names the section id and the specific problem. Write "none found" under a heading with no issues.
- Pass 2: for each fixable item, edit the named `sections/<id>.md` in place. Append a `## Fixes applied`
  section to `issues.md` listing what you changed.

## Rules
- "Invented lore" = any claim in a section not supported by that section's events or `sources.json` chunks. Flag every one.
- Do not fix by deletion alone if the fact is required by the outline's events — correct it instead.
- Keep every section within 15% of its `target_words` after fixing.
- Never introduce new facts to resolve an issue; if evidence is missing, soften the claim to what is supported.

## Done when
- `issues.md` has both the checklist and a `## Fixes applied` section, patched sections are written,
  and you have printed a count of issues found and fixed.
```

- [ ] **Step 7: Run tests to verify they pass**

Run: `python -m pytest tests/test_agent_defs.py -v`
Expected: PASS (2 passed).

- [ ] **Step 8: Commit**

```bash
git add .claude/agents/outline-writer.md .claude/agents/section-writer.md .claude/agents/smoother.md .claude/agents/consistency-checker.md tests/test_agent_defs.py
git commit -m "feat: generation subagents (outline, section, smoother, consistency)"
```

---

### Task 13: Generation command — `/me-generate` (outline phase and `--continue`)

**Files:**
- Create: `.claude/commands/me-generate.md`
- Modify: `tests/test_command_defs.py` (add `me-generate` coverage)

**Interfaces:**
- Consumes: `scripts/new_run.py`, `scripts/retrieve.py`, `scripts/assemble_episode.py`, `scripts/common.py` (`outline_is_approved`), and the four generation subagents from Task 12.
- Produces: the `/me-generate` slash command implementing the spec §6 Stage 3 flow, including the approval pause.

- [ ] **Step 1: Extend `tests/test_command_defs.py`**

Append:
```python
def test_me_generate_command():
    p = CMDS / "me-generate.md"
    fm = _frontmatter(p)
    assert fm.get("description")
    body = p.read_text()
    assert "## Verify" in body
    for needle in ("scripts/new_run.py", "outline-writer", "section-writer",
                   "smoother", "consistency-checker", "scripts/assemble_episode.py",
                   "--continue", "UNAPPROVED"):
        assert needle in body, f"me-generate.md should mention {needle}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_command_defs.py::test_me_generate_command -v`
Expected: FAIL — `FileNotFoundError` for `.claude/commands/me-generate.md`.

- [ ] **Step 3: Write `.claude/commands/me-generate.md`**

```markdown
---
description: Generate a narrated Mass Effect episode. First run produces an outline for approval; `--continue <run-dir>` writes the full script.
---

Usage:
- `/me-generate <narrator> "<theme1, theme2>" [--words 8000]` — outline phase (stops for approval).
- `/me-generate --continue <run-dir>` — generation phase.

## Outline phase
1. Require `timeline/master_timeline.yaml` and `data/bm25_index.pkl`. If missing, tell the user to run
   `/me-scrape`, `/me-build-lore`, `/me-build-timeline` and stop.
2. Require `config/narrators/<narrator>.yaml`. If missing, list the available bibles and stop.
3. Scaffold the run: `python scripts/new_run.py <narrator> "<themes>" --words <words>` and capture the printed path.
4. Dispatch the `outline-writer` subagent for that run dir.
5. Print the outline path and its section table. Tell the user:
   "Review and edit `output/<run>/outline.yaml`, then delete the first line (`# UNAPPROVED …`)
   and run `/me-generate --continue output/<run>`." STOP here.

## Generation phase (`--continue <run-dir>`)
1. Refuse unless
   `python -c "from pathlib import Path,sys; from scripts import common; sys.exit(0 if common.outline_is_approved(Path('<run-dir>')) else 1)"`
   exits 0. If it fails, tell the user the outline is still unapproved and stop.
2. For each section in `outline.yaml`, in order: dispatch `section-writer` with the run dir, that
   section object, and the narrator. Run sequentially. Retry a failed section once, then log to
   `output/<run>/gen_errors.log` and continue.
3. For each section in order, dispatch `smoother` with the run dir and section id.
4. Dispatch `consistency-checker` for the run dir (it does its own find-then-fix two passes).
5. Assemble: `python scripts/assemble_episode.py <run-dir>`.
6. Print the episode path, its word count vs. `target_words`, and the `issues.md` summary.

## Verify
- `output/<run>/episode.md` exists and is within 15% of `target_words`.
- `output/<run>/sources.json` has a non-empty entry (or an explicit `__warnings__` note) for every section.
- `output/<run>/issues.md` has a `## Fixes applied` section.
- Read the first and last 300 words aloud: the voice matches the narrator bible and nothing invented stands out.
```

- [ ] **Step 4: Run the command-def tests**

Run: `python -m pytest tests/test_command_defs.py -v`
Expected: PASS (2 passed — both the lore-commands test and the me-generate test).

- [ ] **Step 5: Commit**

```bash
git add .claude/commands/me-generate.md tests/test_command_defs.py
git commit -m "feat: me-generate command with outline approval gate"
```

---

### Task 14: README, full-suite check, and first real run

**Files:**
- Create: `README.md`
- Create: `lore/manual/.gitkeep`
- Modify: `docs/superpowers/specs/2026-08-27-mass-effect-narrator-design.md` (Status line only)

**Interfaces:**
- Consumes: everything.
- Produces: user-facing documentation and a verified first episode.

- [ ] **Step 1: Write `README.md`**

````markdown
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
| 4a. Outline | `/me-generate garrus "the cost of war, loyalty" --words 8000` | `output/<run>/outline.yaml` (**stops for approval**) |
| 4b. Approve | edit `outline.yaml`, delete the `# UNAPPROVED` first line | — |
| 4c. Write | `/me-generate --continue output/<run>` | `output/<run>/episode.md` (+ `sections/`, `sources.json`, `issues.md`) |

Hand-written lore goes in `lore/manual/*.md` with the same frontmatter as
`data/pages/` files; it is picked up by step 2.

## Adding a narrator

Copy `config/narrators/garrus.yaml` to `config/narrators/<name>.yaml` and rewrite
`tone`, `diction`, `signature`, `avoid`, and `knowledge_bias`. No code change.

## How it works

`docs/superpowers/specs/2026-08-27-mass-effect-narrator-design.md` has the full
design. Short version: the YAML timeline controls pacing and chronology, BM25
retrieval supplies grounding detail per section, and the narrator bible supplies
style. Deterministic steps are Python scripts in `scripts/`; reasoning steps are
Claude Code subagents in `.claude/agents/`.
````

- [ ] **Step 2: Run the full suite**

Run: `python -m pytest -v`
Expected: PASS — every test from Tasks 1–13.

- [ ] **Step 3: First real scrape (small)**

Run `/me-scrape --depth 1 --cap 60 --rate 0.5`. Confirm: dozens of pages in `data/pages/`, `chunks.jsonl` written, `retrieve.py` returns sane hits for `"Sovereign Reaper"` and `"Virmire Wrex"`. Inspect 3 cleaned pages for leftover chrome; if any selector leaked, add it to `_DROP_SELECTORS` in `scripts/clean_md.py`, re-run Task 2 tests, re-chunk, re-run `/me-scrape`.

- [ ] **Step 4: Build lore and timeline**

Run `/me-build-lore` then `/me-build-timeline` on the small corpus. Spot-check 2 summaries and 3 events per those commands' `## Verify` sections.

- [ ] **Step 5: First episode**

Run `/me-generate garrus "the cost of war, loyalty" --words 4000`. Review the outline, approve it, run `/me-generate --continue output/<run>`. Check `episode.md` against the command's `## Verify` list.

- [ ] **Step 6: Fact-preservation check (spec §8)**

In the finished run, copy one section file, edit the copy to state the wrong squadmate died on Virmire, overwrite the real section with it, then re-dispatch `consistency-checker` for the run dir. Confirm `issues.md` lists the injected contradiction under `Chronology` or `Invented lore` and that the fix pass corrects it. Restore the run afterward (or delete it).

- [ ] **Step 7: Flip the spec status and commit**

In `docs/superpowers/specs/2026-08-27-mass-effect-narrator-design.md` change the Status line to `Implemented`.

```bash
git add README.md lore/manual/.gitkeep docs/superpowers/specs/2026-08-27-mass-effect-narrator-design.md
git commit -m "docs: README and mark spec implemented"
```

---

## Self-Review

**1. Spec coverage:**

| Spec section | Task(s) |
|---|---|
| §3.1 deterministic vs reasoning split | Tasks 2–7 (scripts) vs 10, 12 (agents) |
| §3.2 control flow | Tasks 11, 13 (commands wire the stages) |
| §4 directory layout | Task 1 `.gitignore` + every task creates its spec'd paths |
| §5.1 page frontmatter | Task 2 (emit), Task 5 (write), Task 1 (`read/write_frontmatter_md`) |
| §5.2 chunk format | Task 3 |
| §5.3 timeline event YAML | Task 1 (`load_event` schema guard), Task 10 (`timeline-extractor` emits) |
| §5.4 narrator bible | Task 8 (Garrus + schema test), Task 12 (consumed) |
| §5.5 outline YAML | Task 6 (skeleton + marker), Task 12 (`outline-writer` fills) |
| §5.6 sources.json | Task 6 (init `{}`), Task 12 (`section-writer` writes), Task 9 asserts shape |
| §6 Stage 0 | Tasks 5, 3, 4, 11 |
| §6 Stage 1 | Tasks 10, 11 |
| §6 Stage 2 | Tasks 10, 11 |
| §6 Stage 3 | Tasks 6, 12, 13, 7 |
| §7 scrape errors (retry, log, redirects, missing seeds) | Task 5 (`live_fetch` retries, `crawl` errors list, `redirects=1`, error log) |
| §7 clean <200 chars flag | Task 5 (`write_page` short-page list) |
| §7 chunk/BM25 loud failure | Tasks 3, 4 (plain exceptions, no swallowing) |
| §7 subagent retry-once-then-log | Tasks 11 (`me-build-lore`), 13 (`--continue`) |
| §7 unapproved-outline guard | Task 1 (`outline_is_approved`), Task 6 (marker), Task 13 (refuse), Task 7 (assembler refuses) |
| §7 retrieve empty result | Task 12 (`section-writer` `__warnings__`), Task 13 verify |
| §8 unit tests | Tasks 2, 3, 4, 6, 7 |
| §8 integration smoke test | Task 9 (deterministic spine), Task 14 (full manual run) |
| §8 fact-preservation check | Task 14 Step 6 |
| §9 milestones | Tasks 1–9 (M1), 10–11 (M2), 12–13 (M3), 14 (M4) |
| §10 open questions | Task 3 (size/overlap defaults), Task 4 (k=6), Task 5 + Task 8 (seeds), Task 10 (batch ~15, codex in build-lore) |

No spec requirement is left without a task.

**2. Placeholder scan:** No "TBD"/"TODO"/"handle edge cases"/"similar to Task N". Every code step has real code; every markdown-artifact step has the full file content. The only deferred items are the spec's own §10 open questions, which are given concrete defaults here.

**3. Type consistency:** `slugify`, `read_frontmatter_md`/`write_frontmatter_md`, `load_event`/`load_events`, `outline_is_approved`, `word_count` (Task 1) are used with those exact names in Tasks 3, 5, 6, 7, 9, 11, 13. `build_bm25.tokenize` (Task 4) is imported by `retrieve.py` in the same task. `new_run.new_run(narrator, themes, words, out_root)` (Task 6) is called with that signature in Task 9. `assemble_episode.assemble(run_dir)` (Task 7) is called in Task 9. `chunk.chunk_dir(pages_dir, out_path, size=, overlap=)` (Task 3) is called in Task 9. Agent/command filenames in the test `EXPECTED`/`checks` sets (Tasks 10–13) match the files each task creates. `chunk_id` format is `<slug>_<NNN>` everywhere it appears.
