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

State the falloff explicitly: say what stays crisp and legible close to the source, and what recedes into shadow or haze as distance from it increases. This is what sells the light as real and gives the background depth without it competing with the subject.

When two magic effects or two colors of magic share the frame (e.g. a white ward colliding with a black corruption), state explicitly that they are kept visually distinct from one another — different color temperature, different texture of glow, different edge quality — so the two effects don't visually blend into one indistinct wash.

**High-key exception:** not every scene wants strong falloff into shadow. When the reference tone is bright and even throughout (a luminous, high-key subject rather than a moody one), say so explicitly and drop the shadow-heavy language — e.g. "diffuse warm daylight glowing evenly... with only gentle, shallow shadow... no hard falloff, no dark side, the whole figure stays legible and bright." Defaulting to strong rim-light-with-shadow phrasing when the intended result is bright and even will make the output darker and moodier than intended.

## 3. Intricacy rule

Give the subject visible history, not a clean, freshly-rendered surface. This means at least one of: an engraved micro-narrative (a worn inscription, a scene etched into metal or bone), a wear pattern (scorch marks, rust bleeding from a joint, a repaired crack), or an unusual material choice that implies a specific origin (bone instead of wood, living wood instead of dead, a blade quenched in something other than water).

The test: the prompt should reward a second look with a new detail, not just register once at a glance. A generic "ornate" or "detailed" adjective does not satisfy this rule — the detail has to be a specific, nameable thing.

## 4. Palette discipline

State 2-3 dominant colors as an explicit, named short list — e.g. "deep reds, aged gold, near-black shadows" or "bone white, oxidized copper-green, ink black." This list is what keeps a faction's cards visually cohesive across a whole deck.

Never leave the palette open-ended. Phrases like "vibrant colors," "rich colors," or "a striking palette" are banned — they give the image model no actual constraint and produce inconsistent results across a batch.

## 5. Framing: full subject, contained, no crop zone

**Corrected 2026-09-24** — the previous version of this rule (a portrait `5:7` full-bleed with a "expendable" top/bottom zone meant to be cropped by the title bar/text box) was built on an assumption about the target app's frame system that turned out to be wrong, confirmed by a real working generation against the actual production app (CardConjurer): the real art box is a fixed, already-correctly-shaped rectangle — you compose to fit inside it, nothing gets cropped after the fact.

Every prompt must state, in this pattern, that the full subject is contained with margin, not bled to the edge:

> "[subject], entirely contained within the frame with an even roughly 20% margin of background visible on all four sides, not cropped at any edge."

