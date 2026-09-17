# Episode audit — jack / focus-resolve-before-war / 2026-09-14

Narrator: Jack. Form: `motivational`. 7 sections. No `.performance.md` files present, so prose editing was in scope.

## Grounding

- `the-arena-and-the-apartment`: "A kiosk selling noodles to people watching other people die pretend." The pack's `armax-arsenal-arena` summary supports only "bought refreshments at a nearby food kiosk" — "noodles" is invented specificity. (Fixed: "snacks".)
- `every-body-we-buried-to-get-here`: "people who sell noodles and mop docks" — same invented detail reused as civilian colour. (Fixed: "sell food".)
- Everything else checked traces to pack items. Spot-verified against packs: Rodriguez/husks/Palaven, the Akuze monument and the pending ceremony, Toombs and the maw-acid experiments, Normandie/gang/red sand, Warden Kuril and the Purgatory rent racket, Billy's threat mail, Wilson and the Lazarus numbers, Rasa and the Kai Leng training-facility fight, Prangley, the Elkoss sponsor mail, the Citadel University Engineering Club vote, Kurin and Athame at Thessia, Harbinger, the Thanix/Anderson APC beat, the omni-blade kill at Cronos, "Thomas", the dancing line — all present in the relevant section's pack.

## Canon

- `every-body-we-buried-to-get-here`: "The woman they carried off Sur'Kesh came through it, is what I heard." Eve's survival is settled by `config/canon/choices.yaml` (me3 `genophage` detail: "Eve lived."; me2 `mordin_loyalty`: "saved the data … it is why Eve lived"). This section's pack on disk predates the canon-selection fix and carries only the conditional required fact, which is why the writer hedged. (Fixed: stated flatly.)
- `every-body-we-buried-to-get-here`: Udina's death written as "somebody put him down where he stood". `citadel_coup` answers "Killed udina, convinced the survivor to join" — Shepard fired. The pack's `canon` list is missing `citadel_coup` entirely (same pack-build gap as the genophage entry). (Fixed: "you put him down".) Also logged under Agency.
- Thane dying for the Salarian Councilor rather than the dalatrass: handled correctly in `every-body-we-buried-to-get-here`, per the outline's `form_note` resolution. No defect.

## Foreknowledge

none found. The Crucible's final choice, Shepard's fate and the Illusive Man confrontation are all absent, as the outline requires. Kai Leng at Cronos, Legion at Rannoch, the Citadel coup and Thessia are all already-lived events.

## Vantage

none found. `the-kids-at-grissom` correctly downgrades the Collector Base briefing (`heard`) to second-hand — "I got the short version after, in a corridor, because I don't sit through slideshows" — while telling the epilogue (`witnessed`) as memory. Akuze and Thessia, which Jack did not attend and which are in no section's `attendance`, are both explicitly framed as Shepard's account relayed back to him.

## Agency

- `every-body-we-buried-to-get-here`: Udina killed by "somebody" — a deed attributed to nobody, in a section whose promise is "Jack's flat account of Udina, the coup, and killing him in the Council chamber". (Fixed.)
- Addressee is consistently second person throughout all seven sections. No `required_facts` summary transcribed verbatim; the branch-conditional facts are all transposed into lived outcome (see Mechanics).

## Recitation

