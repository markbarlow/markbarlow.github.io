# Keep / Kill / Modify — design

**Date:** 2026-11-04 · **Status:** built

## Intent

Mark is reviewing the team's recurring meetings and activities. Run as a
whiteboard session, this exercise gets anchored by whoever speaks first; run as a
spreadsheet, it doesn't get filled in. Splitting it in two fixes both: everyone
sorts the list alone and anonymously beforehand, then the team spends its meeting
only on the activities where people actually disagree.

The sorting half has to be enjoyable or it won't get finished, hence the theming.
Each activity is dragged onto one of three characters:

| Bucket | Character | Idea |
|---|---|---|
| Keep | Van Helsing | Worth defending |
| Modify | Jekyll & Hyde | Two-faced; needs reworking |
| Kill | Zombie | Shambling on long after it died |

## Goals

- One link, no login, works on a phone, finishable in about three minutes.
- A facilitator view that ranks activities by how contested they are, so the
  meeting starts with the real arguments.
- Anonymous to the team.
- No backend to run or maintain.

## Non-goals and anti-goals

- No build step, no framework, no third-party runtime dependency.
- Individual ballots are never served — only aggregates.
- Not a general-purpose survey tool.
- **Failure even if it works:** unfinishable on a phone; a lost or wrong tally;
  or it looks like a generic form with emoji.

## Decisions the user made

- Solo sort beforehand, facilitator review live in the meeting.
- Anonymous; no straggler tracking.
- Optional one-line note on Modify.
- Juicy but calm: animations and characters, no timer, no points, no leaderboard.
- Collected via a Google Apps Script endpoint into a Sheet Mark owns.
- Shipped both into this repo and as a Claude artifact.
- Every activity forced into one of the three buckets — no abstain, no skip.
- Results gated until a close date.
- No guard on the tally: public URL, open endpoint, honour system.
- Visual direction: engraved woodcut characters and woodtype lettering on the
  dark horror-poster palette, chosen from three mocked-up directions.

### Risks flagged, and chosen anyway

- **Forced buckets.** People who don't attend an activity will guess, and those
  guesses can push an activity nobody knows about to the top of the contested
  list. Read a high-contention row on an obscure activity as possible ignorance.
- **No guard.** One person on two devices counts twice; anyone with the link can
  submit. Fine inside a team; not a number to quote outside it.

## Decisions left to the builder, and how they were settled

- **One card at a time to sort, three columns to review.** The sort is where the
  animation pays off and it works one-handed; the review is where changing your
  mind is easy.
- **Three equivalent input paths** — pointer drag, tap, and keys 1/2/3 — because
  drag alone is neither keyboard-accessible nor pleasant on a phone.
- **Draft saved on every drop**, so a refresh or a dead battery doesn't cost the
  work. Auto-resumes, with a "Start over" so that isn't a trap.
- **Turnout visible before the close date, split not.** Otherwise Mark is blind to
  whether anyone has answered, and checking can't anchor him.
- **The gate lives in the Apps Script, not the page**, so reading the page source
  doesn't get around it. The close date therefore has to be set in both places;
  `SETUP.md` says so.
- **Fonts self-hosted.** A page promising anonymity shouldn't call Google on load,
  and it was the stated non-goal anyway.
- **Single-theme by choice.** A monster-movie page commits to one visual world;
  every colour, the body background and `color-scheme` are set explicitly.
- **Colour is never the only signal** — each bucket also carries its character,
  its label and its number.
- **Violet means Hyde, and nothing else** (changed 2026-11-16). The ground and
  rules were originally violet-tinted (`--ink:#14101A`, `--rule:#4A3F55`), so
  purple read twice: once as Modify, once as the furniture, across fourteen
  dividers and borders. Ground and rules are now neutral warm charcoal
  (`--ink:#141211`, `--rule:#4C4642`). Mark chose to keep violet on the note
  box and the results note stripe, since those are Hyde's own comments — so
  every remaining use of `--modify` is semantic. Contrast re-measured across
  56 text pairs afterwards: no failures, lowest 5.07 against 4.5 required.