When the subject has a part that's easy to lose (wingtips, a weapon's far end, a tail), name that part explicitly as also fully visible — don't rely on "entirely contained" alone to protect it. A described decisive moment that's inherently a close-up event (a blade's tip touching a surface, a hand gripping a hilt) will pull the camera in tight and crop out other important features unless you explicitly state the camera is pulled back far enough to show the whole subject, both ends, in one shot.

Use this pattern in every card prompt across every type skill — paraphrase the specific subject/parts named, but keep the "fully contained... not cropped" structure, since it's the load-bearing instruction against the model's default tendency to crop tight on whatever's most detailed.

## 6. Framing tightness

Default to a shot that shows the complete subject with visible breathing room on all sides (per Rule 5) — not an extreme, edge-to-edge close-up that crops off any part of the subject, and not so wide that the subject reads as small/incidental in the frame. A useful target: roughly a 20% margin of background on each side, subject filling the rest.

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

**Don't overcorrect into a static portrait to dodge this problem.** Dynamic mid-action poses are not the cause of weapon-geometry failures and shouldn't be abandoned for them — real published Magic art is routinely full dynamic combat, multiple things in motion at once, and reads fine. The actual failure mode is *unanchored* geometry, and separately, *conflicting* simultaneous motion (hair blown one way, wings flared another, a cloak reacting to a third implied force, with nothing tying them together). Fix dynamism by giving every moving element the same stated cause — one wind direction, one lunge/momentum vector — so hair, cloak, sash, and wings all read as reacting to the same instant, not by removing the motion.

**Don't overcorrect into a boring weapon either.** The fix above is about grounding geometry, not stripping away character. Keep the weapon fantastical and specific — unusual cross-guard shapes, exotic materials, engraved motifs, an asymmetric silhouette, gemstones, a curved or hooked profile — the ornamentation is exactly what makes it feel like *this* card's weapon and not a generic sword. The trick is to hang all of that invention on a **base type and size a person could plausibly swing**: pick a real weapon category as the starting silhouette (longsword, greatsword, glaive, war-scythe, halberd) and keep its proportions in that category's real range, rather than inventing an exaggerated scale ("a blade taller than she is") as the fantasy element. Once the base type and size read as functionally wieldable, decorate freely — the elaboration should live in material, engraving, and silhouette detail, not in physically implausible proportions.

## 7c. Fused/composite-material object silhouette gotcha

The same root failure as Rule 7b (large blades) applies to any object built from multiple visually distinct materials fused together (a scepter head combining bone, horn, and scale; a staff topped with mixed metals) — it reliably renders as a vague, blended texture-blob with no coherent shape when the prompt describes the *materials* without ever naming the object's actual *silhouette*. Before describing what each material zone looks like, name the shape itself in one concrete term (a leaf-blade, a disc, a trefoil with N distinct lobes, a tapered spike) — then assign materials to specific named parts of that shape (e.g. "a trefoil head, three lobes radiating from one point... one lobe carved bone-white, one lobe blackened horn, one lobe bronze scale, each lobe keeping a clean edge where it meets the others"). Materials described without a named silhouette first, or materials described as "fusing" or "converging" without a stated shape for what they converge into, are what produces the blob.

## 8. Banned words

The following words are banned as mid-scene description, anywhere in the body of the prompt: **epic, majestic, dramatic, stunning, breathtaking, mystical, ethereal, awe-inspiring**. They are empty intensifiers that give the image model no concrete visual instruction and are a strong signal of generic AI-fantasy prose.

Exception: exactly one of these words is allowed once, as a single terminal atmosphere tag at the very end of the prompt, functioning as a short mood label rather than descriptive prose — e.g. "...Magic: The Gathering card art style, epic isolated atmosphere, high detail." This matches observed usage in the proven prompt corpus, where the word appears only in that closing-tag position, never earlier in the scene description.

## 9. Closing suffix

Every prompt ends with this fixed suffix, held constant per deck:

`Painterly digital fantasy illustration, Magic: The Gathering [artifact] card art style, [2-4 word atmosphere tag], high detail. --ar 4:3`

(`--ar 4:3` is the confirmed-working default for this app's art box — corrected 2026-09-24 from an earlier, wrong `5:7` assumption. A type skill may still state its own override for a genuinely different physical format, the way `battle/SKILL.md` does for landscape siege cards.)

Replace `[artifact]` with the card's type-appropriate noun where relevant (or drop the bracket entirely if the type skill's convention doesn't use it), and `[2-4 word atmosphere tag]` with a short mood phrase — this is the one place the single banned-word exception from Rule 8 may land.

Only add `--no <specific clutter terms>` when several generations in a row have converged on the same specific unwanted element (e.g. `--no text, extra limbs`) — never include `--no` by default or speculatively; it is a targeted fix applied after observing a real problem, not a standing parameter.

## 10. Scene composition: actor and reactor, not portraiture

**Added 2026-09-24**, after repeated live testing showed that even a well-executed subject (a weapon correctly grounded per Rule 7b, a creature correctly posed) still reads as generic inventory rather than a card that belongs to a specific world, if the composition is a portrait of one thing existing rather than a moment where something changes. This applies to every card type, including creatures — the failure isn't type-specific, it's "isolated subject" vs. "witnessed event."

- **Translate the mechanic into an event, not an object.** Don't ask what the thing that causes the effect looks like. Ask: if this effect happened once, physically, what would someone standing nearby have seen? A mana rock's story is the moment it was found or the debt it represents coming due, not the rock. This is doubly true for artifact/enchantment/sorcery, which have no body of their own to photograph — see each of those type skills' own guidance on defaulting to an object-optional scene instead of an object portrait.
- **A story needs an actor and a reactor.** A lone figure or creature performing an action, however dynamic, is still a portrait. What makes it a scene is a second presence whose response sells the stakes — a crowd flinching, a rival mid-defeat, a witness reacting to something the main subject is doing or that's happening to them. Two entities in tension, not one entity alone.
- **Decide camera distance and each element's frame-share before writing detail, then match detail density to that share.** The image model allocates canvas space in proportion to how much specific detail an element carries, not to a stated fraction like "fills the upper half." Lavishing five sentences of texture on the actor and one clause on the reactor/environment will produce a tight portrait of the actor with the rest crushed into a sliver, regardless of what ratio was typed. If a scene needs two roughly equal halves, write roughly equal, comparably specific detail for both.
- **The environment should be caused by the mechanic, not decorative.** A generic backdrop is wallpaper. A backdrop that's visibly the result of what this card does (a valley scarred by exactly this effect, a room arranged by exactly this alliance's mistrust) is evidence, not scenery.
- **One bridging element ties both halves into a single moment.** A raised weapon, an upturned face, a shared shadow, a beam of light crossing both zones — without it, a two-part composition reads as two pictures stacked, not one instant.
- **Total detail budget is fixed regardless of element count.** Rule 3's "one specific detail" budget was calibrated for a solo subject. A scene with an actor, a reactor, an environment, and a bridging element divides that same attention across all of them — over-detailing one element starves the others and collapses the composition back toward a portrait of just that one thing (see the second point above).

## 11. No text, frames, or artist names

The described art must never include literal text, letters, numbers, card frames, borders, or any UI element — the art is the illustration only, not a mockup of the finished card. Do not name any living artist to steer style (no "in the style of [artist]"); every stylistic result must come from the conventions in this file (lighting, palette, intricacy, framing) rather than borrowing a named artist's signature look.
