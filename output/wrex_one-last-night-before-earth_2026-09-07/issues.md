# Consistency and coverage audit — wrex / one-last-night-before-earth

Run: `output/wrex_one-last-night-before-earth_2026-09-07`
Sections audited in order: `the-noodle-stand`, `a-drink-and-a-bag-of-ice`, `the-rite`, `one-last-party`.
No `sections/*.performance.md` present, so this pass runs before `tone-marker` as required.

Note on the user's checkpoint: `the-noodle-stand` passed the voice checkpoint. Its ryncol
proof line ("190 proof and acidic"), its restatement rhythm ("Didn't look at it. Climbed it"),
and the "bored krogan is worse than an angry one" aphorism are treated as calibration, not
defects, and are excluded from every heading below.

## Grounding

- `a-drink-and-a-bag-of-ice`: "One had my clan brand memorized and a datapad of her lineage
  back nine generations, and the other one had already picked a name." The pack supports only
  that two more krogan females hounded him on the shuttle up (`scene:citadel-wrex-casino-ice#02`).
  The datapad, the nine generations and the pre-picked name are invented. Clan brands *as proof
  of lineage* are groundable — `shiagur_001` has Shiagur's descendants carrying "the clan brands
  to prove their lineage" — but the rest is not.
- `a-drink-and-a-bag-of-ice`: "Seven hundred years ago." `shiagur_001` dates the genophage to
  *circa 700 CE*; a date has been read as an interval. From 2186 that is roughly fifteen hundred
  years, not seven hundred.
- `a-drink-and-a-bag-of-ice`: "she clawed her way out of a cave in the dark with a rock."
  `eve_002` says she was sealed in for a week in complete darkness and dug out "aided by a
  crystal shard she found". A rock is not what the pack says.
- `a-drink-and-a-bag-of-ice`: "First krogan in two thousand years who's allowed to be afraid."
  No pack item supports the interval; the pack's own genophage dating is circa 700 CE.
- `a-drink-and-a-bag-of-ice`: "a pit boss named Krud running the Quasar booths who still owes
  me money." Krud and the Quasar booths are grounded (`codex/everyday.md:78`); the debt is
  invented.
- `a-drink-and-a-bag-of-ice`: "Three days I've been on this station." The pack has the Council
  expansion argument (`scene:citadel-wrex-casino-ice#01`) but no duration. Low-severity colour;
  left in place, noted.
- `one-last-party`: "Twelve years alive and he's got opinions about my age." Grunt was decanted
  from Okeer's tank in 2185 (`summary:grunt`, canon `grunt_loyalty`); at the party he is about
  a year out of the tank. Also a Canon item — see below.
- `one-last-party`: "Two thousand years of dark after that." `summary:tuchanka` gives nuclear
  firestorms circa 1900 BCE followed by a "little ice age" of nuclear winter. The two-thousand-year
  figure is invented.
- `one-last-party`: "Then your pilot's friends started asking about my planet, so I offered it."
  In `scene:citadel-party-apartment#12` nobody asks: the bar group is ganging up on Joker over
  his refusal to keep a sidearm in the cockpit, and Wrex volunteers Tuchanka unprompted.
- `the-rite`: "nobody bothers putting your skull in the Hollows." The Hollows and the display of
  krogan skulls there are grounded (`krogan_014`); the causal link to dying clanless is Wrex's
  own inference rather than a pack claim. Judged in-voice inference, not invented lore. No fix.

## Canon

- `one-last-party`: "Twelve years alive" contradicts `grunt_loyalty` ("Freed him from the tank")
  in 2185 against a 2186 party.
- `a-drink-and-a-bag-of-ice`: "Seven hundred years ago" misplaces Shiagur and the genophage
  against `shiagur_001` / `genophage_002`.
