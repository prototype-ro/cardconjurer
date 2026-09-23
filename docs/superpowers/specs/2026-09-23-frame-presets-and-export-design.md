# Frame Presets + Export Section

Date: 2026-09-23

## Goal

Speed up making many cards by hand: let a frame layout be saved and
reapplied in one click, and let each card be exported as three PNGs
instead of one, for downstream compositing.

Not in scope: batch/unattended generation over a list of card data.
This spec covers manual, per-card use of both features. A batch
runner is a candidate follow-up spec.

## 1. Frame presets

### What's saved

Just the frame stack: the current value of `card.frames` (the ordered
list of frame/mask image entries drawn by `drawFrames()` at
[js/creator-23.js:386](../../../js/creator-23.js#L386)). Nothing else
on the card (text, art, set symbol, watermark, collector info) is
touched by save or apply.

### Storage

New IndexedDB object store `framePresets` in the existing
`CardConjurerDB` (same database the `cardDB` helper already opens for
saved cards, see `js/creator-23.js` around line 5000). Key = preset
name (string), value = the `card.frames` array at save time
(structured-clone-safe, same as saved cards already are).

### UI

New sub-section in the Frame tab (`#creator-menu-frame` in
[creator/index.html](../../../creator/index.html)), placed after the
existing "frame-list" reorder section:

- Text input + "Save Frame Preset" button. On click: read the frame
  list order live from `card.frames` (not from any separate draft
  state) and write it to `framePresets` under the typed name.
  Empty/duplicate name handling follows the same pattern already used
  for card names in `saveCard()`.
- `<select>` populated from `framePresets` keys (list refreshed after
  save/delete, same pattern as `loadAvailableCards()`).
- "Apply" button: clear `#frame-list` and `card.frames`, set
  `card.frames` to a deep copy of the stored preset, rebuild the
  frame-list DOM the same way `addFrame()` does for each entry, then
  call `drawFrames()` to redraw.
- "Delete" button: removes the selected key from `framePresets`,
  refreshes the list.

### Error handling

Same shape as existing card storage errors: wrap IndexedDB calls in
try/catch, `notify()` on failure. No new failure modes introduced
beyond what `cardDB` already handles.

## 2. Export section

### UI

New tab in `#creator-menu-tabs` (next to "Import/Save"), with its own
`#creator-menu-export` panel, wired through the existing
`toggleCreatorTabs(event, "export")` mechanism used by every other
tab.

Three buttons:

1. **Full Card** — existing behavior, unchanged.
2. **Frame + Text + Symbol (no art)**
3. **Text + Symbol only (no frame, no art)**

### Rendering

`drawCard()` ([js/creator-23.js:4547](../../../js/creator-23.js#L4547))
gains two optional flags, both defaulting to `false` so every existing
call site (auto-redraw on every edit) is unaffected:

```js
function drawCard(skipArt = false, skipFrame = false) { ... }
```

- `skipArt`: skip the `cardContext.drawImage(art, ...)` call at the
  top of the function (art layer left transparent). Text, set symbol,
  watermark, collector/bottom info, and corner cutout all still draw
  normally.
- `skipFrame`: skip the frame-drawing block (`drawFrames()` output /
  frame canvas composite) in addition to art. Text, set symbol,
  watermark, and collector info still draw at their normal positions,
  producing a transparent PNG with just those layers. Corner cutout is
  skipped in this mode (nothing opaque to cut against).

Because `drawCard()` also drives the live preview
(`previewContext.drawImage(cardCanvas, ...)` at the end of the
function), each export variant draws to `cardCanvas` with the flags
set, captures the PNG via `cardCanvas.toDataURL('image/png')`, and
then **re-runs `drawCard()` with no flags** (or restores the previous
canvas state) before returning, so the on-screen preview is left
showing the normal full card afterward.

### Download

Reuse the download mechanism from `downloadCard()`
([js/creator-23.js:4660](../../../js/creator-23.js#L4660)): build an
`<a download>` element per file. Three files per click-through of "Full
Card" only produces one file (existing behavior); the two new buttons
each produce one file per click. File names: `getCardName()` (line
213) plus a suffix — `-frame` for variant 2, `-textonly` for variant
3 — always `.png` (transparency requires PNG; no JPEG option for the
two new variants).

The existing artist-credit guard in `downloadCard()` (blocks download
if no artist credited and real art is set) applies only to the Full
Card button; the two art-less exports skip that check since there's
no art to credit.

## Testing

Manual verification in the running app (this project has no
automated test suite):

- Save a frame preset, change frames, Apply preset, confirm frame
  stack matches what was saved and nothing else on the card changed.
- Delete a preset, confirm it's gone from the dropdown and from a
  fresh page load (IndexedDB persisted).
- Export all three files on a card with art, frame, text, set symbol,
  watermark, and collector info populated; confirm:
  - Full Card matches current export behavior exactly.
  - File 2 has no art, everything else present.
  - File 3 has no art and no frame, everything else present,
    transparent background.
- Confirm the on-screen preview still shows the full card after using
  any export button.
