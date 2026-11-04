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

Mark's feedback after the first build, recorded here while the rest of it
arrives. Nothing below is implemented.

- **A sound on each drop**, one per bucket, in character:
  - **Keep** — a short choral, positive "Gloria!" swell.
  - **Modify** — a quizzical, rising-inflection sound.
  - **Kill** — a zombie groan.

  Open questions when this gets built: whether the sounds are synthesised in the
  page (Web Audio, no files, keeps the "no dependencies" non-goal intact) or
  shipped as three small audio files; and that there must be a mute control,
  defaulted off or on — a page that makes noise unprompted on a work laptop is
  the kind of thing people close. Sound also has to stay a garnish, since
  browsers block audio until the first interaction and the page must work
  silently.
