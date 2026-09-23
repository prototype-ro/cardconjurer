# Batch Card Creator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let a saved frame preset build a card's textbox schema from nothing (by replaying Frame Group/Pack + "Load Frame Version"), and add a Batch tab that runs a plain-text list of cards (name, optional print pin, nickname, frame preset, art flag) through Scryfall import + frame preset apply + the existing 3-file export — sequentially, with stop/resume, a run summary, per-row retry, and a saved-list feature — one card at a time, unattended.

**Architecture:** Extends the already-merged `cardDB`/`framePresets`/Export-tab work. Three small, non-breaking extensions to existing functions (`cardDB` gains a `batchLists` store; `saveFramePreset`/`applyFramePreset` gain frame-group/pack capture+replay; `exportVariant` gains an optional filename override) plus one new, mostly self-contained subsystem: a `batchRows` array driving a preview render, a sequential per-row async pipeline, and Stop/Retry/Run-Remaining controls layered on top of it. No test framework in this project — verification throughout is manual, via the running local server and browser devtools, matching prior work on this codebase.

**Tech Stack:** Vanilla JS (ES2017+, async/await), IndexedDB, static HTML/CSS. No build step.

**Spec:** `docs/superpowers/specs/2026-09-23-batch-card-creator-design.md`

---

## Before you start

```bash
cd /Users/rodgz_mac/Developer/MTG-CardMaker/assets/cardconjurer
python3 -m http.server 4242
```

Open `http://localhost:4242/creator/index.html`. Keep browser devtools (Console + Application > IndexedDB + Network) open throughout — this feature makes real Scryfall API calls during manual verification.

One note on browser-only verification: no automated test framework exists in this project. Every "Manual verification" step below must actually be exercised in a real browser tab, not just statically read — several of the behaviors here (async script loading, Scryfall fetch timing, download throttling) can't be confirmed by reading code alone.

---

### Task 1: `batchLists` IndexedDB store

**Files:**
- Modify: `js/creator-23.js:5121-5185` (the `cardDB` object)

- [ ] **Step 1: Bump the DB version and add the new store**

Find (current `cardDB.open()`, `js/creator-23.js:5123-5141`):

```js
	open() {
		if (this.db) {return Promise.resolve(this.db);}
		return new Promise((resolve, reject) => {
			var request = indexedDB.open('CardConjurerDB', 2);
			request.onupgradeneeded = event => {
				if (!event.target.result.objectStoreNames.contains('cards')) {
					event.target.result.createObjectStore('cards');
				}
				if (!event.target.result.objectStoreNames.contains('framePresets')) {
					event.target.result.createObjectStore('framePresets');
				}
			};
			request.onsuccess = event => {
				this.db = event.target.result;
				resolve(this.db);
			};
			request.onerror = event => reject(event.target.error);
		});
	},
```

Replace with:

```js
	open() {
		if (this.db) {return Promise.resolve(this.db);}
		return new Promise((resolve, reject) => {
			var request = indexedDB.open('CardConjurerDB', 3);
			request.onupgradeneeded = event => {
				if (!event.target.result.objectStoreNames.contains('cards')) {
					event.target.result.createObjectStore('cards');
				}
				if (!event.target.result.objectStoreNames.contains('framePresets')) {
					event.target.result.createObjectStore('framePresets');
				}
				if (!event.target.result.objectStoreNames.contains('batchLists')) {
					event.target.result.createObjectStore('batchLists');
				}
			};
			request.onsuccess = event => {
				this.db = event.target.result;
				resolve(this.db);
			};
			request.onerror = event => reject(event.target.error);
		});
	},
```

(Only the version number `2` → `3` and the new `if` block change — `set`/`get`/`delete`/`clear`/`keys` are untouched; they already take a `store` parameter and will work against `'batchLists'` with no further changes, exactly as they already do for `'framePresets'`.)

- [ ] **Step 2: Manual verification**

`node --check js/creator-23.js`. Then in the browser: reload the page, in devtools Console run `await cardDB.open()` — confirm it resolves with no error, and in Application > IndexedDB > CardConjurerDB, confirm three object stores now exist (`cards`, `framePresets`, `batchLists`) and the version shows `3`. Confirm your existing saved cards and frame presets (from prior sessions) still load in their respective tabs — proves the version bump didn't disturb the other two stores.

