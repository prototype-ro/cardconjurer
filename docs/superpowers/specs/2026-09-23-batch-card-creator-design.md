# Batch Card Creator

Date: 2026-09-23

## Goal

Generate many real cards unattended from a plain-text list: card name
(imported from Scryfall, optionally pinned to a specific set/print),
optional nickname, a saved frame preset, and whether to include art.
Each row produces the same 3 files the Export tab already produces
per card.

Builds on [2026-09-23-frame-presets-and-export-design.md](2026-09-23-frame-presets-and-export-design.md)
(frame presets, Export tab) — both already merged.

## 1. Frame preset enhancement: capture + replay Frame Group/Pack

### Why

Real card text (title/mana/type/rules/P-T) only fills into textboxes
that already exist on `card.text`. Those textboxes are created by
"Load Frame Version" — a mechanism entirely separate from frame
presets today: picking a Frame Group (`#selectFrameGroup`) loads a
group script that populates a Frame Pack list; picking a Frame Pack
(`#selectFramePack`) loads a pack script that defines what "Load Frame
Version" does for that pack (sets `card.version`, art/set-symbol/
watermark bounds, and — via `loadTextOptions(...)` — the `card.text`
schema itself).

For a frame preset to build a card from nothing (as batch needs), it
must also remember and replay that Frame Group + Pack + "Load Frame
Version" step, not just the visual frame-image stack + text styling
it captures today.

### What changes

**Save** (`saveFramePreset()`, [js/creator-23.js](../../../js/creator-23.js),
search `saveFramePreset`): also capture
`document.querySelector('#selectFrameGroup').value` and
`document.querySelector('#selectFramePack').value` into the stored
record:

```js
{
  frameGroup: 'Standard-3',      // #selectFrameGroup value at save time
  framePack: 'M15Regular-1',     // #selectFramePack value at save time
  frames: [...],                  // unchanged from today
  textStyles: {...}               // unchanged from today
}
```

### New helper: `loadScriptAsync(path)`

The existing `loadScript(path)` ([js/creator-23.js](../../../js/creator-23.js),
search `function loadScript`) is fire-and-forget: it appends a
`<script>` tag with no completion signal. It's used all over the
codebase for manual, user-driven frame switching, where "fire and
forget" is fine — the browser executes the script and whatever DOM
updates happen, happen. Frame-preset apply and batch need to know
*when* a given script has finished executing, so they don't proceed
before e.g. `#loadFrameVersion.onclick` has been set to the right
pack's handler.

Add a new, separate helper (does not modify `loadScript` or any of
its ~15 existing call sites):

```js
function loadScriptAsync(scriptPath) {
	return new Promise((resolve, reject) => {
		var script = document.createElement('script');
		script.setAttribute('type', 'text/javascript');
		script.onload = () => resolve();
		script.onerror = () => reject(new Error('Failed to load script: ' + scriptPath));
		script.setAttribute('src', scriptPath);
		document.querySelectorAll('head')[0].appendChild(script);
	});
}
```

### Apply (`applyFramePreset(presetName)`): replay schema before layering frames/styles

Today `applyFramePreset` only rebuilds `card.frames` and merges
`textStyles` onto existing `card.text` keys. It gains a new first
phase, run only when the preset has `frameGroup`/`framePack` saved
(presets saved before this change won't have these fields — treat
their absence as "skip this phase," so old presets keep working
exactly as before, just without the schema-replay step):

```js
async function applyFramePreset(presetName) {
	if (!presetName) {return;}
	try {
		var preset = await cardDB.get(presetName, 'framePresets');
		if (!preset) {
			notify(presetName + ' failed to load.', 5);
			return;
		}
		// NEW: replay Frame Group + Pack + "Load Frame Version", if saved
		if (preset.frameGroup && preset.framePack) {
			document.querySelector('#selectFrameGroup').value = preset.frameGroup;
			await loadScriptAsync('/js/frames/group' + preset.frameGroup + '.js');
			document.querySelector('#selectFramePack').value = preset.framePack;
			await loadScriptAsync('/js/frames/pack' + preset.framePack + '.js');
			await document.querySelector('#loadFrameVersion').onclick();
		}
		// frame stack (unchanged from today, still runs after the above)
		document.querySelector('#frame-list').innerHTML = null;
		card.frames = JSON.parse(JSON.stringify(preset.frames));
		card.frames.reverse();
		await card.frames.forEach(item => addFrame([], item));
		card.frames.reverse();
		// linked text styling (unchanged from today)
		Object.entries(preset.textStyles || {}).forEach(([key, style]) => {
			if (card.text[key]) {
				Object.assign(card.text[key], style);
			}
		});
		drawTextBuffer();
	} catch (error) {
		notify('Failed to apply frame preset "' + presetName + '" (' + error.message + ').');
	}
}
```

