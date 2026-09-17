# Audit — jack_eulogy-grief-drunk-love-after-the-war

Two sections are locked to canon-error-only edits per the coordinator's direction:
`get-a-drink-in-your-hand` (user-approved) and `what-he-was-for-the-rest-of-you`
("perfect"). Both were audited in full; neither had a hard canon/grounding error, so
neither was touched. Sections 2–6 were audited for characterization against
`config/narrators/shepard.notes.md` as well as their packs. No tone/anger pass was
performed on sections 2–6 per instruction — that is a separate pass.

## Grounding

- `grissom-academy`: "Kahlee thought they'd earned the front lines and argued for it,
  straight to his face" — invented. The pack (`manual-jack-in-game-dialogue-and-banter_006`)
  supports an argument over how the students should be deployed (support vs. front-line
  artillery), but it's Jack vs. the Alliance brass in general — Kahlee is never on record
  arguing for the front line, and canon (`grissom_academy` choice) simply says the
  students were "sent to the support lines, as per Jack's request." **Fixed** — reattributed
  the argument to "the brass," dropped Kahlee's invented position.
- `the-bubble`: "Kelly wanted music" — no pack support for this specific detail. **Fixed**
  — softened to an unattributed "somebody wanted music."
- `the-bubble`: "half the ship screamed at him through the comm about it — me, Tali,
  Kasumi, Thane, Jacob, all telling him no" — no scene in the pack shows this squad-wide
  comms argument over preserving the Collector Base for Cerberus. The pack does support
  Jack's own objection (`jack-unique-dialogue_003`: she "vehemently argues against the
  Illusive Man's suggestion to save the Collector Base," calling him a "user"). **Fixed**
  — replaced the invented ensemble scene with Jack's own grounded objection.
- `the-place-that-made-me`: "I found out from a news alert like a stranger" — the pack
  (`scene:pragia-jack-teltin-facility#06`, `summary:aresh-aghdashloo`) is explicit that
  **Shepard** received the news alert about Aresh's death on Elysium, not Jack. This is a
  vantage/grounding error, not just a stylistic choice. **Fixed** — reattributed: Shepard
  received the alert and told her.
- `so-she-can-find-me`: "I've still got the tattoo kit. Didn't throw it out." — no direct
  pack support, but it's a low-stakes personal-object detail consistent with her
  characterization and doesn't contradict anything. Left as is; not worth cutting a
  grounded, working line over a prop with no counter-evidence.

## Canon

