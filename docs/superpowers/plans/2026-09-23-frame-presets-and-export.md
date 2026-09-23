# Frame Presets + Export Section Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let a user save the current frame stack as a named preset and reapply it later, and export a card as three PNGs (full card, frame+text+symbol without art, text+symbol only without frame or art) instead of one.

**Architecture:** Extend the existing `CardConjurerDB` IndexedDB database (currently used only for saved cards) with a second object store, `framePresets`, reusing the same connection. Add preset save/apply/delete UI to the Frame tab, mirroring the existing saved-card UI pattern in the Import/Save tab. Add optional `skipArt`/`skipFrame` flags to the existing `drawCard()` function (default `false`, so all existing call sites are unaffected), and a new Export tab with three buttons that render each variant to the card canvas, download it, then restore the normal on-screen preview.

**Tech Stack:** Vanilla JS (ES2017+, async/await), IndexedDB, static HTML/CSS. No build step, no test framework — this project has none; verification is manual via the running local server and browser devtools, per the design spec's Testing section.

**Spec:** `docs/superpowers/specs/2026-09-23-frame-presets-and-export-design.md`

---

## Before you start

Serve the app locally so you can verify each task in a real browser:

```bash
cd /Users/rodgz_mac/Developer/MTG-CardMaker/assets/cardconjurer
python3 -m http.server 4242
```

Open `http://localhost:4242/creator/index.html`. Keep browser devtools (Console + Application > IndexedDB) open throughout.

---

### Task 1: Add a `framePresets` object store to CardConjurerDB

**Files:**
- Modify: `js/creator-23.js:5000-5052` (the `cardDB` object)

The current `cardDB` hardcodes the object store name `'cards'` in every method and opens the database at version 1. Bump to version 2, create `framePresets` alongside `cards` in `onupgradeneeded`, and generalize `set`/`get`/`delete`/`clear` to take a store name (defaulting to `'cards'` so every existing call site — `cardDB.set(key, val)`, `cardDB.get(key)`, etc. — keeps working unchanged).

- [ ] **Step 1: Replace the `cardDB` object**

Find this block (starts at `js/creator-23.js:5000`, the comment `//Card storage backend...`):

```js
const cardDB = {
	db: null,
	open() {
		if (this.db) {return Promise.resolve(this.db);}
		return new Promise((resolve, reject) => {
			var request = indexedDB.open('CardConjurerDB', 1);
			request.onupgradeneeded = event => {
				if (!event.target.result.objectStoreNames.contains('cards')) {
					event.target.result.createObjectStore('cards');
				}
			};
			request.onsuccess = event => {
				this.db = event.target.result;
				resolve(this.db);
			};
			request.onerror = event => reject(event.target.error);
		});
	},
	async set(key, value) {
		var db = await this.open();
		return new Promise((resolve, reject) => {
			var tx = db.transaction('cards', 'readwrite');
			tx.objectStore('cards').put(value, key);
			tx.oncomplete = () => resolve();
			tx.onerror = event => reject(event.target.error);
		});
	},
	async get(key) {
		var db = await this.open();
		return new Promise((resolve, reject) => {
			var request = db.transaction('cards', 'readonly').objectStore('cards').get(key);
			request.onsuccess = () => resolve(request.result);
			request.onerror = event => reject(event.target.error);
		});
	},
	async delete(key) {
		var db = await this.open();
		return new Promise((resolve, reject) => {
			var tx = db.transaction('cards', 'readwrite');
			tx.objectStore('cards').delete(key);
			tx.oncomplete = () => resolve();
			tx.onerror = event => reject(event.target.error);
		});
	},
	async clear() {
		var db = await this.open();
		return new Promise((resolve, reject) => {
			var tx = db.transaction('cards', 'readwrite');
			tx.objectStore('cards').clear();
			tx.oncomplete = () => resolve();
			tx.onerror = event => reject(event.target.error);
		});
	}
};
```

Replace it with:

