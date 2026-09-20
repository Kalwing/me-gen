"""Shared helpers for the Mass Effect narrator pipeline."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The episode's subject when a run names none — see `episode_subject`.
DEFAULT_SUBJECT = "shepard"

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


def _marker_is_approved(path: Path) -> bool:
    """True when the file's first non-blank line is not an `# UNAPPROVED` marker."""
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            return not line.strip().startswith("# UNAPPROVED")
    return False


def outline_is_approved(run_dir: Path) -> bool:
    p = Path(run_dir) / "outline.yaml"
    return p.exists() and _marker_is_approved(p)


def voice_check_state(run_dir: Path) -> str:
    """Where the run stands on the voice checkpoint (see `voice_check_sections`).

    `missing`  — the checkpoint has not been reached; write the checkpoint sections and stop.
    `pending`  — `voice_check.md` is waiting on the user; stop and say so.
    `approved` — the user cleared the marker; write the remaining sections.
    """
    p = Path(run_dir) / "voice_check.md"
    if not p.exists():
        return "missing"
    return "approved" if _marker_is_approved(p) else "pending"


def episode_narrators(outline: dict) -> list[str]:
    """Every voice in the episode, in speaking order.

    A monologue has one: `narrator:`. A multi-voice episode also lists `narrators:`, and each
    section names whose turn it is. Section narrators are folded in too, so a voice a hand
    edit added to one section is never missed.
    """
    out: list[str] = []
    for n in [*(outline.get("narrators") or []), outline.get("narrator"),
              *((s or {}).get("narrator") for s in outline.get("sections") or [])]:
        n = str(n or "").strip()
        if n and n not in out:
            out.append(n)
    return out


def episode_subject(outline: dict) -> str:
    """Who the episode is *about*: the person the narrators address and characterize.

    Shepard by default — every narrator's episodes orbit the Commander. A run may name
    someone else (`subject: thomas` in `outline.yaml`, from `new_run.py --subject`), and
    then that person's `config/narrators/<slug>.notes.md` is what every section reads in
    Shepard's place. It changes the addressee, not the world: the canon store still says
    which branch of the trilogy happened.
    """
    return str(outline.get("subject") or "").strip().lower() or DEFAULT_SUBJECT


def subject_notes_rel(subject: str) -> str:
    """Repo-relative path of a subject's notes file. Existence is the caller's business."""
    return f"config/narrators/{subject}.notes.md"


def section_narrator(outline: dict, section: dict) -> str:
    """Who speaks this section: its own `narrator:`, else the episode's."""
    return str(section.get("narrator") or outline.get("narrator") or "").strip()


def is_multi_voice(outline: dict) -> bool:
    return len(episode_narrators(outline)) > 1


def voice_check_sections(outline: dict) -> list[str]:
    """The sections the voice checkpoint shows: the first turn of each voice.

    A monologue's checkpoint is its first section, as it always was. With two voices, each
    one's first turn is shown — approving only the opener would let the second voice through
    unread.
    """
    seen: set[str] = set()
    out: list[str] = []
    for s in outline.get("sections") or []:
        n = section_narrator(outline, s)
        if n not in seen:
            seen.add(n)
            out.append(s["id"])
    return out


def display_name(narrator: str) -> str:
    return str(narrator).replace("_", " ").title()


def voices_title(outline: dict) -> str:
    """The episode header's name line: "Garrus", or "Tali & Liara" for alternating voices."""
    return " & ".join(display_name(n) for n in episode_narrators(outline))


def section_heading(outline: dict, section: dict) -> str:
    """A section's `##` heading. Multi-voice episodes name the speaker, so the script shows
    whose turn it is and a performance can switch voice there; a monologue's is unchanged."""
    title = section.get("title", section["id"])
    if is_multi_voice(outline):
        return f"## {title} — {display_name(section_narrator(outline, section))}"
    return f"## {title}"


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


FORMS_PATH = REPO_ROOT / "config" / "forms.yaml"
_SPINES = ("events", "scenes", "mixed")
_FORM_REQUIRED = ("id", "description", "spine", "section_count")

# Used only for a form that predates `words_per_section` / `words_clamp`, so a hand-written
# or third-party forms file still yields a usable episode length instead of failing.
DEFAULT_WORDS_PER_SECTION = 800
DEFAULT_WORDS_CLAMP = (5000, 11000)


def target_words_for(form: dict, section_count: int) -> int:
    """The episode's word target: the form's per-section budget times its section count.

    A form with few, long sections (`motivational`, `eulogy`) and one with many short ones
    (`tunnel`, `lecture`) should not produce the same episode, which is what a fixed global
    default did. The clamp keeps an unusually short or long outline from running away.
    """
    per = int(form.get("words_per_section") or DEFAULT_WORDS_PER_SECTION)
    lo, hi = form.get("words_clamp") or DEFAULT_WORDS_CLAMP
    return max(int(lo), min(int(hi), per * max(1, int(section_count))))


def load_forms(path: Path | None = None) -> dict[str, dict]:
    """Load `config/forms.yaml` — the episode-form reference set, keyed by id.

    A form is the episode's skeleton: where its sections come from (`spine`) and roughly
    how many there are. The narrator bible supplies the gait.
    """
    path = Path(path or FORMS_PATH)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    forms = data.get("forms") or []
    if not isinstance(forms, list) or not forms:
        raise ValueError(f"{path}: `forms:` must be a non-empty list")
    out: dict[str, dict] = {}
    for form in forms:
        missing = [k for k in _FORM_REQUIRED if k not in form]
        if missing:
            raise ValueError(f"{path}: form {form.get('id', '?')!r} missing keys: {missing}")
        fid = str(form["id"])
        if fid in out:
            raise ValueError(f"{path}: duplicate form id {fid!r}")
        if form["spine"] not in _SPINES:
            raise ValueError(f"{path}: form {fid!r} spine must be one of {_SPINES}")
        count = form["section_count"]
        if not (isinstance(count, list) and len(count) == 2 and 1 <= count[0] <= count[1]):
            raise ValueError(f"{path}: form {fid!r} section_count must be [min, max]")
        out[fid] = form
    return out
