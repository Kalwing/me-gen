# Consistency check — issues found

## Chronology

- **virmire-and-the-cure-that-burned.md**: the closing lines said "Ashley stayed. Didn't come back. Kaidan did." This is the exact opposite of the run's stated player canon (Kaidan is the Virmire casualty; Ashley survives and rejoins in ME3). Direct contradiction — fixed.
- No other chronology contradictions found against `timeline/master_timeline.yaml` or the stated player-canon block (Wrex alive/Urdnot leader, rachni queen freed over Wrex's objection, Grunt survives Utukku, genophage genuinely cured, salarian sabotage deal refused, Mordin dies at the Shroud, Thane dies protecting the Dalatrass reference not present/not needed, Citadel DLC apartment party attendance, etc. — all consistent with what's on the page).
- Checked for references to the outcome of the final battle (destroy/control/synthesis, who lives) across all sections — none found. `pride-and-what-it-costs.md`'s "We win tomorrow" and `you-should-be-sleeping.md`'s "if I'm wrong" both read as Wrex's superstition/hope, not omniscient narration, and are consistent with "nobody knows how it ends."

## Repetition

- The verbal tic **"doesn't matter"** appeared 14+ times across the run (as many as 3 times in a single section), well past the style bible's "no catchphrase more than once or twice." Trimmed down to at most 2 occurrences in any one section, and removed several redundant instances during the length pass.
- The tic **"Told you [X] already"** was used as a callback device in five separate sections (`the-bomb-in-the-kelphic-valley`, `what-tuchanka-looks-like-now`, `the-rachni-queens-choice`, `the-hollows`, `utukku-and-the-rachni-debt`). A couple of these are legitimate cross-section callbacks the outline depends on (e.g. "Utukku's a story I'm saving" paid off in `utukku-and-the-rachni-debt`), but the literal phrase recurring five times reads as an overused verbal tic rather than a device. Thinned it out in `the-bomb-in-the-kelphic-valley.md`, `what-tuchanka-looks-like-now.md`, and `the-rachni-queens-choice.md`.
- `bounty-hunter-years-and-fist.md` had a self-referential aside ("I said that already. It's a good one twice.") that duplicated the same tic — removed.
- `the-rachni-queens-choice.md` contained a stray non-sequitur ("Tonn Actus never got the second stash back. Different fight.") that invents an unestablished second Tonn Actus stash and reads as a repetition artifact rather than a real callback — removed.
- No duplicated anecdotes found being told twice without being framed as a deliberate callback, beyond the ones the run brief explicitly flags as intentional (Utukku setup/payoff, the family-armor callback, the thresher-maw paragraph).
- Repeated opening pattern: several sections open with a direct rhetorical question to Shepard ("You want a story, Shepard?", "You know what I still think about, Shepard?", "You said Noveria."). Minor and not overused enough to require a rewrite pass, but noted for awareness.

## Missing events

None found — every event ID listed in `outline.yaml` for every section is represented with the correct participants, sequence, and outcome per `timeline/master_timeline.yaml` and the run's player-canon block.

## Voice drift

- **`you-should-be-sleeping.md`** contains "That's turians for you — not clever, just patient, which they mistake for the same thing," which is exactly the kind of neat turian aphorism the style bible forbids ("that's turian thinking for you"). This file is marked user-approved verbatim and DO NOT TOUCH, so it was **not fixed** — flagging only.
- Found a stray literal `</content>` tag appended to the end of `sur-kesh-and-eve.md` (a generation artifact, not narration) — removed.
- No stage directions, parenthetical performance cues, or asterisked sound effects found anywhere in the sections (checked all files for `*` and `(`).
- No poetic place-setting violations found (no "I've got Tuchanka's on my end" style vagueness) — all location description is concrete.
- No repeated-cadence-for-emphasis violations found matching the rejected pattern (checked for consecutive near-identical sentences; the few "That's not X. That's Y." constructions found add new content in the second clause rather than repeating the first, so they were left alone).

## Recited facts

- No clear recited-facts violations found. The history-heavy sections (`the-rebellions-and-the-debt`, `the-uplift-and-the-rachni-wars`) are explicitly framed as secondhand retellings Wrex wasn't present for ("wasn't standing in this one either... where mine and theirs don't match, believe mine"), and carry his opinion and bitterness throughout rather than reciting bare facts — consistent with `docs/generation-example.md`'s density and the narrator's stated bias toward personal, opinionated digression.

## Invented lore

- **`grunts-rite-and-the-camp-before-a-fight.md`**: Gatatog Uvenk was described as wearing "Battlemaster armor off a geth foundry like it made a point." Nothing in the sourced material (`data/pages/gatatog-uvenk.md`) supports a geth origin for Uvenk's armor — his kit is a standard krogan Battlemaster loadout with biotic Barrier. Fixed by softening the claim to "wore his Battlemaster gear like it made a point," which keeps the character beat without the fabricated detail.
- **`bounty-hunter-years-and-fist.md`**: the Tonn Actus anecdote claimed Wrex had to "burn the place down to get it back" — no source supports Actus's hidden base being burned down (he's killed in a firefight and the base is destroyed as an incidental result of the raid, not arson as a method). Softened to "took it back" to avoid asserting an unsupported detail.
- Everything else checked against `sources.json` chunks and `timeline/master_timeline.yaml` (Okeer/Korlus origin for Grunt, Aleena bounty, Adrien Victus at Taetrus, Clan Weyrloc/Nakmor history, the Shroud's 2,000-year-old STG sabotage, the "champion/real quads/means hero" speech, Eve's "I can handle myself" line, the +75 turian war asset figure) is accurate and sourced — no other fabrications found.

