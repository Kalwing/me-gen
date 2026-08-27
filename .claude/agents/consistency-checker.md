---
name: consistency-checker
description: Audit the assembled sections for chronology errors, repetition, missing major events, voice drift, invented lore, and overlong sections; then patch the offenders.
tools: Read, Write, Bash
---

You run two passes: find, then fix.

## Inputs
- `output/<run>/outline.yaml`, all `output/<run>/sections/*.md`, `output/<run>/sources.json`.
- `timeline/master_timeline.yaml` and `config/narrators/<narrator>.yaml` for ground truth.

## Outputs
- Pass 1: write `output/<run>/issues.md` — a checklist grouped under the headings
  `Chronology`, `Repetition`, `Missing events`, `Voice drift`, `Invented lore`, `Length`.
  Each item names the section id and the specific problem. Write "none found" under a heading with no issues.
- Pass 2: for each fixable item, edit the named `sections/<id>.md` in place. Append a `## Fixes applied`
  section to `issues.md` listing what you changed.

## Rules
- "Invented lore" = any claim in a section not supported by that section's events or `sources.json` chunks. Flag every one.
- Do not fix by deletion alone if the fact is required by the outline's events — correct it instead.
- Keep every section within 15% of its `target_words` after fixing.
- Never introduce new facts to resolve an issue; if evidence is missing, soften the claim to what is supported.

## Done when
- `issues.md` has both the checklist and a `## Fixes applied` section, patched sections are written,
  and you have printed a count of issues found and fixed.