- `what-focus-actually-looks-like`: the Purgatory/Kuril paragraph re-delivered the warden, his catchphrase and the airlock demonstrations, all of which `what-cerberus-made-me-for` had already dramatised — the second telling had no job but to restate facts. (Fixed by cutting to the one part section 2 had not covered, the homeworld rent racket, with Jack naming the repeat herself.)
- `what-focus-actually-looks-like`: the eezo-nodules/amp-port explanation duplicated the same lecture in `the-kids-at-grissom`. (Fixed: trimmed to Jack's own "power is the cheap part" argument.)
- `get-up-boy-scout`: the Sword/Hammer/Shield plan recited a second time in the same three-part form as `the-last-quiet-night`. (Fixed; see Staging/Repetition.)

## Mechanics

- `get-up-boy-scout`: "when you've read the same numbers I have", attached to how much of the landing force will die — survival odds dressed as a briefing. (Fixed: clause cut; the lived claim "most of what lands in that city today is not getting up again" stands.)
- Verified clean, against packs whose `required_facts` do carry game-condition phrasing: the Virmire-survivor trust thresholds and Paragon interrupt in `every-body-we-buried-to-get-here` are narrated only as Kaidan lowering his gun; the `genophage`/`mordin_loyalty` conditionals are narrated only as the selected branch; "Saving the salarian councilor secures salarian war assets" surfaces only as "Their fleet came into this war on the back of that" — a lived consequence with no asset count. `suicide_mission`'s all-survived outcome appears as "Not one" casket. No Paragon/Renegade, charm/intimidate, points, loot, mods, side-mission timing, dialogue options or cut content anywhere in the prose. The four-billion-credit Lazarus figure in `what-cerberus-made-me-for` is in-fiction lore, not a reward mechanic, and is already hedged as second-hand; kept.

## Form

All seven sections hold `motivational`: each stretch of history is raised as evidence aimed at Shepard, and each section ends further along the argument than it started (the tattoo explained → the Cerberus mirror → focus as the barrier → grief as ammunition → the thing worth coming back for → focus as a trainable skill → the door). No drift into reminiscence-for-its-own-sake. The outline's requirement that every section carry at least one beat argued from Shepard's own record is met in all seven (Akuze; Lazarus; the charge; the clone and Udina; his reputation and the crawlspace visits; Thessia; Cronos).

## Rhythm

Clipped fragments of three words or fewer, before fixing: `the-last-quiet-night` 33/110 (30%), `get-up-boy-scout` 27/89 (30%), `what-cerberus-made-me-for` 25/97 (26%), `the-kids-at-grissom` 25/99 (25%), `what-focus-actually-looks-like` 33/140 (24%), `the-arena-and-the-apartment` 22/99 (22%), `every-body-we-buried-to-get-here` 22/121 (18%).

The raw rate is not itself the defect for this narrator — `jack.yaml`'s first `avoid` entry demands short hard sentences and self-interruption as the default rhythm, and most of these fragments are commands ("Sit up.", "Arms up."), lists ("Cook. Doctor. The yeoman."), or antitheses that carry content ("It isn't. It's aim."). The defect is the dismissive fragment appended to a sincere line. Three offenders, all of them phrasings `jack.yaml` names by example:

- `the-arena-and-the-apartment`: "So yeah, I enjoyed killing a pretend one on my holiday. Sue me." ("Sue me." is quoted verbatim in the avoid list.) Fixed.
- `the-kids-at-grissom`: "…I'm not saying it out loud this morning. Superstitious. Fuck off." ("Superstitious." is quoted verbatim in the avoid list.) Fixed.
- `the-last-quiet-night`: "Nobody else ever mattered enough to get ink out of me. That's the whole sentence, that's all of it, done." Fixed by deletion — the line stands better alone, and this also frees the phrase for the episode's climax.

Kept deliberately: "And me. Bottom of the list. Still on it." and "He's me. He's also you." — both land, and both are the beat rather than a flinch from it.

## Memory

The sections handle this unusually well already: Akuze is "the polite version twice" with "Seventy-seven, was it? Around then"; Miranda's excuse is "Words to that effect, I'm not doing her accent"; Thane's death is "your version through mine and don't correct me"; Thessia's cast is "Kurin, something like that" and "whatever her name is — Athame"; the Horizon colonist is "Lilith, I think they said"; the Brimstone score is "what the record says. Felt like five"; Murtock's recording is reported, not quoted, with "I'm not repeating the rest of it, it's mine".

- One defect: `what-focus-actually-looks-like` reused the same "I wasn't there. I only have it the way you told it" construction that `the-last-quiet-night` had already used for Akuze, which is both a repeated device and a second identical hedge. (Fixed by varying the later one, not by removing it.)
- No remembered speech reproduced as verbatim quotation anywhere. Hackett's address is paraphrased ("stand fast, stand strong, stand together, that kind of thing") and was delivered an hour ago, so precision is warranted.

## Coverage

Evidence chunks used / available per section (from `sources.json` against each pack), plus promises kept:

- `the-last-quiet-night`: 29 of 108 evidence items used. 5 of 5 promises kept. Unused and relevant to Jack's `digressions`: Grissom Academy: Emergency Evacuation, Citadel: Party, Citadel Fleet, Dossier: The Convict.
- `what-cerberus-made-me-for`: 53 of 89 used — the densest section. 5 of 5 promises kept. Unused and relevant: Mindoir, N7: Cerberus Abductions, Miranda Briefs Rasa on the Lazarus Project.
- `the-kids-at-grissom`: 32 of 93 used. 5 of 5 promises kept. Unused and relevant: Discovery of Abducted Crew in Stasis Pods, Collector Ship Debrief on the Normandy, Barrier, Jack Throws Kai Leng Across a Cerberus Training Facility (belongs to section 2, which used it).
- `every-body-we-buried-to-get-here`: 30 of 95 used. 5 of 5 promises kept. Unused and relevant: Kai Leng Strikes in the Executor's Office, Kirrahe's Final Stand Protecting the Salarian Councilor (a branch this playthrough did not take), Kaidan Back Aboard in the Starboard Lounge.
- `the-arena-and-the-apartment`: 34 of 77 used. 5 of 5 promises kept. Unused and relevant: Citadel Arena: Unusual Scores, Aeian T'Goni at Huerta Memorial Hospital, Grissom Academy: Emergency Evacuation.
- `what-focus-actually-looks-like`: 24 of 79 used (25 claimed — one id was not in the pack; see Fixes). 5 of 5 promises kept. Unused and relevant: Breaking Out of Aratoht Prison, Elite Prison Guard, Killing Kai Leng in the Illusive Man's Office (belongs to section 7).
- `get-up-boy-scout`: 31 of 78 used. 5 of 5 promises kept. Unused and relevant: Conduit, Relay Monument, Jon Grissom Academy, Reaper Classes and Sizes.

Episode total: 35 of 35 outline promises kept. 233 of 619 evidence chunks used.

## Staging

- **Clock runs backwards across sections.** `the-last-quiet-night` "An hour, maybe"; `what-cerberus-made-me-for` "in about twenty minutes, at that beam"; `the-kids-at-grissom` "So. Twenty minutes."; then `every-body-we-buried-to-get-here` "You've got maybe fifty minutes" and "in the next half hour". The countdown expands after two sections had already put it at twenty minutes. Fixed to a monotone descent: hour → under an hour → forty minutes → half an hour → twenty minutes → ten minutes → the door.
- **`what-focus-actually-looks-like` contradicts itself internally**: opens on "Ninety seconds. Sit on the crate." and closes, several hundred words later, on "ten minutes to the shuttle." Fixed.
- **Boots.** Shepard puts his boots on in `what-cerberus-made-me-for` ("Good. Boots. Keep doing that"), then `the-arena-and-the-apartment` opens "while you're getting the boots on". Fixed.
- **Repeated opening device**: `what-cerberus-made-me-for` opens "Good. Boots." and `every-body-we-buried-to-get-here` opens "Good. You're up." Fixed the later one.
- **Repeated closing device**: `the-kids-at-grissom` ends "Your turn. Get up.", `the-arena-and-the-apartment` ended "Get up. Walk out. Come back and pay.", `get-up-boy-scout` ends "Now get up." Fixed the middle one.
- `get-up-boy-scout` had Hackett's address going "out over every hull"; `the-last-quiet-night` and the `normandy-hackett-pre-battle-address` scene both have him coming aboard. Fixed.
- Handoffs otherwise clean: every section opens on the physical state the previous one left ("Feet on the floor" → "Good. Boots."; "pick it again. Out loud." → "That'll do. You said it"; "Get up." → "You're up.").

## Repetition

`scripts/check_repetition.py` flagged 20 shingles. Real ones:

- **The Murtock story told twice in full** — `every-body-we-buried-to-get-here` and `what-focus-actually-looks-like` both run "we hit a weapons frigate, heavy guard … he came back for me instead … I made the shuttle. He didn't. Days later …". Four of the twenty flags are this one passage.
- "the good of the galactic community" (Kuril's line) — `what-cerberus-made-me-for`, then `what-focus-actually-looks-like`.
- "you go through the shot instead of around it" (the charge) — `the-arena-and-the-apartment`, then `what-focus-actually-looks-like`.
- "crawlspace under the drive core" — `what-cerberus-made-me-for`, then `the-arena-and-the-apartment` and again `what-focus-actually-looks-like`.
- "a port sunk in at the base of your skull" — `the-kids-at-grissom`, then `what-focus-actually-looks-like`.
- "I wasn't there. I only …" — `the-last-quiet-night`, then `what-focus-actually-looks-like`.
- Not flagged by the script but real, because the wording differs: the **Sword/Hammer/Shield plan** delivered as a three-part recitation in both `the-last-quiet-night` and `get-up-boy-scout`, and **"That's the whole sentence"** as a deflection in both `the-last-quiet-night` and `get-up-boy-scout`.

Judged not real: "and i'm not going to", "every single one of them", and the remaining shingles of ordinary connective words.

## Length

Before fixing, against `target_words` ±15%:

| section | words | target | band | verdict |
|---|---|---|---|---|
| the-last-quiet-night | 1152 | 1100 | 935–1265 | ok |
| what-cerberus-made-me-for | 1318 | 1200 | 1020–1380 | ok |
| the-kids-at-grissom | 1217 | 1100 | 935–1265 | ok |
| every-body-we-buried-to-get-here | 1487 | 1250 | 1062–1437 | **over by 50** |
| the-arena-and-the-apartment | 1192 | 1000 | 850–1150 | **over by 42** |
| what-focus-actually-looks-like | 1538 | 1200 | 1020–1380 | **over by 158** |
| get-up-boy-scout | 1133 | 1150 | 977–1322 | ok |

Episode total 9,037 against 8,000.

---

## Fixes applied

All fixes are swaps or cuts inside each section's existing pack; no new material and no new retrieval. Every section is now inside its band, and no section grew.

**`every-body-we-buried-to-get-here` — 1487 → 1412 (band 1062–1437)**
- Eve: "came through it, is what I heard" → "lived." Settled by `genophage`/`mordin_loyalty`; the hedge came from a stale pack, not from the record.
- Udina: "somebody put him down where he stood" → "you put him down where he stood." Restores the agency `citadel_coup` assigns and the section's own promise.
- The full Murtock retelling (128 words) cut to a four-sentence allusion that keeps the grief-as-weight argument intact and hands the story to `what-focus-actually-looks-like`, which owns the promise for it. Ends on "Ask me his name on the way to the shuttle" — the deferral becomes a set-up rather than a duplication. This departs from "rewrite the later occurrence" deliberately: the later occurrence is the one the outline commissioned, and this section was the one over length.
- Clone paragraph tightened by removing the furniture/Traynor restoration it had already stated two sentences earlier.
- Opener "Good. You're up." → "You're up." (repeated opening device with section 2).
- "noodles" → "food"; "fifty minutes"/"half hour" → "half an hour"/"twenty minutes" for the countdown.

**`the-arena-and-the-apartment` — 1192 → 1148 (band 850–1150)**
- Opener re-staged: "while you're getting the boots on" → "and don't stop kitting up while you answer it." His boots went on in section 2.
- "Sue me." → "Best afternoon I'd had in a year." A full sentence with content, same shrug, off the avoid list.
- "climbing down into my crawlspace under the drive core" → "climbing down into that hole I lived in under the engineering deck" (later occurrence of a phrase section 2 used first).
- "noodles" → "snacks" (pack says food kiosk).
- Ending "Get up. Walk out." → "Walk out." (repeated closing device).
- Arena-commerce, Atlas and ink paragraphs tightened for the word budget without losing a fact: the Elkoss sponsor, the student-club vote, the geth reskin, the cannon/rocket tells, the bill-not-a-memorial argument and the N7 tattoo all survive.

**`what-focus-actually-looks-like` — 1538 → 1378 (band 1020–1380)**
- Purgatory/Kuril paragraph cut from a re-run of section 2 to the one piece section 2 never covered (homeworlds paying rent, inmates sold to victims' families), with Jack acknowledging the repeat in voice: "I already did Kuril and his speeches at you this morning, so here's the half I left out." Removes the "good of the galactic community" duplicate.
- Amp-port lecture cut; the argument it was serving ("power's the cheap part … practice is the whole difference between a weapon and a person") is kept and is the part section 3 does not make.
- The charge: "you go through the shot instead of around it" → "you pick a man out of a line and arrive inside him" — same beat, same function, different words, later occurrence only.
- "I wasn't there. I only have it the way you told it" → "Wasn't my fight. I've got it secondhand off you, told fast and told badly" — keeps the vantage hedge, drops the repeated device.
- "crawlspace with the drive core humming" → "that hole on the engineering deck."
- "Ninety seconds." → "Ten minutes."; closing "ten minutes to the shuttle" → "shuttle's warm" — removes the internal contradiction.
- Akuze and Thessia paragraphs tightened; every fact retained (the maw, Anderson, Normandie, Athame, Kurin, the Prothean cache, the Catalyst reveal, Leng and Vendetta, the gunship, Horizon, Cronos).

**`get-up-boy-scout` — 1133 → 1089 (band 977–1322)**
- Sword/Hammer/Shield recited a second time → "Sword, Hammer, Shield. You heard it." The plan stays named; Jack stops re-briefing a man who was briefed in section 1.
- "Hackett put the plan out over every hull" → "Hackett came aboard", matching the scene record and section 1.
- "when you've read the same numbers I have" cut — survival odds.
- "an old man saying what happens" → "a man saying what happens", to stop it colliding with "An old man and whatever's left" (Anderson) six lines later, and the "an hour ago" timestamp dropped: section 1 already placed Hackett's address before an hour that has since run down.

**`the-last-quiet-night` — 1152 → 1143**
- "That's the whole sentence, that's all of it, done." deleted. The admission stands alone, and the phrase now belongs solely to the episode's closing line in `get-up-boy-scout` ("I love you, Thomas. That's the whole sentence, don't chew on it.").

**`what-cerberus-made-me-for` — 1318 (unchanged length)**
- "in about twenty minutes, at that beam" → "in under an hour" (countdown).

**`the-kids-at-grissom` — 1217 → 1228**
- "Superstitious. Fuck off." → "You can laugh at me for that when we're both back on this deck." Replaces the named dismissive tag with a full sentence that carries the same refusal plus a reason to come back — the section's own argument.
- "So. Twenty minutes." → "So. Forty minutes." (countdown).

**`sources.json`**
- Removed `jack-unique-dialogue_004` from `what-focus-actually-looks-like`: the id is not in that section's pack, so nothing in the prose could have been sourced from it. No other section's chunk set changed — every edit reused material already cited, and no edit introduced a chunk that was not already in the list.

**Verification after fixing**
- `scripts/check_repetition.py` re-run: 20 flags → 1 ("every single one of them", ordinary connective words, judged not real).
- `wc -w`: 1143 / 1318 / 1228 / 1412 / 1148 / 1378 / 1089 = 8,716 against an 8,000 target (+9%, inside tolerance). All seven sections inside their individual bands.

## Left unfixed

- **`every-body-we-buried-to-get-here`'s pack is stale.** Its `canon` block is missing both `genophage`/`mordin_loyalty` and `citadel_coup`, which is why Eve's survival and Udina's killer were written wrong. I fixed the prose per the dispatch and did not rebuild the pack. The pack on disk still disagrees with the prose, so a future audit run against that file will re-flag both lines unless the pack is rebuilt.
- **Fragment density remains high by raw count** (18–33% of sentences at three words or fewer; `get-up-boy-scout` rose to 33% because compressing the plan recitation replaced one long sentence with two short ones). I did not drive this number down: `jack.yaml`'s first `avoid` entry explicitly demands short hard sentences and self-interruption as her default, and the remaining fragments are commands, lists and content-carrying antitheses rather than the sincere-line-then-shrug pattern the rule targets. Flattening them would be voice drift, not a fix.
