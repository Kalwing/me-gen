"""Concatenate tone-marked section drafts into episode.performance.md.

The performance pass is an overlay: bracketed cues are added, prose is not touched.
This script enforces that. For every section it strips the tags from the marked draft
and compares the result to the plain draft; any difference fails the build and names
the section, because a tone-marker that silently rewrote a line has corrupted an
already-approved episode.
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
import pathlib
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts import common

TAG = re.compile(r"\[[^\]\n]*\]")

DEFAULT_NOTE = (
    "Oral-tone annotation of `episode.md`, using Fish Audio S2-compatible tags. Bracketed cues "
    "are delivery direction for a voice performance; the prose between them is unchanged."
)


def strip_tags(text: str) -> str:
    """Text as it will be spoken: cues removed, whitespace normalised."""
    return re.sub(r"\s+", " ", TAG.sub("", text)).strip()


def narrator_default(narrator: str) -> str:
    """The `performance.default` line from the narrator bible, if it has one."""
    bible = Path("config/narrators") / f"{narrator}.yaml"
    if not bible.exists():
        return ""
    data = yaml.safe_load(bible.read_text(encoding="utf-8")) or {}
    return str((data.get("performance") or {}).get("default", "")).strip()


def header_block(outline: dict) -> str:
    narrator = common.voices_title(outline)
    themes = ", ".join(outline.get("themes", []))
    note = DEFAULT_NOTE
    voices = common.episode_narrators(outline)
    if len(voices) == 1:
        default = narrator_default(voices[0])
        if default:
            note += f" Default register is {default} Tags mark departures from that."
    else:
        defaults = [(common.display_name(v), narrator_default(v)) for v in voices]
        defaults = [f"{name}: {d}" for name, d in defaults if d]
        note += (" Each section heading names its speaker; switch voice there."
                 + (" Default registers — " + " ".join(defaults) if defaults else "")
                 + " Tags mark departures from each speaker's default.")
    return (f"# {narrator} — Mass Effect (performance script)\n\n"
            f"_Themes: {themes} · generated {time.strftime('%Y-%m-%d')}_\n\n"
            f"_{note}_\n")


def _is_subsequence(needle: list[str], haystack: list[str]) -> bool:
    """True if `needle`'s words appear in `haystack`, in order, with insertions allowed."""
    it = iter(haystack)
    return all(word in it for word in needle)


def verify(plain: str, marked: str, section_id: str) -> None:
    """The tone pass may only add bracketed cues and, sparingly, onomatopoeia words
    (a spelled-out laugh, sigh, breath, grunt) alongside a matching effect tag. It may
    never reorder, remove, or reword the source prose. We check that by requiring the
    plain source's words to appear, in order, inside the spoken (tag-stripped) text —
    insertions pass, deletions/reorders/rewording do not."""
    spoken, source = strip_tags(marked), strip_tags(plain)
    if spoken == source:
        return
    if _is_subsequence(source.split(), spoken.split()):
        return
    diff = [d for d in difflib.unified_diff(source.split(". "), spoken.split(". "), lineterm="", n=0)
            if d.startswith(("+", "-")) and not d.startswith(("+++", "---"))]
    raise RuntimeError(
        f"section '{section_id}': the tone pass changed the prose, not just the cues.\n"
        + "\n".join(f"  {d[:200]}" for d in diff[:10])
        + f"\n  ({len(diff)} differing fragments; the performance script is rejected)"
    )


def assemble(run_dir: Path) -> Path:
    run_dir = Path(run_dir)
    if not common.outline_is_approved(run_dir):
        raise RuntimeError(f"{run_dir}: outline.yaml is missing or still marked UNAPPROVED")
    outline = yaml.safe_load((run_dir / "outline.yaml").read_text(encoding="utf-8"))
    sections = outline.get("sections") or []

    missing = [s["id"] for s in sections
               if not (run_dir / "sections" / f"{s['id']}.performance.md").exists()]
    if missing:
        raise FileNotFoundError(
            f"{run_dir}: missing tone-marked drafts: {missing} — run the tone-marker pass first")

    bodies = []
    for s in sections:
        plain = (run_dir / "sections" / f"{s['id']}.md").read_text(encoding="utf-8").strip()
        marked = (run_dir / "sections" / f"{s['id']}.performance.md").read_text(encoding="utf-8").strip()
        verify(plain, marked, s["id"])
        bodies.append(f"{common.section_heading(outline, s)}\n\n{marked}\n")

    out = run_dir / "episode.performance.md"
    out.write_text(header_block(outline) + "\n" + "\n".join(bodies), encoding="utf-8")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Assemble episode.performance.md from tone-marked drafts")
    ap.add_argument("run_dir", type=Path)
    a = ap.parse_args()
    try:
        ep = assemble(a.run_dir)
    except RuntimeError as e:
        sys.exit(f"ERROR: {e}")
    text = ep.read_text(encoding="utf-8")
    print(f"{ep} ({len(TAG.findall(text))} cues over {common.word_count(strip_tags(text))} spoken words; "
          f"prose verified unchanged)")
