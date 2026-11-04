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

## 4. Set the session and the close date

At the top of the script, edit `CONFIG`:

```js
closeDates: {
  'platform-team-2026-11': '2026-11-14'
},
expected: {
  'platform-team-2026-11': 12
}
```

The key must match `SESSION_ID` in [`config.js`](config.js) exactly.

**The close date has to be set in both places.** The one in `config.js` is only
what the page displays; the one here is what actually withholds the results. If
you only change `config.js`, the page will say the wrong date and the tally will
unlock at the old one.

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
3. Open the page at `#results`. Before the close date you'll see turnout only;
   after it, the full split.

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
- **`#results` is unlisted, not secret.** Anyone reading the page source can find
  it. What protects the tally before the meeting is the close date in the script,
  which no amount of reading the page gets around.