- Otherwise clean. Wrex alive (`wrex_virmire: alive`), leading the krogan (`krogan_leader: Wrex`),
  genophage cured with Mordin dead at the Shroud (`mordin_fate`), Grunt alive and commanding
  Aralakh Company with the company wiped covering the queen (`grunt_fate`), the clone dying by
  letting go and Brooks arrested rather than shot (`citadel_dlc`) — all narrated consistently.

## Foreknowledge

None found. `shepard_fate` ("Dead (synthesis)") is nowhere anticipated; nothing after the
Citadel shore leave is narrated as known. "Tomorrow's Earth" is the frame's present, not a
result. `the-noodle-stand`'s "Then you fixed that, so I don't have to say it anymore" refers to
the cure, which has already happened at the moment of speaking.

## Vantage

- `one-last-party`: the Brooks/clone paragraph is narrated in the first person plural —
  "We shot every one of them", "it locked us in an iridium vault", "if that Glyph thing hadn't
  found the release we'd still be in there", "in the old days we'd have shot her". The pack's
  `attendance` block covers only `citadel-party-apartment: witnessed`. The Archives material
  arrives as `required_facts` on event `citadel-dlc-archives` with no attendance entry putting
  Wrex inside the Archives. Presence is claimed that the pack does not grant.
- `the-noodle-stand`: correct. `attendance: heard`, `private_to: [Shepard, Grunt]`, and the
  section opens by naming it hearsay ("I heard about the noodle stand", "tell me if I've got it
  wrong", "neither of us was invited"). No issue.
- `a-drink-and-a-bag-of-ice` and `the-rite`: both `witnessed`, both narrated firsthand. No issue.

## Agency

- `a-drink-and-a-bag-of-ice`: "She's already decided the first one gets named Mordin. I didn't
  argue." `eve_007` has it the other way round — Wrex is the one who insists on naming their
  firstborn after Mordin. The deed is handed to the wrong person.
- `one-last-party`: the clone paragraph reads as an event summary transcribed rather than
  transposed — see Recitation. Shepard, the addressee, is largely displaced into a "we".
- No deed elsewhere is attributed to nobody; Shepard is addressed in the second person
  throughout all four sections.

## Recitation

- `one-last-party`, paragraph 5 (Brooks/clone), roughly 190 words: a run of plot delivered in
  sequence — Lazarus spare parts, six months out of stasis, implants, sushi bar, casino,
  Spectre codes, CAT6, the vault, Traynor, Glyph, the codes breaking, Brooks's arrest. Wrex's
  two interjections ("didn't we used to win these things?", "in the old days we'd have shot
  her") are bolted onto a summary rather than carrying it. Against `generation-example.md` this
  is the one passage in the episode where the narrator is delivering information he does not
  own.
- `one-last-party`, paragraph 3 (Tuchanka's history): borderline, but it is carried by opinion
  and possession — "me not born yet to see the good part", "telling tourists nobody's coming to
  collect their bodies". Kept.
- Nothing recited in `the-noodle-stand`, `a-drink-and-a-bag-of-ice` or `the-rite`.

## Coverage

`the-noodle-stand`: 20 of 67 pack items used (6 of 6 scene beats, ~8 of 43 evidence, ~6 of 17
codex). Unused and relevant to this narrator's `digressions`: Grunt's inherited genetic legacy
from Shiagur and the other named krogan (`summary:grunt`), the Relay Monument that Wrex openly
finds less impressive than his own (`relay-monument` chunks, and `urdnot-wrex-unique-dialogue_004`
where he says so), Wrex baiting Garrus at the Monument ("the turians made sure to finish it").
Promises: "What the Krogan Monument means to a krogan, and what it means that Grunt climbed it"
— kept. "Why Grunt was on the Citadel at all" — kept (Huerta, after Utukku). 2 of 2.

`a-drink-and-a-bag-of-ice`: 18 of 102 pack items used (4 of 4 scene beats, ~8 of 48 evidence,
~6 of 50 codex). The codex block here is the least mined in the run. Unused and relevant:
the Silver Coast waterfalls announced as "hanar urinals" (`codex/everyday.md:138`), the
black-market trade in krogan testicles that existed because there was no cure
(`codex/everyday.md:198`), burukh, the krogan ceremonial drink set on fire and drunk from a
scalding cup, Bakara seizing Wrex's shotgun on Sur'Kesh and telling him "I can handle myself"
(`eve_006`). Promises: "What being fertile again actually costs Wrex day to day" — kept.
"Wrex saying out loud that he has something to lose now" — kept. 2 of 2.

`the-rite`: 21 of 66 pack items used (7 of 7 scene beats, the killing-the-maw variant, ~8 of 44
evidence, ~5 of 14 codex). Best-covered section per word. Unused and relevant: Wrex killing his
father Jarrod after being betrayed at a Crush in the Hollows (`codex/characters.md:408`), the
breeding requests the dead maw generated for Grunt and one for Shepard, the Urdnot camp's varren
pit, krogan jubilation about "thresher steaks for months". Promises: "What a krogan name is for"
— kept. "Wrex's own thresher maw, and what the feat bought him" — half kept: the maw is there
("I killed mine"), what it bought him is never stated, though `scene:tuchanka-grunt-rite-of-passage#07`
gives it ("the feat that made his name in Clan Urdnot"). 1.5 of 2.

`one-last-party`: 28 of 105 pack items used (7 of 21 scene beats, 9 of 9 required facts, ~10 of
48 evidence, ~2 of 25 codex). Unused and relevant: Traynor's full to-order cocktail menu with
Garrus's Dextro Heat Sink (`codex/social.md`), Grunt on the door as bouncer sorting fake salarian
lip-hair and turning away Sheppy the Volus, Grunt daring Wrex into a drinking contest with
"logic is for salarians", the periodic-table recital and Garrus on thulium, Garrus's verdict that
the apartment would be a good place to retire. Promises: "The headbutting contest, from Wrex's
side of it" — kept. "Wrex shooting bottles off the counter and why that counted as a party" —
kept. 2 of 2.

Episode promises: 7.5 of 8 kept.

## Staging

- Frame contradiction across a section boundary. `a-drink-and-a-bag-of-ice` is staged live in
  the Silver Coast casino bar with a bartender being ordered at twice ("Bartender. Another. And
  ice." / "Bartender. More ice."). `the-noodle-stand`, `the-rite` and `one-last-party` are staged
  in a private room with a bottle passing between two people — "Hold the bottle still, Shepard",
  "Pour it", and "That photograph's still hanging by the bar *down there*", which places the
  speakers in Shepard's apartment, above its downstairs bar. The outline's `form_note` is
  explicit: "a room with a bottle the night before the end". Section two puts them somewhere
  else, on a different night, with staff.
- Repeated opening device. Two of four sections open on a barked imperative at Shepard: "Sit.
  No — sit there" (`a-drink-and-a-bag-of-ice`) and "Hold the bottle still, Shepard"
  (`one-last-party`). Three sections apart, invisible to a sliding window.
- No section ends mid-task in a way the next ignores.
- No beat repeats across sections. Checked specifically: Grunt appears in one and four on
  different material (Utukku/monument vs. the headbutt and the recruits); Aralakh appears in one
  as the company and in four as the star-name; Mordin's death at the Shroud appears only in two;
  the maw appears only in three; the genophage cost is stated in two and never restated.

## Length

| section | words | target | delta |
|---|---|---|---|
| `the-noodle-stand` | 358 | 350 | +2.3% |
| `a-drink-and-a-bag-of-ice` | 408 | 400 | +2.0% |
| `the-rite` | 209 | 200 | +4.5% |
| `one-last-party` | 695 | 650 | +6.9% |

All four inside 15%. Episode total 1670 words against `outline.yaml`'s `target_words: 2000`,
but the outline's own per-section targets sum to 1600 — the outline is internally inconsistent
by 400 words, and the sections are faithful to the per-section figures they were written to.
Reported, not closed: padding prose to reach 2000 would be exactly the failure this pass exists
to prevent.

## Fixes applied

The audit's fix pass was interrupted by a session limit partway through; the state below was
re-verified against the sections on disk afterwards, and the remaining items closed by hand.

Grounding
- `a-drink-and-a-bag-of-ice`: the invented datapad, nine generations and pre-picked name cut;
  replaced with the groundable clan brands as proof of lineage ("Clan brands out, tracing
  lineage at me like a deed of sale").
- `a-drink-and-a-bag-of-ice`: "Seven hundred years ago" removed; Shiagur is now placed by event
  (turian bombardment, put down at Canrum at the end of the Rebellions) rather than by interval.
- `a-drink-and-a-bag-of-ice`: the rock is now "a shard of crystal she found down there"
  (`eve_002`).
- `a-drink-and-a-bag-of-ice`: "in two thousand years" → "since the genophage".
- `a-drink-and-a-bag-of-ice`: Krud's invented debt cut; he keeps the Quasar booths only.
- `a-drink-and-a-bag-of-ice`: "Three days I've been on this station" kept as low-severity colour,
  and moved to the section opening (see Staging).
- `one-last-party`: "Twelve years alive" → "A year out of the tank".
- `one-last-party`: "Two thousand years of dark" → "Our own ice age after that", per
  `summary:tuchanka`.
- `one-last-party`: the party-scene beat re-footed on `scene:citadel-party-apartment#12` — the
  bar group is on Joker about the sidearm and Wrex volunteers Tuchanka unprompted ("Then the talk
  got off your pilot and his missing sidearm, so I put my planet on the table. Nobody took it.").

Canon
- Both canon items were the same two lines as above; closed with them.

Agency
- `a-drink-and-a-bag-of-ice`: the naming restored to Wrex per `eve_007` — "I told her the first
  one gets named Mordin. She didn't argue."

Vantage
- `one-last-party`: the Archives material is no longer narrated as presence. The plural is gone
  throughout the clone paragraph — "You put every one of them down", "it sealed you in a box you
  couldn't shoot your way out of", "you'd still be in there", "In the old days I'd have shot her."

Recitation
- `one-last-party` paragraph 5 rewritten from the outside: the sequence is now carried by Wrex's
  read of Brooks and of the copy rather than transcribed, and the two interjections sit inside
  the telling instead of on top of it. The airlock beat is separated into its own paragraph and
  ends on his own verdict about attachments.

Coverage
- `a-drink-and-a-bag-of-ice` was the least-mined section; the Silver Coast waterfalls announced
  as "hanar urinals" (`codex/everyday.md:138`) and Shiagur's fuller record are now in it.

Staging
- `a-drink-and-a-bag-of-ice` re-staged into the room with the bottle, per the outline's
  `form_note`. The bartender is gone; the drink and the ice are now asked of Shepard ("Pour. And
  the ice — the bag, not a cup.", "More ice.").
- The repeated barked opening is gone: section two now opens on "Three days I've been on this
  station arguing krogan expansion at the Council", and the imperative survives only mid-line.

Narrator register (applied after the audit, from user feedback folded into
`config/narrators/wrex.yaml`)
- Wrex does not borrow specialist vocabulary outside weapons and fighting. In `one-last-party`:
  "a shroud hanging at the Lagrange point" → "a tower standing out there holding the sky off us";
  "grew off the Lazarus table … learning to be a person off implants" → "A copy Cerberus grew out
  of the leftovers, six months out of stasis and still learning how to be one"; "an iridium vault"
  → "a box you couldn't shoot your way out of".

Not fixed, by design
- Episode total against `target_words: 2000`. The outline's per-section targets sum to 1600 and
  every section is inside 15% of the figure it was written to. This is an outline-level
  inconsistency, not a prose defect; padding to 2000 is refused.