```js
const cardDB = {
	db: null,
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
	async set(key, value, store = 'cards') {
		var db = await this.open();
		return new Promise((resolve, reject) => {
			var tx = db.transaction(store, 'readwrite');
			tx.objectStore(store).put(value, key);
			tx.oncomplete = () => resolve();
			tx.onerror = event => reject(event.target.error);
		});
	},
	async get(key, store = 'cards') {
		var db = await this.open();
		return new Promise((resolve, reject) => {
			var request = db.transaction(store, 'readonly').objectStore(store).get(key);
			request.onsuccess = () => resolve(request.result);
			request.onerror = event => reject(event.target.error);
		});
	},
	async delete(key, store = 'cards') {
		var db = await this.open();
		return new Promise((resolve, reject) => {
			var tx = db.transaction(store, 'readwrite');
			tx.objectStore(store).delete(key);
			tx.oncomplete = () => resolve();
			tx.onerror = event => reject(event.target.error);
		});
	},
	async clear(store = 'cards') {
		var db = await this.open();
		return new Promise((resolve, reject) => {
			var tx = db.transaction(store, 'readwrite');
			tx.objectStore(store).clear();
			tx.oncomplete = () => resolve();
			tx.onerror = event => reject(event.target.error);
		});
	},
	async keys(store = 'cards') {
		var db = await this.open();
		return new Promise((resolve, reject) => {
			var request = db.transaction(store, 'readonly').objectStore(store).getAllKeys();
			request.onsuccess = () => resolve(request.result);
			request.onerror = event => reject(event.target.error);
		});
	}
};
```

