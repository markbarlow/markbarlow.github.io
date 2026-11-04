/* Keep / Kill / Modify — the only file you need to edit.
   After changing this, commit and push; GitHub Pages picks it up. */

window.KKM_CONFIG = {

  /* ---- Which review this is -------------------------------------------- */

  /* A short id. Change it to start a fresh round; old rounds stay in the
     Sheet under their own id and are not mixed in. No spaces. */
  SESSION_ID: 'platform-team-2026-11',

  /* Shown on the page. */
  SESSION_NAME: 'Platform team',

  /* ---- Where the answers go -------------------------------------------- */

  /* Paste the Apps Script /exec URL here. See SETUP.md — about three
     minutes, once. Left empty, the page still plays through but says it
     cannot send anything. */
  ENDPOINT_URL: '',

  /* Results stay locked until this date, so nobody can see the tally while
     people are still voting. The Apps Script enforces it, not the page.
     Format YYYY-MM-DD, treated as that date at 00:00 UTC. */
  CLOSE_DATE: '2026-11-14',

  /* How many people you asked, so the results read "7 of 12 responded".
     Set to 0 to show a bare count instead. */
  EXPECTED_RESPONDENTS: 12,

  /* ---- The list -------------------------------------------------------- */

  /* Replace these with your real activities. Keep the ids stable once
     people have started voting, or their answers will not line up.
     "meta" is optional. */
  ACTIVITIES: [
    { id: 'a01', name: 'Daily stand-up',             meta: 'Weekdays, 15 min, 9 people' },
    { id: 'a02', name: 'Sprint planning',            meta: 'Fortnightly, 90 min, whole team' },
    { id: 'a03', name: 'Sprint retrospective',       meta: 'Fortnightly, 60 min, whole team' },
    { id: 'a04', name: 'Backlog refinement',         meta: 'Weekly, 60 min, 6 people' },
    { id: 'a05', name: 'Weekly metrics review',      meta: 'Thursdays, 60 min, 9 people' },
    { id: 'a06', name: 'Weekly team meeting',        meta: 'Mondays, 45 min, whole team' },
    { id: 'a07', name: 'Monthly all-hands',          meta: 'Monthly, 60 min, everyone' },
    { id: 'a08', name: 'Quarterly OKR review',       meta: 'Quarterly, half a day' },
    { id: 'a09', name: 'Weekly one-to-ones',         meta: 'Weekly, 30 min each' },
    { id: 'a10', name: 'Design review forum',        meta: 'Weekly, 60 min, open invite' },
    { id: 'a11', name: 'Architecture review board',  meta: 'Fortnightly, 90 min, 5 people' },
    { id: 'a12', name: 'On-call handover',           meta: 'Weekly, 30 min, 4 people' },
    { id: 'a13', name: 'Incident post-mortems',      meta: 'As needed, 60 min' },
    { id: 'a14', name: 'Friday demo',                meta: 'Weekly, 45 min, open invite' },
    { id: 'a15', name: 'Written status update',      meta: 'Weekly, written, everyone' },
    { id: 'a16', name: 'Stand-up bot thread',        meta: 'Daily, in Slack, whole team' },
    { id: 'a17', name: 'Lunch and learn',            meta: 'Monthly, 60 min, optional' },
    { id: 'a18', name: 'Code review rota',           meta: 'Daily, ad hoc, whole team' },
    { id: 'a19', name: 'Documentation day',          meta: 'Quarterly, full day' },
    { id: 'a20', name: 'Team social',                meta: 'Monthly, evening, optional' }
  ]

};