- [ ] **Step 3: Commit**

```bash
git add js/creator-23.js
git commit -m "Add batchLists IndexedDB store"
```

---

### Task 2: `loadScriptAsync` helper

**Files:**
- Modify: `js/creator-23.js` — add directly after the existing `loadScript` function (search `function loadScript`)

- [ ] **Step 1: Add the helper**

Find:

```js
function loadScript(scriptPath) {
	var script = document.createElement('script');
	script.setAttribute('type', 'text/javascript');
	script.onerror = function(){notify('A script failed to load, likely due to an update. Please reload your page. Sorry for the inconvenience.');}
	script.setAttribute('src', scriptPath);
	if (typeof script != 'undefined') {
		document.querySelectorAll('head')[0].appendChild(script);
	}
}
```

Add directly after its closing brace:

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

This does not modify `loadScript` or any of its existing call sites — it's a separate, dedicated helper for code that needs to know when a script has finished executing (frame-preset apply, batch).

- [ ] **Step 2: Manual verification**

`node --check js/creator-23.js`. In devtools Console:

```js
await loadScriptAsync('/js/frames/groupStandard-3.js');
console.log('resolved');
```

Confirm `"resolved"` logs (proves the promise resolves on a real script load) and that `#selectFramePack` now has options (proves the script actually executed, not just that the network request completed).

- [ ] **Step 3: Commit**

```bash
git add js/creator-23.js
git commit -m "Add loadScriptAsync helper"
```

---

### Task 3: `saveFramePreset()` captures Frame Group/Pack

**Files:**
- Modify: `js/creator-23.js:3099-3130` (`saveFramePreset`)

- [ ] **Step 1: Capture the two select values**

Find (`js/creator-23.js:3121-3124`):

```js
		var presetToSave = {
			frames: framesToSave,
			textStyles: captureTextStyles()
		};
```

Replace with:

```js
		var presetToSave = {
			frameGroup: document.querySelector('#selectFrameGroup').value,
			framePack: document.querySelector('#selectFramePack').value,
			frames: framesToSave,
			textStyles: captureTextStyles()
		};
```

- [ ] **Step 2: Manual verification**

`node --check js/creator-23.js`. In the browser: Frame tab, pick a Frame Group + Frame Pack, click "Load Frame Version", add a frame image, click "Save Frame Preset", name it `test-schema-preset`. In devtools Application > IndexedDB > CardConjurerDB > framePresets, confirm the stored record now has `frameGroup` and `framePack` fields matching whatever was selected in the two dropdowns at save time.

- [ ] **Step 3: Commit**

```bash
git add js/creator-23.js
git commit -m "saveFramePreset() captures Frame Group/Pack selection"
```

---

### Task 4: `applyFramePreset()` replays Frame Group/Pack schema

**Files:**
- Modify: `js/creator-23.js:3146-3170` (`applyFramePreset`)

- [ ] **Step 1: Add the schema-replay phase**

Find the full current function:

