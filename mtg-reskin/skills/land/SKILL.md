> Built on skills/art-template/SKILL.md.

This file adds land-specific art direction on top of the shared rules in `art-template/SKILL.md` (diegetic lighting, palette discipline, intricacy, framing, banned words, closing suffix, etc. — all apply unmodified). It does not repeat those rules.

**Land-specific override of the "Who" step:** art-template's Who/What/Why/Where brief (art-template/SKILL.md:11) frames "Who" as a decision about whether a figure belongs in frame at all. For lands, weight that decision harder toward "no figure, or a small distant one" than any other card type. A land's job is to sell a *place*, not a character's action — the framing-percentage rule from Rule 5 still applies unmodified (the same subject sits in the same 20-65% vertical band, and the same top/bottom areas stay expendable for the crop), but for most lands the "most detailed part" filling that band is a landscape feature (a horizon, a rock formation, a cave mouth, a structure) rather than a face or a hand. When a figure does appear, it is normally small, distant, or partial (a silhouette on a ridge, a boat on the water) — a land where a figure fills the frame at creature scale has usually stopped being a land shot and started being a creature shot.

This is a **reduced-depth sample**, scaled to the design spec's cost trade-off for non-creature types, further scaled down for land specifically: one query for basic lands (`t:land t:basic -t:snow -set:sld`), one general query for non-basic lands (`t:land -t:basic -is:funny`), and one for legendary lands (`t:land t:legendary`), each `year>=2010 -is:digital -is:promo`, `unique=art&order=usd&dir=desc`. Roughly 4-6 images were actually opened and viewed per query (not the full 8-10 candidate list each query returns) — this file's conventions are grounded in that smaller viewed subset, not an exhaustive read of every result.

**Sampling note — non-basic query skew:** the general non-basic query, sorted by price, returned almost entirely two things: fetch lands (Polluted Delta, Misty Rainforest, Arid Mesa, Scalding Tarn, Ancient Tomb, Cavern of Souls) and legendary lands (Mount Doom, Eye of Ugin). It did not surface a meaningful population of simple, non-legendary "named location" wide-shot lands (e.g. a plain Temple- or Gate-cycle card) at this depth — the price-sorted top slice skews toward high-value constructed staples, which for non-basic lands means fetches and legendary utility lands, not mid-value flavor lands. Mode 1's "named location" sub-case below is therefore thinner than its basic-land sub-case and leans on general principle rather than several worked examples; mode 2 and mode 3 absorbed most of what this query actually returned.

**Universes Beyond exclusions caught mid-sampling, verified by set code:** the legendary-land query's top price hits included Mount Doom (set `ltr`, *The Lord of the Rings: Tales of Middle-earth* — a Universes Beyond draft set) and reprints of Urborg, Tomb of Yawgmoth, Gemstone Caverns, Minamo, School at Water's Edge, and Yavimaya, Cradle of Growth all under set `ltc` (*Tales of Middle-earth Commander*, also Universes Beyond). Mount Doom was excluded outright as a Tolkien-IP-specific card with no non-crossover printing. For the reprinted originals, the `ltc` printing of each was skipped in favor of a non-crossover printing of the same card (Urborg from `m15`/`tsr`, Gemstone Caverns from `eos`/`tsr`, Minamo from `chk`/`plst`, Yavimaya from `mh2`/`m3c`) rather than treating the Commander-deck art as representative of the corpus's register.

**Not every mode/color cell is evenly populated at this depth**, and this file doesn't force it — see the per-mode notes below for where the sample was thin.

## Contents