Why `await document.querySelector('#loadFrameVersion').onclick()`
rather than `.click()`: every pack script assigns `onclick` to an
`async function`. Calling it as a plain function (`el.onclick()`)
invokes it with `this` bound to `el` — identical runtime behavior to
a real click dispatch — but, unlike `.click()`, returns its promise so
we can `await` the schema being fully set up (text options loaded,
art/set-symbol/watermark bounds reset) before touching `card.frames`/
`card.text` ourselves in the next phase. This deliberately bypasses
the user's personal "Auto load Frame Version" checkbox
(`localStorage.autoLoadFrameVersion`) — preset apply always loads the
version explicitly, regardless of that setting, so its behavior is
deterministic.

`resetCardIrregularities()` (called inside every pack's Load Frame
Version handler) does not touch `card.frames`, so no reordering
hazard between the schema-replay phase and the existing frame-image
phase.

## 2. Batch Card Creator

### UI

New tab, "Batch", next to Export (same `toggleCreatorTabs` mechanism,
`#creator-menu-batch` panel).

- `<textarea id='batch-input'>` — one card per line:

  ```
  Cardname | SetCode | CollectorNumber | Nickname | FramePresetName | art-flag
  ```

  - `Cardname` — required, passed verbatim to Scryfall's exact-name
    search (same as typing it into Import/Save's "Import a real card
    by name" field).
  - `SetCode` — optional, blank allowed. When given, picks that
    specific printing (e.g. `MH3`) instead of Scryfall's
    default/most-recent print, matched case-insensitively against
    each result's `set` field.
  - `CollectorNumber` — optional, blank allowed, only meaningful
    together with `SetCode` (a set alone can still have many prints —
    e.g. showcase/borderless variants share a set code with the
    regular printing but differ by collector number). Matched as a
    trimmed string against each result's `collector_number` field.
  - `Nickname` — optional, blank allowed
    (`Card Name | MH3 | 343 || Preset | art`). Overwrites
    `card.text.nickname.text` after import, only if non-blank.
  - `FramePresetName` — required, must match a key in the
    `framePresets` IndexedDB store.
  - `art-flag` — required, literal `art` or `no-art`.
  - Blank lines ignored. Leading/trailing whitespace trimmed per
    field. This is the app's own structured format — pasting a
    decklist (e.g. Moxfield's `1 Kaalia of the Vast (MH3) 343`
    export syntax) directly into the textarea is not supported by the
    app itself; translating that kind of list into this pipe-delimited
    format is a task for whoever is preparing the batch input (may be
    done conversationally, outside the app).

- "Parse" button → splits the textarea into rows, builds a
  `batchRows` array (`{cardname, setCode, collectorNumber, nickname,
  presetName, artFlag, status: 'pending'}` per row — `status` is what
  the summary/retry features below read and update), renders a
  preview `<table>` below: row #, cardname (with set/number suffix
  shown if given, e.g. "Kaalia of the Vast (MH3 #343)"), nickname (or
  "—"), preset name with ✅/❌ (checked against a fresh
  `cardDB.keys('framePresets')` read), art-flag with ✅/❌ (valid only
  if exactly `art` or `no-art`, case-insensitive), and a Status
  column (blank until a run starts). A row failing the preset/art-flag
  check is styled red and excluded from the run. `SetCode`/
  `CollectorNumber` are never validated at parse time (Scryfall is the
  only source of truth for whether they match a real print) — a bad
  set/number is only caught when the row actually runs, per step 2
  below.

- "Run Batch" button — disabled until at least one row has been
  parsed and is valid. Runs rows sequentially (never in parallel —
  see Error Handling below for why). Shows a simple progress line
  ("Processing 3 / 12: Lightning Bolt...") above the table, updated
  per row, and updates each row's Status cell live (⏳ running, ✅
  done, ❌ + reason) as it goes.

- "Stop" button — appears only while a run is in progress, next to
  the progress line. Sets a module-level `batchCancelled = true` flag.
  The run loop (per-row processing, below) checks this flag once
  *between* rows — after the current row's 800ms inter-row delay
  finishes, before starting the next row — and exits the loop if set.
  It does not interrupt a row already in progress (no clean way to
  abort a row mid-Scryfall-fetch/mid-download without leaving `card`
  in a half-applied state); the in-flight row always finishes first.
  Stopping still produces the end-of-run summary below, scoped to
  whatever ran before the stop.

