# Issues — tali-liara_home-what-the-war-cost-the-good-things-in-the-universe

Multi-voice episode (Tali / Liara, `reminiscing`, 12 sections, strict alternation). This audit
supersedes the interrupted pass; the three sections it had already touched without a log
(`the-last-room`, `two-years-and-after`, `what-the-evening-keeps`) were re-read in full as
part of this pass. Per the dispatch, the following were already fixed by the coordinator and
are not re-flagged below: §1 helmet/vantage/gut-lining, §3's retelling of §1's Rannoch
material, §4's mission walkthrough, §6's age and "Keelah", §9's run paragraph.

## Grounding

None found. Spot-checked against packs: the Migrant Fleet's "fifty thousand ships" / "17
million" (`seventeen-million-and-a-species`), Koris's rescue and Dorn'Hazt's dying message
(`the-good-things-in-the-universe`), the Hagalaz yahg takeover and Feron's chair
(`what-the-network-still-watches`, `two-years-and-after`), Aethyta's "Little Wing" nickname
and her marriage to Benezia (`the-admiral-and-the-archivist`), Legion's dreadnought rescue and
Rannoch standoff (`the-machines-that-remember`, `two-homes-at-sunset`), and the FOB goodbyes
and final squad (`the-man-we-both-loved`, `the-last-room`) all trace to pack scenes, summaries
or required_facts. Small invented framing (the calibrated targeting laser, "vas Rannoch" heard
in the wild, Koris as "a decent man, the kind who argues too long in meetings") is lore-
consistent and not load-bearing, per standing guidance.

## Canon

None found. The overrides (crew never knew the choice, Tali/Garrus evacuated before the
crossing, Shepard held dead with no body and a memorial ceremony, Tali as the romance and
Liara as the friend) are all honored. No section names Synthesis, Control, Destroy or Refuse.

## Foreknowledge

None found.

## Vantage

- `two-years-and-after` (Liara, unlogged edit from the interrupted pass): "I stood at that
  same wall once already with Garrus, after Thessia, when it was only my homeworld gone and
  not yet his." This is wrong twice over — the pack's `normandy-memorial-wall-after-thessia`
  scene has Liara going to Javik and then shutting herself in her quarters after Thessia, not
  to the wall (and she says exactly that herself, three sections earlier, in `thessia-after`);
  and the scene's actual wall moment for Garrus is "after the Cerberus coup," standing there
  until Shepard joined him — not with Liara, not after Thessia. **Fixed** (see below).