```js
async function applyFramePreset(presetName) {
	if (!presetName) {return;}
	try {
		var preset = await cardDB.get(presetName, 'framePresets');
		if (!preset) {
			notify(presetName + ' failed to load.', 5);
			return;
		}
		// frame stack
		document.querySelector('#frame-list').innerHTML = null;
		card.frames = JSON.parse(JSON.stringify(preset.frames));
		card.frames.reverse();
		await card.frames.forEach(item => addFrame([], item));
		card.frames.reverse();
		// linked text styling
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

Replace with:

```js
async function applyFramePreset(presetName) {
	if (!presetName) {return;}
	try {
		var preset = await cardDB.get(presetName, 'framePresets');
		if (!preset) {
			notify(presetName + ' failed to load.', 5);
			return;
		}
		// replay Frame Group + Pack + "Load Frame Version", if saved (older presets won't have these fields — skip this phase for them)
		if (preset.frameGroup && preset.framePack) {
			document.querySelector('#selectFrameGroup').value = preset.frameGroup;
			await loadScriptAsync('/js/frames/group' + preset.frameGroup + '.js');
			document.querySelector('#selectFramePack').value = preset.framePack;
			await loadScriptAsync('/js/frames/pack' + preset.framePack + '.js');
			await document.querySelector('#loadFrameVersion').onclick();
		}
		// frame stack
		document.querySelector('#frame-list').innerHTML = null;
		card.frames = JSON.parse(JSON.stringify(preset.frames));
		card.frames.reverse();
		await card.frames.forEach(item => addFrame([], item));
		card.frames.reverse();
		// linked text styling
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

- [ ] **Step 2: Manual verification**

`node --check js/creator-23.js`. In the browser:
1. Reload the page cold (fresh `card` state — the default group script auto-loads a frame version per the app's own init logic, so first confirm `card.text` exists as usual).
2. Go to Frame tab, select `test-schema-preset` (from Task 3) in the "Apply a saved frame preset" dropdown.
3. Confirm: `#selectFrameGroup` and `#selectFramePack` visibly change to match what was saved, the frame-image thumbnails in `#frame-list` match what was saved, and `card.text` (check in Console: `card.text`) has the correct schema for that frame pack (e.g. `title`, `mana`, `type`, `rules`, `pt` keys for an M15-style pack).
4. Apply an *old* preset (one saved before Task 3, if you have one from earlier testing — or simulate by manually deleting `frameGroup`/`framePack` from a stored record via devtools before applying) — confirm it still applies frames + text styles with no error, since the `if (preset.frameGroup && preset.framePack)` guard skips the new phase entirely for those.

- [ ] **Step 3: Commit**

```bash
git add js/creator-23.js
git commit -m "applyFramePreset() replays Frame Group/Pack + Load Frame Version"
```

---

### Task 5: `exportVariant()` gains an optional filename override

**Files:**
- Modify: `js/creator-23.js:4795-4807` (`exportVariant`)

- [ ] **Step 1: Add the 4th parameter**

Find:

```js
function exportVariant(skipArt, skipFrame, suffix) {
	drawCard(skipArt, skipFrame);
	var imageDataURL = cardCanvas.toDataURL('image/png');
	var imageName = getCardName() + suffix + '.png';
	const downloadElement = document.createElement('a');
	downloadElement.download = imageName;
	downloadElement.target = '_blank';
	downloadElement.href = imageDataURL;
	document.body.appendChild(downloadElement);
	downloadElement.click();
	downloadElement.remove();
	drawCard();
}
```

Replace with:

```js
function exportVariant(skipArt, skipFrame, suffix, nameOverride) {
	drawCard(skipArt, skipFrame);
	var imageDataURL = cardCanvas.toDataURL('image/png');
	var imageName = (nameOverride || getCardName()) + suffix + '.png';
	const downloadElement = document.createElement('a');
	downloadElement.download = imageName;
	downloadElement.target = '_blank';
	downloadElement.href = imageDataURL;
	document.body.appendChild(downloadElement);
	downloadElement.click();
	downloadElement.remove();
	drawCard();
}
```

`exportFrameAndText()` and `exportTextOnly()` (directly below, unchanged) call `exportVariant` with only 3 arguments, so `nameOverride` is `undefined` there and `(nameOverride || getCardName())` falls through to `getCardName()` exactly as before — zero behavior change for the existing Export tab.

- [ ] **Step 2: Manual verification**

`node --check js/creator-23.js`. In the browser, Export tab: click both "Export Frame + Text + Symbol" and "Export Text + Symbol Only" on a card with a title set — confirm filenames are unchanged from before (`<title>-frame.png`, `<title>-textonly.png`). In devtools Console: `exportVariant(true, true, '-test', 'Custom Name')` — confirm a file named `Custom Name-test.png` downloads.

- [ ] **Step 3: Commit**

```bash
git add js/creator-23.js
git commit -m "exportVariant() accepts an optional filename override"
```

---

### Task 6: Batch tab — HTML shell

**Files:**
- Modify: `creator/index.html:107` (tab header) and `creator/index.html:715` area (tab panel, inserted after the Export panel)

- [ ] **Step 1: Add the tab header**

Find:

```html
					<h3 class='selectable readable-background' onclick='toggleCreatorTabs(event, "export")'>Export</h3>
					<h3 class='selectable readable-background' onclick='toggleCreatorTabs(event, "tutorial"); loadTutorialVideo();'>Tutorial</h3>
```

Replace with:

```html
					<h3 class='selectable readable-background' onclick='toggleCreatorTabs(event, "export")'>Export</h3>
					<h3 class='selectable readable-background' onclick='toggleCreatorTabs(event, "batch")'>Batch</h3>
					<h3 class='selectable readable-background' onclick='toggleCreatorTabs(event, "tutorial"); loadTutorialVideo();'>Tutorial</h3>
```

- [ ] **Step 2: Add the tab panel**

Find the end of the Export panel followed by the Tutorial panel:

```html
					</div>
					<div id='creator-menu-tutorial' class='hidden'>
```

(this is the specific occurrence right after `<button class='input' onclick='exportTextOnly();'>Export Text + Symbol Only</button>` and its two closing `</div>` — the Export panel added in the prior feature)

Replace with:

```html
					</div>
					<div id='creator-menu-batch' class='hidden'>
						<div class='readable-background margin-bottom padding'>
							<h5 class='margin-bottom padding input-description'>One card per line: Cardname | SetCode | CollectorNumber | Nickname | FramePresetName | art-flag<br>SetCode, CollectorNumber, and Nickname may be left blank. art-flag must be exactly "art" or "no-art".<br>Example: Lightning Bolt | | | | MyRedPreset | art</h5>
							<textarea id='batch-input' class='input margin-bottom' rows='8' placeholder='Lightning Bolt | | | | MyRedPreset | art'></textarea>
							<button id='batch-parse' class='input' onclick='parseBatchInput();'>Parse</button>
						</div>
						<div class='readable-background margin-bottom padding'>
							<h5 class='padding margin-bottom input-description'>Save the current list</h5>
							<button class='input margin-bottom' onclick='saveBatchList();'>Save Batch List</button>
							<h5 class='padding margin-bottom input-description'>Load a saved list</h5>
							<select id='load-batch-list-options' class='input margin-bottom' onchange='loadBatchList(this.value);'></select>
							<h5 class='padding margin-bottom input-description'>Delete selected list</h5>
							<button class='input' onclick='deleteBatchList();'>Delete Batch List</button>
						</div>
						<div id='batch-preview' class='readable-background margin-bottom padding hidden'>
							<div id='batch-preview-rows'></div>
							<div class='padding input-grid'>
								<button id='batch-run' class='input' onclick='runBatch();' disabled>Run Batch</button>
								<button id='batch-stop' class='input hidden' onclick='stopBatch();'>Stop</button>
							</div>
							<h5 id='batch-progress' class='padding input-description hidden'></h5>
						</div>
						<div id='batch-summary' class='readable-background margin-bottom padding hidden'></div>
					</div>
					<div id='creator-menu-tutorial' class='hidden'>
```

Note: the preview rows and summary are plain `<h5>`/`<div>` blocks styled with the existing `readable-background`/`padding`/`input-description` utility classes already used throughout this file — there is no `<table>` CSS anywhere in this codebase (every other "list of things" section, e.g. the Text Code Reference, uses this same div/h5 convention), so Tasks 7-9 render rows this way rather than introducing new table markup/CSS.

- [ ] **Step 3: Manual verification**

`python3 -m http.server 4242` (if not already running), reload the page. Confirm a "Batch" tab appears between Export and Tutorial, clicking it shows the new panel (textarea, Parse button, batch-list save/load/delete controls), and clicking other tabs still shows/hides correctly (the generic `toggleCreatorTabs` mechanism should need no changes — confirm by reading its definition, `js/creator-23.js`, search `function toggleCreatorTabs`, and confirming it iterates all children of `#creator-menu-sections` generically).

- [ ] **Step 4: Commit**

```bash
git add creator/index.html
git commit -m "Add Batch tab HTML shell"
```

---

### Task 7: Parse batch input + render preview

**Files:**
- Modify: `js/creator-23.js` — add new functions after `exportTextOnly()` (search `function exportTextOnly`, insert after its closing brace, before `//IMPORT/SAVE TAB`)

- [ ] **Step 1: Add `parseBatchInput()` and `renderBatchPreview()`**

```js
var batchRows = [];
async function parseBatchInput() {
	var lines = document.querySelector('#batch-input').value.split('\n');
	var presetKeys = await cardDB.keys('framePresets');
	batchRows = [];
	lines.forEach(line => {
		if (!line.trim()) {return;}
		var parts = line.split('|').map(part => part.trim());
		var [cardname, setCode, collectorNumber, nickname, presetName, artFlag] = parts;
		var artFlagNormalized = (artFlag || '').toLowerCase();
		batchRows.push({
			cardname: cardname || '',
			setCode: setCode || '',
			collectorNumber: collectorNumber || '',
			nickname: nickname || '',
			presetName: presetName || '',
			artFlag: artFlagNormalized,
			presetValid: presetKeys.includes(presetName || ''),
			artFlagValid: artFlagNormalized === 'art' || artFlagNormalized === 'no-art',
			status: 'pending',
			reason: ''
		});
	});
	renderBatchPreview();
}
function renderBatchPreview() {
	var container = document.querySelector('#batch-preview-rows');
	container.innerHTML = '';
	batchRows.forEach((row, index) => {
		var rowValid = row.cardname && row.presetValid && row.artFlagValid;
		var line = document.createElement('h5');
		line.className = 'padding input-description' + (rowValid ? '' : ' batch-row-invalid');
		var printSuffix = row.setCode ? ' (' + row.setCode.toUpperCase() + (row.collectorNumber ? ' #' + row.collectorNumber : '') + ')' : '';
		var statusText = {pending: '—', running: '⏳', success: '✅', error: '❌ ' + row.reason}[row.status] || '—';
		line.innerHTML = 'Row ' + (index + 1) + ': ' + (row.cardname || '(missing cardname)') + printSuffix +
			' — Nickname: ' + (row.nickname || '—') +
			' — Preset: ' + (row.presetValid ? '✅' : '❌') + ' ' + row.presetName +
			' — Art: ' + (row.artFlagValid ? '✅' : '❌') + ' ' + row.artFlag +
			' — Status: ' + statusText;
		if (row.status === 'error') {
			var retryButton = document.createElement('button');
			retryButton.className = 'input';
			retryButton.innerHTML = 'Retry';
			retryButton.onclick = () => retryBatchRow(index);
			line.appendChild(retryButton);
		}
		container.appendChild(line);
	});
	document.querySelector('#batch-preview').classList.toggle('hidden', batchRows.length === 0);
	document.querySelector('#batch-run').disabled = !batchRows.some(row => row.cardname && row.presetValid && row.artFlagValid);
	document.querySelector('#batch-summary').classList.add('hidden');
}
```

`retryBatchRow` is implemented in Task 9 — this file references it now (the Retry button's `onclick`), which is fine since Task 9 lands in the same session before this is manually exercised end-to-end.

- [ ] **Step 2: Add the `.batch-row-invalid` CSS class**

**Files:** Modify: `css/style-9.css` — add near other small utility classes (search for `.hidden {` at `css/style-9.css:296` and add directly after its closing brace)

```css
.batch-row-invalid {
	color: #ff6b6b;
}
```

- [ ] **Step 3: Manual verification**

Reload. Paste into the Batch textarea:

```
Lightning Bolt | | | | MyRealPresetName | art
Bad Row | | | | NotARealPreset | maybe
```

(replace `MyRealPresetName` with an actual saved preset name from your testing). Click Parse. Confirm: 2 rows render, row 1 shows both ✅ (preset and art-flag), row 2 is styled red/invalid (❌ preset, ❌ art-flag, since "maybe" isn't "art"/"no-art" and "NotARealPreset" doesn't exist), "Run Batch" is enabled (since row 1 is valid), and the preview panel is visible.

- [ ] **Step 4: Commit**

```bash
git add js/creator-23.js css/style-9.css
git commit -m "Parse batch input and render preview rows"
```

---

### Task 8: Per-row import + art resolution

**Files:**
- Modify: `js/creator-23.js` — add directly after `renderBatchPreview()` from Task 7

- [ ] **Step 1: Add `importCardByNameAsync()`**

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
			importCard(cards);
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
				changeCardIndex();
			}
			resolve();
		}, '');
	});
}
```

- [ ] **Step 2: Add `waitForArtOrReset()`**

```js
function waitForArtOrReset(artFlag) {
	return new Promise(resolve => {
		if (artFlag === 'no-art') {
			uploadArt(fixUri('/img/blank.png'));
			resolve();
			return;
		}
		var previousArtSource = card.artSource;
		var elapsed = 0;
		var pollInterval = 200;
		var timeoutMs = 6000;
		var poll = setInterval(() => {
			elapsed += pollInterval;
			if (card.artSource !== previousArtSource || elapsed >= timeoutMs) {
				clearInterval(poll);
				resolve();
			}
		}, pollInterval);
	});
}
```

- [ ] **Step 3: Manual verification**

`node --check js/creator-23.js`. In devtools Console, on a card with a frame preset already applied (so `card.text` schema exists):

```js
await importCardByNameAsync('Lightning Bolt', '', '');
card.text.title.text; // should now be "Lightning Bolt" (or similar)
```

Then:

```js
await importCardByNameAsync('Lightning Bolt', 'LEA', '');
card.infoSet; // or inspect card.text for signs it's the LEA (Alpha) printing specifically — compare against a fresh import with no set pin
```

And confirm the timeout path: `await importCardByNameAsync('Zzzznotarealcardxyz', '', '', 2000)` rejects after ~2s with an error, doesn't hang.

For `waitForArtOrReset`: after triggering `importCardByNameAsync` for a card with real art, `await waitForArtOrReset('art')` — confirm it resolves once `card.artSource` has visibly changed (check the Art tab's art preview). `await waitForArtOrReset('no-art')` — confirm art resets to blank immediately.

- [ ] **Step 4: Commit**

```bash
git add js/creator-23.js
git commit -m "Add per-row Scryfall import and art-resolution helpers"
```

---

### Task 9: Batch runner — sequential loop, Stop, Retry, Run Remaining, summary

**Files:**
- Modify: `js/creator-23.js` — add directly after `waitForArtOrReset()` from Task 8

- [ ] **Step 1: Add the single-row pipeline `runBatchRow(index)`**

```js
async function runBatchRow(index) {
	var row = batchRows[index];
	row.status = 'running';
	row.reason = '';
	renderBatchPreview();
	try {
		await applyFramePreset(row.presetName);
		await importCardByNameAsync(row.cardname, row.setCode, row.collectorNumber);
		await waitForArtOrReset(row.artFlag);
		if (row.nickname) {
			card.text.nickname.text = row.nickname;
			textEdited();
		}
		var batchNameBase = getCardName() +
			(row.setCode ? ' (' + row.setCode.toUpperCase() +
				(row.collectorNumber ? ' #' + row.collectorNumber.trim() : '') +
			')' : '');
		exportVariant(false, false, '', batchNameBase);
		exportVariant(true, false, '-frame', batchNameBase);
		exportVariant(true, true, '-textonly', batchNameBase);
		row.status = 'success';
	} catch (error) {
		row.status = 'error';
		row.reason = error.message;
		notify('Batch row "' + row.cardname + '" failed: ' + error.message, 5);
	}
	renderBatchPreview();
}
```

- [ ] **Step 2: Add the sequential runner, Stop, and summary**

```js
var batchCancelled = false;
var batchRunning = false;
async function runBatch(indexesOverride) {
	if (batchRunning) {return;}
	batchRunning = true;
	batchCancelled = false;
	document.querySelector('#batch-run').disabled = true;
	document.querySelector('#batch-stop').classList.remove('hidden');
	document.querySelector('#batch-progress').classList.remove('hidden');
	document.querySelector('#batch-summary').classList.add('hidden');
	var indexes = indexesOverride || batchRows
		.map((row, index) => index)
		.filter(index => {
			var row = batchRows[index];
			return row.cardname && row.presetValid && row.artFlagValid;
		});
	var stoppedEarly = false;
	for (var i = 0; i < indexes.length; i++) {
		var index = indexes[i];
		document.querySelector('#batch-progress').innerHTML = 'Processing ' + (i + 1) + ' / ' + indexes.length + ': ' + batchRows[index].cardname + '...';
		await runBatchRow(index);
		await new Promise(r => setTimeout(r, 800));
		if (batchCancelled) {
			stoppedEarly = true;
			break;
		}
	}
	batchRunning = false;
	document.querySelector('#batch-run').disabled = false;
	document.querySelector('#batch-stop').classList.add('hidden');
	document.querySelector('#batch-progress').classList.add('hidden');
	renderBatchSummary(stoppedEarly);
}
function stopBatch() {
	batchCancelled = true;
}
async function retryBatchRow(index) {
	if (batchRunning) {return;}
	batchRunning = true;
	await runBatchRow(index);
	batchRunning = false;
	renderBatchSummary(false);
}
async function runRemainingBatchRows() {
	var indexes = batchRows
		.map((row, index) => index)
		.filter(index => batchRows[index].status !== 'success' && batchRows[index].cardname && batchRows[index].presetValid && batchRows[index].artFlagValid);
	await runBatch(indexes);
}
function renderBatchSummary(stoppedEarly) {
	var succeeded = batchRows.filter(row => row.status === 'success').length;
	var failed = batchRows.filter(row => row.status === 'error');
	var notRun = batchRows.filter(row => row.status === 'pending' && row.cardname && row.presetValid && row.artFlagValid).length;
	var summary = document.querySelector('#batch-summary');
	var html = '<h5 class="padding input-description">' + succeeded + ' succeeded, ' + failed.length + ' failed' + (notRun ? ', ' + notRun + ' not yet run' : '') + (stoppedEarly ? ' (stopped)' : '') + '</h5>';
	if (failed.length) {
		html += '<h5 class="padding input-description">Failed: ' + failed.map(row => row.cardname + ' (' + row.reason + ')').join(', ') + '</h5>';
	}
	if (failed.length || notRun) {
		html += '<button class="input" onclick="runRemainingBatchRows();">Run Remaining</button>';
	}
	summary.innerHTML = html;
	summary.classList.remove('hidden');
	renderBatchPreview();
}
```

`renderBatchPreview()` (Task 7) is called from inside `runBatchRow`/`renderBatchSummary`, so Status cells and the Retry button per row stay in sync automatically — no separate DOM-patching path to keep in sync.

- [ ] **Step 3: Manual verification**

Using the two-row batch from Task 7's verification (make both rows valid this time — real preset name, real card names, one `art`/one `no-art`), click "Run Batch". Confirm: progress line updates per row, both rows' Status cells go ⏳ → ✅, 6 files download total (3 per row), "Stop" button disappears when done, summary shows "2 succeeded, 0 failed".

Add a 3rd row with a misspelled card name, re-Parse, Run Batch. Confirm the bad row ends ❌ with a reason, the batch continues past it, summary lists it under "Failed," and clicking its Retry button re-runs just that row.

Add several more rows (5+), click Run Batch, click Stop partway through. Confirm the in-flight row finishes (still downloads/succeeds), the loop then stops before the next row, summary shows accurate counts including "not yet run," and "Run Remaining" is offered. Click it — confirm only not-yet-run/failed rows execute, already-succeeded rows are skipped (check their Status stays ✅, no duplicate downloads for them).

- [ ] **Step 4: Commit**

```bash
git add js/creator-23.js
git commit -m "Add sequential batch runner with stop, retry, and run-remaining"
```

---

### Task 10: Batch list persistence (save/load/delete)

**Files:**
- Modify: `js/creator-23.js` — add directly after `renderBatchSummary()` from Task 9

- [ ] **Step 1: Add `saveBatchList()`, `loadAvailableBatchLists()`, `loadBatchList()`, `deleteBatchList()`**

```js
async function saveBatchList() {
	var listName = prompt('Enter the name you would like to save this batch list under:');
	if (!listName) {return null;}
	listName = listName.trim();
	if (!listName) {return null;}
	try {
		var existingKeys = await cardDB.keys('batchLists');
		if (existingKeys.includes(listName)) {
			if (!confirm('Would you like to overwrite the batch list "' + listName + '"?\n(Clicking "cancel" will affix a version number)')) {
				var originalListName = listName;
				var listNumber = 1;
				while (existingKeys.includes(listName)) {
					listName = originalListName + ' (' + listNumber + ')';
					listNumber++;
				}
			}
		}
		await cardDB.set(listName, document.querySelector('#batch-input').value, 'batchLists');
		loadAvailableBatchLists();
	} catch (error) {
		notify('Your batch list failed to save (' + error.message + ').');
	}
}
async function loadAvailableBatchLists() {
	try {
		var listKeys = await cardDB.keys('batchLists');
		var select = document.querySelector('#load-batch-list-options');
		select.innerHTML = '<option selected="selected" disabled>None selected</option>';
		listKeys.sort().forEach(item => {
			var listOption = document.createElement('option');
			listOption.innerHTML = item;
			listOption.value = item;
			select.appendChild(listOption);
		});
	} catch (error) {
		notify('Failed to load batch lists (' + error.message + ').');
	}
}
async function loadBatchList(listName) {
	if (!listName) {return;}
	try {
		var listText = await cardDB.get(listName, 'batchLists');
		if (listText === undefined) {
			notify(listName + ' failed to load.', 5);
			return;
		}
		document.querySelector('#batch-input').value = listText;
	} catch (error) {
		notify('Failed to load batch list "' + listName + '" (' + error.message + ').');
	}
}
async function deleteBatchList() {
	var listName = document.querySelector('#load-batch-list-options').value;
	if (listName) {
		try {
			await cardDB.delete(listName, 'batchLists');
			loadAvailableBatchLists();
		} catch (error) {
			notify('Failed to delete batch list "' + listName + '" (' + error.message + ').');
		}
	}
}
```

This is a direct mirror of `saveFramePreset`/`loadAvailableFramePresets`/`deleteFramePreset`'s shape, adapted for a plain-string value instead of a structured object (no `applyFramePreset`-style third "apply" step — "loading" a batch list just means putting its text back in the textarea; the user still clicks Parse themselves, per the spec).

- [ ] **Step 2: Wire the init call**

Find the init block near the end of the file:

```js
// Load / init whatever
loadScript('/js/frames/groupStandard-3.js');
loadAvailableCards();
loadAvailableFramePresets();
initDraggableArt();
```

Change to:

```js
// Load / init whatever
loadScript('/js/frames/groupStandard-3.js');
loadAvailableCards();
loadAvailableFramePresets();
loadAvailableBatchLists();
initDraggableArt();
```

- [ ] **Step 3: Manual verification**

`node --check js/creator-23.js`. Reload. Type/paste something into the Batch textarea, click "Save Batch List", name it `test-list`. Confirm it appears in the "Load a saved list" dropdown. Clear the textarea, select `test-list` from the dropdown — confirm the exact text comes back. Reload the page cold — confirm `test-list` is still in the dropdown (IndexedDB-persisted, not just in-memory) and still loads correctly. Delete it, confirm it's gone from the dropdown and from a fresh reload.

- [ ] **Step 4: Commit**

```bash
git add js/creator-23.js
git commit -m "Add batch list save/load/delete persistence"
```

---

### Task 11: Full end-to-end verification and spec sign-off

**Files:** none (verification only)

- [ ] **Step 1: Run through the spec's Testing section**

With the local server running, work through every bullet in the "Testing" section of `docs/superpowers/specs/2026-09-23-batch-card-creator-design.md` in a real browser tab — all 11 of them (frame-preset schema replay cold-start, old-preset backward compatibility, mixed-validity batch run, bad set/number handling, preview validation, filename collision avoidance across two prints of one title, Stop mid-run, Retry a failed row, Run Remaining after a stop, and batch-list save/load-across-reload). This task is the same kind of final composed-branch check used for the frame-presets-and-export feature — confirming the pieces from Tasks 1-10 actually compose correctly together, which no single task's isolated verification could catch (e.g. does a preset applied via the schema-replay path from Task 4 actually produce a `card.text` shape that Task 8's `importCardByNameAsync` can successfully write into, end to end, for a real Scryfall card?).

- [ ] **Step 2: `node --check` on the fully composed file**

```bash
node --check js/creator-23.js
```

- [ ] **Step 3: Fix any discrepancies found, then commit**

If Step 1 surfaces anything, fix it in the relevant task's code and commit as a follow-up fix describing what was wrong. If everything passes, no commit is needed for this task — it's verification-only.