- **End-of-run summary** — rendered above the table once a run
  finishes or is stopped: counts ("14 succeeded, 2 skipped, 1
  stopped before running") plus a list of every non-success row with
  its reason (the same message the per-row `notify()` call used —
  see Error Handling). Stays on screen until the next "Parse" or "Run
  Batch" click clears it.

- **Retry** — each failed row's Status cell gets a small "Retry"
  button once the run finishes. Clicking it re-runs just that one row
  through the same per-row pipeline (step 1-6 below) and updates its
  Status cell + the summary counts in place — no need to re-run the
  whole batch for one bad row.

- **Run Remaining** — appears in the summary once a run was stopped
  or partially failed: re-runs only rows whose `status` is not yet
  `'success'` (i.e. `'pending'` rows never reached because of a Stop,
  plus any `'error'` rows), in their original order, without
  re-running rows that already succeeded.

### Persistence: saving a batch list

New IndexedDB object store `batchLists` (same `CardConjurerDB`,
alongside `cards` and `framePresets`, bumping the DB version again —
same pattern as the `framePresets` store's own addition: guard
creation with `objectStoreNames.contains` in `onupgradeneeded` so
existing data in the other two stores is untouched). Key = list name,
value = the raw textarea string (no need to store the parsed
`batchRows` — re-parsing on load is cheap and keeps this store
trivial: one string per name).

UI, in the Batch tab, mirroring the frame-preset save/load/delete
pattern already built:
- "Save Batch List" button → `prompt()` for a name → same
  overwrite/duplicate-name flow as `saveFramePreset()` → stores the
  current textarea content.
- `<select>` of saved list names + "Load" button → replaces the
  textarea content with the stored string (does not auto-parse; user
  still clicks "Parse" same as with freshly-typed input).
- "Delete" button → removes the selected saved list.

### Filenames: avoiding collisions across prints

`exportVariant(skipArt, skipFrame, suffix)` (Export tab, already
merged) always names files from `getCardName()` alone — two different
prints of the same title (e.g. a reprint) produce identical filenames
and silently overwrite each other in the browser's downloads. Batch
gains a 4th, optional parameter:

```js
function exportVariant(skipArt, skipFrame, suffix, nameOverride) {
	drawCard(skipArt, skipFrame);
	var imageDataURL = cardCanvas.toDataURL('image/png');
	var imageName = (nameOverride || getCardName()) + suffix + '.png';
	...
}
```

(Existing Export tab call sites — `exportFrameAndText()`,
`exportTextOnly()` — pass no 4th argument, so `nameOverride` is
`undefined` and behavior is unchanged; only batch's per-row export
step passes one.)

Per row, batch computes:

```js
var batchNameBase = getCardName() +
	(row.setCode ? ' (' + row.setCode.toUpperCase() +
		(row.collectorNumber ? ' #' + row.collectorNumber.trim() : '') +
	')' : '');
```

and exports all three files with it:

```js
exportVariant(false, false, '', batchNameBase);   // full card — see note below
exportVariant(true, false, '-frame', batchNameBase);
exportVariant(true, true, '-textonly', batchNameBase);
```

Note: this uses `exportVariant(false, false, ...)` for the "full
card" file instead of calling `downloadCard()` directly, because
`downloadCard()` has no filename-override parameter and always names
from `getCardName()` alone. The one behavioral difference this
introduces: `downloadCard()`'s artist-credit guard (blocks download
if no artist is set and real art is loaded) does not run for batch's
full-card export. This is intentional — batch already deterministically
resolves art per row via the `art-flag` (real Scryfall art always
carries its artist credit from the import; `no-art` rows have no art
to credit), so the guard's failure mode (accidentally shipping
uncredited fan art) doesn't apply the same way in an unattended batch
context.

### Per-row processing

For each valid row, in order:

1. **Apply frame preset** (now async per section 1 above):
   `await applyFramePreset(row.presetName);`