(Added a `keys()` helper — Task 3 needs to list preset names, and there's no `framePresetKeys`-in-localStorage equivalent to the `cardKeys` pattern, so it reads directly from IndexedDB via `getAllKeys()`.)

- [ ] **Step 2: Manual verification — DB upgrade runs cleanly**

Reload `http://localhost:4242/creator/index.html`. In devtools Console:

```js
await cardDB.open();
```

Expected: resolves with an `IDBDatabase` object (no thrown error). In devtools Application > IndexedDB > CardConjurerDB, confirm two object stores now exist: `cards` and `framePresets`, and version shows `2`.

Also confirm existing saved cards still load: if you have any saved cards, open the Import/Save tab and check the "Load a saved card" dropdown still lists them (proves the version bump didn't break the existing `cards` store).

- [ ] **Step 3: Commit**

```bash
git add js/creator-23.js
git commit -m "Add framePresets IndexedDB store, generalize cardDB helper"
```

---

### Task 2: Save Frame Preset

**Files:**
- Modify: `js/creator-23.js` (add new function near the frame-handling functions, e.g. directly after `addFrame` ends, around line 3100 — exact insertion point found by locating the end of `addFrame`)
- Modify: `creator/index.html:172` (insert new UI block after the frame-list section)

- [ ] **Step 1: Add `saveFramePreset()`**

Add this function in `js/creator-23.js`. Place it right after the closing brace of `addFrame` (search for `async function addFrame(additionalMasks = [], loadingFrame = false) {` at line 2993 and find its matching closing `}` — insert immediately after):

```js
async function saveFramePreset() {
	var presetName = prompt('Enter the name you would like to save this frame preset under:');
	if (!presetName) {return null;}
	presetName = presetName.trim();
	if (!presetName) {return null;}
	var existingKeys = await cardDB.keys('framePresets');
	if (existingKeys.includes(presetName)) {
		if (!confirm('Would you like to overwrite the frame preset "' + presetName + '"?\n(Clicking "cancel" will affix a version number)')) {
			var originalPresetName = presetName;
			var presetNumber = 1;
			while (existingKeys.includes(presetName)) {
				presetName = originalPresetName + ' (' + presetNumber + ')';
				presetNumber++;
			}
		}
	}
	var framesToSave = JSON.parse(JSON.stringify(card.frames));
	framesToSave.forEach(frame => {
		delete frame.image;
		frame.masks.forEach(mask => delete mask.image);
	});
	try {
		await cardDB.set(presetName, framesToSave, 'framePresets');
		loadAvailableFramePresets();
	} catch (error) {
		notify('Your frame preset failed to save (' + error.message + ').');
	}
}
```

This mirrors `saveCard()` at `js/creator-23.js:5088` exactly: same prompt/overwrite/versioning flow, same `delete frame.image` / `delete mask.image` stripping before storage (Image objects aren't meaningfully serializable and get rebuilt from `src` on load — see `addFrame`'s handling of `loadingFrame`).

- [ ] **Step 2: Add `loadAvailableFramePresets()`**

Add directly after `saveFramePreset`:

```js
async function loadAvailableFramePresets() {
	var presetKeys = await cardDB.keys('framePresets');
	var select = document.querySelector('#load-frame-preset-options');
	select.innerHTML = '<option selected="selected" disabled>None selected</option>';
	presetKeys.sort().forEach(item => {
		var presetOption = document.createElement('option');
		presetOption.innerHTML = item;
		presetOption.value = item;
		select.appendChild(presetOption);
	});
}
```

This mirrors `loadAvailableCards()` at `js/creator-23.js:5071`.

- [ ] **Step 3: Add the UI block**

In `creator/index.html`, insert after line 172 (the closing `</div>` of the "Drag to reorder frame images" block that contains `#frame-list`, right before the "Upload custom frame images" block):

```html
						<div class='readable-background padding margin-bottom'>
							<h5 class='padding margin-bottom input-description'>Save the current frame stack as a preset</h5>
							<button class='input margin-bottom' onclick='saveFramePreset();'>Save Frame Preset</button>
							<h5 class='padding margin-bottom input-description'>Apply a saved frame preset</h5>
							<select id='load-frame-preset-options' class='input margin-bottom' onchange='applyFramePreset(this.value);'></select>
							<h5 class='padding margin-bottom input-description'>Delete selected frame preset</h5>
							<button class='input' onclick='deleteFramePreset();'>Delete Frame Preset</button>
						</div>
```

(`applyFramePreset` is implemented in Task 3 — this button is wired now but has no handler yet, which is fine since it isn't called until Task 3 lands in the same session before manual testing.)

- [ ] **Step 4: Call `loadAvailableFramePresets()` on page init**

In `js/creator-23.js`, find the init block near the end of the file:

```js
// Load / init whatever
loadScript('/js/frames/groupStandard-3.js');
loadAvailableCards();
initDraggableArt();
```

Change to:

```js
// Load / init whatever
loadScript('/js/frames/groupStandard-3.js');
loadAvailableCards();
loadAvailableFramePresets();
initDraggableArt();
```

- [ ] **Step 5: Manual verification**

Reload the page. Go to the Frame tab, add a couple of frames to the card (any frame from the picker), click "Save Frame Preset", enter a test name like `test-preset-1`. Confirm:
- No console errors.
- In devtools Application > IndexedDB > CardConjurerDB > framePresets, a record with key `test-preset-1` exists, value is an array of frame objects with no `image` property.
- The "Apply a saved frame preset" dropdown now lists `test-preset-1`.

- [ ] **Step 6: Commit**

```bash
git add js/creator-23.js creator/index.html
git commit -m "Add Save Frame Preset UI and storage"
```

---

### Task 3: Apply Frame Preset

**Files:**
- Modify: `js/creator-23.js` (add `applyFramePreset` after `loadAvailableFramePresets`)

- [ ] **Step 1: Add `applyFramePreset()`**

Add directly after `loadAvailableFramePresets` (from Task 2):

```js
async function applyFramePreset(presetName) {
	if (!presetName) {return;}
	var frames = await cardDB.get(presetName, 'framePresets');
	if (!frames) {
		notify(presetName + ' failed to load.', 5);
		return;
	}
	document.querySelector('#frame-list').innerHTML = null;
	card.frames = JSON.parse(JSON.stringify(frames));
	card.frames.reverse();
	await card.frames.forEach(item => addFrame([], item));
	card.frames.reverse();
}
```

This mirrors the frame-loading portion of `loadCard()` at `js/creator-23.js:5170-5173` exactly: clear `#frame-list`, set `card.frames`, reverse/add/reverse (because `addFrame(additionalMasks, loadingFrame)` prepends each DOM element, so building in reverse order yields the correct final on-screen order), where `addFrame([], item)` with `item` truthy takes the `loadingFrame` branch and does not re-push onto `card.frames` (already set above), only rebuilds the DOM element and reloads each frame/mask image.

- [ ] **Step 2: Manual verification**

Reload the page. In the Frame tab:
1. Add frame A to the card, save it as preset `preset-a`.
2. Clear the card's frames (remove them from `#frame-list`, or just add a different frame B without saving).
3. Select `preset-a` from the "Apply a saved frame preset" dropdown.

Expected: the frame list on screen updates to show only frame A again, the card preview redraws with frame A, and nothing else about the card (any text you'd typed, art, etc.) changed.

Also verify order preservation: save a preset with two different frames stacked in a specific order, change the order, apply the preset again, confirm the original order is restored.

- [ ] **Step 3: Commit**

```bash
git add js/creator-23.js
git commit -m "Add Apply Frame Preset"
```

---

### Task 4: Delete Frame Preset

**Files:**
- Modify: `js/creator-23.js` (add `deleteFramePreset` after `applyFramePreset`)

- [ ] **Step 1: Add `deleteFramePreset()`**

Add directly after `applyFramePreset`:

```js
async function deleteFramePreset() {
	var presetName = document.querySelector('#load-frame-preset-options').value;
	if (presetName) {
		await cardDB.delete(presetName, 'framePresets');
		loadAvailableFramePresets();
	}
}
```

This mirrors `deleteCard()` at `js/creator-23.js:5158`.

- [ ] **Step 2: Manual verification**

With `preset-a` (or `test-preset-1`) selected in the dropdown, click "Delete Frame Preset". Confirm:
- The dropdown no longer lists it.
- Reload the page — confirm it's still gone (proves the delete persisted to IndexedDB, not just the in-memory dropdown).

- [ ] **Step 3: Commit**

```bash
git add js/creator-23.js
git commit -m "Add Delete Frame Preset"
```

---

### Task 5: `drawCard()` gains `skipArt` / `skipFrame` flags

**Files:**
- Modify: `js/creator-23.js:4547-4658` (`drawCard` function)

- [ ] **Step 1: Replace `drawCard()`**

Find the full function (starts `function drawCard() {` at line 4547, ends at the matching `}` at line 4658):

```js
function drawCard() {
	// reset
	cardContext.globalCompositeOperation = 'source-over';
	cardContext.clearRect(0, 0, cardCanvas.width, cardCanvas.height);
	// art
	cardContext.save();
	cardContext.translate(scaleX(card.artX), scaleY(card.artY));
	cardContext.rotate(Math.PI / 180 * (card.artRotate || 0));
	if (document.querySelector('#grayscale-art').checked) {
		cardContext.filter='grayscale(1)';
	}
	cardContext.drawImage(art, 0, 0, art.width * card.artZoom, art.height * card.artZoom);
	cardContext.restore();
	// frame elements
	if (card.version.includes('planeswalker') && typeof planeswalkerPreFrameCanvas !== "undefined") {
		cardContext.drawImage(planeswalkerPreFrameCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	}
	cardContext.drawImage(frameCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	if (card.version.toLowerCase().includes('planeswalker') && typeof planeswalkerPostFrameCanvas !== "undefined") {
		cardContext.drawImage(planeswalkerPostFrameCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	} else if (card.version.toLowerCase().includes('planeswalker') && typeof planeswalkerCanvas !== "undefined") {
		cardContext.drawImage(planeswalkerCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	} else if (card.version.toLowerCase().includes('qrcode') && typeof qrCodeCanvas !== "undefined") {
		cardContext.drawImage(qrCodeCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	} // REMOVE/DELETE PLANESWALKERCANVAS AFTER A FEW WEEKS
	// guidelines
	if (document.querySelector('#show-guidelines').checked) {
		cardContext.drawImage(guidelinesCanvas, scaleX(card.marginX) / 2, scaleY(card.marginY) / 2, cardCanvas.width, cardCanvas.height);
	}
	// watermark
	cardContext.drawImage(watermarkCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	// custom elements for sagas, classes, and dungeons
	if (card.version.toLowerCase().includes('saga') && typeof sagaCanvas !== "undefined") {
		cardContext.drawImage(sagaCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	} else if (card.version.toLowerCase().includes('class') && typeof classCanvas !== "undefined") {
		cardContext.drawImage(classCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	} else if (card.version.toLowerCase().includes('dungeon') && typeof dungeonCanvas !== "undefined") {
		cardContext.drawImage(dungeonCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	}
	// text
	cardContext.drawImage(textCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	// set symbol
	cardContext.drawImage(setSymbol, scaleX(card.setSymbolX), scaleY(card.setSymbolY), setSymbol.width * card.setSymbolZoom, setSymbol.height * card.setSymbolZoom)
	// serial
	if (card.serialNumber || card.serialTotal) {
		var x = parseInt(card.serialX) || 172;
		var y = parseInt(card.serialY) || 1383;
		var scale = parseFloat(card.serialScale) || 1.0;

		cardContext.drawImage(serial, scaleX(x/2010), scaleY(y/2814), scaleX(464/2010) * scale, scaleY(143/2814) * scale);

		var number = {
			name:"Number",
			text: '{kerning3}' + card.serialNumber || '',
			x: (x+(30 * scale))/2010,
			y: (y+(52 * scale))/2814,
			width: (190 * scale)/2010,
			height: (55 * scale)/2814,
			oneLine: true,
			font: 'gothambold',
			color: 'white',
			size: (55 * scale)/2010,
			align: 'center'
		};

		var total = {
			name:"Number",
			text: '{kerning3}' + card.serialTotal || '',
			x: (x+(251 * scale))/2010,
			y: (y+(52 * scale))/2814,
			width: (190 * scale)/2010,
			height: (55 * scale)/2814,
			oneLine: true,
			font: 'gothambold',
			color: 'white',
			size: (55 * scale)/2010,
			align: 'center'
		};

		writeText(number, cardContext);
		writeText(total, cardContext);
	}
	// bottom info
	if (card.bottomInfoTranslate) {
		cardContext.save();
		cardContext.rotate(Math.PI / 180 * (card.bottomInfoRotate || 0));
		cardContext.translate(card.bottomInfoTranslate.x || 0, card.bottomInfoTranslate.y || 0);
		cardContext.drawImage(bottomInfoCanvas, 0, 0, cardCanvas.width * (card.bottomInfoZoom || 1), cardCanvas.height * (card.bottomInfoZoom || 1));
		cardContext.restore();
	} else {
		cardContext.drawImage(bottomInfoCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	}
	
	
	// cutout the corners
	cardContext.globalCompositeOperation = 'destination-out';
	if (!card.noCorners && (card.marginX == 0 && card.marginY == 0)) {
		var w = card.version == 'battle' ? 2100 : getStandardWidth();

		cardContext.drawImage(corner, 0, 0, scaleWidth(59/w), scaleWidth(59/w));
		cardContext.rotate(Math.PI / 2);
		cardContext.drawImage(corner, 0, -card.width, scaleWidth(59/w), scaleWidth(59/w));
		cardContext.rotate(Math.PI / 2);
		cardContext.drawImage(corner, -card.width, -card.height, scaleWidth(59/w), scaleWidth(59/w));
		cardContext.rotate(Math.PI / 2);
		cardContext.drawImage(corner, -card.height, 0, scaleWidth(59/w), scaleWidth(59/w));
		cardContext.rotate(Math.PI / 2);
	}
	// show preview
	previewContext.clearRect(0, 0, previewCanvas.width, previewCanvas.height);
	previewContext.drawImage(cardCanvas, 0, 0, previewCanvas.width, previewCanvas.height);
}
```

Replace with (only the `art` block, the `frame elements` block, and the `cutout the corners` block gain guards — every other line is untouched):

```js
function drawCard(skipArt = false, skipFrame = false) {
	// reset
	cardContext.globalCompositeOperation = 'source-over';
	cardContext.clearRect(0, 0, cardCanvas.width, cardCanvas.height);
	// art
	if (!skipArt) {
		cardContext.save();
		cardContext.translate(scaleX(card.artX), scaleY(card.artY));
		cardContext.rotate(Math.PI / 180 * (card.artRotate || 0));
		if (document.querySelector('#grayscale-art').checked) {
			cardContext.filter='grayscale(1)';
		}
		cardContext.drawImage(art, 0, 0, art.width * card.artZoom, art.height * card.artZoom);
		cardContext.restore();
	}
	// frame elements
	if (!skipFrame) {
		if (card.version.includes('planeswalker') && typeof planeswalkerPreFrameCanvas !== "undefined") {
			cardContext.drawImage(planeswalkerPreFrameCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
		}
		cardContext.drawImage(frameCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
		if (card.version.toLowerCase().includes('planeswalker') && typeof planeswalkerPostFrameCanvas !== "undefined") {
			cardContext.drawImage(planeswalkerPostFrameCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
		} else if (card.version.toLowerCase().includes('planeswalker') && typeof planeswalkerCanvas !== "undefined") {
			cardContext.drawImage(planeswalkerCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
		} else if (card.version.toLowerCase().includes('qrcode') && typeof qrCodeCanvas !== "undefined") {
			cardContext.drawImage(qrCodeCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
		} // REMOVE/DELETE PLANESWALKERCANVAS AFTER A FEW WEEKS
	}
	// guidelines
	if (document.querySelector('#show-guidelines').checked) {
		cardContext.drawImage(guidelinesCanvas, scaleX(card.marginX) / 2, scaleY(card.marginY) / 2, cardCanvas.width, cardCanvas.height);
	}
	// watermark
	cardContext.drawImage(watermarkCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	// custom elements for sagas, classes, and dungeons
	if (card.version.toLowerCase().includes('saga') && typeof sagaCanvas !== "undefined") {
		cardContext.drawImage(sagaCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	} else if (card.version.toLowerCase().includes('class') && typeof classCanvas !== "undefined") {
		cardContext.drawImage(classCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	} else if (card.version.toLowerCase().includes('dungeon') && typeof dungeonCanvas !== "undefined") {
		cardContext.drawImage(dungeonCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	}
	// text
	cardContext.drawImage(textCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	// set symbol
	cardContext.drawImage(setSymbol, scaleX(card.setSymbolX), scaleY(card.setSymbolY), setSymbol.width * card.setSymbolZoom, setSymbol.height * card.setSymbolZoom)
	// serial
	if (card.serialNumber || card.serialTotal) {
		var x = parseInt(card.serialX) || 172;
		var y = parseInt(card.serialY) || 1383;
		var scale = parseFloat(card.serialScale) || 1.0;

		cardContext.drawImage(serial, scaleX(x/2010), scaleY(y/2814), scaleX(464/2010) * scale, scaleY(143/2814) * scale);

		var number = {
			name:"Number",
			text: '{kerning3}' + card.serialNumber || '',
			x: (x+(30 * scale))/2010,
			y: (y+(52 * scale))/2814,
			width: (190 * scale)/2010,
			height: (55 * scale)/2814,
			oneLine: true,
			font: 'gothambold',
			color: 'white',
			size: (55 * scale)/2010,
			align: 'center'
		};

		var total = {
			name:"Number",
			text: '{kerning3}' + card.serialTotal || '',
			x: (x+(251 * scale))/2010,
			y: (y+(52 * scale))/2814,
			width: (190 * scale)/2010,
			height: (55 * scale)/2814,
			oneLine: true,
			font: 'gothambold',
			color: 'white',
			size: (55 * scale)/2010,
			align: 'center'
		};

		writeText(number, cardContext);
		writeText(total, cardContext);
	}
	// bottom info
	if (card.bottomInfoTranslate) {
		cardContext.save();
		cardContext.rotate(Math.PI / 180 * (card.bottomInfoRotate || 0));
		cardContext.translate(card.bottomInfoTranslate.x || 0, card.bottomInfoTranslate.y || 0);
		cardContext.drawImage(bottomInfoCanvas, 0, 0, cardCanvas.width * (card.bottomInfoZoom || 1), cardCanvas.height * (card.bottomInfoZoom || 1));
		cardContext.restore();
	} else {
		cardContext.drawImage(bottomInfoCanvas, 0, 0, cardCanvas.width, cardCanvas.height);
	}


	// cutout the corners
	cardContext.globalCompositeOperation = 'destination-out';
	if (!skipFrame && !card.noCorners && (card.marginX == 0 && card.marginY == 0)) {
		var w = card.version == 'battle' ? 2100 : getStandardWidth();

		cardContext.drawImage(corner, 0, 0, scaleWidth(59/w), scaleWidth(59/w));
		cardContext.rotate(Math.PI / 2);
		cardContext.drawImage(corner, 0, -card.width, scaleWidth(59/w), scaleWidth(59/w));
		cardContext.rotate(Math.PI / 2);
		cardContext.drawImage(corner, -card.width, -card.height, scaleWidth(59/w), scaleWidth(59/w));
		cardContext.rotate(Math.PI / 2);
		cardContext.drawImage(corner, -card.height, 0, scaleWidth(59/w), scaleWidth(59/w));
		cardContext.rotate(Math.PI / 2);
	}
	// show preview
	previewContext.clearRect(0, 0, previewCanvas.width, previewCanvas.height);
	previewContext.drawImage(cardCanvas, 0, 0, previewCanvas.width, previewCanvas.height);
}
```

- [ ] **Step 2: Manual verification — default behavior unchanged**

Reload the page, make any edit (e.g. type card text). Confirm the preview draws exactly as before — every existing call site (`drawCard()` with no arguments, called from dozens of `onchange` handlers throughout the file) is unaffected since both new parameters default to `false`.

- [ ] **Step 3: Manual verification — flags work**

In devtools Console, with a card that has art, a frame, and some text set up:

```js
drawCard(true, false);
```

Expected: the visible preview (which `drawCard` also updates via `previewContext`) now shows the frame/text/symbol with a transparent/empty hole where the art was.

```js
drawCard(true, true);
```

Expected: preview shows only text/symbol/watermark/collector info on a transparent background, no frame, no art, no rounded-corner cutout.

```js
drawCard();
```

Expected: preview returns to the normal full card.

- [ ] **Step 4: Commit**

```bash
git add js/creator-23.js
git commit -m "Add skipArt/skipFrame flags to drawCard"
```

---

### Task 6: Export tab

**Files:**
- Modify: `creator/index.html:107` (add tab header) and `:691` (add tab panel, after Import/Save panel, before Tutorial panel)
- Modify: `js/creator-23.js` (add export functions near `downloadCard`)

- [ ] **Step 1: Add the tab header**

In `creator/index.html`, find:

```html
					<h3 class='selectable readable-background' onclick='toggleCreatorTabs(event, "import")'>Import/Save</h3>
					<h3 class='selectable readable-background' onclick='toggleCreatorTabs(event, "tutorial"); loadTutorialVideo();'>Tutorial</h3>
```

Replace with:

```html
					<h3 class='selectable readable-background' onclick='toggleCreatorTabs(event, "import")'>Import/Save</h3>
					<h3 class='selectable readable-background' onclick='toggleCreatorTabs(event, "export")'>Export</h3>
					<h3 class='selectable readable-background' onclick='toggleCreatorTabs(event, "tutorial"); loadTutorialVideo();'>Tutorial</h3>
```

- [ ] **Step 2: Add the tab panel**

In `creator/index.html`, find the closing of the Import/Save panel followed by the Tutorial panel opening:

```html
					</div>
					<div id='creator-menu-tutorial' class='hidden'>
```

Replace with:

```html
					</div>
					<div id='creator-menu-export' class='hidden'>
						<div class='readable-background margin-bottom padding'>
							<h5 class='margin-bottom padding input-description'>Export the full card, exactly as it downloads today</h5>
							<button class='input' onclick='downloadCard();'>Export Full Card</button>
						</div>
						<div class='readable-background margin-bottom padding'>
							<h5 class='margin-bottom padding input-description'>Export frame, text, and set symbol only (no art)</h5>
							<button class='input' onclick='exportFrameAndText();'>Export Frame + Text + Symbol</button>
						</div>
						<div class='readable-background margin-bottom padding'>
							<h5 class='margin-bottom padding input-description'>Export text and set symbol only (no frame, no art) as a transparent PNG</h5>
							<button class='input' onclick='exportTextOnly();'>Export Text + Symbol Only</button>
						</div>
					</div>
					<div id='creator-menu-tutorial' class='hidden'>
```

- [ ] **Step 3: Add `exportVariant`, `exportFrameAndText`, `exportTextOnly`**

In `js/creator-23.js`, add directly after `downloadCard` (which ends at line 4693, right before the `//IMPORT/SAVE TAB` comment):

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
function exportFrameAndText() {
	exportVariant(true, false, '-frame');
}
function exportTextOnly() {
	exportVariant(true, true, '-textonly');
}
```

`exportVariant` mirrors the download portion of `downloadCard()` (`js/creator-23.js:4660-4693`) but always exports PNG (transparency requires it — no JPEG path for these two variants), always uses the direct-download branch (no `alt`/new-tab option, matching what the spec asks for: just a file), and skips the artist-credit guard that gates `downloadCard()` since there's no art to credit in these variants. After capturing the data URL it calls `drawCard()` with no arguments to redraw the normal full card, so the on-screen preview is restored.

- [ ] **Step 4: Manual verification**

Reload the page, build a test card with art, a frame, a text box, and a set symbol. Go to the new Export tab:

1. Click "Export Full Card" — confirm a PNG downloads and looks identical to what "Download" in the old flow produced (same content).
2. Click "Export Frame + Text + Symbol" — confirm a PNG named `<card name>-frame.png` downloads showing frame, text, and set symbol but no art (transparent where art was).
3. Click "Export Text + Symbol Only" — confirm a PNG named `<card name>-textonly.png` downloads showing only text and set symbol on a fully transparent background (open it in an image viewer that shows alpha, e.g. Preview.app, to confirm transparency — not just a black/white fill).
4. After each of the two new exports, confirm the on-screen card preview in the Frame/Text/etc. tabs still shows the normal full card (proves the final `drawCard()` restore call works).

- [ ] **Step 5: Commit**

```bash
git add js/creator-23.js creator/index.html
git commit -m "Add Export tab: frame+text+symbol and text+symbol-only PNG exports"
```

---

### Task 7: Full end-to-end verification and spec sign-off

**Files:** none (verification only)

- [ ] **Step 1: Run through the spec's Testing section**

With the local server running, in the browser:

1. Save a frame preset, change frames, Apply preset — confirm frame stack matches what was saved and nothing else on the card changed.
2. Delete a preset, confirm it's gone from the dropdown and from a fresh page reload.
3. On a card with art, frame, text, set symbol, watermark, and collector info all populated, export all three files and confirm:
   - Full Card matches current export behavior exactly.
   - File 2 has no art, everything else present.
   - File 3 has no art and no frame, everything else present, transparent background.
4. Confirm the on-screen preview still shows the full card after using any export button.

- [ ] **Step 2: Fix any discrepancies found, then commit**

If Step 1 surfaces anything, fix it in the relevant file from the task above and commit as a follow-up fix with a message describing what was wrong (e.g. `git commit -m "Fix frame preset order not preserved on apply"`).

If everything passes, no commit is needed for this task — it's verification-only.
