"""Load and summarise the player's narrative-choices questionnaire.

The questionnaire (``config/narrative_choices.template.yaml`` -> the user's
``config/narrative_choices.yaml``) captures the player's canon so generation
matches their playthrough. Unanswered questions mean "use default canon".
"""
from __future__ import annotations

import argparse
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


def _answer(question: dict) -> str:
    return str(question.get("answer") or "").strip()


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
            options = q["options"] or []
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
            parts.append(f"{label}: " + " ".join(a for _, a in answered))
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
    choices = load_choices(args.path)
    if is_blank(choices):
        print("all questions unanswered")
    else:
        print(summary_for_prompt(choices))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