2. **Import text from Scryfall**, with a timeout (the existing
   `fetchScryfallData` never invokes its callback on a 404/no-match —
   see [js/creator-23.js](../../../js/creator-23.js), search
   `fetchScryfallData` — so an un-timed-out wait would hang the whole
   batch on a single bad name), and — when `row.setCode` is given —
   select that specific print before importing:

   ```js
   function importCardByNameAsync(cardName, setCode, collectorNumber, timeoutMs = 8000) {
       return new Promise((resolve, reject) => {
           var settled = false;
           var timer = setTimeout(() => {
               if (!settled) { settled = true; reject(new Error('timed out or not found')); }
           }, timeoutMs);
           fetchScryfallData(cardName, cards => {
               if (settled) {return;}
               settled = true;
               clearTimeout(timer);
               if (!cards || cards.length === 0) {
                   reject(new Error('no match'));
                   return;
               }
               importCard(cards); // sets scryfallCard, #import-index, runs changeCardIndex() on the default (index 0) print
               if (setCode) {
                   var matchIndex = cards.findIndex(c =>
                       c.set && c.set.toLowerCase() === setCode.toLowerCase() &&
                       (!collectorNumber || (c.collector_number || '').trim() === collectorNumber.trim())
                   );
                   if (matchIndex === -1) {
                       reject(new Error('no printing found matching set "' + setCode + '"' + (collectorNumber ? ' #' + collectorNumber : '')));
                       return;
                   }
                   document.querySelector('#import-index').value = matchIndex;
                   changeCardIndex(); // re-run text import against the specific print
               }
               resolve();
           }, '');
       });
   }
   ```

   `cards` here is the same array `importCard` assigns to the global
   `scryfallCard`, in the same order — so an index found via
   `cards.findIndex(...)` is directly usable as `#import-index`'s
   value without any remapping (`importCard`'s dropdown-population
   loop skips entries lacking `type_line`, but still assigns each
   `<option>` its *original* array index as `value`, specifically so
   this kind of direct indexing stays valid — see
   [js/creator-23.js](../../../js/creator-23.js), search
   `function importCard`).

   `importCard(cards)` / `changeCardIndex()` synchronously set every
   `card.text[key].text` field (title/mana/type/rules/pt/nickname/etc.)
   before kicking off a *separate*, un-awaitable async chain to fetch
   art and the set symbol *for whichever print is currently selected
   in `#import-index`* — which is why the set/number re-selection
   above must happen, and `changeCardIndex()` must be re-run, before
   this promise resolves: it re-triggers that art/set-symbol fetch
   against the correct print too, not just the text.

   Called as: `await importCardByNameAsync(row.cardname, row.setCode, row.collectorNumber);`

3. **Resolve art**, based on `row.artFlag`:
   - `art`: `importCard`'s internal art-fetch is already in flight
     (triggered synchronously inside `changeCardIndex`, at the "//art"
     section). Poll `card.artSource` (set by `artEdited()` once the
     art image finishes loading — see
     [js/creator-23.js](../../../js/creator-23.js), search
     `function artEdited`) for a change from its pre-import value,
     every 200ms, up to a 6-second timeout. Timing out doesn't fail
     the row — proceed with whatever art is currently set, and note
     it in the row's status as a warning rather than an error. (This
     polls a value the existing pipeline already sets as a side
     effect — nothing about `uploadArt`/`artEdited`/`art.onload` is
     modified, so this is non-invasive.)
   - `no-art`: don't wait for the in-flight art fetch to matter —
     immediately call `uploadArt(fixUri('/img/blank.png'))` to reset
     art to blank. (The in-flight fetch may still land moments later
     and overwrite this — see Known Limitation below.)

4. **Apply nickname override**: if `row.nickname` is non-blank,
   `card.text.nickname.text = row.nickname; textEdited();`

5. **Export all 3 files**, with the collision-safe filename from the
   Filenames section above:

   ```js
   var batchNameBase = getCardName() +
       (row.setCode ? ' (' + row.setCode.toUpperCase() +
           (row.collectorNumber ? ' #' + row.collectorNumber.trim() : '') +
       ')' : '');
   exportVariant(false, false, '', batchNameBase);
   exportVariant(true, false, '-frame', batchNameBase);
   exportVariant(true, true, '-textonly', batchNameBase);
   ```

6. **Mark the row `'success'`** in `batchRows`, update its Status
   cell to ✅, update the running summary counts.

7. **Delay** exactly 800ms (`await new Promise(r => setTimeout(r, 800));`),
   then check `batchCancelled` — if set, stop the loop (see the Stop
   button, above) rather than continuing to the next row. Otherwise
   proceed. The 800ms delay itself exists because browsers throttle
   rapid unattended multi-file downloads (Chrome/Safari may prompt
   "Allow multiple downloads" after several in quick succession
   without a fresh user gesture per file) — the Batch tab's UI copy
   tells the user they may need to allow this once, the first time
   they run a batch on this site.

