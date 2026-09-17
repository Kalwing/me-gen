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


def new_run(narrator: str, themes: list[str], words: int | None, out_root: Path,
            brief: str = "", form: str = "") -> Path:
    """Scaffold the run. ``words=None`` lets the form decide the episode's length.

    With a named form we can size it here, from the midpoint of that form's section range.
    Without one the outline-writer picks the form, so it computes the real figure once it
    knows how many sections it is writing; 0 is the placeholder meaning "not yet decided".
    """
    out_root = Path(out_root)
    if words is None:
        forms = common.load_forms()
        spec = forms.get(form) if form else None
        if spec:
            lo, hi = spec["section_count"]
            words = common.target_words_for(spec, round((lo + hi) / 2))
        else:
            words = 0
    base = f"{common.slugify(narrator)}_{common.slugify('-'.join(themes))}_{time.strftime('%Y-%m-%d')}"
    run = out_root / base
    n = 2
    while run.exists():
        run = out_root / f"{base}_{n}"
        n += 1
    (run / "sections").mkdir(parents=True)
    (run / "packs").mkdir()
    # `form` / `form_note` are placeholders the outline-writer fills — see config/forms.yaml.
    # They are scaffolded empty so the shape of an outline is visible before one is written.
    body = yaml.safe_dump(
        {"narrator": narrator, "themes": themes, "brief": brief,
         "form": form, "form_note": "",
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
    ap.add_argument("--words", type=int, default=None,
                    help="pin the episode length; omit to let the form decide "
                         "(words_per_section x section count, clamped — see config/forms.yaml)")
    ap.add_argument("--brief", default="",
                    help="free-text directorial note: scene, occasion, mood, who "
                         "the narrator is addressing (shapes framing, not canon)")
    ap.add_argument("--form", default="",
                    help="episode form id from config/forms.yaml; blank lets "
                         "outline-writer choose one")
    ap.add_argument("--out", type=Path, default=Path("output"))
    a = ap.parse_args()
    themes = [t.strip() for t in a.themes.split(",") if t.strip()]
    if a.form and a.form not in common.load_forms():
        raise SystemExit(f"unknown form {a.form!r}; known: {', '.join(common.load_forms())}")
    print(new_run(a.narrator, themes, a.words, a.out, brief=a.brief.strip(), form=a.form))
