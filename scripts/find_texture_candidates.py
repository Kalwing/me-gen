"""Deterministic, no-LLM keyword search over the scraped corpus for world-texture
content (culture/social/everyday codex categories), so only genuinely relevant pages
get sent to a page-summarizer agent instead of re-mining the whole corpus.

Usage:
    .venv/bin/python scripts/find_texture_candidates.py

Reads scripts/texture_keywords.txt, greps data/pages/*.md (+ lore/manual/*.md), and
cross-references codex/culture.md + codex/social.md + codex/everyday.md source
citations to mark each hit as already-covered or new. Writes
data/texture_candidates.tsv (slug, title, matched_keywords, skip_status, covered).
Safe to re-run any time — fully deterministic, no state to corrupt.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEYWORDS_FILE = ROOT / "scripts" / "texture_keywords.txt"
PAGES_DIRS = [ROOT / "data" / "pages", ROOT / "lore" / "manual"]
CODEX_FILES = [ROOT / "codex" / "culture.md", ROOT / "codex" / "social.md", ROOT / "codex" / "everyday.md"]
LORE_SKIPPED = ROOT / "data" / "lore_skipped.txt"
OUT_FILE = ROOT / "data" / "texture_candidates.tsv"

SOURCE_RE = re.compile(r"\(source:\s*([^)]+)\)")
TITLE_RE = re.compile(r"^title:\s*(.+)$", re.MULTILINE)


def load_keywords(path: Path) -> list[re.Pattern]:
    patterns = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if " " in line or "-" in line:
            # multi-word / hyphenated phrase: literal, case-insensitive
            patterns.append((line, re.compile(re.escape(line), re.IGNORECASE)))
        elif line.endswith("*"):
            # explicit prefix match, opt-in only (e.g. "discriminat*" -> -ion/-ory)
            stem = line[:-1]
            patterns.append((line, re.compile(r"\b" + re.escape(stem) + r"\w*", re.IGNORECASE)))
        else:
            # exact whole-word match — no silent prefix matching (avoids "art" hitting
            # "Arterius", "opera" hitting "operative", etc.)
            patterns.append((line, re.compile(r"\b" + re.escape(line) + r"\b", re.IGNORECASE)))
    return patterns


def load_covered_titles() -> set[str]:
    covered = set()
    for f in CODEX_FILES:
        if not f.exists():
            continue
        for m in SOURCE_RE.finditer(f.read_text(encoding="utf-8")):
            covered.add(m.group(1).strip().lower())
    return covered


def load_skipped() -> dict[str, str]:
    skipped = {}
    if LORE_SKIPPED.exists():
        for line in LORE_SKIPPED.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if parts:
                skipped[parts[0]] = parts[1] if len(parts) > 1 else "?"
    return skipped


def main() -> int:
    patterns = load_keywords(KEYWORDS_FILE)
    covered_titles = load_covered_titles()
    skipped = load_skipped()

    rows = []
    for pages_dir in PAGES_DIRS:
        if not pages_dir.exists():
            continue
        for p in sorted(pages_dir.glob("*.md")):
            if p.name == "README.md":
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            hits = sorted({kw for kw, pat in patterns if pat.search(text)})
            if not hits:
                continue
            slug = p.stem
            title_m = TITLE_RE.search(text)
            title = title_m.group(1).strip() if title_m else slug
            is_covered = title.strip().lower() in covered_titles
            skip_reason = skipped.get(slug, "")
            rows.append((slug, title, ",".join(hits), skip_reason, "yes" if is_covered else "no"))

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8") as f:
        f.write("slug\ttitle\tmatched_keywords\tskip_reason\talready_covered\n")
        for row in rows:
            f.write("\t".join(row) + "\n")

    total = len(rows)
    new_uncovered = sum(1 for r in rows if r[4] == "no" and not r[3])
    filtered = sum(1 for r in rows if r[3])
    already = sum(1 for r in rows if r[4] == "yes")
    print(f"{total} pages matched a texture keyword -> {OUT_FILE}")
    print(f"  {new_uncovered} new candidates (not filtered, not yet cited in culture/social/everyday.md)")
    print(f"  {already} already have a codex citation in one of those 3 files")
    print(f"  {filtered} are in data/lore_skipped.txt (review for false positives, e.g. Blasto)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
