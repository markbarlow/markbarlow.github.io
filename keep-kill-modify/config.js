/* Keep / Kill / Modify — the only file you need to edit.
   After changing this, commit and push; GitHub Pages picks it up. */

window.KKM_CONFIG = {

  /* ---- Which review this is -------------------------------------------- */

  /* >>> CURRENTLY IN REHEARSAL MODE <<<
     Practice ballots go to their own id, so they never mix into the real
     tally and #results starts empty on the day.

     ON THE DAY, change BOTH of these back:
         SESSION_ID:   'product-team-rehearsal'  ->  'product-team-2026-11'
         SESSION_NAME: 'Rehearsal ...'           ->  'Product team away day'

     Leave it in rehearsal mode and the away day's answers land in the
     practice bucket on top of the practice votes. The name below says
     "Rehearsal" on the page itself so this is visible, not just a comment.

     The Apps Script has a matching list in its CONFIG.expected, holding
     BOTH ids. So long as both are there, switching between them needs no
     script change and no redeploy. If you ever add a new session id,
     add it there too, or the results show a bare count instead of
     "7 of 10" -- and adding one means redeploying the script. */
  SESSION_ID: 'product-team-rehearsal',

  /* Shown on the page. */
  SESSION_NAME: 'Rehearsal — Product team away day',

  /* ---- Where the answers go -------------------------------------------- */

  /* Paste the Apps Script /exec URL here. See SETUP.md — about three
     minutes, once. Left empty, the page still plays through but says it
     cannot send anything. */
  ENDPOINT_URL: 'https://script.google.com/macros/s/AKfycbzYyx_gJtrg6GlNMn8dE63gc3-cZX5a7V6ZYdDkrKj8OwDavW71xefOIrl9WDG4ob_9/exec',

  /* Leave this EMPTY for a live session (everyone votes in the room, you
     put the results on the screen there and then). Results are then
     readable as soon as ballots arrive.

     Set a date (YYYY-MM-DD, 00:00 UTC) only if people vote over several
     days and you want the split withheld until a reveal. If you do, set
     the SAME date in the Apps Script's closeDates -- the script is what
     actually withholds it; this one is only what the page displays. */
  CLOSE_DATE: '',

  /* How many people you asked, so the results read "7 of 10 responded".
     In a live session this is your "are we done yet?" signal, so it is
     worth getting right. Set to 0 to show a bare count instead. */
  EXPECTED_RESPONDENTS: 10,

  /* ---- The list -------------------------------------------------------- */

  /* Mark's list, 2026-11-16. Ids are names rather than numbers on purpose:
     votes are stored against the id, so if you reorder or insert an
     activity, numbered ids quietly attach old answers to the wrong thing.
     Renaming the "name" is always safe; changing an "id" is not, once
     anyone has voted. "meta" is optional. */
  ACTIVITIES: [
    { id: 'team-weekly-update',         name: 'Weekly update for our team',            meta: 'Weekly, 15 min, 9 people' },
    { id: 'company-weekly-update',      name: 'Weekly update for the company',         meta: 'Weekly, 5 min, 9 people' },
    { id: 'quarterly-product-review',   name: 'Quarterly product reviews',             meta: 'Quarterly, 4–5 hours including prep, 9 people' },
    { id: 'weekly-team-meeting',        name: 'Weekly team meeting',                   meta: 'Weekly, 15–60 min, 9 people' },
    { id: 'biweekly-design-catchup',    name: 'Biweekly design catchup',               meta: 'Fortnightly, 1 hour, 10–15 people' },
    { id: 'design-team-catchup',        name: 'Design team catchup',                   meta: 'Fortnightly, 1 hour, 3 people' },
    { id: 'frontend-catchup',           name: 'Frontend catchup',                      meta: 'Monthly, 1 hour, 6 people' },
    { id: 'product-psa',                name: 'Product <> PSA',                        meta: 'Fortnightly, 1 hour, 4–8 people' },
    { id: 'ai-agentic-marketing',       name: 'AI and Agentic marketing',              meta: 'Monthly, 30 min, 6 people' },
    { id: 'sausage-sandwich-game',      name: 'Sausage sandwich game',                 meta: 'Monthly, 30 min, 9 people' },
    { id: 'sales-closed-lost-review',   name: 'Sales closed/lost review',              meta: 'Quarterly, 45 min, 10–20 people' },
    { id: 'beamer-updates',             name: 'Beamer updates',                        meta: 'As needed, 30 min, 2 people' },
    { id: 'product-feature-pages',      name: 'Product feature pages',                 meta: 'As needed, 30–60 min, 1 person' },
    { id: 'integrating-clients-update', name: 'Integrating clients update',            meta: 'Fortnightly, 30 min, 10–20 people' },
    { id: 'team-learning-sessions',     name: 'Team learning sessions',                meta: 'Occasional, 30–60 min, inside the team meeting' },
    { id: 'product-detection-roadmap',  name: 'Product <> Detection roadmap planning', meta: 'Every 6 months, 45 min, 3–6 people' },
    { id: 'product-team-away-day',      name: 'Product team away day',                 meta: 'Annual, a full day, 9 people' }
  ]

};
