# Audit — Tali: The Eve of the Final Battle

## Chronology

- [x] `rannoch-in-the-offing`: closing paragraph slipped out of the retrospective frame —
  "Tomorrow we go down to Rannoch" narrates as if spoken *before* the Rannoch mission,
  even though the whole episode is Tali recounting Rannoch as something already in the
  past, the night before the push on Earth. Breaks the single-continuous-scene frame.
- [x] `keelah-selai`: "we come back to each other... That's not a wish, Shepard. That's a
  specification" asserts certainty about surviving tomorrow. Tali cannot know how tomorrow
  ends; this reads as dramatic irony / a premonition of the outcome, which the brief
  explicitly forbids.

## Repetition

- [x] `the-battle-of-rannoch` and `engineering-a-people` both fully re-explain, in
  near-identical mechanical detail, geth uploading into quarian suits (environmental
  processors, filtration loops, controlled/survivable infection) to rebuild quarian
  immune systems.
- [x] `rael-and-the-trial` and `what-she-is-to-him` both narrate the full mechanics of the
  Board stripping "vas Neema" and renaming her "vas Normandy" mid-trial.
- [x] `the-collectors-and-the-question` and `what-she-is-to-him` both fully re-derive the
  suit-linking/immunosuppressant protocol (antibiotics, sterile field, fever afterward)
  in near-identical terms.

## Missing events

- none found — all outline events for all 15 sections are represented and traceable to
  timeline entries and sources.json chunks.

## Voice drift

- [x] `haestrom-and-the-suit` (section 3, pre-signature-update range): the hardest
  emotional beat in the section — the unsent letter to a dead marine's parents — was
  stated flatly with no trace of the nervous over-explain-then-catch-herself beat that
  the updated bible calls for, even though it's exactly the kind of subject that should
  trigger it.
- [x] `the-fleet-and-the-exile` (section 5, pre-signature-update range): the entire
  section reads in a composed, essay-like register even though "home" and the Morning War
  are clearly the subjects closest to her — no rambling, no self-interruption, no catch.
  (Same underlying fix as the Recited facts item below.)

## Recited facts

- [x] `the-fleet-and-the-exile`: the whole section was an unbroken lecture on the Morning
  War, the exile, Fleet governance, and rationing — long declarative sentences with no
  self-interruption, opinion-in-the-moment, or address to Shepard's reactions. Compared
  against `docs/generation-example.md`'s density standard, this read as recitation rather
  than a person talking.
- [x] `pilgrimage-and-jacobus` (paragraph on Talitha/Mindoir): an encyclopedic aside about
  an unrelated NPC's backstory, delivered in exhaustive biographical detail for a passage
  whose only real job in the scene is a single thematic point.

## Invented lore

- [x] `the-battle-of-rannoch`: Tali is described opening her faceplate's outer seal on
  Rannoch's surface and taking an actual breath of unfiltered air. This isn't supported
  by any source chunk, and it directly contradicts the section's own established fact
  (paragraph above it) that immune reconstruction is a gradual, years-long project that
  has to happen before quarians can safely go maskless — she wouldn't do this days after
  the battle.

## Length

- [x] `pilgrimage-and-jacobus`: 880 words vs. 750 target (+17.3%), outside the 15% band.

---

## Fixes applied

- `rannoch-in-the-offing`: rewrote the closing paragraph into consistent past tense
  ("that's where we actually were... I didn't know what was waiting...") so it reads as
  retrospective narration the night before Earth, not live narration before Rannoch.
- `keelah-selai`: softened "that's not a wish, that's a specification" to an explicit
  hope she knows she can't guarantee ("It's not a specification. It's a hope, and I'm
  allowed a few of those tonight"), removing the implied certainty about the outcome.
- `engineering-a-people`: trimmed the immune/suit-upload mechanism explanation to a
  callback ("I already told you what three hundred years... did to us... I'm not running
  that whole diagnostic twice in one week") instead of re-deriving it, keeping only the
  new information (the staged, ship-by-ship schedule).
- `what-she-is-to-him`: condensed the vas Normandy renaming story to a quick callback
  ("You already know how I got this name...") instead of re-narrating it, and condensed
  the suit-linking passage to a callback plus one new detail (her mother and Shala'Raan's
  clean-room reaction) rather than re-deriving the mechanics. Added a new short passage
  on trust as an engineering problem she tested and solved for him specifically (per the
  outline's brief for this section) to restore the words trimmed by the repetition fixes,
  and restored a beat of emotional weight to the renaming paragraph without repeating its
  mechanics.
- `haestrom-and-the-suit`: reshaped the sentence about the unsent letter to Myrr'Jorin's
  parents so she over-explains it (rewriting the same sentence over and over) and then
  catches herself — "keelah, you didn't ask for a recitation of my own guilt" — landing
  the nervous-rambling beat at the section's hardest moment. Trimmed elsewhere in the
  section to keep it in the length band after the addition.
- `the-fleet-and-the-exile`: rewrote the section into her voice — added a self-aware
  opening ("Bear with me, I get lecture-y about this one... my father used to call it
  'the lecture voice'"), an interruption/catch at the hardest fact (the sub-1%-survival
  casualty count: "keelah, I still count it that way in my head sometimes... I don't know
  why I do that, it doesn't change anything"), and a self-aware pivot out of the history
  section ("Anyway. History's done."). Every fact from the original (geth origin/meaning,
  the Morning War, exile numbers, Fleet governance, rationing, external prejudice) is
  preserved; only the delivery changed. Trimmed elsewhere to keep the section in the
  length band.
- `pilgrimage-and-jacobus`: trimmed the Talitha/Mindoir aside from a full biographical
  recitation to a tight one-sentence account that keeps the required facts and the
  thematic point, fixing both the recited-facts item and the length overage.
- `the-battle-of-rannoch`: replaced the faceplate-breach/first-breath beat with Tali
  kneeling and pressing a gloved palm to the ground and reading it through suit sensors —
  keeps the emotional payoff ("that's what home means to me now... not the word. The
  dirt.") without contradicting the section's own established fact that going maskless is
  years away.

### Verification
- All 15 sections re-checked for length: every section is within 15% of its
  `target_words`, and the run total is 12,989 words against the 12,000 target (+8.2%,
  down from the pre-fix +9.4%).
- Re-scanned all sections for "Ashley"/"Williams" (none found) and for
  death/Synthesis/ending foreshadowing (none found) after fixes.

**Issues found: 10. Issues fixed: 9** (all except the Length item, which was fixed
jointly with its Recited-facts counterpart in `pilgrimage-and-jacobus` — counted once
here as one fix covering both checklist items).