- All other `heard`/`witnessed` distinctions check out: `rannoch-admiral-koris` is correctly
  told as secondhand in `the-good-things-in-the-universe` ("Cortez told part of it, Shepard
  told less than that, and I filled the rest in"); `flotilla-tali-treason-trial` is correctly
  hedged as secondhand in `the-admiral-and-the-archivist` ("I only know your trial the way I
  know most of what happened while I was off the Normandy") and told firsthand, precisely, in
  `what-the-trial-cost`, where Tali actually stood trial.

## Agency

None found. Each narrator addresses the other in second person throughout; no third-person
slippage into "she" for the listener.

## Recitation

None found beyond what's already fixed (§4). The remaining lore digressions (geth
architecture in `the-machines-that-remember`, Thessia's fall in `thessia-after`, quarian
logistics in `seventeen-million-and-a-species`) are each interrupted, hedged or self-mocked
per the narrators' `digressions` style rather than delivered as clean exposition.

## Mechanics

None found. No Paragon/Renegade, charm/intimidate, reputation points, war-asset numbers,
loot, or dialogue-option language leaked into any section's prose. The "number" Anderson
gives before the conduit run (`the-man-we-both-loved`, `the-last-room`) is dramatized as a
commander's grim tally, not a displayed survival-odds stat.

## Form

None found. The alternation is strict (6/6, no voice holds two turns), each section's first
line answers the one before, and both narrators keep losing the thread onto lore before
drifting back to the cliff, matching `form_note`.

## Rhythm

No new issues. Clipped fragments ("I know. Don't say it." / "Both true. Still both true.")
are present at a rate consistent with the form and the narrators' own diction (Tali
interrupts herself constantly; Liara's clipped moments are rarer and land as understatement),
and none read as padding.

## Memory

None found beyond what's already fixed. No verbatim quotation of another character appears;
remembered speech is consistently reported ("something short and dry I don't fully remember,"
"I could be wrong about which admiral said which line"). Tali's account of Shepard's speech at
the FOB ("something about this being for every version of home... near enough, was I think the
actual word") is appropriately hedged despite being the day that changed her, per the
imperfect-memory standard.

## Coverage

Word counts against 15% of `target_words` (all sections pass):

| section | words | target | delta |
|---|---|---|---|
| two-homes-at-sunset | 865 | 800 | +8.1% |
| what-the-network-still-watches | 845 | 780 | +8.3% |
| the-machines-that-remember | 897 | 800 | +12.1% |
| thessia-after | 890 | 800 | +11.3% |
| seventeen-million-and-a-species | 776 | 800 | -3.0% |
| the-admiral-and-the-archivist | 889 | 780 | +14.0% |
| what-the-trial-cost | 789 | 800 | -1.4% |
| the-man-we-both-loved | 820 | 800 | +2.5% |
| the-last-room | 930 | 820 | +13.4% |
| two-years-and-after | 851 | 780 | +9.1% |
| the-good-things-in-the-universe | 1123 | 1000 | +12.3% |
| what-the-evening-keeps | 858 | 1000 | -14.2% |

Episode total: 10,533 words (Tali 5,380, Liara 5,153) against `target_words: 11000` — 4.2%
under, consistent with the reminiscing form running lean rather than padded.

Per-section pack usage (chunks referenced in `sources.json` vs pack size) and promises:

- `two-homes-at-sunset`: 14 of a much larger pack's items used; all 4 promises kept.
- `what-the-network-still-watches`: 10 chunks used; all 4 promises kept.
- `the-machines-that-remember`: 19 chunks used; all 4 promises kept, including the
  self-interrupted digression.
- `thessia-after`: 27 chunks used (this section leans hardest on its pack, appropriately,
  since it's Liara's one first-person atrocity account); all 4 promises kept.
- `seventeen-million-and-a-species`: 11 chunks used; all 4 promises kept, including the
  handoff to Liara about Aethyta.
- `the-admiral-and-the-archivist`: 17 chunks used; all 4 promises kept.
- `what-the-trial-cost`: 11 chunks used; all 4 promises kept.
- `the-man-we-both-loved`: 7 chunks used; all 4 promises kept.
- `the-last-room`: 12 chunks used; all 4 promises kept, including the honest "nobody knows"
  and the mixed, unresolved grief beat.
- `two-years-and-after`: 26 chunks used; all 5 promises kept (see Vantage fix above for the
  one that needed correcting rather than dropping).
- `the-good-things-in-the-universe`: 22 chunks used; all 6 promises kept, including the
  Koris digression correctly told as secondhand.
- `what-the-evening-keeps`: 7 chunks used; all 4 promises kept.

No promise across the 12 sections was dropped.

## Staging

- The memorial-wall contradiction above is also a staging error (physical whereabouts
  contradicted across a section boundary within the same episode) — logged once, under
  Vantage, and fixed there.
- No repeated opening device across sections: each turn opens differently (a direct rebuttal,
  a hedge, an exclamation, a flat correction), consistent with `form_note`'s requirement that
  each turn's first line answer the one before rather than restart a monologue.
- No section ends mid-task that the next one ignores; each closing line hands the floor to the
  other narrator by name or by direct question, and the next section's opening line takes it.

## Repetition

`repetition_flags.md` judged entry by entry:

- **Real, fixed:** Liara's "I am not going to [verb]" recurred in 4 of her 6 turns
  (`what-the-network-still-watches`, `thessia-after`, `the-man-we-both-loved`,
  `what-the-evening-keeps`) — not in the original scan's shingle list as one item (the exact
  5-word windows differed slightly) but confirmed by direct grep. Kept the first
  occurrence (`what-the-network-still-watches`); rewrote the later three in her own voice
  without the tic.
- **Deliberate, kept:** "careful people hedging about platforms" — Tali quoting Liara's own
  line back at her one section later. "arithmetic ... souls against ground" — Liara
  deliberately echoing Tali's cliff line from three sections earlier ("I did your arithmetic
  without meaning to"). "the one who tends a bar" — Liara repeating Tali's phrase back to her
  in the very next turn. "ask me again after the second drink" — Liara quoting her own
  earlier line, explicitly flagged as a callback in the prose ("Ask me again after the second
  drink, I told you"). All four are same-conversation callbacks with the beat and function
  preserved; none rewritten.
- **Not real, judged as ordinary phrasing, not fixed:** "first time in longer than" (two
  different narrators, generic construction, no distinctive shared content); "and I have
  never once" (a common English intensifier, used by Tali across two sections but not a
  distinctive stock phrase in her `signature`/`diction`; over-reported per the scan's stated
  bias).
- A rewrite of the memorial-wall passage in `two-years-and-after` (see Vantage) briefly
  introduced two new incidental overlaps with `thessia-after` ("I went to find Javik" / "shut
  myself in my quarters") since both describe the same remembered afternoon; reworded to
  remove the overlap while keeping the same fact.

## Voices

- Turn order and speaker alternation: strict 6/6, verified against each pack's
  `section.previous` — every section's opening line answers the one immediately before it
  (confirmed for all 12 sections).
- Register: both narrators talk to each other as friends who lived through this together —
  interrupting, teasing (the Mako-odds callback, the "Keelah, you even do the pause right"
  needle), correcting each other's secondhand versions — not as an audience being informed.
  No composed, testimonial turn found in the current text.
- Voice bleed: "Keelah" appears only in Tali's sections, "Goddess" only in Liara's (checked by
  grep across all 12 files) — clean.
- Cadence/diction: Tali's turns run on engineering asides, self-interruption, and technical
  precision the moment a subject gets close to her (the Morning War, the trial, Legion);
  Liara's stay hedged, archaeological/intelligence-flavored, and correct herself mid-claim
  ("I want to say Shala'Raan announced it, though it might have been..."). No pet phrase or
  stock deflection crossed voices beyond the "I am not going to" tic (fixed above, and that
  was a within-Liara repetition, not a cross-voice one).
- Word share: Tali 5,380 / Liara 5,153 — a 4.2% split, well inside the ±15% band.
- No turn recounts something only the *other* speaker witnessed as its own memory: Liara's
  account of Thessia, the trial, and the FOB are all her own attendance; Tali's account of the
  Rannoch standoff, the trial, and the last room are all hers. The one violation of this
  (Liara claiming to have stood at the memorial wall with Garrus after Thessia, an event she
  did not attend per her own earlier turn and the pack) is logged and fixed under Vantage.

## Length

All 12 sections within 15% of `target_words` — see table under Coverage. Closest to the edge:
`the-admiral-and-the-archivist` at +14.0% and `what-the-evening-keeps` at -14.2%, both inside
tolerance and unchanged by this pass's edits (the two-years-and-after edits added and removed
single-digit word counts and left it at +9.1%, down from a pre-edit +7.8%).

## Fixes applied

1. **`two-years-and-after.md`** — Vantage/Staging error. Rewrote the sentence claiming Liara
   stood at the memorial wall with Garrus after Thessia (she didn't; per the pack and her own
   account in `thessia-after` she went to Javik and then her quarters, and Garrus's wall
   moment was after the Cerberus coup, not with her). New text: Garrus's wall moment is
   correctly placed after the Cerberus coup, and Liara now correctly says she was not there
   herself after Thessia and went to Javik and her quarters instead — same beat (the wall as a
   recurring, silently-shared space), corrected attribution. Net word change: +10 words
   (851 vs. 841), section stays at +9.1% of target, well inside 15%.
2. **`thessia-after.md`** — Repetition. "I am not going to give you either" → "I will give
   you neither" (Liara's "I am not going to" tic, occurrence 2 of 4; kept the wording that
   carries the same refusal-to-choose beat). Section word count: 890 (was 893).
3. **`the-man-we-both-loved.md`** — Repetition. "Understand first what I am not going to
   tell you" → "Understand first the one thing I will not tell you" (occurrence 3 of 4; same
   boundary-setting beat, same position in the sentence). Section word count: 820 (unchanged).
4. **`what-the-evening-keeps.md`** — Repetition. "I am not going to make either of us do that
   arithmetic again tonight" → "I will not make either of us do that arithmetic again
   tonight" (occurrence 4 of 4). Section word count: 858 (was 860).

No section's word count increased beyond its pre-audit figure by more than 10 words, and all
remain within 15% of `target_words`. `sources.json` required no changes — every fix reused
chunks the section's pack already cited (the memorial-wall scene and the Garrus/Cerberus-coup
chunks were already in `two-years-and-after`'s source list); no new pack items were pulled in.

## Left unfixed

None. All issues found in this pass were fixed within the existing word targets and pack
material.
