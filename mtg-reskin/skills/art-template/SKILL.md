# Art Template — Shared Art-Direction Skeleton

This is the shared base every card-type skill (`creature`, `artifact`, `instant`, `sorcery`, `enchantment`, `land`, `planeswalker`, `battle`) is built on. It encodes the rules that keep all cards in a themed deck reading as one coherent, professionally-art-directed set instead of eight unrelated AI-fantasy generators. **Do not duplicate these rules inside a type skill.** A type skill should reference this file by name and add only its own compositional-mode taxonomy (the type-specific "what kind of shot is this" step) plus any per-type defaults — everything below is shared and applies unmodified to every card, regardless of type.

These rules are derived from Rodrigo's corpus of 21 proven Midjourney prompts (`reference/user-prompts.md`), not invented from scratch — when in doubt, they are ground truth over general prompt-engineering intuition.

## 1. Who/What/Why/Where brief

Before drafting any prompt, silently answer four questions. This is a private reasoning step — its output shapes the prompt, but the four labels themselves do not need to appear in the final prompt text.

- **Who**: Decide whether a figure, a hand, or an implied second party belongs in the frame at all, or whether the object or scene carries itself alone without needing a human/creature presence. Do not default to "add a figure" — many strong artifact and land prompts have none.
- **What**: Name the specific frozen moment being depicted. Never describe the subject at rest, at idle, or in a neutral pose — pick the instant of action, change, or consequence that the card's effect implies.
- **Why**: The visual metaphor chosen for What must map onto the card's actual mechanic (what it does in the rules) or the deck's lore (its place in the faction's story) — never decoration chosen because it looks nice in isolation. If you can't state which mechanic or lore beat the image is dramatizing, the concept isn't ready.
- **Where**: Establish the setting and a diegetic light source (see Rule 2) together, and position that light source relative to the framing band described in Rule 5 — the light source is part of staging the shot, not an afterthought added after the composition is set.

## 2. Diegetic lighting rule

Every prompt must name the physical, in-world source of its light explicitly: a candle, a spell's own glow, moonlight through a specific gap, forge fire, an energy burst, bioluminescence, etc. Never write "dramatic lighting," "moody lighting," or any other lighting descriptor that doesn't point to a physical source in the scene.

State the falloff explicitly: say what stays crisp and legible close to the source, and what recedes into shadow or haze as distance from it increases. This is what sells the light as real and also does the compositional work of Rule 5 — the falloff is what naturally darkens the areas meant to be cropped.

When two magic effects or two colors of magic share the frame (e.g. a white ward colliding with a black corruption), state explicitly that they are kept visually distinct from one another — different color temperature, different texture of glow, different edge quality — so the two effects don't visually blend into one indistinct wash.

## 3. Intricacy rule

Give the subject visible history, not a clean, freshly-rendered surface. This means at least one of: an engraved micro-narrative (a worn inscription, a scene etched into metal or bone), a wear pattern (scorch marks, rust bleeding from a joint, a repaired crack), or an unusual material choice that implies a specific origin (bone instead of wood, living wood instead of dead, a blade quenched in something other than water).

The test: the prompt should reward a second look with a new detail, not just register once at a glance. A generic "ornate" or "detailed" adjective does not satisfy this rule — the detail has to be a specific, nameable thing.

## 4. Palette discipline

State 2-3 dominant colors as an explicit, named short list — e.g. "deep reds, aged gold, near-black shadows" or "bone white, oxidized copper-green, ink black." This list is what keeps a faction's cards visually cohesive across a whole deck.

Never leave the palette open-ended. Phrases like "vibrant colors," "rich colors," or "a striking palette" are banned — they give the image model no actual constraint and produce inconsistent results across a batch.

## 5. Framing for card crop

Every prompt must state, in this exact phrasing pattern, where the subject sits in the frame and why the rest is deliberately expendable:

> "composition composed so the [subject/most detailed part] sits within the vertical middle band of the frame, roughly between 20% and 65% down from the top, well clear of both the top 15% and bottom 35% of the image — [upper area] fading into plain dark atmosphere, expendable space meant to be cropped by the title bar; [lower area] fading into shadow, expendable space meant to be cropped by the text box."

Fill in `[subject/most detailed part]` with the specific focal element (e.g. "the creature's face and clawed hand," "the blade's inscribed fuller") and `[upper area]` / `[lower area]` with what's actually receding there (e.g. "smoke and rafters above," "loose stone and shadow below"). Use this pattern verbatim in every card prompt across every type skill — other skills and the orchestrator quote this exact phrasing, so it must not be paraphrased or shortened.

## 6. Framing tightness

Default to a close-up or medium-tight shot with a visible pocket of dim surrounding environment left in frame — not an extreme, edge-to-edge close-up that fills the entire canvas with the subject. The card crop needs real, undetailed space to eat into at the top and bottom (per Rule 5); an edge-to-edge composition leaves nothing for the crop to consume without cutting into the subject itself.

## 7. Body-part continuity gotcha

If a figure's own limb or body part is transforming into, fusing with, or growing an object (a hand becoming a blade, an arm sprouting bark), describe it as one single continuous part — e.g. "an arm that ends in a jagged crystal blade, the crystal growing directly from the forearm." Never phrase this as the figure "gripping," "holding," or "wielding" a separate object, even if that's visually similar to what you intend — the image model reads "gripping X" as two distinct objects (a hand, and a separate item), which breaks the fused/transforming read entirely.

## 7b. Large single-blade weapon geometry gotcha

Oversized bladed weapons (greatswords, glaives, single tall blades held two-handed) reliably render as a shapeless flat slab — no visible cross-section, no consistent width along its length, ambiguous edge vs. flat — when described only by size and ornament ("a massive curved greatsword," "an ornate blade taller than she is"). This is a distinct failure from Rule 7's fusion gotcha: here the object is held correctly, but its own geometry collapses. It gets worse in a symmetrical, vertical, frontal composition, where a long blade held upright reads as just another vertical shape alongside wings/limbs and loses its silhouette entirely.

Fixes, apply together when a large single-blade weapon is the focal object:
- **State the cross-section explicitly**: "a blade with a clear diamond cross-section" or "a flat blade with a raised central fuller running its length" — never leave width/thickness to be inferred from size alone.
- **Anchor the width to something concrete**, not just overall length: "roughly a hand's-width at the base, tapering evenly to a point" rather than "massive" or "towering" alone.
- **State each hand's grip point relative to a named part of the weapon** (hilt, crossguard, grip-wrap) rather than just "gripping the sword" — e.g. "one hand at the crossguard, the other lower on the wrapped grip" — an unanchored two-handed grip on an oversized object is exactly where the model loses track of hand-to-object relationship.
- **Give the blade a resting point or clear termination** (point driven into the ground, point held level, tip resting on a shoulder) rather than letting it run off the bottom of the frame — an ambiguous, cropped blade base is a second place the shape can fall apart.
- **Break bilateral symmetry** if the weapon is held centrally in an otherwise symmetrical pose (e.g. wings spread evenly on both sides) — angle the blade a few degrees off the body's centerline, or offset it against one side, so its edges don't visually merge with a wing or limb silhouette behind it.

## 8. Banned words

The following words are banned as mid-scene description, anywhere in the body of the prompt: **epic, majestic, dramatic, stunning, breathtaking, mystical, ethereal, awe-inspiring**. They are empty intensifiers that give the image model no concrete visual instruction and are a strong signal of generic AI-fantasy prose.

Exception: exactly one of these words is allowed once, as a single terminal atmosphere tag at the very end of the prompt, functioning as a short mood label rather than descriptive prose — e.g. "...Magic: The Gathering card art style, epic isolated atmosphere, high detail." This matches observed usage in the proven prompt corpus, where the word appears only in that closing-tag position, never earlier in the scene description.

## 9. Closing suffix

Every prompt ends with this fixed suffix, held constant per deck:

`Painterly digital fantasy illustration, Magic: The Gathering [artifact] card art style, [2-4 word atmosphere tag], high detail. --ar 5:7`

Replace `[artifact]` with the card's type-appropriate noun where relevant (or drop the bracket entirely if the type skill's convention doesn't use it), and `[2-4 word atmosphere tag]` with a short mood phrase — this is the one place the single banned-word exception from Rule 8 may land.

Only add `--no <specific clutter terms>` when several generations in a row have converged on the same specific unwanted element (e.g. `--no text, extra limbs`) — never include `--no` by default or speculatively; it is a targeted fix applied after observing a real problem, not a standing parameter.

## 10. No text, frames, or artist names

The described art must never include literal text, letters, numbers, card frames, borders, or any UI element — the art is the illustration only, not a mockup of the finished card. Do not name any living artist to steer style (no "in the style of [artist]"); every stylistic result must come from the conventions in this file (lighting, palette, intricacy, framing) rather than borrowing a named artist's signature look.