## Length

Total run length was ~9,217 words against a target of 8,000 (max 9,200 at 15% tolerance) — over budget, and several individual sections exceeded their own 15% tolerance:

- `grunts-rite-and-the-camp-before-a-fight.md` — 859 words vs. 600 target (43% over, well past tolerance)
- `bounty-hunter-years-and-fist.md` — 590 words vs. 500 target (18% over)
- `one-last-party-on-the-citadel.md` — 584 words vs. 500 target (16.8% over)
- `curing-the-genophage.md` — 865 words vs. 750 target (15.3% over, just past tolerance)

Several other sections were within tolerance individually but flagged by the run brief as contributors to the overall overage (`the-hollows`, `sur-kesh-and-eve`, `the-uplift-and-the-rachni-wars`, `what-tuchanka-looks-like-now`, `the-rebellions-and-the-debt`, `the-bomb-in-the-kelphic-valley`, `virmire-and-the-cure-that-burned`, `the-rachni-queens-choice`).

All of the above were trimmed (see Fixes applied). The thresher-maw paragraph in `grunts-rite-and-the-camp-before-a-fight.md` and the rachni-queen paragraph in `the-uplift-and-the-rachni-wars.md` were left untouched as instructed; all cuts came from surrounding text.

---

## Fixes applied

1. **`virmire-and-the-cure-that-burned.md`** — Fixed the Chronology/canon violation: swapped "Ashley stayed. Didn't come back. Kaidan did." to "Kaidan stayed. Didn't come back. Ashley did." to match player canon (Kaidan is the Virmire casualty). Trimmed filler throughout (removed redundant clauses like "Doesn't matter now," "rather than risk it being poisoned same as the first one," "I never did find out what happened to him after") to bring the section from 730 to 675 words.
2. **`grunts-rite-and-the-camp-before-a-fight.md`** — Removed the invented "geth foundry" detail on Gatatog Uvenk's armor. Trimmed non-protected paragraphs heavily (the thresher-maw paragraph ending "Last krogan to kill one that way was me." was left completely untouched) to bring the section from 859 to 690 words, within the 600-word target's 15% tolerance.
3. **`bounty-hunter-years-and-fist.md`** — Removed the unsupported "burn the place down" detail on the Tonn Actus raid (softened to "took it back"). Removed the repeated "I said that already. It's a good one twice." tic. Trimmed filler to bring the section from 590 to 536 words.
4. **`one-last-party-on-the-citadel.md`** — Trimmed filler and two minor asides ("Tuchanka smells different after the rains," "Never told Traynor I liked her better after") that weren't load-bearing to any outline event, bringing the section from 584 to 541 words.
5. **`curing-the-genophage.md`** — Trimmed redundant clauses throughout (kept every fact and beat) to bring the section from 865 to 781 words.
6. **`the-hollows.md`** — Removed one instance of the "doesn't matter" tic and trimmed filler throughout, from 687 to 610 words.
7. **`the-uplift-and-the-rachni-wars.md`** — Trimmed filler in the historical paragraphs; left the protected "Funny thing about the rachni, though..." paragraph completely untouched. 605 to 576 words.
8. **`sur-kesh-and-eve.md`** — Removed a stray literal `</content>` tag left over from generation. Removed two instances of the "doesn't matter" tic and trimmed filler. 619 to 592 words.
9. **`what-tuchanka-looks-like-now.md`** — Removed one "Told you that already" instance and trimmed filler while preserving the deliberate family-armor callback paragraph. 606 to 552 words.
10. **`the-rebellions-and-the-debt.md`** — Trimmed filler in the historical narration without cutting any fact. 624 to 592 words.
11. **`the-bomb-in-the-kelphic-valley.md`** — Removed two "Told you that already" instances and trimmed filler. 555 to 527 words.
12. **`the-rachni-queens-choice.md`** — Removed the invented "Tonn Actus... second stash" non-sequitur and one "Told you the ledger already" tic instance; trimmed filler. 490 to 471 words.
13. **`you-should-be-sleeping.md`** — Not touched, per instructions (user-approved verbatim), despite containing one voice-drift violation (the "that's turians for you" aphorism) — flagged above only.

**Totals:** 9,217 words before → 8,546 words after (target 8,000, max 9,200; goal was ~8,800 or below).

**Issue count:** 12 issues found (1 Chronology, 3 Repetition, 2 Voice drift, 2 Invented lore, 4 Length/over-budget sections plus the aggregate total-length issue). 11 fixed directly; 1 flagged as unfixable due to the DO-NOT-TOUCH instruction on `you-should-be-sleeping.md`.