None found. Checked every section against its pack's `canon` array and the binding
overrides (nobody in the crew knows there was a choice or which one; nobody saw anything
between Shepard leaving Anderson and the wave; Tali and Garrus were the final squad,
evacuated by the Normandy; Shepard's death is unconfirmed). `get-a-drink-in-your-hand`
complies with all four explicitly and correctly. No other section names the final choice,
narrates the beam interior, or contradicts the Tali/Garrus/evacuation fact.

## Foreknowledge

None found. The whole episode is framed as post-war hindsight from the one moment where
every event being described has already happened; no section reenacts a scene as if live
while claiming knowledge only available later.

## Vantage

- `the-place-that-made-me`: Aresh's-death vantage error — see Grounding above. **Fixed.**
- `grissom-academy`: the corridor sequence (Joker's diversion, the intercom threat,
  Reiley Bellarmine's rescue) was narrated as a flat first-hand account, but Jack's own
  pack attendance record (`grissom-academy-jack-and-the-biotic-students`: "witnessed") only
  covers Orion Hall — she was not with Shepard for the earlier corridors. **Fixed** —
  added an explicit "I got this part after, pieced together from Kahlee" frame so the
  passage reads as reported, not remembered.

## Agency

None found. Shepard, third-person throughout, is appropriate — he is the dead subject of
a eulogy, not a living addressee being talked past. No deed is attributed to nobody, and
no `required_facts` summary is transcribed uncredited elsewhere.

## Recitation

- `grissom-academy`: the same corridor passage flagged under Vantage was also a flat
  recitation of the emergency-evacuation summary in sequence. **Fixed** in the same edit
  — folded in Jack's own voice/positioning rather than just fixing the vantage framing.
- No other section reads as encyclopedic; `the-bubble` and `what-he-was-for-the-rest-of-you`
  are dense with plot facts but each fact is carried by Jack's opinion, joke, or grievance,
  matching `generation-example.md`'s density standard.

## Mechanics

None found. No Paragon/Renegade, points, loot/credits, dialogue-option, war-asset-number,
or "if Shepard chose X" language anywhere in the episode. "Ammo mods" in `grissom-academy`
and referenced in pack evidence is an in-world job description (what support squads do),
not a UI/mechanic leak, and was left as is.

## Coverage

Evidence items used (from `sources.json`) vs. total evidence chunks in each pack:

- `get-a-drink-in-your-hand`: 8/64 (locked, not touched)
- `the-place-that-made-me`: 17/49
- `purgatory`: 16/57
- `the-bubble`: 29/53 (+1 after fix)
- `below-decks`: 10/58
- `grissom-academy`: 29/53 (+1 after fix)
- `everyone-showed-up`: 19/64
- `what-he-was-for-the-rest-of-you`: 39/64 (locked, not touched)
- `so-she-can-find-me`: 7/63

All 27 `promises` across all nine sections are kept — verified line by line against the
outline. No promise was dropped. Lower-coverage sections (`below-decks`, `so-she-can-find-me`,
`the-place-that-made-me`, `purgatory`) lean on a small, well-chosen core of scene/summary
chunks rather than the long tail of trivia/guide-walkthrough chunks in their packs (loyalty
mission strategy tips, cut-content voicelines, wiki-page footnotes) — that unused material
is mostly not narratable by Jack in first person and its omission is not a defect.

## Staging

- Repeated opening device: `the-bubble` ("Next one's called the Bubble..."), `below-decks`
  ("Below decks. That's the next one..."), and `grissom-academy` ("Next thing. Grissom
  Academy.") used near-identical "next [thing]" transitions in three consecutive sections.
  **Fixed** — kept `the-bubble`'s (the first use), rewrote the transitions in `below-decks`
  ("Down to engineering next, since...") and `grissom-academy` ("Onto Grissom Academy —").
- No physical-state contradictions across section boundaries and no section left a task
  hanging that the next section ignores — each section is a self-contained speech in the
  same wake, which the frame supports.

## Repetition

From `repetition_flags.md` (10 flags), judged against context:

Real, and fixed:
- "because saying it out loud" (`the-place-that-made-me` / `below-decks`) — the same
  reluctance-to-admit-feelings tic, reused near-verbatim. **Fixed** in `below-decks`
  (later occurrence); `the-place-that-made-me`'s use stands.
- "didn't do the thing every [X] has done, which is" (`the-place-that-made-me` /
  `below-decks`) — identical rhetorical construction reused for two different men (Shepard
  vs. "every other man"). **Fixed** in `below-decks`.
- "every one of my kids" (`get-a-drink-in-your-hand` / `grissom-academy`) — same phrase,
  same referent (her students), reused. **Fixed** in `grissom-academy` (later occurrence);
  `get-a-drink-in-your-hand` is locked and stands as the first use.

Real, but unfixable under the current lock:
- "don't let anybody tell you" / "so don't let anybody tell" (`the-bubble` /
  `what-he-was-for-the-rest-of-you`) — a genuine reused rhetorical tic. The later
  occurrence is in `what-he-was-for-the-rest-of-you`, which is locked to no edits. See
  Left unfixed.
- "i'm not going to stand [here]" / "going to stand here and" / "not going to stand here"
  (`get-a-drink-in-your-hand` / `what-he-was-for-the-rest-of-you`) — same construction,
  reused. Both occurrences are in locked sections. See Left unfixed.

Judged as coincidental, not real (script over-reports, left alone):
- "and every one of you" — ordinary phrase, different sentences, no shared function.
- "the size of a building" — an ordinary scale comparison applied to two unrelated things
  (a Reaper larva, a thresher maw), not a reused stock line.

## Length

All sections are within 15% of `target_words` except:

- `get-a-drink-in-your-hand`: 869 words vs. 750 target (+15.9%), marginally over. This
  section is locked to canon-error-only edits, so it was not trimmed. Reporting instead of
  fixing, per instruction — worth a look outside this audit if it matters.

All other sections: `the-place-that-made-me` +14.2%, `purgatory` +13.1%, `the-bubble`
+8.7%, `below-decks` +12.8%, `grissom-academy` +14.8%, `everyone-showed-up` -1.2%,
`what-he-was-for-the-rest-of-you` +3.9%, `so-she-can-find-me` -1.9% — all within range,
before and after fixes (fixes were swaps, not additions).

## Characterization check against `shepard.notes.md` (sections 2–6)

Sections 2–6 (`the-place-that-made-me`, `purgatory`, `the-bubble`, `below-decks`,
`grissom-academy`) were written before `shepard.notes.md` existed. Checked each against
it:

- The "doesn't play the officer card... reaches for whatever gets both of you breathing
  normal again" characterization in `below-decks` matches the bible's "leads by listening"
  and "the build, not the snap" register well — no drift.
- "Shepard didn't take the gun. Didn't order me one way or the other... let it be my call"
  (`the-place-that-made-me`) matches "compassionate... seeks peaceful solutions" and the
  Anarchist/anti-hierarchy belief ("respect is earned, not owed") — consistent.
- Purgatory's "Shepard shot him before I got the chance" (killing the batarian going for
  Jack) fits "protective to a fault... will do messy, morally gray... things" and the
  belief statement's carve-out ("Paragon, except against oppressors" per `choices.yaml`).
  No drift.
- Grissom Academy's Shepard ("didn't debate me on it... made it an order") is consistent
  with backing people's own calls rather than over-explaining — matches the profile.
- No section gives Shepard a line, belief, or reaction that contradicts the bible (no
  cruelty, no indifference, no bravado without the underlying guilt/idealism). No fix
  needed anywhere on this axis.

## Fixes applied

1. `grissom-academy` — replaced the invented "Kahlee argued for the front lines" claim
   with the pack-supported "the brass wanted my kids running as another artillery unit."
2. `grissom-academy` — reframed the corridor-rescue passage (Joker's diversion through
   Reiley Bellarmine's rescue) as reported/pieced-together rather than witnessed, fixing
   both the vantage error and the flat recitation.
3. `grissom-academy` — reworded the closing line ("every one of my kids is a person
   tonight" → "my kids get to be people tonight") to remove the cross-section repeat with
   `get-a-drink-in-your-hand`.
4. `grissom-academy` — reworded the opening ("Next thing. Grissom Academy." → "Onto
   Grissom Academy —") to remove the repeated three-section opening device.
5. `the-bubble` — softened the unsourced "Kelly wanted music" to an unattributed
   "somebody wanted music."
6. `the-bubble` — replaced the invented squad-wide comms argument over the Collector Base
   with Jack's own pack-supported objection to the Illusive Man.
7. `the-place-that-made-me` — reattributed the Aresh's-death news alert from Jack to
   Shepard, matching the pack, and turned it into a small character beat (Shepard telling
   her) instead of dropping the fact.
8. `below-decks` — reworded the opening ("Below decks. That's the next one" → "Down to
   engineering next") to remove the repeated opening device.
9. `below-decks` — reworded "didn't do the thing every other man... has done" to remove
   the cross-section construction repeat with `the-place-that-made-me`.
10. `below-decks` — reworded "because saying it out loud" to "because hearing myself say
    it" to remove the cross-section phrase repeat with `the-place-that-made-me`.
11. `sources.json` — added `jack-unique-dialogue_003` to `the-bubble` and
    `manual-jack-in-game-dialogue-and-banter_006` to `grissom-academy`, reflecting the
    chunks the fixes now draw on.

All fixes were swaps within each section's existing word budget; no section's length
moved outside its 15% band as a result (see Length).

## Left unfixed

- **Cross-section repetition into locked sections.** Two real repeated tics —
  "don't let anybody tell you" (`the-bubble` / `what-he-was-for-the-rest-of-you`) and
  "I'm not going to stand here" (`get-a-drink-in-your-hand` / `what-he-was-for-the-rest-of-you`)
  — have their later occurrence in a section locked to canon-error-only edits
  (`what-he-was-for-the-rest-of-you`). Per the fix rule, only the later occurrence should
  be rewritten, and that section cannot be touched under the current instruction. Left as
  is; if the lock is lifted, both should be reworded in `what-he-was-for-the-rest-of-you`
  in the same voice, keeping the same rhetorical function.
- **`get-a-drink-in-your-hand` length.** 869 words vs. 750 target (+15.9%), marginally
  outside the 15% band. Locked to canon-error-only edits, and this is not a canon error,
  so it was not trimmed. Flagging for a length pass if the lock is ever lifted.

## Post-audit changes (coordinator)

- `so-she-can-find-me` — cut the ungrounded matching tattoo ("the twin of it on my own
  back"); the pack only has Jack tattooing Shepard's back. Replaced with the kit and her
  not being able to check whether the ink is still out there.
- `so-she-can-find-me` — cut the ungrounded pre-London exchange ("I told him myself before he
  ran off… and he said it back"); now "it's written on his back in my ink".
- Anger pass (user feedback: "she might be angrier during the first sections") over
  `the-place-that-made-me`, `purgatory`, `the-bubble`, `below-decks`: tone only, no fact
  changes. It also rewrote the earlier "don't let anybody tell you" in `the-bubble`, which
  resolves the first Left-unfixed repetition pair.
- `the-place-that-made-me` — cut the ungrounded "killed God knows how many of those things"
  (Aresh on Elysium); trimmed a clause for length.
- `below-decks` — trimmed three clauses to bring it back inside its band after the anger pass.
- Final lengths: the-place-that-made-me 1133/1000, below-decks 1074/950, the-bubble 1078/950,
  purgatory 856/750, all within 15%. Episode 8785 / 8000 (+9.8%).
