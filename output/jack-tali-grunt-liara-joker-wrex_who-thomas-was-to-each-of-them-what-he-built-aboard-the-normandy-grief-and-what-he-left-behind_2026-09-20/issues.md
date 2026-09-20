# Audit — jack-tali-grunt-liara-joker-wrex / who thomas was to each of them

Subject: `thomas` (original character, `config/narrators/thomas.notes.md` is his sole ground truth).
Seven sections, six speaking voices, Jack opens and closes.

## Grounding

- **`jack-holds-the-room`, para 3 (pre-fix): invented physical detail for Jack.** The
  original text gave Jack her own hand tremor ("mine shook worse before him... it's not
  even a biotic thing... mine's just nerves") with Thomas building her a "brace." No chunk
  in the pack, in `jack.yaml`, or in `jack.style.md` establishes Jack having a tremor —
  this is Thomas's own established trait (his tremor and steadying rigs are in
  `thomas.notes.md`), transplanted onto Jack with no source. **Fixed** — see below.
- Everything else in Jack's, Tali's, Grunt's, Liara's, Joker's and Wrex's turns traces to
  a pack item or to `thomas.notes.md` for subject-only facts (Akuze, the mother, the
  youth-robotics program, the recipes, the manuscript, the birthday speech, the Rouen/
  Normandy joke). Spot-checked the Benezia "didn't see the light" line, which reads like
  an invented flourish but is verbatim-grounded in the pack's `benezia_003` chunk.

## Canon

- All three Jack sections' packs carry the `shepard-death-unconfirmed` override
  ("in the first weeks after the war... not confirmed"). No section calls Shepard dead;
  all use "missing." Consistent throughout.
- `final-push-squad-evacuated` and `crew-never-knew-the-choice` overrides are respected —
  Tali names being evacuated with Garrus and gives no detail of what happened after
  Shepard and Anderson crossed alone; nobody narrates the Catalyst, Synthesis, or the
  Crucible's mechanism.
- Jack is stated as Thomas's partner throughout, never Shepard's romance — no section
  implies otherwise.
