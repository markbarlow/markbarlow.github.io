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

## Noted, not yet built

### A sound on each drop — TODO, waiting on Mark's audio files

One per bucket, in character: a positive choral swell for **Keep**, a quizzical
rising inflection for **Modify**, a groan for **Kill**.

**Synthesis was tried and rejected.** Nine candidates were generated with Web
Audio — three per bucket, balanced to within 1.3x peak — and published as a
preview at <https://claude.ai/artifact/BqefxNFo6zW1zK8W6J44cw>. Mark did not
like them. So "synthesised or sampled" is settled: **sampled**, and he is
sourcing the audio himself. Do not re-propose synthesis.

When the files arrive, what the implementation needs:

- **Where they live:** `keep-kill-modify/sounds/`, with a `README.md` naming
  each file's source and licence, as `fonts/README.md` already does. Anything
  without a licence that clearly permits this use does not ship.
- **Format:** MP3 plays everywhere that matters. Keep each file small — these
  load on venue wifi, and the page's whole point is that it is light.
- **Length is the design constraint, not timbre.** Each sound plays once per
  card, about twenty times in three minutes. Measured against the synthesised
  set, anything past roughly half a second wears out fast. If Mark's files are
  long, trim them for the per-card sound and consider keeping the full-length
  version for the final card only, where it reads as a reward rather than a tax.
- **Default off**, with a visible speaker toggle, remembered in `localStorage`.
  People open this from a Slack link on a work laptop, sometimes beside someone
  else. Browsers block audio until the first interaction anyway, so the first
  card would be silent whatever we do; an explicit toggle turns that limitation
  into a choice.
- **Fire-and-forget.** Playback is decorative: a failed, missing or blocked file
  must never delay or block a drop, exactly as the drop animations already work.
  Call `play()` inside a try and swallow the rejected promise.
- **Not tied to `prefers-reduced-motion`.** That flag is about motion, not
  sound. The toggle is the control for this.

#### Candidate sources (Mark's, unchecked)

Found by Mark, saved here to audition later. Nothing below has been listened
to, licence-checked or trimmed, and the bucket column is only my reading of
what each might be for.

| Possible bucket | Sound | Link |
|---|---|---|
| Kill | Zombie craving for brain | <https://audio.com/hertzheirloomvoyager/audio/zombie-craving-for-brain> |
| Kill or Modify | Sinister female laughter | <https://audio.com/sonicfableforge/audio/sinister-female-laughter-sound-effects> |
| Keep | Nepomuk's church bells | <https://audio.com/freqshiftnomad/audio/nepomuk-s-church-bells> |
| Keep | Struck singing bowl | <https://audio.com/decibelphantomx/audio/sound-of-striking-a-singing-bowl> |
| Modify | Large bubbles, vol. 3 | <https://audio.com/freqshiftnomad/audio/large-bubbles-volume-3> |
| Modify | Bubble sound effects (collection) | <https://audio.com/acousticalchemyartisan5/collections/bubble-sound-effects> |

Read together these suggest a different and better scheme than the original
note: church bells for Van Helsing, a bubbling potion for Jekyll, a groan for
the Zombie. That is more legible than "choral swell / quizzical rise / groan",
because each sound names its character rather than its mood.

Two things to settle before any of these ship:

- **Licence.** audio.com terms vary per upload, so each file needs its own
  check, and whatever it says goes in `sounds/README.md` beside the file. No
  licence, no ship.
- **Length.** Bells and singing bowls ring for seconds. Per-card sounds need
  trimming to roughly half a second, with the full ring kept for the final
  card at most.
