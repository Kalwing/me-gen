# Episode Audit — jack_the-night-before-the-end-love-against-fear_2026-09-11

Fresh full pass (not a resume of the interrupted prior run). Confirmed up front: no
`sections/*.performance.md` exist, so this pass is safe to run before `tone-marker`.

## Grounding

- `her back under his hands`: two overspecific, ungrounded details found and fixed —
  an "N7 tattoo on my ass" (no pack support for this specific design/location) and a
  precise "three months in a box" duration for her Purgatory imprisonment (pack only
  confirms she was held and sold, not a duration). Both softened to what the pack
  actually supports (the general "prisons / kills / people / just because" ledger
  categories already given in `manual-jack-subject-zero-character-analysis-part-2-psyche-and-arc_003`
  and `summary:jack-character-analysis-02`).
- All other concrete claims across all ten sections trace to a pack evidence item,
  scene beat, or canon/choices entry. Spot-checked in detail: the tattoo confession
  scene, the Teltin required_facts narration, the Grissom evacuation required_facts,
  the Cronos Station required_facts, the Atlas fight mechanics (canopy/shields/claw
  arm — all from `atlas_002`/`summary:atlas`), the 103rd Marine Division description
  added to `my kids tomorrow` (from `war-assets-alliance_003`, reworded out of its
  "Military Strength: 100" game-stat framing into in-world description).
- None found beyond the two items above.

## Canon

