"""Concatenate approved section drafts into episode.md."""
from __future__ import annotations

import argparse
import sys
import pathlib
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

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
