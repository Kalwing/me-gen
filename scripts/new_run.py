"""Scaffold an output/<run>/ folder for a generation run."""
from __future__ import annotations

import argparse
import sys
import pathlib
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from scripts import common

MARKER = "# UNAPPROVED — remove this line to approve the outline"


def new_run(narrator: str, themes: list[str], words: int, out_root: Path,
            brief: str = "") -> Path:
    out_root = Path(out_root)
    base = f"{common.slugify(narrator)}_{common.slugify('-'.join(themes))}_{time.strftime('%Y-%m-%d')}"
    run = out_root / base
    n = 2
    while run.exists():
        run = out_root / f"{base}_{n}"
        n += 1
    (run / "sections").mkdir(parents=True)
    body = yaml.safe_dump(
        {"narrator": narrator, "themes": themes, "brief": brief,
         "target_words": words, "sections": []},
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
    ap.add_argument("--brief", default="",
                    help="free-text directorial note: scene, occasion, mood, who "
                         "the narrator is addressing (shapes framing, not canon)")
    ap.add_argument("--out", type=Path, default=Path("output"))
    a = ap.parse_args()
    themes = [t.strip() for t in a.themes.split(",") if t.strip()]
    print(new_run(a.narrator, themes, a.words, a.out, brief=a.brief.strip()))
