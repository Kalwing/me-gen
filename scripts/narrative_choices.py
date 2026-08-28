"""Load and summarise the player's narrative-choices questionnaire.

The questionnaire (``config/narrative_choices.yaml``) captures the player's canon
so generation matches their playthrough. A question is answered when ``answer`` is
set or its ``options`` are narrowed to a single value; anything left blank means
"use default canon".
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REQUIRED_KEYS = ("id", "prompt", "options", "answer", "detail")

# Order + display label for the top-level question groups.
GROUP_LABELS = {
    "shepard": "Shepard",
    "me1": "ME1",
    "me2": "ME2",
    "me3": "ME3",
}


def _norm(value) -> str:
    """Stringify a YAML scalar. ``yes``/``no`` parse as booleans — map them back."""
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value or "").strip()


def _options(question: dict) -> list[str]:
    return [_norm(o) for o in (question.get("options") or [])]


def _answer(question: dict) -> str:
    ans = _norm(question.get("answer"))
    if ans:
        return ans
    # A question whose options have been narrowed to a single choice is itself
    # answered — that lone option is the player's pick.
    options = _options(question)
    if len(options) == 1:
        return options[0]
    return ""


def load_choices(path: Path) -> dict:
    """Parse the questionnaire YAML.

    Raises ``ValueError`` if a question is missing a required key, or if an
    ``answer`` is non-empty but not one of that question's non-empty ``options``.
    """
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for group, questions in data.items():
        if not isinstance(questions, list):
            raise ValueError(f"{path}: group {group!r} must be a list of questions")
        for q in questions:
            if not isinstance(q, dict):
                raise ValueError(f"{path}: question in {group!r} is not a mapping")
            missing = [k for k in REQUIRED_KEYS if k not in q]
            if missing:
                raise ValueError(
                    f"{path}: question {q.get('id', '?')!r} in {group!r} missing keys: {missing}"
                )
            options = _options(q)
            ans = _answer(q)
            if ans and options and ans not in options:
                raise ValueError(
                    f"{path}: answer {ans!r} for {q['id']!r} is not one of {options}"
                )
    return data


def is_blank(choices: dict) -> bool:
    """True when no question has an answer yet."""
    return all(
        not _answer(q)
        for questions in choices.values()
        for q in questions
    )


def summary_for_prompt(choices: dict) -> str:
    """A compact one-line block built only from answered questions."""
    parts: list[str] = []
    for group, questions in choices.items():
        label = GROUP_LABELS.get(group, group)
        answered = [(q, _answer(q)) for q in questions]
        answered = [(q, a) for q, a in answered if a]
        if not answered:
            continue
        if group == "shepard":
            fields = "; ".join(f"{q['id'].replace('_', ' ')} {a}" for q, a in answered)
            parts.append(f"{label}: {fields}")
        else:
            for q, a in answered:
                parts.append(f"{label} {q['id'].replace('_', ' ')}: {a}")
    return " · ".join(parts)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Print the player's narrative-choices summary for prompt injection."
    )
    ap.add_argument("path", type=Path, help="path to narrative_choices.yaml")
    args = ap.parse_args(argv)
    if not args.path.exists():
        # No working copy yet — generation should fall back to default canon, not crash.
        print(f"{args.path}: not found — treating every question as unanswered", file=sys.stderr)
        print("all questions unanswered")
        return 0
    choices = load_choices(args.path)
    if is_blank(choices):
        print("all questions unanswered")
    else:
        print(summary_for_prompt(choices))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
