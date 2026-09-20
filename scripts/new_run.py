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


def new_run(narrator: str | list[str], themes: list[str], words: int | None, out_root: Path,
            brief: str = "", form: str = "", subject: str = "") -> Path:
    """Scaffold the run. ``words=None`` lets the form decide the episode's length.

    ``narrator`` is one voice, or several for an episode whose sections alternate between
    them (``["tali", "liara"]``). The first is the episode's lead ``narrator:``; the full list
    goes to ``narrators:`` and the outline-writer assigns each section its speaker. A single
    voice writes no ``narrators:`` key, so a monologue outline is unchanged.

    ``subject`` is who the episode is about — the person every narrator addresses and
    characterizes. Blank means Shepard, which is what it has always been; naming someone
    else swaps which `config/narrators/<slug>.notes.md` the writers read in his place, so
    the file has to exist before a run is scaffolded around it.

    With a named form we can size it here, from the midpoint of that form's section range.
    Without one the outline-writer picks the form, so it computes the real figure once it
    knows how many sections it is writing; 0 is the placeholder meaning "not yet decided".
    """
    out_root = Path(out_root)
    voices = [narrator] if isinstance(narrator, str) else list(narrator)
    voices = [v.strip() for v in voices if v and v.strip()]
    if not voices:
        raise ValueError("at least one narrator is required")
    subject = (subject or "").strip().lower() or common.DEFAULT_SUBJECT
    notes = common.REPO_ROOT / common.subject_notes_rel(subject)
    if not notes.is_file():
        raise ValueError(
            f"no notes for subject {subject!r}: {common.subject_notes_rel(subject)} does not "
            f"exist. The subject is who the episode is about; write their notes file first.")
    if words is None:
        forms = common.load_forms()
        spec = forms.get(form) if form else None
        if spec:
            lo, hi = spec["section_count"]
            words = common.target_words_for(spec, round((lo + hi) / 2))
        else:
            words = 0
    base = f"{common.slugify('-'.join(voices))}_{common.slugify('-'.join(themes))}_{time.strftime('%Y-%m-%d')}"
    run = out_root / base
    n = 2
    while run.exists():
        run = out_root / f"{base}_{n}"
        n += 1
    (run / "sections").mkdir(parents=True)
    (run / "packs").mkdir()
    # `form` / `form_note` are placeholders the outline-writer fills — see config/forms.yaml.
    # They are scaffolded empty so the shape of an outline is visible before one is written.
    head: dict = {"narrator": voices[0]}
    if len(voices) > 1:
        head["narrators"] = voices
    body = yaml.safe_dump(
        {**head, "subject": subject, "themes": themes, "brief": brief,
         "form": form, "form_note": "",
         "target_words": words, "sections": []},
        sort_keys=False, allow_unicode=True,
    )
    (run / "outline.yaml").write_text(f"{MARKER}\n{body}", encoding="utf-8")
    (run / "sources.json").write_text("{}\n", encoding="utf-8")
    return run


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Scaffold a generation run folder")
    ap.add_argument("narrator", help="narrator id, or comma-separated ids for alternating voices")
    ap.add_argument("themes", help="comma-separated theme list")
    ap.add_argument("--words", type=int, default=None,
                    help="pin the episode length; omit to let the form decide "
                         "(words_per_section x section count, clamped — see config/forms.yaml)")
    ap.add_argument("--brief", default="",
                    help="free-text directorial note: scene, occasion, mood, who "
                         "the narrator is addressing (shapes framing, not canon)")
    ap.add_argument("--subject", default="",
                    help="who the episode is about — the person the narrators address "
                         "and characterize (default: shepard). Needs "
                         "config/narrators/<subject>.notes.md")
    ap.add_argument("--form", default="",
                    help="episode form id from config/forms.yaml; blank lets "
                         "outline-writer choose one")
    ap.add_argument("--out", type=Path, default=Path("output"))
    a = ap.parse_args()
    themes = [t.strip() for t in a.themes.split(",") if t.strip()]
    if a.form and a.form not in common.load_forms():
        raise SystemExit(f"unknown form {a.form!r}; known: {', '.join(common.load_forms())}")
    voices = [v.strip() for v in a.narrator.split(",") if v.strip()]
    try:
        run = new_run(voices if len(voices) > 1 else voices[0], themes, a.words, a.out,
                      brief=a.brief.strip(), form=a.form, subject=a.subject.strip())
    except ValueError as exc:
        raise SystemExit(str(exc))
    print(run)
