/**
 * Keep / Kill / Modify — collection endpoint.
 *
 * Paste this whole file into a Google Apps Script project bound to a Sheet,
 * then deploy it as a Web App with access "Anyone". See SETUP.md.
 *
 * It does two things:
 *   POST  one ballot  -> upserted into the sheet by ballotId
 *   GET   ?session=X  -> aggregate counts only, and only once sealed
 *
 * Individual ballots are never served. Before the close date not even the
 * split is served, only the turnout.
 */

var CONFIG = {

  /* The tab the ballots are written to. Created on first use. */
  sheetName: 'ballots',

  /* Reject anything larger than this, in bytes. */
  maxBytes: 20000,

  /* EMPTY = no gate: results are readable as soon as ballots arrive.
     That is what you want for a live session.

     For a vote that runs over several days, add the session id here with
     the date its results may be revealed, and set the SAME date in
     config.js. THIS is the real gate -- config.js only displays it.
       closeDates: { 'platform-team-2026-11': '2026-11-14' }
     Format YYYY-MM-DD, compared at 00:00 UTC. */
  closeDates: {},

  /* Sessions not listed above: '' means never sealed. */
  defaultCloseDate: '',

  /* How many people were asked, per session. Shown as "7 of 12". */
  expected: {
    'platform-team-2026-11': 12
  },

  /* Hard ceiling on how many activities one ballot may carry. */
  maxActivities: 200
};

var BUCKETS = { keep: true, modify: true, kill: true };

/* ------------------------------------------------------------------ */
/* POST: receive one ballot                                            */
/* ------------------------------------------------------------------ */

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return json({ ok: false, error: 'Empty request.' });
    }
    var raw = e.postData.contents;
    if (raw.length > CONFIG.maxBytes) {
      return json({ ok: false, error: 'That ballot is too large.' });
    }

    var body;
    try {
      body = JSON.parse(raw);
    } catch (parseErr) {
      return json({ ok: false, error: 'Could not read that ballot.' });
    }

    var sessionId = asId(body.sessionId);
    var ballotId = asId(body.ballotId);
    if (!sessionId) { return json({ ok: false, error: 'Missing session.' }); }
    if (!ballotId) { return json({ ok: false, error: 'Missing ballot id.' }); }

    var votes = cleanVotes(body.votes);
    if (!votes.count) { return json({ ok: false, error: 'That ballot has no verdicts.' }); }
    var notes = cleanNotes(body.notes, votes.map);

    var lock = LockService.getScriptLock();
    lock.waitLock(20000);
    try {
      var sheet = getSheet();
      var rows = sheet.getDataRange().getValues();
      var at = new Date().toISOString();
      var line = [at, sessionId, ballotId, JSON.stringify(votes.map), JSON.stringify(notes)];

      var found = 0;
      for (var i = 1; i < rows.length; i++) {
        if (String(rows[i][1]) === sessionId && String(rows[i][2]) === ballotId) {
          found = i + 1;
          break;
        }
      }
      if (found) {
        sheet.getRange(found, 1, 1, line.length).setValues([line]);
      } else {
        sheet.appendRow(line);
      }
    } finally {
      lock.releaseLock();
    }

    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: 'The server could not store that ballot.' });
  }
}

/* ------------------------------------------------------------------ */
/* GET: serve aggregates only                                          */
/* ------------------------------------------------------------------ */

function doGet(e) {
  try {
    var sessionId = asId(e && e.parameter ? e.parameter.session : '');
    if (!sessionId) { return json({ error: 'Missing session.' }); }

    var sheet = getSheet();
    var rows = sheet.getDataRange().getValues();

    var total = 0;
    var counts = {};
    var notes = {};

    for (var i = 1; i < rows.length; i++) {
      if (String(rows[i][1]) !== sessionId) { continue; }
      total++;

      var v = {};
      var n = {};
      try { v = JSON.parse(rows[i][3] || '{}'); } catch (e1) { v = {}; }
      try { n = JSON.parse(rows[i][4] || '{}'); } catch (e2) { n = {}; }

      for (var id in v) {
        if (!Object.prototype.hasOwnProperty.call(v, id)) { continue; }
        var b = v[id];
        if (!BUCKETS[b]) { continue; }
        if (!counts[id]) { counts[id] = { keep: 0, modify: 0, kill: 0 }; }
        counts[id][b]++;
      }
      for (var nid in n) {
        if (!Object.prototype.hasOwnProperty.call(n, nid)) { continue; }
        var text = String(n[nid] || '').slice(0, 160);
        if (!text) { continue; }
        if (!notes[nid]) { notes[nid] = []; }
        notes[nid].push(text);
      }
    }

    var expected = CONFIG.expected[sessionId] || 0;

    if (isSealed(sessionId)) {
      return json({ open: true, total: total, expected: expected });
    }

    /* Shuffle each activity's notes so their order cannot be matched up
       against the order ballots arrived in. */
    for (var key in notes) {
      if (Object.prototype.hasOwnProperty.call(notes, key)) {
        notes[key] = shuffle(notes[key]);
      }
    }

    return json({
      open: false,
      total: total,
      expected: expected,
      counts: counts,
      notes: notes
    });
  } catch (err) {
    return json({ error: 'The server could not read the results.' });
  }
}

/* ------------------------------------------------------------------ */
/* helpers                                                             */
/* ------------------------------------------------------------------ */

function isSealed(sessionId) {
  var raw = Object.prototype.hasOwnProperty.call(CONFIG.closeDates, sessionId)
    ? CONFIG.closeDates[sessionId]
    : CONFIG.defaultCloseDate;
  if (!raw) { return false; }
  var when = new Date(raw + 'T00:00:00Z');
  if (isNaN(when.getTime())) { return false; }
  return new Date().getTime() < when.getTime();
}

function cleanVotes(votes) {
  var map = {};
  var count = 0;
  if (votes && typeof votes === 'object') {
    for (var id in votes) {
      if (!Object.prototype.hasOwnProperty.call(votes, id)) { continue; }
      if (count >= CONFIG.maxActivities) { break; }
      var key = asId(id);
      var val = String(votes[id] || '');
      if (key && BUCKETS[val]) {
        map[key] = val;
        count++;
      }
    }
  }
  return { map: map, count: count };
}

function cleanNotes(notes, voteMap) {
  var out = {};
  if (!notes || typeof notes !== 'object') { return out; }
  var n = 0;
  for (var id in notes) {
    if (!Object.prototype.hasOwnProperty.call(notes, id)) { continue; }
    if (n >= CONFIG.maxActivities) { break; }
    var key = asId(id);
    if (!key || !voteMap[key]) { continue; }
    var text = String(notes[id] || '').replace(/[\u0000-\u001F\u007F]/g, ' ').trim().slice(0, 160);
    if (text) { out[key] = text; n++; }
  }
  return out;
}

function asId(v) {
  var s = String(v == null ? '' : v).trim().slice(0, 80);
  return /^[A-Za-z0-9._:-]+$/.test(s) ? s : '';
}

function shuffle(list) {
  var a = list.slice();
  for (var i = a.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}

function getSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(CONFIG.sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(CONFIG.sheetName);
    sheet.appendRow(['submitted_at', 'session_id', 'ballot_id', 'votes_json', 'notes_json']);
  }
  return sheet;
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
