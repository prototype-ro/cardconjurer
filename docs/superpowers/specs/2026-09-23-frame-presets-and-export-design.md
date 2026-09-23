# Frame Presets + Export Section

Date: 2026-09-23

## Goal

Speed up making many cards by hand: let a frame layout be saved and
reapplied in one click, and let each card be exported as three PNGs
instead of one, for downstream compositing.

Not in scope: batch/unattended generation over a list of card data.
This spec covers manual, per-card use of both features. A batch
runner is a candidate follow-up spec.

## 1. Frame presets (frame stack + linked text styling)

### What's saved

One combined preset, saved and applied as a single unit:

1. **Frame stack** — the current value of `card.frames` (the ordered
   list of frame/mask image entries drawn by `drawFrames()` at
   [js/creator-23.js:386](../../../js/creator-23.js#L386)).
2. **Text styling** — for every key currently in `card.text` (each
   textbox: title, rules text, P/T, mana cost, etc. — see
   `loadTextOptions` at
   [js/creator-23.js:3286](../../../js/creator-23.js#L3286)), the
   *style* fields only, captured per textbox name so title keeps its
   own style, rules text keeps its own, etc.:
   `color`, `font`, `fontStyle`, `shadow`, `shadowX`, `shadowY`,
   `shadowBlur`, `outlineColor`, `outlineWidth`, `kerning`,
   `lineSpacing`, `align`, `justify`.

Explicitly **not** captured, on either the frame or text side: text
*content* (`text`), textbox position/size (`x`, `y`, `width`,
`height`), art, set symbol, watermark, collector info. Save/apply only
ever touches frame stack + the listed style fields on textboxes that
already exist on the card at apply time.

### Storage

New IndexedDB object store `framePresets` in the existing
`CardConjurerDB` (same database the `cardDB` helper already opens for
saved cards, see `js/creator-23.js` around line 5000). Key = preset
name (string). Value = one object:

```js
{
  frames: [...],       // deep copy of card.frames, image refs stripped
  textStyles: {         // keyed by textbox name, e.g. "title", "rules", "pt"
    title: { color, font, fontStyle, shadow, shadowX, shadowY,
              shadowBlur, outlineColor, outlineWidth, kerning,
              lineSpacing, align, justify },
    rules: { ... },
    ...
  }
}
```

### UI

New sub-section in the Frame tab (`#creator-menu-frame` in
[creator/index.html](../../../creator/index.html)), placed after the
existing "frame-list" reorder section:

- Text input + "Save Frame Preset" button. On click: read the frame
  list order live from `card.frames`, and the style fields from every
  entry currently in `card.text`, and write both into a single
  `framePresets` record under the typed name. Empty/duplicate name
  handling follows the same pattern already used for card names in
  `saveCard()`.
- `<select>` populated from `framePresets` keys (list refreshed after
  save/delete, same pattern as `loadAvailableCards()`).
- "Apply" button:
  - Frame side: clear `#frame-list` and `card.frames`, set
    `card.frames` to a deep copy of the stored preset's `frames`,
    rebuild the frame-list DOM the same way `addFrame()` does for each
    entry, then call `drawFrames()` to redraw.
  - Text side: for each key in the stored preset's `textStyles` that
    also exists in the *current* `card.text` (a preset saved against
    one frame layout may name textboxes a differently-loaded frame
    doesn't have — those are skipped, not errored), merge the saved
    style fields onto `card.text[key]` (overwriting only those fields,
    leaving `text`/`x`/`y`/`width`/`height` untouched), then call
    `drawTextBuffer()` to redraw.
- "Delete" button: removes the selected key from `framePresets`,
  refreshes the list.

### Error handling

Same shape as existing card storage errors: wrap IndexedDB calls in
try/catch, `notify()` on failure. No new failure modes introduced
beyond what `cardDB` already handles. A `textStyles` entry naming a
textbox absent from the current card is silently skipped (not an
error) — the preset is meant to be reusable across cards whose frame
version may expose a different set of textboxes.

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

- Save a frame preset with distinct text styling on two textboxes
  (e.g. different shadow colors), change frames and text styles,
  Apply preset, confirm frame stack AND per-textbox styling both
  match what was saved, text content/position untouched.
- Apply a frame preset saved on one card to a card whose `card.text`
  is missing one of the saved textbox names — confirm it applies the
  frame + the styles that do match, and does not error on the rest.
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