## Shape

| File | Purpose |
|---|---|
| `keep-kill-modify/index.html` | The whole app. Vanilla, no dependencies. |
| `keep-kill-modify/config.js` | The only file to edit: list, session, endpoint, close date, headcount. |
| `keep-kill-modify/fonts/` | Rye and Crimson Pro, latin subset, OFL. |
| `keep-kill-modify/apps-script/Code.gs` | The endpoint. |
| `keep-kill-modify/SETUP.md` | Three-minute deployment, and what is and isn't private. |

Ballot posted as `{sessionId, ballotId, submittedAt, votes, notes}`; `ballotId`
lives in `localStorage` so an edited resubmission upserts rather than
double-counting. `GET ?session=` returns aggregates only, and before the close
date only the turnout. POST uses `text/plain` to stay a simple request, because
Apps Script has no `OPTIONS` handler.

Contested-first ordering is the Shannon entropy of each activity's three-way
split, descending.

## What was verified

Against a local mock of the endpoint contract: all three input paths; draft
recovery across a hard reload; moving a card between columns; the failure path
(answers kept, retry and download offered); upsert on resubmit; the close-date
gate asserted on the response body, not just the UI; contention ordering checked
against hand-computed entropy; CSV contents; settled-group counters; a hostile
string in a Modify note rendering as literal text; phone width; reduced motion;
and WCAG AA contrast measured on every text pair, which caught one failing label.

**Not verified:** the live round-trip against a real Apps Script deployment, which
needs Mark's own Google account.

## Drop sounds — built 2026-11-16

Three files Mark supplied, one per bucket, in `keep-kill-modify/sounds/`:
`helsing-bells.mp3` (Keep, 8.5s), `jekyll-bubbles.mp3` (Modify, 4.3s),
`zombie.mp3` (Kill, 4.0s). 280KB in total.

### Mark's calls, which overrule my earlier advice

Both of these were argued the other way in this document and decided the other
way on purpose. Do not quietly "fix" them.

- **Played full length, overlapping.** People sort every couple of seconds and
  the bells ring for eight, so drops pile on top of each other. That is the
  intent: Mark wants surprise and cacophony the first time a room tries it.
  I had recommended trimming to half a second; he wants the mess.
- **Sound on by default**, with a small mute button in the top right corner,
  remembered per browser. I had recommended defaulting to off. Overruled for
  the same reason — a sound nobody hears is not a surprise.

### How it works

- One `AudioContext` built at page load and the three files decoded into it
  immediately. **This timing matters:** decoding on the first gesture is too
  late, because the gesture and the first drop can be the same keypress, and
  that card lands silent — the one card the surprise exists for. Found by
  measurement, not reasoning; the first version had exactly this bug.
- A fresh `AudioBufferSourceNode` per drop, so sounds overlap rather than cut
  each other off. Every gesture also resumes the context, so a tab switch
  cannot leave it dead.
- Muting stops everything already ringing, not just future drops. Muting
  halfway through an eight-second peal has to actually stop the peal.
- Playback is fire-and-forget throughout: a missing, blocked or undecodable
  file leaves the page silent and working, and nothing in the sound path can
  delay a drop.
- Fires on sort drops and on review-screen moves alike.
- **Mastered up about 10 dB** from how they were downloaded (−26/−28.5 LUFS to
  roughly −17) and matched to within 1 dB of each other, so no bucket is the
  loud one. Details and the ffmpeg command are in `sounds/README.md`.
- **A limiter before the destination, which is load-bearing.** At these levels a
  fast run of eight drops measured 1.085 of full scale — distortion. The
  limiter brings it to 0.87 and leaves a single sound at 0.60. Anyone raising
  the file levels again has to re-measure a pile-up, not assume it still holds.

