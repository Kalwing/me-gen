"""Shared helpers for the Mass Effect narrator pipeline."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

_EVENT_REQUIRED = (
    "event_id", "title", "game", "chronological_order",
    "summary", "characters", "consequences", "source_chunks",
)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def read_frontmatter_md(path: Path) -> tuple[dict, str]:
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path}: no frontmatter block")
    _, _, rest = text.partition("---\n")
    fm_text, sep, body = rest.partition("\n---\n")
    if not sep:
        raise ValueError(f"{path}: unterminated frontmatter block")
    return yaml.safe_load(fm_text) or {}, body


def write_frontmatter_md(path: Path, frontmatter: dict, body: str) -> None:
    fm_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).rstrip("\n")
    Path(path).write_text(f"---\n{fm_text}\n---\n\n{body.lstrip()}", encoding="utf-8")


def load_event(path: Path) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    missing = [k for k in _EVENT_REQUIRED if k not in data]
    if missing:
        raise ValueError(f"{path}: missing event keys: {missing}")
    return data


def load_events(events_dir: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(Path(events_dir).glob("*.yaml")):
        ev = load_event(p)
        out[ev["event_id"]] = ev
    return out


def outline_is_approved(run_dir: Path) -> bool:
    p = Path(run_dir) / "outline.yaml"
    if not p.exists():
        return False
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            return not line.strip().startswith("# UNAPPROVED")
    return False


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))