**Modes:** [Mode 1 — Wide Establishing Shot](#mode-1--wide-establishing-shot) · [Mode 2 — Utility Land Close-Up](#mode-2--utility-land-close-up) · [Mode 3 — Legendary Location Landmark Shot](#mode-3--legendary-location-landmark-shot)

---

## Mode 1 — Wide Establishing Shot

**When it applies:** basic lands, and non-basic "named place" lands with no single mechanical gimmick to foreground (a plain flavorful location card rather than a fetch, a filter, or a legendary utility land). The shot sells the *scale and character of a place*, not an action.

**Decisive moment:** there usually isn't one in the action-frozen sense the other card types use — the "moment" is a specific time-of-day and weather state that gives the place a mood (a particular slant of light, a specific weather condition passing through), not a character doing something. Per the land-specific Who override above, keep any figure small and distant or omit it; the horizon, skyline, or terrain silhouette is the subject that occupies art-template Rule 5's focal band.

### The five basics — each with its own identity

Basics are not "one generic landscape reskinned five times." The corpus (John Avon, Ralph Horsley, Jesper Ejsing, and other classic Magic landscape artists) treats each basic as a distinct terrain type with its own light, palette, and defining feature:

- **Plains:** wide open grassland running to a low, distant horizon, sky occupying most of the frame — the emptiness and the light itself are the subject, not any single object in it. Warm, low-angle sun (sunrise or sunset) is the default diegetic light source; wind-bent grass in the foreground sells scale.
- **Island:** coastline or open water meeting land — a shoreline, a lake ringed by mountains, or a strait — with water's reflectivity doing most of the compositional work. Cool, overcast or crisp daylight is typical; ice, mist, or fog is a common and welcome complication, not a deviation.
- **Swamp:** dense, wet, half-submerged vegetation — mangrove-like canopy, standing water threaded through roots and lily pads, murky depth rather than open sky. Diffuse, filtered light (jungle canopy, low fog) rather than a hard sun; the wetness and closeness of the growth is the defining feature, whether the specific take skews toward rot-and-murk or toward lush overgrowth.
- **Mountain:** vertical rock — canyon walls, spires, or a peak — with a hard, high-contrast sky-vs-stone read. Strong directional daylight (a shaft of sun cutting between rock walls) is the default; red-orange stone tones do most of the palette work even under a blue sky.
- **Forest:** wooded interior rather than a distant tree-line — mossy trunks, a fallen log, filtered canopy light reaching a stream or clearing floor. Diegetic light is almost always broken/dappled (sun through leaves) rather than a single visible source; the "clearing" is often a small bright pocket surrounded by darker wood, which does the Rule 5 framing job naturally.

**Worked examples (one per basic):**
1. *(Plains.)* A wind-flattened sea of tall grass rolls toward a low horizon where a molten-gold sun sits half-risen between two distant standing rock spires, the light source's warm falloff crisping the nearest grass blades and rocks while the horizon itself dissolves into pale haze — no figure, the openness itself is the subject.
2. *(Island.)* A frozen alpine lake meets a rocky far shore lined with dark conifers, snow-capped peaks receding into cool blue-white mist behind them, the ice's own crack-lines catching the flat overcast sky's light and throwing faint blue-green glow up through the surface — the water's reflectivity is the frame's brightest, most detailed element, per Rule 5, with the peaks fading into haze above.
3. *(Swamp.)* A canopy of broad, dark-veined leaves arches low over black standing water dense with lily pads, a lone dark shape (a small winged creature, distant and incidental) perched on an overhanging branch, filtered greenish light seeping down through the canopy gap directly above the water's calmest patch — the light source is the canopy break itself, and everything outside that pocket recedes into damp shadow.
4. *(Mountain.)* A narrow canyon of sun-baked red-orange rock spires opens onto a hazy blue sky, a thin waterfall catching hard midday light on the canyon's near wall while a small distant figure (a lone traveler, silhouette only) stands dwarfed at the canyon floor far below — the scale gap between the tiny figure and the towering rock is the entire point.
5. *(Forest.)* A fallen, moss-crusted trunk arches low over a narrow stream, framing a small sunlit clearing beyond it where two indistinct pale shapes stand at the water's edge, dappled light breaking through the canopy overhead and scattering unevenly across the wet rock and dark water in the foreground — the bright clearing beyond the log is the framed focal point, with the nearer, darker wood doing the Rule 5 cropping work.

### Named-location non-basics (thin sample)

At this sample depth, plain non-legendary "named place" lands didn't surface in numbers — the non-basic query's price-sorted results skewed almost entirely to fetch lands (Mode 2) and legendary lands (Mode 3). Treat this sub-case as an extension of the basic-land principle above (a specific, distinct terrain type, minimal or absent figure, weather/light doing the mood work) rather than a separately-verified convention; no worked example is offered here to avoid presenting an invented case with false confidence.

---

## Mode 2 — Utility Land Close-Up

**When it applies:** non-basic lands with a specific mechanical gimmick tied to a specific physical feature — fetch lands, lands with a tap-ability tied to an object, lands that filter or fix mana through a visible mechanism.

**Decisive moment:** close in on the one physical feature the card's mechanic is actually about, rather than a wide shot of the land as a whole place. If the card searches your library for a land, stage the specific terrain feature that a search-and-fetch implies (a fork in a river, a canyon mouth splitting into two paths); if the card taps for a specific effect (colorless mana at a cost, sanctuary from a name-based effect), stage the object or threshold that effect visibly emanates from.

**Worked examples:**
1. *(Fetch land, based on Polluted Delta.)* A high-angle view looks down into a steep, moss-slicked ravine where a river forks hard around a cluster of water-worn boulders, one branch catching a thin shaft of grey daylight while the other recedes into darker channel below — the fork itself, not any wider landscape, fills the frame's focal band, exactly the kind of specific, searchable feature the card's fetch effect implies.
2. *(Tap-for-colorless-at-a-cost, based on Ancient Tomb.)* A ring of ancient carved stone pillars frames a shallow set of worn steps leading up to a dark, eye-shaped archway, hard directional light spilling from an unseen source beyond the arch and throwing the carved pillar-faces into deep relief — the archway itself is the "cost," a threshold clearly worth paying to pass through.
3. *(Creature-type sanctuary, based on Cavern of Souls.)* Deep inside a glowing crystal cave, a submerged stone ziggurat rises just above still, luminous violet-pink water, stalactite spires framing the ziggurat on both sides and their reflections doubling the structure in the water below — the cave's enclosed, protective geometry does the visual work of "a place nothing from outside can reach," matching the card's naming-protection effect.

---

## Mode 3 — Legendary Location Landmark Shot

**When it applies:** legendary lands — a land is capped at one copy per deck and is usually a named, singular place with outsized lore weight (a specific city, a named tree, a specific ruin). The shot treats the location the way a portrait treats a face: this is *the* place, rendered as an icon, not an example of a terrain type.

**Decisive moment:** frame the location at the scale and angle that makes it read as singular and recognizable at a glance — usually a straight-on or slightly-low landmark composition, often symmetrical, with the location's single most distinctive structural feature (a tree fused into a skyline, a floating palace, a ring of standing stones around an altar) placed dead in Rule 5's focal band. Diegetic light is doing extra work here: it should mark the location as significant (a colored sky-glow, starlight, a single beam) without tipping into the banned "epic/majestic" adjectives from Rule 8 — let the framing and the light's physical logic carry that weight instead of naming it.

**Worked examples:**
1. *(Green, based on Boseiju, Who Endures.)* A massive, ancient pine tree rises alone above a skyline of tall, narrow city towers, its gnarled roots draping down between the towers like a canopy the city was built to grow around rather than through, cool blue-violet storm light silhouetting both the tree's canopy and the towers beneath a churning night sky — the single tree dominating an entire skyline is the whole point, no figure needed.
2. *(Blue, based on Otawara, Soaring City.)* A tiered palace of white stone and gold trim floats among thick banked clouds, smaller structures and archways visible drifting at different heights around it, soft daylight diffusing evenly through the surrounding cloud bank so the palace's own white stone is the brightest element in frame — the floating, tiered structure reads as a single coherent city rather than a random cluster of buildings.
3. *(Multicolor, based on Nykthos, Shrine to Nyx.)* A ring of weathered stone columns, capped by two flanking horned statues, opens onto a shallow altar bowl glowing with soft golden light, a dense field of stars and nebula-light filling the sky directly above the altar as the composition's clear vertical axis — the altar's light and the star-field above it are aligned on the same central line, marking this as a place where sky and ground are meant to be read together.

Blue, black, and red legendary lands (Eye of Ugin, Urborg, Tomb of Yawgmoth) were also present in this sample but skewed toward the "world-altering enchantment" register of a wide, empty, lit threshold or ruin rather than a distinct new convention — Eye of Ugin's carved eye-shaped archway and Urborg's storm-lit black spires both fit the landmark-shot description above without needing a separate per-color write-up at this depth.