Verified in the browser by instrumenting Web Audio: all three start with real
decoded buffers including the first card, twenty sounds across a full sort,
overlapping output measured, mute silences a peal mid-ring and blocks new
drops, the setting survives a reload, and the default is unmuted.

### Licence — settled, all CC0

All three came from Freesound and all three are CC0: bells #870015 by
SignatureSoundsOrg, bubbles #145797 by 211redman112, zombie #196723 by
PaulMorek. CC0 permits redistribution, modification and commercial use and
requires no attribution, so there is nothing outstanding. `sounds/README.md`
credits them anyway, as courtesy rather than obligation, and the page carries
a one-line Freesound credit that could be removed without consequence.

Identifying them took the original filenames from Mark. The MP3s' own ID3 tags
are worthless here: all three carry a byte-identical block naming a title and
uploader belonging to none of them, left by whatever tool did the conversion.
Do not trust embedded metadata as provenance.

#### Reference sounds — audio.com, cannot ship, kept on purpose

Found by Mark on audio.com. Licences checked 2026-11-04: **none of these six
can ship** (why, below). Mark is sourcing or recording his own and asked to
keep these as the comparison — they are the target to match, not files to
use. Listen to them, then find or record something that sounds like them
under a licence that permits it.

| Possible bucket | Sound | Length | Link |
|---|---|---|---|
| Kill | Zombie craving for brain | 0:33 | <https://audio.com/hertzheirloomvoyager/audio/zombie-craving-for-brain> |
| Kill or Modify | Sinister female laughter | 0:01 | <https://audio.com/sonicfableforge/audio/sinister-female-laughter-sound-effects> |
| Keep | Nepomuk's church bells | 2:00 | <https://audio.com/freqshiftnomad/audio/nepomuk-s-church-bells> |
| Keep | Struck singing bowl | 0:05 | <https://audio.com/decibelphantomx/audio/sound-of-striking-a-singing-bowl> |
| Modify | Large bubbles, vol. 3 | 0:21 | <https://audio.com/freqshiftnomad/audio/large-bubbles-volume-3> |
| Modify | Bubble sound effects (collection) | — | <https://audio.com/acousticalchemyartisan5/collections/bubble-sound-effects> |

Read together these suggest a different and better scheme than the original
note: church bells for Van Helsing, a bubbling potion for Jekyll, a groan for
the Zombie. That is more legible than "choral swell / quizzical rise / groan",
because each sound names its character rather than its mood.

**Why none of them ship.** No upload on audio.com states its own licence — all
six were checked, and the only terms are the site-wide ones. Those say:

> Content received through the Service, that isn't modified after acquisition,
> may be accessed for your personal, non-commercial use only.

and separately prohibit users from choosing to "publish, transmit, distribute,
display [or] redistribute" that content. Putting a file in this repo serves it
from a public website, which is distribution, and an employer's away day is not
personal use. Two independent reasons it fails; no amount of trimming fixes
either, since the "modified after acquisition" wording grants nothing.

**Where to look instead.** Each of these states a licence per file, which is
the thing audio.com does not do:

- **freesound.org**, filtered to CC0. Strong on groans, bells and bubbles, and
  CC0 needs no attribution at all.
- **Pixabay** — its own licence covers commercial use with no attribution.
- **Zapsplat** — free with attribution, paid to drop it.
- A paid library (Epidemic Sound, Artlist, Soundsnap) if the employer will
  cover it. Cleanest rights, and these are three files.

**Or record them.** Bubbles are a straw in a glass of water. A groan is a phone
voice memo pitched down. A bell is a wine glass. Thirty seconds of effort,
nothing to attribute, nobody's terms to read, and it is funnier at the away day
for being the team's own. Of all the routes this is the one most likely to
actually get done.

**Length, whatever the source.** The durations above are why this matters: two
minutes of church bells is not a drop sound. Per-card sounds want trimming to
roughly half a second, with a longer version kept for the final card at most.
