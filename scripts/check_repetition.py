"""Flag phrases a narrator's sections repeat near-verbatim across one episode.

Each `section-writer` dispatch is stateless: it never sees what earlier sections in
the same episode already said. Left unchecked, a narrator converges on the same stock
line for a recurring need (a deflection, a verbal tic) simply because nothing told the
model it had already reached for that exact phrasing. This is a deterministic backstop
for `episode-auditor`'s `Staging` check, which a close read can miss on a paraphrase.

Method: normalize each section's prose, slide a fixed-width word window (a "shingle")
across it, and flag any shingle that recurs in two or more different sections — unless
it is one of the narrator's own declared `catchphrases` (config/narrators/<slug>.yaml),
which are allowed to recur on purpose. Shingles that are mostly stopwords are dropped;
they are grammatical glue, not a repeated line.

    python scripts/check_repetition.py output/<run>
    python scripts/check_repetition.py output/<run> --n 6 --check
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts import common

STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "but", "by", "did", "do", "does", "for",
    "he", "her", "him", "his", "i", "if", "in", "is", "it", "its", "me", "my",
    "no", "not", "of", "on", "or", "our", "said", "she", "so", "than", "that",
    "the", "their", "them", "then", "there", "they", "this", "to", "us", "was",
    "we", "were", "what", "when", "where", "who", "why", "with", "you", "your",
}

_WORD = re.compile(r"[a-z0-9']+")


def normalize_words(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def shingles(text: str, n: int) -> list[str]:
    words = normalize_words(text)
    return [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]


def is_flaggable(shingle: str, min_content_words: int = 2) -> bool:
    content = [w for w in shingle.split() if w not in STOPWORDS]
    return len(content) >= min_content_words


def load_catchphrases(narrator: str) -> list[str]:
    """A narrator's own declared recurring lines (opt-in, `catchphrases:` in their
    yaml bible) — these are allowed to repeat on purpose and never get flagged."""
    bible = common.REPO_ROOT / "config" / "narrators" / f"{narrator}.yaml"
    if not bible.exists():
        return []
    data = yaml.safe_load(bible.read_text(encoding="utf-8")) or {}
    return [str(p) for p in (data.get("catchphrases") or [])]


def _matches_catchphrase(shingle: str, catchphrase_word_sets: list[list[str]]) -> bool:
    words = shingle.split()
    return any(
        " ".join(cp) in " ".join(words) or " ".join(words) in " ".join(cp)
        for cp in catchphrase_word_sets
    )


def find_repeats(sections: dict[str, str], n: int = 5,
                  catchphrases: list[str] | None = None,
                  catchphrases_by_section: dict[str, list[str]] | None = None,
                  ) -> dict[str, list[str]]:
    """shingle -> sorted list of distinct section ids it appears in (only for
    shingles appearing in 2+ sections, excluding catchphrases and stopword-heavy
    shingles).

    `catchphrases` applies to every section. `catchphrases_by_section` adds a section's own
    speaker's lines on top: in a multi-voice episode one narrator's catchphrase is exempt in
    their turns, and still flagged if it turns up in the other voice's mouth.
    """
    catchphrase_words = [normalize_words(c) for c in (catchphrases or [])]
    per_section = {sid: catchphrase_words + [normalize_words(c) for c in cps]
                   for sid, cps in (catchphrases_by_section or {}).items()}
    locations: dict[str, set[str]] = {}
    offending: set[str] = set()
    for section_id, text in sections.items():
        exempt = per_section.get(section_id, catchphrase_words)
        for sh in set(shingles(text, n)):
            if not is_flaggable(sh):
                continue
            locations.setdefault(sh, set()).add(section_id)
            if not _matches_catchphrase(sh, exempt):
                offending.add(sh)
    # Every occurrence counts toward "2+ sections"; at least one must be outside its
    # speaker's catchphrases. A monologue exempts the same lines everywhere, so this is
    # the old rule there.
    return {sh: sorted(ids) for sh, ids in locations.items()
            if len(ids) >= 2 and sh in offending}


def _load_sections(run_dir: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted((run_dir / "sections").glob("*.md")):
        if p.name.endswith(".performance.md"):
            continue
        out[p.stem] = p.read_text(encoding="utf-8")
    return out


def check(run_dir: Path, narrator: str | None = None, n: int = 5) -> dict[str, list[str]]:
    run_dir = Path(run_dir)
    sections = _load_sections(run_dir)
    by_section: dict[str, list[str]] = {}
    if narrator is None:
        outline_path = run_dir / "outline.yaml"
        outline = (yaml.safe_load(outline_path.read_text(encoding="utf-8")) or {}
                   if outline_path.exists() else {})
        if common.is_multi_voice(outline):
            by_section = {s["id"]: load_catchphrases(common.section_narrator(outline, s))
                          for s in outline.get("sections") or []}
        else:
            narrator = outline.get("narrator")
    catchphrases = load_catchphrases(narrator) if narrator else []
    flags = find_repeats(sections, n=n, catchphrases=catchphrases,
                         catchphrases_by_section=by_section)
    write_report(run_dir, flags, n)
    return flags


def write_report(run_dir: Path, flags: dict[str, list[str]], n: int) -> None:
    lines = [f"# Repetition flags — {run_dir}\n",
             f"Deterministic {n}-word shingle scan. A narrator's own declared "
             f"`catchphrases` are excluded. Not every flag is a bug — judge each "
             f"against the narrator's voice before fixing.\n"]
    if not flags:
        lines.append("(none found)\n")
    else:
        for sh, ids in sorted(flags.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            lines.append(f"- \"{sh}\" — appears in: {', '.join(ids)} ({len(ids)} sections)")
    (run_dir / "repetition_flags.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Flag near-verbatim repeated phrases across one episode's sections")
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--narrator", default=None, help="Override the narrator read from outline.yaml")
    ap.add_argument("--n", type=int, default=5, help="Shingle width in words (default 5)")
    ap.add_argument("--check", action="store_true", help="Exit 1 if any repeats are flagged")
    a = ap.parse_args()
    found = check(a.run_dir, narrator=a.narrator, n=a.n)
    print(f"{a.run_dir}/repetition_flags.md ({len(found)} phrase(s) flagged)")
    if a.check and found:
        sys.exit(1)