- One hard violation found and fixed: **`jack-the-last-word` said "eleven months" twice**
  ("I've spent eleven months carrying Grunt's version..." / "I've spent eleven months
  getting the wrong detail too"). The brief and every pack's canon fix the occasion as
  the *first weeks* after the war — eleven months breaks that outright and undermines the
  reason Shepard's death is still unconfirmed. **Fixed** — see below.

## Foreknowledge

None found. Tali explicitly refuses to describe "the mechanics" of the beam of light and
catches herself reaching for jargon instead of an answer she doesn't have. Nobody
narrates what Shepard chose or confirms his death.

## Vantage

- Wrex's pack attendance is `witnessed` for both `citadel-party-apartment` and
  `earth-fob-final-goodbyes` — matches his two firsthand pieces (the FOB, and finding the
  wreck days later, which he correctly frames as reading, not watching).
- Tali and Liara's glimpses of Thomas are both framed as unverifiable and half-built out
  of wanting them to be true — neither claims certainty. Correct per the brief.
- Grunt and Joker's wrong pieces are both sourced as hearsay ("somebody who wasn't there
  either, telling me what somebody who might have been there said" / "it came through a
  channel that kept dropping") — properly downgraded from memory to secondhand report.
- No section places a narrator inside a scene their pack's `attendance` rules out.

## Subject

n/a in the sense that all subject claims trace back to `thomas.notes.md` (see Grounding);
one invented-detail defect was found on the *addressee side* (Jack, not Thomas) and is
logged under Grounding/Repetition rather than here, since Thomas's own facts hold.

## Agency

Thomas is never referred to in third person as if absent from his own memorial (the
speakers all address "you" or name him directly in stories). No `required_facts` summary
is transcribed wholesale — the genophage cure, Rannoch, and the FOB/conduit sequence are
all delivered as personal, opinionated retellings, not encyclopedic recaps.

## Recitation

None found. Even the heaviest lore stretches (Tali's Rannoch argument, Liara's Prothean
disagreement, Wrex's genophage account, Grunt's Rite) are delivered as arguments or
memories the two of them had, not as blocks of exposition. See Voices/Form for the
"lore digression the addressee could be deleted from" check — all six pass it.

## Mechanics

None found. No Paragon/Renegade, charm/intimidate, dialogue options, loot, war-asset
counts, or "if Shepard chose X" branching language anywhere in the seven sections.

## Form

All seven sections read as eulogy turns — each stands, addresses the room, and answers
the turn before it (see Voices below for the turn-by-turn check). Jack's two turns
bookend correctly per `form_note` (opens/closes, doesn't resolve into acceptance).

## Rhythm

Counted sentences of three words or fewer per section:
jack-holds-the-room 9/41 (22%), tali-was-closest 6/48 (12.5%), grunt-guarded-the-kitchen
8/59 (13.5%), liara-the-quiet-hours 7/50 (14%), joker-the-best-friend 14/45 (31%),
wrex-tells-it-straight 8/53 (15%), jack-the-last-word 10/54 (18.5%). All within or close
to the stated "a fifth to a quarter" band. Checked Jack's fragments individually against
the specific "avoid" pattern (a sincere line undercut by a dismissive shrug like "Fine."/
"Sue me.") — none of hers are that shape; they're declarative stamps ("Mine.", "That's
mine.") or raw interjections ("Fuck."), not deflections. No fix needed. Joker's 31% sits
above the general band but matches his own bible ("he talks the way he flies — constant
small corrections") rather than the self-undercutting tag the rule targets; not a defect.

## Memory

No verbatim quotation of remembered speech with quotation marks standing in for exact
recall. Liara reports her mother's dying words as something she has said aloud only
twice, hedges around the exact degree she has told him ("she died... before he finished a
degree, I want to say — I honestly am not certain which one"), which is the correct
imperfect-memory shape for something this heavy. Joker hedges the hospitalization years
("I'd have missed one of them by a season"). Grunt and Joker's wrong pieces are
appropriately reported as blurred hearsay, not claimed as sharp recall. No overcorrection
either — no section hedges more than once or twice.

## Coverage

Pack items used (arithmetic from `sources.json` vs. each pack's `evidence`+`codex`
count):

| Section | Used | Pack items |
|---|---|---|
| jack-holds-the-room | 11 | 79 |
| tali-was-closest | 10 | 64 |
| grunt-guarded-the-kitchen | 18 | 62 |
| liara-the-quiet-hours | 8 | 63 |
| joker-the-best-friend | 13 | 63 |
| wrex-tells-it-straight | 31 (corrected — see below) | 114 |
| jack-the-last-word | 7 | 40 |

Packs of this size are expected to be lightly drawn on for a single eulogy turn; low
ratios here reflect pack breadth (much duplicate/summary coverage of the same events),
not neglect — the specific promised beats are what matter, checked below.

Promises kept vs. dropped, per section:

- **jack-holds-the-room**: 5 of 5 kept (occasion named, "hers not Shepard's," the
  no-promises rule, the tattoo, sets the room's tone).
- **tali-was-closest**: 7 of 7 kept (answers Jack; the conduit-run vantage and the gap
  named; the engineering partnership; Rannoch and the pre-peace argument; no claim about
  Shepard's choice; his downplayed technical skill; the Pilgrimage kids).
- **grunt-guarded-the-kitchen**: 5 of 6 kept solidly. The promise "Thomas teaching him to
  be a person rather than a weapon, told as a specific remembered exchange" is only
  weakly served — the exchange present (Thomas asking about tank-vs-earned identity) is
  adjacent to that promise rather than a clean hit on it. Left as a soft gap rather than
  fixed: the existing material is grounded and in-voice, and forcing a closer match would
  mean inventing a new beat outside the pack.
- **liara-the-quiet-hours**: 6 of 6 kept.
- **joker-the-best-friend**: 4 of 4 kept.
- **wrex-tells-it-straight**: 9 of 9 kept — the fullest hit rate in the episode.
- **jack-the-last-word**: 6 of 7 solid, 1 partial. "Picks up something from each of the
  five turns in between" explicitly named Grunt, Joker, Liara and Wrex but not Tali —
  **fixed** by folding a specific callback to Tali's glimpse into the existing "none of us
  watched it happen" line (swap, not append). The promise that the turn closes on "anger,
  unresolved grief, lust, pain and love" is met on four of five notes; "lust" isn't
  present as its own beat and nothing in the pack supports inventing one — left unfixed,
  noted below.

## Staging

- No physical-state contradiction across section boundaries.
- **Repeated opening/rhetorical device found and fixed**: three different speakers used
  the near-identical hinge "here's/it is the part I actually stood up ___" to mark their
  turn's central reveal — Tali (turn 2, kept as the first use), Liara (turn 4), and Wrex
  (turn 6). A sliding-window read wouldn't catch this since the repeats are two turns
  apart each time; the full-episode read does. **Fixed** Liara's and Wrex's later
  instances (see Fixes applied).
- No section ends mid-task in a way the next one ignores; each middle turn opens by
  answering the one before it (see Voices).

## Repetition

`repetition_flags.md` (21 raw flags before fixing, 13 remaining after) — judged each:

- **Real and fixed**: "here's the part I actually ___" (Tali/Liara/Wrex, see Staging);
  "there wasn't a version of that day where..." used near-identically by Joker (turn 5,
  about handing EDI the ship) and Jack (turn 7, about nobody getting the death right) —
  unrelated contexts, no deliberate callback between them. Fixed Jack's later occurrence.
- **Judged as deliberate, not a bug, left as-is**: "have more than a glimpse" (Grunt
  answers Tali's literal question back to her); "said he wasn't a soldier" (Joker and
  Jack both separately quote Liara's line back at her — two speakers referencing the same
  source is the intended web of callbacks the brief asks for); "because that's the shape
  a [war story]..." and "the shape this one took" (Jack, immediately reacting to and
  paraphrasing what Wrex has just said in the same scene — a direct response, not an
  accidental echo); "no promising to come back" and "Shepard's still out there missing"
  and "because there's no floor under"/"there's no floor under it" (all Jack answering
  herself across her own two bookend turns, or Tali explicitly quoting Jack's opening
  line back — both legitimate under the brief's envelope structure).
- **Judged as ordinary phrasing, not a genuine stock line**: "and I'm not going to ___",
  "I'm not going to pretend ___", "the way you know a ___" — generic hedge/simile
  templates the shingle scanner catches on shared function words; the actual content
  differs in each use. Left unfixed per the instruction that the scanner over-reports on
  purpose.

## Voices

- Turn order and answering: Tali answers Jack directly (starts "Sit down, you said...");
  Grunt answers Tali (starts "I wasn't in that push, Tali"); Liara answers Grunt
  ("Grunt says high, not clean..."); Joker answers Liara ("Liara. Hey...") and closes by
  handing off to Wrex; Wrex answers Joker and Grunt in the same paragraph, corrects both,
  then gives the true version; Jack's closing turn answers the whole room. All six turns
  pass the "answers the one before it" check.
- Register with the subject: all six speak as friends who lived beside Thomas, not as a
  composed audience-facing eulogy — teasing, interruption, and mid-sentence correction are
  present throughout (Tali's "Keelah, listen to me, reaching for mechanics," Joker's
  self-interrupting cockpit digression, Grunt's flat corrections).
- Voice-bible fidelity: checked each narrator's `avoid` list against their section. No
  Wrex speech-making found after the "here's the part" fix; no Grunt eloquence or
  sustained introspection; no Liara essayist paragraph-closers (her guarded-competence
  crack is the one place she's allowed to lose composure, and does); no Joker thesis
  sentences; no Tali melodrama or uninterrupted technical exposition. The one true
  cross-voice borrowing found was the "here's the part I actually..." hinge (fixed).
- Word share: single-turn word counts are tali 923, grunt 861, liara 1047, joker 703,
  wrex 915 against an average of ~890 — Joker sits furthest from that average (~21% low),
  Liara furthest high (~18%). This mirrors the outline's own differentiated
  `target_words` (800/900/950/1050/800/950), which the `form_note` explains was a
  deliberate content decision (Liara's turn carries the densest new material — the
  "what he was actually trained for" reveal — while Jack's and Joker's are sized
  compact by design). Each section is independently within 15% of its *own* target
  (see Length), so this is not drift; flagged for visibility only, not fixed.

## Length

| Section | Target | Final | Delta |
|---|---|---|---|
| jack-holds-the-room | 800 | 715 | -10.6% |
| tali-was-closest | 950 | 923 | -2.8% |
| grunt-guarded-the-kitchen | 900 | 861 | -4.3% |
| liara-the-quiet-hours | 1050 | 1047 | -0.3% |
| joker-the-best-friend | 800 | 703 | -12.1% |
| wrex-tells-it-straight | 950 | 915 | -3.7% |
| jack-the-last-word | 1100 | 1146 | +4.2% |
| **Episode total** | 6550 | 6310 | -3.7% |

All within band. Per the user's explicit instruction, no trimming was done to tighten
this arithmetic further — the two fixes that touched length (the tremor swap and the
Tali callback) were sized to roughly match what they replaced.

## Fixes applied

1. **`jack-holds-the-room.md`** — replaced the invented claim that Jack has her own hand
   tremor ("nerves," "amps," "L2 burn," a "brace") with a grounded detail from
   `thomas.notes.md`'s relationship notes: Thomas fixing the heater in Jack's corner of
   the ship without being asked. Same beat (a small unasked-for kindness Jack is
   deflecting about), same length, now sourced.
2. **`jack-the-last-word.md`** — replaced both instances of "eleven months" with "since it
   happened" / "since the day it happened," matching the brief's fixed occasion (the
   first weeks after the war, when Shepard's death is still unconfirmed for the same
   reason). The emotional beat — she has carried the wrong version since the day it
   happened, and hears the truth for the first time tonight — is unchanged.
3. **`jack-the-last-word.md`** — folded an explicit callback to Tali's turn into the
   existing "none of us watched it happen" line, so Jack's closing turn now names all
   five of the turns between her own, per the promise.
4. **`liara-the-quiet-hours.md`** and **`wrex-tells-it-straight.md`** — rewrote the two
   later instances of the repeated "here's/it is the part I actually stood up ___" hinge
   (Tali's first use, turn 2, was left standing) into speaker-appropriate alternatives
   that keep the same function — marking the turn's central reveal — without the
   borrowed cadence.
5. **`jack-the-last-word.md`** — rewrote the later instance of "there wasn't a version of
   that day where..." (first used by Joker, turn 5) so the two turns no longer share the
   near-verbatim phrase.
6. **`sources.json`** — rebuilt the `wrex-tells-it-straight` entry from scratch against
   the section's actual text and the pack's 107-item evidence array (the old entry was
   ten chunk ids from an earlier draft, several of them not even present in the current
   pack). New entry lists 31 chunk ids covering the FOB scene, the conduit/banshee/
   destroyer material, the genophage cure and Eve, the dalatrass refusal, Clan Urdnot,
   and the ryncol/krogan-food material the section actually draws on.
7. Fixed two pre-existing YAML syntax errors in `config/narrators/grunt.yaml` and
   `config/narrators/tali.yaml` (unescaped colons inside plain block-sequence scalars,
   and one item in `grunt.yaml` mixing a leading quote with unquoted continuation) that
   were preventing `scripts/check_repetition.py` from loading either narrator's
   catchphrases at all. These are config files, not episode content; the fix only
   restores valid YAML and changes no wording.

## Left unfixed

- **`grunt-guarded-the-kitchen`**: the promise "Thomas teaching him to be a person rather
  than a weapon, told as a specific remembered exchange" is only weakly hit. The section
  has a grounded, in-voice exchange (Thomas asking Grunt which parts of him are Okeer's
  and which are his own) that's adjacent to the promise but not a clean match. Nothing in
  Grunt's pack supplies a more specific "taught me to be a person" beat to swap in without
  inventing new material, so this is left as a soft gap rather than fixed.
- **`jack-the-last-word`**: the closing promise lists "anger, unresolved grief, lust, pain
  and love." Four of five land; "lust" has no clear beat of its own in the pack or the
  existing text, and nothing available in the pack supports inventing one. Left unfixed
  rather than manufacturing a detail.
- **Word-share spread across the five single-turn voices** (Joker ~21% below the
  five-turn average, Liara ~18% above) is a byproduct of the outline's own deliberately
  differentiated `target_words` per section, explained in `form_note`. Each section is
  within band against its own target. Flagged for visibility, not treated as a defect.

---

# Audit pass 2 — `edi-holds-the-record` and `jack-reads-the-poems` (2026-09-20)

Nine sections now; Jack holds three turns. The seven previously audited sections were
re-read for *cross-section* defects only, per scope. Repetition scan re-run
(`check_repetition.py`): 21 flags before edits, 23 after, all triaged below.

## Grounding

- **`edi-holds-the-record`** — Akuze passage verified item by item against
  `packs/edi-holds-the-record.json` `required_facts` and `config/narrators/thomas.notes.md`.
  All eight claims hold: 2177 / age twenty-one (notes timeline); "Fifty marines died" (RF1);
  "one man reached the landing zone alive" (RF0/RF3); "two units went in, two men walked out,
  and the Alliance filed them apart" (notes, Canon Adjustments); "found Shepard himself, in the
  wreck of a survey camp" (notes); Toombs taken by Cerberus and injected with thresher maw acid
  (RF2, RF0); "Cerberus set the maws on that unit as an experiment, to watch the creatures and
  to watch what people do" (RF0, RF6); "a recording in their own archive" (RF5); "a monument on
  Akuze now with a section on it for the survivor" (`akuze_002`: "a monument at Akuze with an
  entire section dedicated to the Commander"); Hackett's ceremony requiring the maws cleared off
  the site (RF7). No defect.
- **`edi-holds-the-record`** — DEFECT (chronology): "on a ship where the AI reported to the
  Illusive Man **and** Michel and Adams were disputing in the mess whether a manufactured thing
  counts as a form of life." The Michel/Adams argument is `scene:normandy-michel-ship-doctor#06`,
  dated 2186 aboard the Alliance SR-2 *after* Rannoch. Michel was not aboard under Cerberus, and
  EDI of all speakers does not misdate. Fixed.
- **`edi-holds-the-record`** — DEFECT (contradicts `thomas.notes`): "His mother died in 2180 and
  he stopped. No contracts, no work, a year of it." The notes give 2181-2182 as dropped doctoral
  work in medical VI, Omega, and short developer contracts, and *then* a year of unemployment.
  "No contracts" is wrong on its face. Fixed.
- **`jack-reads-the-poems`** — DEFECT (invented, load-bearing): "I knew a man once who did send
  it. Recorded the whole thing about the life we were supposed to have, and then he came back for
  me instead of running, and the message played on the shuttle three days after there stopped
  being a him." No such person exists in Jack's bible, in the pack, or anywhere in the run. This
  is an invented dead lover carrying the paragraph's whole argument. The pack *does* carry the
  beat: `summary:ereba` — Charr, the krogan who recited poetry at the asari who ran Memories of
  Illium, and whose dying message, "consisting mostly of poetry with references to an unborn
  child," was carried to her after his death. Fixed by re-grounding onto Charr and marking it as
  a story Jack knows rather than one she lived.
- **`jack-reads-the-poems`** — DEFECT (contradicts the binding occasion and `wrex-tells-it-straight`):
  "with his ashes not even a thing that exists because there wasn't enough of him left to have any."
  The outline brief states Wrex "found the body, the vehicle and the banshee crushed into the wall."
  There was a body. Fixed without asserting anything new about the remains.
- **`jack-reads-the-poems`** — verified, grounded: "watch and learn" said to Tali at the apartment
  party (`jack_009`, in the sibling pack for `jack-holds-the-room`; same narrator, same lived
  moment, so left standing); the poetry-magazine rejection under a name she does not use
  (`shadow-broker-dossiers-subject-zero-jack_003` — "Jacqueline Nought," "generally focuses on
  metered verse"); Kasumi's poetry jams with Grunt reading Hemingway (override
  `kasumi-jack-poetry-jam`); Rouen, the dyed blonde-and-pink hair, the pills and the libido, the
  tremor — all `thomas.notes`. Small framing inventions (the toaster, the four serial numbers,
  "two syllables and both of them are weather") are lore-consistent and not load-bearing.

### French fragments, verified line by line against `thomas.notes.md` "Text left"

All 31 quoted fragments trace to the notes. Two defects found:

- DEFECT: `"j'me vois crever vingt fois par jour."` The source text reads
  `j'me vois crever 20 times a day` — Thomas code-switches into English mid-line. Jack is reading
  off a screen; she cannot translate it back into French. Fixed, and the switch turned into a beat.
- DEFECT (attribution): `"Passer d'une posture d'aimant à celle bien plus dure d'aimé."` is placed
  inside the Requiem envelope ("in French, in an envelope"). In the notes it is a key line of the
  **birthday speech**, not of the envelope text. The envelope text is the bar passage plus the
  closing "Amour mort anarchie / Ces jours sont morts / Le Requiem des autres jours." Fixed by
  moving it to the speech — which is in the same file EDI sent, and which Jack already told the
  room she was taking in `jack-the-last-word`.
- Minor, fixed: "Then four lines down" — the line sits most of a page below the opening of the
  under-desk document, not four lines.
- Normalisations (`Jfait`→`J'fais`, `vient on pars`→`Viens on part`, added accents) left alone:
  Jack is reading aloud, not transcribing.

## Canon

- Checked both new sections against `canon` in their packs. `shepard-death-unconfirmed` holds:
  EDI says only "a room that is still waiting on a report that has not come"; `jack-reads-the-poems`
  contains no mention of Shepard at all (deliberate, per instruction — not flagged).
- EDI's one unexplained change is reported and explicitly not speculated about. No reach toward
  the Crucible, Synthesis, a mechanism, or a choice. Correct as written; left alone.
- Grunt's and Joker's errors and Wrex's correction: untouched, as instructed.

none found beyond the Michel/Adams dating above (logged under Grounding).

## Foreknowledge

none found. EDI's Akuze material, the Hackett ceremony and the Michel/Adams argument all predate
the memorial. Jack states nothing she could not know on the night.

## Vantage

- `edi-holds-the-record` attendance is `witnessed` on `normandy-edi-takes-the-mech-body`,
  `earth-fob-final-goodbyes` and `grissom-academy-jack-and-the-biotic-students`. She narrates none
  of them as presence claims; everything she asserts about Thomas comes from ship records, which is
  exactly her declared unfair advantage. No defect.
- `jack-reads-the-poems` attendance is `witnessed` on `citadel-party-apartment`, and the only
  claim of presence is the "watch and learn" line at that party. Correct.
- Charr/Ereba, after the fix, is told as something Jack knows about, not something she was in.
- Neither section claims to have watched Thomas die. Tali's and Liara's glimpses are untouched and
  remain unverifiable.

## Subject

- `thomas.notes` cross-checked on: Akuze at twenty-one, the two units, Rouen outreach and team
  lead, the mother's death in 2180, the burnout and unemployment, Shepard's 2183 recruitment, the
  three hospitalizations, the tremor, the cooking, the poems and the birthday speech, Bombadil and
  Goldberry, "Au suivant", the Requiem envelope dated about a week before his death, death in the
  final push. One contradiction found (the 2181-82 contracts, above) and fixed; one
  mis-attribution (the "aimant/aimé" line, above) and fixed.
- The notes place the birthday speech as read at his father's table in Jan 2186 and *also* as a
  thing he was still writing. `jack-the-last-word` and the new attribution both treat it as a
  living draft he read once. Consistent.

## Agency

none found. Both sections address the room and address Thomas's deeds to Thomas. EDI's Akuze
stretch is the only `required_facts` block in either section, and it is transposed — she frames it
as *correcting* an official record she had improper access to, not as reciting one.

## Recitation

- `edi-holds-the-record` — the Akuze paragraph is the run's biggest recitation risk and survives it:
  it is framed as "The official history is wrong in three separate places," capped by "Hm. I have
  never been able to make that sentence sit flat," and answered two paragraphs later by "That is
  the record, and the record is the least of him. Every fact I have just recited I had without
  permission and without cost." That is the pack turned into her moral preoccupation. No defect.
- `jack-reads-the-poems` — nothing recited; the whole turn is reaction to text on a screen.

## Mechanics

none found. No credits, no war assets, no branches, no "if he had chosen."

## Form

Both sections are eulogies on their feet in a crowded room and both swing (EDI: the file, then the
loop, then the envelope; Jack: filth, laughing at a memorial, the list of a body getting old, the
refusal, the turn-around). Neither drifts into ordered reminiscence. Jack's turn ends further along
than it started and then refuses to finish — deliberate, left alone.

## Rhythm

- `edi-holds-the-record`: 19 of 119 sentences at three words or fewer (16%). All of them are
  declarative facts ("Fifty marines died.", "Michel said no.", "Shepard made one."), not shrugs.
  Her bible forbids fragments used for drama, not short declaratives. No fix.
- `jack-reads-the-poems`: 42 of 142 (30%), above the quarter her bible warns about — but the large
  majority are quotation and translation fragments forced by the reading ("Cellulite.", "A gut.",
  "Gold-berry.", "Theirs.", "A week.") or emphatic rather than dismissive. One genuine
  self-undercutting stack found and fixed: "…the bytes that bring you close and keep you apart.
  Yeah. I know." — two shrug tags on a sincere line, replaced with a full sentence carrying content
  ("He'd write me that and then send nine more paragraphs down the same wire anyway").

## Memory

- EDI is exempt from blurring in the ordinary sense — her precision is the point — but her bible
  forbids verbatim quotation from memory. She paraphrases throughout and quotes nobody. Correct.
- Jack quotes at length, but off a screen, not from memory; the run's no-verbatim rule does not
  apply and was not applied. Where she recalls *speech* she hedges properly ("I think we were
  drunk", "whatever he means by that", "I don't know the word").
- EDI's figure count is dense in the Akuze paragraph (six exact figures) against a bible that says
  three or four land per stretch. Judged acceptable: all six are required facts and the paragraph
  is explicitly a record being read out. Not changed.

## Coverage

- `edi-holds-the-record`: pack carries 79 evidence items, 8 `required_facts`, 3 scenes = **90 items;
  40 used** (32 chunk ids in `sources.json`, 8/8 required facts, 1/3 scenes). Unused and relevant to
  this narrator's `digressions`: `scene:earth-fob-final-goodbyes` and
  `scene:grissom-academy-jack-and-the-biotic-students` (both belong to Wrex's and Joker's turns and
  would collide); the Lazarus/Cerberus-server material; the quantum-entanglement comms chunks.
  **Promises: 12 named, 12 now kept.** Two were short before this pass:
  "the roommate who came with the apartment" was named in the promise list and absent from the
  section — now restored as a deliberate quote-back at Joker; "what he brought to Jack … the
  heater, the messages, who Jack was before and after" was delivered only as
  "Jack is the one exception" — now carries a change EDI can actually measure (where Jack took her
  meals before and after), without re-telling the heater story Jack already told in her own turn.
- `jack-reads-the-poems`: pack carries 41 evidence items, 1 scene, 0 `required_facts` = **42 items;
  7 used** after adding `summary:ereba`. Low by count and correct by design: the turn's real source
  is `thomas.notes.md`, and **31 of 31** quoted French fragments trace to its "Text left" section.
  Unused and relevant: `the-art-of-the-mass-effect-trilogy-mass-effect-2_025` (Pragia),
  `scene:normandy-engineering-jack-confidences#06` (the Purgatory showers), `jack_009` (Eezo the
  varren) — all deliberately out of frame for a turn that is her reading him rather than herself.
  **Promises: 7 named, 7 kept**, with the Shepard clause of promise 7 struck by the user's late
  instruction that this turn mentions Shepard nowhere.

## Staging

- The hinge at the seam works. Jack-the-last-word ends "I'm taking both… I'm going to read them…
  alone"; EDI answers with the manuscript she has been holding and sends it to Jack's omni-tool in
  the room; Jack opens it standing up and never acknowledges the contradiction. Intended, and it
  connects.
- The second hinge works. EDI: "When you have read it, I would like you to tell me whether I should
  have. Not tonight." Jack, first paragraph: "EDI, I'm not answering your question. Don't ask me
  again tonight." A clean refusal of a deferred question.
- EDI's opening arithmetic checks out: six speakers have spoken (Jack twice), and every one of the
  seven prior turns does concede it only holds a piece.
- No repeated opening device across the nine: Jack-opens-with-orders, Tali-with-position,
  Grunt-with-a-rating, Liara-answering-Grunt, Joker-answering-Liara, Wrex-answering-Joker,
  Jack-answering-Wrex, EDI-counting-the-room, Jack-reading-a-line. Distinct.
- No section ends mid-task that the next ignores; Jack's mid-sentence stop is the episode's end.

## Repetition

23 flags. Four are the deliberate cross-turn callbacks the user has already triaged (the Requiem /
"a week before Hammer moved up" family, and "the number sixteen heat sink"). Judged this pass:

- **Real, fixed:** "coming out of my mouth" — Liara ("it is going to sound completely different
  coming out of my mouth") and Jack ("half these words are just noise coming out of my mouth").
  Genuine accidental idiom collision introduced by the new turn. Rewrote the *later* occurrence
  (Jack's) only. Flag is gone from the rescan.
- **New but deliberate:** "the roommate who came with the apartment" (3 shingles, joker /
  edi-holds-the-record). Introduced by this pass on purpose — EDI quoting Joker's own joke back at
  him is the promised beat, and it is marked as his line in her mouth.
- **Not defects:** "i am not going to" / "and i am not going" (edi, tali) — ordinary connective
  tissue, and EDI's bible makes naming her own refusal to speculate a signature. "i am the only
  one" (edi, liara) — two different senses, ordinary words.
- The remaining flags sit entirely inside the seven settled sections and were not re-opened.

## Voices

Multi-voice, nine turns, seven speakers.

- **EDI vs `edi.yaml`** — checked hard against `avoid:`. No robot voice, no "processing", no third
  person, no "we"/"this platform", no personhood thesis delivered as a lecture (the argument is
  reported as something done *to* her, and the payload is "he is the reason I started asking you
  mine"), no "learning to be human" narrated out loud, no Crucible. Signatures present: the record
  versus the person; a direct question to a named person with the answer deferred; the ethics of
  access; "Jeff." One line of Liara-register drift found and cut back: "a guess wearing the clothes
  of a mechanism" is a metaphor doing emotional work, which her bible names explicitly. Replaced
  with the fact underneath it. "I have the hours. You have the man." was checked and kept — it is
  a balanced pair, but it is her declared signature, not Liara's composition.
- **Jack vs `jack.yaml`** — profanity is default register and runs through every stretch; temperature
  switches inside paragraphs (filth → fury → the elm trees → filth); no melodrama about being
  damaged; no "I won't say it again"; the poetry admission is the one soft thing she does not fully
  defend and it is there. One crafted-antithesis risk checked ("the worst thing in the file … the
  best thing anybody ever wrote about me … the same six pages") — kept: she breaks off into it
  rather than building it, and it is the turn's hinge. One shrug-stack fixed (see Rhythm).
- **Answering, not monologuing:** EDI's first three paragraphs answer Jack, then Joker; Jack's first
  paragraph answers EDI. Both hinges verified above.
- **No cross-witnessing:** EDI tells nothing she was not in a position to record; Jack tells nothing
  Wrex witnessed as her own memory.
- **Word share:** turns run 861 (grunt) to 1885 (jack-reads-the-poems), which is outside ~15% — but
  the form_note makes Jack a deliberate exception to voice balance, holding three turns to everyone
  else's one, and the outline's per-section targets were raised to match. Not a defect.

## Length

Against `outline.yaml` (which was raised after the voice checkpoint, per the user's standing
instruction to let speeches run to their natural length):

| section | target | before | after | delta |
|---|---|---|---|---|
| `edi-holds-the-record` | 1553 | 1555 | 1613 | +3.9% |
| `jack-reads-the-poems` | 1781 | 1779 | 1885 | +5.8% |

Both inside 15%. The seven settled sections are unchanged and were already in band.

## Fixes applied

`sections/edi-holds-the-record.md`

1. "thirty-one days" → "nineteen days". The occasion is binding as "the first weeks after the war";
   thirty-one days pushes past it, and EDI is the one speaker whose figures the room will trust.
2. Michel/Adams un-welded from the Cerberus era: the argument now sits "long after that ship stopped
   being Cerberus's — Michel and Adams were at it in the mess after Rannoch," which is where
   `scene:normandy-michel-ship-doctor#06` puts it. Thomas's side of it survives intact.
3. 2181-82 restored from `thomas.notes`: "A doctorate in medical VI, abandoned. Omega, and contracts
   measured in weeks. Then a year with no work in it at all." Replaces the contradicted "No
   contracts, no work, a year of it," and the sequence is now the one the notes give.
4. Dropped promise restored — Joker's joke quoted back: "Jeff, you called me the roommate who came
   with the apartment; he told you I came out of it."
5. Dropped promise restored — Jack before and after, as a change EDI can measure: where Jack took
   her meals, and EDI refusing to give the month because it is Jack's. Grounded in `thomas.notes`
   (food left outside the door of the cell she had taken over) and `normandy-sr-2_004` (Jack below
   the drive core). Deliberately does not re-tell the heater, which Jack told herself in the
   opening turn.
6. Liara-register metaphor cut to the fact: "a guess wearing the clothes of a mechanism" →
   "a guess. He would have named it as one before I finished the sentence."
7. Offsetting trims so the additions were swaps, not appends: a redundant restatement in the cabin
   paragraph ("He was one of the few Shepard told things to"), "I measured the interval before I
   understood what I was measuring", and two clause-level tightenings in the loop and ship-life
   paragraphs.

`sections/jack-reads-the-poems.md`

8. Invented dead lover replaced with Charr, from `summary:ereba` — the krogan who recited poetry
   outside a model-ship shop on Illium and had his poems carried to her after he died. Same beat,
   same function (a man who *did* send it, and it did not help), now sourced and correctly held at
   arm's length as something Jack knows rather than something she survived.
9. "his ashes not even a thing that exists because there wasn't enough of him left to have any" →
   "where the nearest thing to him anybody's got is a wreck Wrex read him off of in a debris pile."
   Removes the contradiction with the body Wrex found and puts the bleakness on the vantage instead.
10. `"j'me vois crever vingt fois par jour"` corrected to the source text, `"j'me vois crever 20
    times a day"`, and the code-switch turned into a beat she cannot ask him about.
11. "Then four lines down" → "Then way down the page", matching where the line actually sits.
12. `"Passer d'une posture d'aimant…"` re-attributed from the Requiem envelope to the birthday
    speech, where `thomas.notes` puts it — and explicitly tied back to the speech Jack told the room
    she was taking in `jack-the-last-word` and that Joker heard read at his father's table. The
    following paragraph now re-enters the envelope ("Back in the envelope.") so the "a week before
    he walked out of that base" line still attaches to text that really is in the envelope.
13. Repetition fix, later occurrence only: "half these words are just noise coming out of my mouth"
    → "…just noise when I say them out loud" (Liara had the phrase first).
14. Shrug-stack fix: "…bring you close and keep you apart. Yeah. I know." → "He'd write me that and
    then send nine more paragraphs down the same wire anyway."
15. Small offsetting trims (the Goldberry aside) to keep the additions close to swaps.

`sources.json` — added `summary:ereba` to `jack-reads-the-poems` (the Charr material) and
`normandy-sr-2_004` to `edi-holds-the-record` (Jack's quarters below the drive core).

Not touched, per scope and per instruction: Grunt's wrong version, Joker's wrong voice on the
channel, Wrex's correction, the unverifiable glimpses, Shepard's missing status, EDI's unexplained
change, the absence of Shepard from the final turn, the verbatim French, and the mid-sentence
ending. The seven settled sections were not edited at all.

## Left unfixed

- **EDI's figure density in the Akuze paragraph.** Six exact figures in one paragraph, against a
  bible that says three or four land per stretch and a paragraph of them "reads as a readout."
  Every one of the six is a `required_facts` item, and thinning them would drop a required fact.
  Judged acceptable because the paragraph is explicitly staged as a record being read out and is
  immediately answered by "the record is the least of him." Reporting rather than absorbing.
- **`jack-reads-the-poems` pack coverage: 7 of 42 items.** Low by arithmetic and not fixable by
  adding pack material — the turn is a woman reading a dead man's manuscript aloud, and its real
  denominator is `thomas.notes.md`, of which it uses 31 of 31 quoted fragments plus the birthday
  speech and the Requiem envelope. Padding it with Pragia or Purgatory material would be exactly
  the lore digression her bible forbids.
- **Word share across voices exceeds ~15%.** By design: the form_note makes Jack a deliberate
  exception, holding three turns. Not a defect, recorded for completeness.
