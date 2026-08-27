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
    md = _md(str(soup), heading_style="ATX", strip=["a"], bullets="-")
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
