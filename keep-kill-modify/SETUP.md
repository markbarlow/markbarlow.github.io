# Setting it up

About three minutes, once. You need a Google account; everything stays in your
own Drive.

## 1. Make a Sheet

Create a new Google Sheet. Call it whatever you like. Leave it empty — the
script creates the tab and headers itself on the first submission.

## 2. Open Apps Script

In that Sheet: **Extensions → Apps Script**. A new tab opens with a file called
`Code.gs` containing a stub `myFunction`.

## 3. Paste the script

Delete everything in the editor and paste the whole contents of
[`apps-script/Code.gs`](apps-script/Code.gs). Save (⌘S).

## 4. Set the headcount

At the top of the script, edit `CONFIG`:

```js
expected: {
  'platform-team-2026-11': 12
}
```

The key must match `SESSION_ID` in [`config.js`](config.js) exactly. It is only
used to render "7 of 12 responded".

`closeDates` is empty, which means **no gate**: results are readable as soon as
ballots arrive. That is what you want for a live session. See "Running it live"
below, and "Withholding results" if you ever need the other mode.

## 5. Deploy it

**Deploy → New deployment**, then:

- Select type: **Web app** (click the gear icon if the option isn't showing)
- Description: anything
- Execute as: **Me**
- Who has access: **Anyone**

Click **Deploy**. Google asks you to authorise it — this is your own script
writing to your own Sheet, so approve it. You may have to click through
"Advanced → Go to (project name)"; that warning appears for every unpublished
personal script.

Copy the **Web app URL**. It ends in `/exec`.

## 6. Paste the URL into config.js

```js
ENDPOINT_URL: 'https://script.google.com/macros/s/AKfy..../exec',
```

Commit and push. Done.

## Check it works

1. Open the page, sort the list, send it. You should land on the thank-you screen.
2. Look at the Sheet — one row should have appeared.
3. Open the page at `#results`. You should see your own ballot counted.

Do this once yourself before the session. It is the only step that proves the
whole round trip, and it takes a minute.

## Running it live

For an away-day session where everyone votes in the room and you show the
results there and then:

- Leave `CLOSE_DATE` empty in `config.js` and `closeDates` empty in the script.
  Results are then live.
- Share the page URL. A short link or a QR code on the slide beats reading it out.
- Keep `#results` open on the projector while people sort. It shows turnout —
  "14 of 20 have returned a card" — so you can see when to call time. Hit
  refresh to re-poll; it never auto-reloads under you.
- Set `EXPECTED_RESPONDENTS` to the number of people in the room, or that
  counter has nothing to count against.
- **Venue wifi is the risk, not the script.** If a send fails the page keeps the
  answers and offers a retry plus a download, so nobody loses their sorting —
  but tell people to speak up if they see a red banner rather than silently
  giving up.

If the send fails, the page says so, keeps your answers, and offers a retry and
a "save as file" button. Nothing is lost.

## A note on caching

GitHub Pages serves `config.js` with a ten-minute cache. If you change the
session, the list or the endpoint and immediately reload, you may still get the
old one — I hit this while testing. Wait a few minutes, or hard-refresh
(⌘⇧R). It only affects you during setup; by the time the team opens the link
it will be the current version.

## When you change the list or start a new round

- **Changing the activity list** after people have started voting will mis-align
  their answers. Change `SESSION_ID` at the same time and treat it as a new round.
- **A new round** needs a new `SESSION_ID` in `config.js` plus matching entries in
  the script's `closeDates` and `expected`. Old rounds stay in the same Sheet
  under their own id and are not mixed in.
- **Re-deploying** after editing the script: Deploy → Manage deployments → edit
  (pencil) → Version: New version → Deploy. The URL stays the same.

## What is and isn't private

- **Anonymous to the team and to the page.** No name, no email. The endpoint only
  ever serves aggregate counts, never individual ballots, so there is nothing to
  read even in the page's network traffic. The Modify notes are shuffled before
  being served, so their order can't be matched against arrival order.
- **Not anonymous to you.** The Sheet holds one row per ballot with a timestamp,
  which is what makes an edited resubmission replace the old one instead of
  double-counting. On a small team, submission order plus timestamps are partly
  identifying. So tell the team it's anonymous to each other, which is true — not
  that it's anonymous full stop.
- **The tally runs on the honour system.** There is no login and no guard, by
  choice. One person voting from a laptop and a phone counts twice, and anyone
  with the link can submit. Fine for a team exercise; don't quote the numbers
  outside the team as if they were audited.
- **`#results` is unlisted, not secret.** Anyone reading the page source can
  find it, and with no gate configured it shows the running tally to anyone who
  does. For a live session that is the point. If you ever need it withheld, see
  below — obscurity is not what protects it.

## Withholding results (the other mode)

Only needed if people vote over several days and you want the split hidden until
a reveal. Add the session to `closeDates` in the script **and** set the same date
in `config.js`:

```js
closeDates: { 'platform-team-2026-11': '2026-11-14' }
```

Then redeploy (Deploy → Manage deployments → edit → New version). Two things to
know: the script is the real gate, so a date in `config.js` alone does nothing
but change the wording on the page; and a session id missing from `closeDates`
is **never sealed**, so it fails open, not closed. Before the date, `#results`
shows turnout only — enough to see who is still outstanding, not enough to
anchor you.
