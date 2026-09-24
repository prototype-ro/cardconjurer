---
name: "artifact"
description: "Use when generating Midjourney prompts for MTG artifact card art (mana rocks, equipment, relics) for Rodrigo's decks, including original/replacement artifacts for his Raphael, Fiendish Savior deck. Covers the Who/What/Why/Where design brief and the five compositional modes for artifact art."
---

# MTG Artifact Card Art

> Built on skills/art-template/SKILL.md — see that file for the shared lighting/framing/palette/banned-word rules. This file adds only the artifact-specific compositional modes below.

Artifact cards are a different design problem from creature or planeswalker art: there is no face, no pose, no obvious protagonist. An object sitting still, photographed well, still reads as boring. This skill is the process for avoiding that.

## Step 1 — Run the Who/What/Why/Where brief before writing any prompt

Do this silently (or out loud if asked) before drafting. If any answer is weak, the composition will be weak — fix it here, not after seeing a bad result.

- **Who** — an artifact has no inherent "who." Decide whether a figure, hand, or implied second party belongs in the frame, or whether the object's own material/shape can carry the piece alone.
- **What** — the specific frozen moment. Never "a sword," always "a sword breaking free of stone at the instant it comes loose." If you can't name a concrete moment, the object is at rest and the piece will read as generic — this is the single most common failure mode for artifact art.
- **Why** — the visual metaphor must map onto the card's actual mechanic or the deck's story. A two-faced chalice for a life-payment card, a fading/blurring boot for hexproof-through-speed, a mid-signature contract for a card about broken bargains. If the why doesn't connect to the mechanic, the art is decoration, not storytelling.
- **Where** — setting and light source, diegetic (the object's own glow, a candle, a crack of light) rather than generic "dramatic lighting," plus where the composition's weight sits relative to the printed card's actual art window (see Framing below).

## Step 2 — Pick a compositional mode

Five modes cover almost every well-regarded MTG artifact illustration. Naming the mode before writing the prompt keeps the piece from defaulting to a generic object portrait.

1. **Caught mid-use, not at rest.** The object doing the thing it mechanically does, at the exact instant it does it (Embercleave mid-swing, Skullclamp biting into a skull, Colossus Hammer at impact). Needs a genuinely distinctive "use" moment tied to the card's ability, not just a generic action pose — a static object mid-air is not automatically more interesting than a static object on a table.
2. **A human gesture implying a larger ritual.** Hands mid-action (signing, sealing, exchanging, reaching) with the object as the one lit thing. Requires an actual reason for the touch — a pact, a claiming, a working — or it collapses back into a random hand holding an object. Best mode for anything with an inherent "exchange" concept (pacts, bargains, tributes).
2b. **Painterly half-figure portrait variant.** When a hand alone isn't enough weight, pull back to a half-figure portrait (aristocrat, patron, wielder) caught mid-gesture with the object — classical oil-painting chiaroscuro, figure's head in the upper-middle band, object at the true center, robes/setting fading out toward the bottom. Good for pieces that want narrative gravity a bare hand can't carry.
3. **Material duality as the whole concept.** The object's own material tells the mechanical story with no figure or action needed (Sword of Fire and Ice's elemental split, a chalice that's wine on one side and ichor on the other). Only works when the mechanic has a natural physical metaphor baked into the material itself.
4. **Minimal iconic object, no scene at all.** Works only when the object's silhouette is inherently striking on its own (a giant lotus bloom, an ornate spinning top). Plain armor, plain boots, plain rings do NOT qualify — staging can't rescue a shape that isn't interesting to begin with.
5. **A window into a wider world.** The object as a threshold into something bigger (a swirling void in a chest, a skull altar in a dark chamber), using scale and implied menace rather than tight cropping.

## Step 3 — Add real intricacy, not just a lighting trick

A color-shift or a single glow is not depth. Give the object visible history: engraved reliefs that tell a micro-story (tiny figures being pulled under, a tally of names too small to read), an unusual material choice (serpents forming the stem, a frieze wrapping the bowl), wear patterns. The object should reward a second look, not just catch the eye once.

## Step 4 — Framing for full-art card crop

A printed full-art card's title bar covers roughly the top 10-15% of the image and the text box covers roughly the bottom 35-40%. The actual visible "art window" is the middle band — roughly 20% to 65% down from the top. State this explicitly and with real percentages in every prompt:

> "composition composed so the [subject/most detailed part] sits within the vertical middle band of the frame, roughly between 20% and 65% down from the top, well clear of both the top 15% and the bottom 35% of the image... [upper area] fading into plain dark atmosphere — expendable space meant to be cropped by the title bar, [lower area] fading into shadow — expendable space meant to be cropped by the text box"

Just saying "kept clear of the top/bottom edge" is not enough — it tells the model what to avoid, not where the composition's actual weight should concentrate.

## Step 5 — Framing tightness: close-up, not extreme close-up

Extreme, edge-to-edge close-ups fix genericness but overcorrect into claustrophobic results that fight the art-window crop (no negative space left for the title bar / text box to eat into). Default to "close-up, medium-tight shot" with a visible pocket of dim surrounding environment around the object, not "extreme close-up... nothing else in frame." The object should still be the clear focal point — it just needs room to breathe.

## Technical settings currently in use

- Aspect ratio: `--ar 5:7`
- Palette discipline: 2-3 dominant colors per piece (e.g. warm gold + blood-red + near-black), not a full rainbow — this is what makes tight/limited-palette pieces read as intentional rather than washed out.
- Avoid stacking multiple "near-black / crushing shadow" phrases — always pair dark atmosphere with an explicit legible-detail instruction on the focal point ("that glow the single strongest light source... spilling warm highlights across [subject] while [background] fades to near-black").
- If a creature/figure's own limb or body part is transforming, describe it as ONE continuous body part, never as "gripping/holding" a separate limb — the engine misreads that as two distinct objects.
- For genuinely cluttered/chaotic results (e.g. crystal-shard visual noise), use `--no` negatives naming the specific clutter terms (e.g. `--no crystal shards, glass fracture, shattered glass, prism shards, chaotic debris`) rather than trying to talk the model down with fewer adjectives.

## Reference-gathering keywords (Pinterest/web)

When research is needed before drafting, search across both object-only and scene-level references — defaulting to one or the other produces one-note results:
- Object/material references: "[object type] macro photography," "[object type] concept art," "gothic [object] engraved relief"
- Painterly portrait references: "Baroque portrait [pose] candlelight," "Rembrandt chiaroscuro portrait hand," "classical oil painting [role] robes candlelight"
- Scene/environment references: "[mood] throne room dark academia painting," "cursed relic altar fantasy environment," "two figures negotiation dark painting"
- Direct comps: "Magic the Gathering artifact art" (surfaces real MTG illustrations directly)