### Error handling

- A row whose Scryfall import fails (404/timeout, or an
  unmatched `SetCode`/`CollectorNumber` per step 2) is marked
  `'error'` with the specific error message as its reason, its Status
  cell shows ❌ + that reason, `notify(...)` fires once, and the loop
  continues to the next row. Does not stop the batch.
- A row whose frame preset fails to apply (caught inside
  `applyFramePreset`'s own try/catch, which already notifies) is
  likewise marked `'error'` (reason: the caught error's message);
  the batch runner skips exporting that row and continues.
- Every `'error'` row lands in the end-of-run summary's failure list
  and gets a "Retry" affordance (see UI section above) — the summary
  and retry mechanism read the same `status`/reason fields these
  error paths write, there's no separate error-tracking structure.
- Rows are processed **strictly sequentially** (`for...of` with
  `await`, not `Promise.all`) — both because `card`/`card.frames`/
  `card.text` are single shared globals (concurrent rows would
  clobber each other's state) and because the polling-based art wait
  in step 3 only makes sense against one in-flight fetch at a time.
  "Retry" and "Run Remaining" reuse this same sequential per-row
  function on a subset of `batchRows`, never in parallel with a
  still-running main batch (both buttons are disabled while
  `batchCancelled === false` and a run is actively in progress).

### Known limitation (documented, not solved by this spec)

For `no-art` rows, if the previous row's Scryfall art fetch is still
in flight when `uploadArt(blank)` runs, that stale fetch can complete
moments later and silently replace the blank art before export
happens — a race inherent to `changeCardIndex()`'s fire-and-forget
internal art fetch, which this spec does not modify (doing so is a
larger, riskier change to shared, heavily-used import code, out of
scope here). Mitigation: the 800ms inter-row delay (step 6) gives
the previous row's fetch time to settle before the next row starts,
which in practice is enough since art crops are small images on a
CDN; this is a heuristic, not a guarantee.

## Testing

Manual, in the running app (no automated test framework in this
project, consistent with prior work):

- Save a frame preset (with the frame-group/pack capture), reload the
  page cold (fresh `card` state), Apply it directly from the Frame
  tab — confirm it builds a full working card shell (correct
  textboxes, frame images, styling) from nothing, without any manual
  "Load Frame Version" click first.
- Apply an old preset saved *before* this change (no `frameGroup`/
  `framePack` fields) — confirm it still applies frames + text styles
  exactly as before, no error from the missing fields.
- Batch: 4-line input — one deliberately misspelled card name, one
  `art`, one `no-art`, one with a real card name plus a valid
  `SetCode`/`CollectorNumber` pinning a specific (non-default) print.
  Confirm: the bad row is skipped with a notification, the others
  each produce 3 downloaded files with correct text/frame/styling,
  the `art`-flagged card has real art, the `no-art`-flagged card
  doesn't, and the pinned-print card's art/collector info actually
  matches that specific printing (not Scryfall's default/most-recent
  one).
- A row with a `SetCode`/`CollectorNumber` that doesn't match any
  real printing of that card — confirm it's skipped with a
  notification naming the set/number that failed to match, and the
  batch continues to the next row.
- Confirm the preview table correctly flags an unknown preset name
  and an invalid art-flag value as red/invalid before "Run Batch" is
  even enabled, and that a row with only `Cardname` + blank
  `SetCode`/`CollectorNumber` still parses as valid (both fields are
  optional).
- Batch two different prints of the same card title in one run (e.g.
  two rows with the same `Cardname`, different `SetCode`s) — confirm
  the 6 resulting files (3 each) have distinct filenames including
  each print's set/number, no overwrite in Downloads.
- Start a 5+ row batch, click "Stop" partway through — confirm the
  in-flight row finishes normally, the loop stops before starting the
  next row, and the summary reflects exactly what ran ("N succeeded,
  M not yet run") rather than claiming the whole batch completed.
- After a run with at least one `'error'` row, click that row's
  "Retry" — confirm it re-runs only that row and updates its Status
  cell + the summary counts without touching the already-succeeded
  rows.
- After a Stop, click "Run Remaining" — confirm it only processes
  rows still `'pending'`/`'error'`, in original order, and skips every
  row already marked `'success'`.
- Save the current textarea as a named batch list, clear the
  textarea, Load it back — confirm the content matches exactly.
  Reload the page cold, confirm the saved list is still there
  (persisted in IndexedDB, not just in-memory).