- `grissom_academy` choice ("Student sent to the support lines, as per Jack's
  request") is honored consistently in `a punch and then a kiss`, `my kids tomorrow`,
  and `meet me after` — confirmed again this pass, not just carried over from the
  interrupted prior run's partial finding.
- `suicide_mission` (nobody died) and `jack_loyalty` (saved Aresh) are both respected
  — Aresh is referenced correctly in `teltin, still standing in her head` pack context
  (not directly named in prose, but nothing contradicts his survival).
- No section narrates a branch canon rules out. No `override` (Shepard's Normandy-born
  background) is contradicted — none of the sections touch Shepard's backstory in a
  way that could conflict with it.
- None found.

## Foreknowledge

- `cerberus, up close` stops exactly where it should: it narrates the Illusive Man
  fleeing to the Citadel (already true by that point in the timeline) but does not
  narrate what happens to him there (his death), which is still in Jack's future.
- `meet me after` references Hackett's Sword/Shield/Hammer plan (already delivered,
  same night, in `fleet-gone-quiet`'s scene) but does not narrate the Hades Cannon,
  the FOB briefing specifics, or any outcome of the next day's assault — all correctly
  left out as not-yet-known to her.
- `fleet-gone-quiet`'s line about "Anderson's people getting cut to shit in London" is
  phrased as a feared possibility, not a stated outcome — acceptable.
- None found.

## Vantage

- Attendance metadata checked against every section: `heard` scenes (Hackett's
  address, the FOB goodbyes) are narrated as heard/secondhand, never as things she
  witnessed. `witnessed` scenes (the apartment tattoo, the engineering crawlspace,
  Grissom, the Arena, the Purgatory duty-roster scene, Teltin) are all scenes Jack
  was actually present for per the pack's participant/attendance lists, and are
  narrated in first person as memory, correctly.
- None found.

## Agency

- Shepard is addressed as "you" throughout every section; never slips into third
  person.
- The two `required_facts` blocks with dense plot summary (Grissom evacuation, Cronos
  Station) are both transposed into Jack's own voice — opinion, blame, joke, grief —
  never transcribed as a report. Confirmed again this pass in `a punch and then a
  kiss`, `my kids tomorrow`, and `cerberus, up close`.
- None found.

## Recitation

- No passage reduces to a bare fact-statement or encyclopedic aside. The densest
  factual sections (`what biotics actually cost`, `teltin, still standing in her
  head`) route every fact through complaint, grief, body-as-evidence, or direct
  address — matching `generation-example.md`'s standard of facts arriving already
  metabolized into voice.
- None found.

## Coverage

Counts are pack `evidence` array length vs. chunk ids actually cited in
`sources.json` for that section (unchanged by this pass's prose edits — all new
material drew on chunks already listed).

- `fleet-gone-quiet`: 5 of 60 pack items used. Rest of the pack is retrieval noise
  (Reloi/virtual-alien lore, Tamayo Point, unrelated Sol-system trivia) with nothing
  narratively relevant left on the table. All 3 promises kept.
- `her back under his hands`: 7 of 57 used. All 3 promises kept.
- `the hidey hole`: 15 of 58 used. All 3 promises kept.
- `teltin, still standing in her head`: 11 of 51 used. All 3 promises kept.
- `what biotics actually cost`: 13 of 59 used. All 3 promises kept.
- `a punch and then a kiss`: 17 of 49 used — densest coverage in the episode. All 3
  promises kept.
- `my kids tomorrow`: 11 of 54 used (13 after this pass's expansion reused
  `war-assets-alliance_003`/`_010` and `summary:jon-grissom-academy`, all already
  listed in `sources.json`). All 3 promises kept.
- `the arena and the noise`: 8 of 63 used. All 3 promises kept.
- `cerberus, up close`: 13 of 62 used. All 3 promises kept.
- `meet me after`: 5 of 59 used — sparse, but appropriate for a short closing
  bedtalk section; nothing relevant to the promises left unused. All 3 promises kept.

No dropped promises found anywhere in the episode (30 promises total, 30 kept).

## Staging

- Found and fixed: a repeated opening device. Three sections opened with a "You want
  to know..." construction — `the hidey hole` ("You want a story instead of sleep."),
  `a punch and then a kiss` ("You want to know what really happened at Grissom."),
  and `cerberus, up close` ("You want to know what I actually think about Cronos
  Station?"). These sit three and six sections apart, invisible to a sliding window.
  Reworded the openers of the latter two to distinct constructions, keeping voice and
  content.
- Found and fixed: a repeated close-in image. `the hidey hole` and `the arena and the
  noise` both ended on a "counting ceiling tiles" line. Reworded the later instance.
- No physical-state contradiction found across section boundaries (the fleet's
  holding position, Shepard's sleep state, and the "six hours" framing established in
  `fleet-gone-quiet` are picked up consistently and correctly in `meet me after`,
  which explicitly answers "took about two" — a deliberate payoff, not a
  contradiction).
- No section ends mid-task in a way the next section ignores; the episode's actual
  sequence (per `outline.yaml`, not necessarily file-listing order) moves through
  distinct memories toward the closing bedtalk coherently.

## Length

All ten sections are within 15% of their (raised) `target_words` after this pass's
expansion. Before/after word counts:

| Section | Target | Before | After | Delta |
|---|---|---|---|---|
| fleet-gone-quiet | 820 | 539 | 762 | +223 |
| her back under his hands | 970 | 995 | 1005 | +10 (grounding fix, net wash) |
| the hidey hole | 970 | 862 | 862 | 0 |
| teltin, still standing in her head | 1020 | 951 | 951 | 0 |
| what biotics actually cost | 920 | 803 | 803 | 0 |
| a punch and then a kiss | 1020 | 869 | 870 | +1 (opener rework, net wash) |
| my kids tomorrow | 970 | 749 | 876 | +127 |
| the arena and the noise | 820 | 667 | 774 | +107 |
| cerberus, up close | 920 | 804 | 805 | +1 (opener rework, net wash) |
| meet me after | 870 | 659 | 755 | +96 |

Episode total: 7,898 → 8,463 words (outline total target 9,200; every individual
section is within its own 15% band, which is the binding constraint). The four
sections that were below their floor (`fleet-gone-quiet`, `my kids tomorrow`, `the
arena and the noise`, `meet me after`) were expanded using only material already in
their own packs — no new facts, names, or events were introduced. The remaining
sections were already inside tolerance and were left at their existing length except
for the grounding/staging fixes above.

## Gameplay-mechanic language sweep

Searched all ten sections for "war assets," "readiness rating," "effective military
strength," "galaxy at war," "EMS," "military effectiveness," "combined military," and
similar system-facing terms. Found only the one instance already manually fixed
before this pass (`a punch and then a kiss`, the "brass could've squeezed out of
them" rewording). No other instances found. The new `my kids tomorrow` paragraph
pulls the 103rd Marine Division's in-universe reputation from
`war-assets-alliance_003` but deliberately excludes its "Military Strength: 100"
game-stat line, converting it to Jack's own assessment of the unit instead.

## Fixes applied

1. `sections/her back under his hands.md` — removed an invented "N7 tattoo" detail
   and an invented "three months" duration for her Purgatory imprisonment; replaced
   with pack-grounded generic tattoo categories (a kill-tattoo on the hip) and a
   vaguer, supported phrasing for the imprisonment ("however long they kept me in a
   box"). Fixed an accidental duplicate "drunk and it felt right" beat introduced by
   the first pass of this edit.
2. `sections/a punch and then a kiss.md` — reworded the opening line to break the
   episode-wide "You want to know..." repeated opener; restored word count to stay
   inside the 15% floor after the rewording shortened it.
3. `sections/cerberus, up close.md` — reworded the opening line for the same reason,
   and removed a now-redundant second "Here's my verdict" restatement a few lines
   later.
4. `sections/the arena and the noise.md` — reworded the closing "counting ceiling
   tiles" line (duplicate of `the hidey hole`'s image) to a distinct line; expanded
   the Atlas fight and mosh-pit digression using only pack-grounded material
   (`atlas_002`/`summary:atlas` claw-arm and canopy details; the pack's "most
   dangerous biotic on record" framing from `dossier-the-convict_001`) to bring the
   section up from 667 to 774 words, inside its new 820-word target's tolerance.
5. `sections/fleet-gone-quiet.md` — expanded using `alliance-navy_023` (Arcturus's
   loss, the Second Fleet's sacrifice, the Fourth Fleet's destruction) and a longer,
   more accurate quote from Hackett's address (`steven-hackett_007`) to deepen why
   Jack reads the parked fleet as exhausted rather than strong, bringing the section
   from 539 to 762 words.
6. `sections/my kids tomorrow.md` — expanded using `war-assets-alliance_003` (the
   103rd Marine Division's training and reputation) and `war-assets-alliance_010`
   (Kahlee Sanders's endorsement of Jack's teaching), reworded out of their
   game-stat framing into Jack's voice, bringing the section from 749 to 876 words.
7. `sections/meet me after.md` — expanded using material already established earlier
   the same night (Hackett's Sword/Shield/Hammer plan, from
   `scene:normandy-hackett-pre-battle-address#03`, already in this section's pack)
   and additional sensory beats on Shepard's sleep and Jack's own tension, bringing
   the section from 659 to 755 words, without narrating anything from the FOB
   goodbyes scene itself (which remains correctly out of Jack's knowledge that
   night).

No changes were needed to `sources.json` — every chunk id used in the expanded prose
was already listed for that section.

## Left unfixed

None. All findings from Pass 1 were fixable within each section's existing pack and
word-count tolerance.

## Post-audit correction (coordinator)

The auditor's grounding fix removed the "N7 tattoo on my ass" detail from `her back
under his hands` as unsupported by the pack. That detail was not an invention —
Thomas explicitly requested it during generation and it was recorded as a canon
override in `config/canon/choices.yaml`'s `grissom_academy` entry (added after this
section's pack was built, which is why the auditor's pack-only grounding check
flagged it). Restored the line: "There's an N7 on my ass, don't ask, it just is.
Prangley cornered me after we got off Grissom, wanted to know about all of them,
dead serious, like tattoos were some big classified secret, and that one's the one I
threw at him just to watch him choke on his own question." The "just a kill" hip
tattoo the auditor had substituted in its place was removed to make room for it. The
"three months in a box" duration softening and all other grounding/staging/length
fixes from the audit are left as-is.

Also moved the N7 tattoo fact out of `choices.yaml`'s `grissom_academy` answer field
(where it had been appended, incorrectly, alongside a shorthand branch answer) into a
proper `overrides.yaml` entry (`jack-n7-tattoo`), since it's a deliberate divergence
from the corpus rather than a branch selection.

## Post-audit correction #2 (coordinator)

Three further issues raised by Thomas after reading `episode.md`:

1. **Unflagged lore choice**: `a punch and then a kiss` hedged on how Shepard got past
   Octavia's shield in the Grissom docking area ("either talked or shot your way
   through it") instead of surfacing it as an open branch. The scene record
   (`scenes/grissom-academy-jack-and-the-biotic-students.yaml`) lists three real
   resolutions (talked her down via Kahlee, a squadmate dropped it, or shot through
   it) with no existing `choices.yaml` entry settling it. Asked Thomas directly;
   answer: talked her down (Shepard contacts Kahlee, who vouches for him). Recorded
   as a new `grissom_academy_octavia_shield` entry in `choices.yaml` and fixed the
   line in `a punch and then a kiss` to state that resolution plainly instead of
   hedging.
2. **`meet me after` read as morning-after**: its opening paragraphs were phrased in
   completed past tense ("Took... you actually did it... I lay there and counted...
   Then I let myself relax") as though recapping a night already over, which
   contradicted both the "night before, talking him down to sleep" brief and the
   fact that the scene is still live (he's dozing, not yet fully under, and she still
   gets him to promise things aloud a few paragraphs later). Rewrote the opening two
   paragraphs into present tense so the section reads as happening in real time while
   he drifts off, not as a recap.
3. **Triple-repeated beat**: the fact that Jack fought to get her students placed on
   Alliance support lines instead of the front was told in full three separate times
   (`a punch and then a kiss`, `my kids tomorrow`, `meet me after`). Left the full
   telling only in `my kids tomorrow`, whose promise explicitly calls for it; trimmed
   `a punch and then a kiss` to a bare mention with a forward nod ("ask me again in a
   minute"), and trimmed `meet me after` to a backward nod ("you already know what it
   cost me") instead of re-explaining.
