# Theme Bible — Building `/themes/<theme>.md`

This skill governs how to build a theme bible: the one document that turns "reskin this deck as [theme]" from a vague instruction into a set of concrete, checkable answers every other skill in this environment can draw from. `art-template/SKILL.md` and its type-specific children tell you *how* to art-direct a card once you know what it depicts; `naming/SKILL.md` tells you how a name must behave once you know what vocabulary it's drawn from. Neither of those skills can do their job on a new theme without a theme bible to draw the *what* and the *vocabulary* from. This skill is what produces that bible — once, per theme, before any card in that theme is ever reskinned.

This skill is deliberately about *process*, not about any specific theme's content. It must work for a clean, well-mapped franchise setting (Lord of the Rings), a setting with no inherent MTG-style five-faction color split (Greek myth, a cyberpunk city, a single film), and even an abstract or non-narrative theme (a mood, a scientific field, a color itself). Where the sections below use Lord of the Rings as a worked example, that example illustrates the *shape* of a good answer — it is not the only valid shape, and a theme that resists that shape should not be forced into it. Section 7 below exists specifically for themes where the clean shape doesn't apply.

**This is not a fully silent one-shot generation.** Building a new theme bible is an interactive, reviewed step. Draft each section, then check it with the person requesting the reskin before treating it as final — every downstream card in every future deck reskinned under this theme inherits whatever this document gets wrong. A bad color→faction map or a thin naming vocabulary doesn't surface as an obvious error later; it surfaces as every card in the deck quietly feeling generic, which is exactly the failure mode this whole environment exists to kill. Treat a first draft as a proposal to be corrected, not a deliverable to be shipped.

## Where the bible fits in the pipeline

The orchestrator (built in a later task) loads `/themes/<theme>.md` once per deck run, in the pipeline step right after decklist enrichment and before the deck lore doc is built. The deck lore doc then does per-deck work that this document does not do: it clusters this specific decklist's cards into faction candidates by subtype density and color identity, and asks this bible for that faction candidate's seed material via the subtype-translation table (Section 3) and the color→faction map (Section 1). The theme bible is theme-wide and reusable across every deck reskinned into that theme; the deck lore doc is deck-specific and rebuilt every run. Do not let deck-specific detail leak into the theme bible (a specific commander's story does not belong here), and do not let this bible try to pre-decide a specific deck's faction clustering (a deck might only surface three of five mapped factions, or split one mapped faction into two if two different subtype clusters both belong to it).

## Required sections

Every `/themes/<theme>.md` must contain the following sections, in this order. Each one is described below with what it must contain and why the downstream skills need it in that shape.

### 1. Color → faction/region map

One line per color, plus one line for multicolor and one for colorless — seven entries total (White, Blue, Black, Red, Green, Multicolor, Colorless). Each line names the in-world faction, people, or region that color identity maps to in this theme, and one clause on why that mapping fits the color's own philosophical register (protection/order for white, knowledge/manipulation for blue, and so on) rather than an arbitrary assignment.

**Worked example (Lord of the Rings):**
- **White** — Gondor and the Reunited Kingdom: order, stewardship, and the long defense of a failing line.
- **Blue** — the Elves of Rivendell and Lothlórien: memory, foresight, and a fading, world-weary mastery.
- **Black** — Mordor and Sauron's forces: domination through corruption and the will to power at any cost.
- **Red** — the Rohirrim: impulsive courage, cavalry aggression, oaths kept at cost.
- **Green** — the Fellowship's wilder allies (Ents, the Woodland Realm, the Shire): growth, endurance, and a reluctance to act until pushed.
- **Multicolor** — alliances and divided loyalties that cross faction lines (Aragorn's Gondor-and-Rangers claim, Gandalf's cross-faction meddling).
- **Colorless** — the Rings of Power and artifacts of unclear allegiance (the One Ring, palantíri): objects whose danger lies precisely in not belonging to any one faction's values.

Multicolor does not need its own new faction per gold pair — it can be handled as "which two mapped factions are in tension or alliance here," resolved per deck by the deck lore doc rather than pre-enumerated for every possible color pair in the bible itself.

### 2. Card type → motif map

One entry per major card type, stating what that type *represents* in this theme's internal logic, not just a restated dictionary definition. This is what keeps, say, every artifact in a themed deck from being an arbitrary "cool object" and instead being legible as one class of thing within the setting.

**Worked example (Lord of the Rings):**
- **Artifacts** → forged relics and made objects: rings, blades passed down through lineages, palantíri, devices whose danger or power is a function of who wields them.
- **Enchantments** → oaths, wards, and curses laid on people or places: a geas, a blessing over a ford, Saruman's corrupting influence over Théoden.
- **Sagas** → a chapter of the setting's own established chronology, told as a vignette (a saga card is a natural fit for "The Council of Elrond" or "The Scouring of the Shire" read as a three-beat story).
- **Lands** → named locations drawn from the setting's actual geography — never a generic "Forest" or "Plains," always a specific place (Fangorn, the Pelennor Fields, the Argonath).
- **Instants/Sorceries** → a single decisive act performed by a person or force, not an ambient magic system — the theme should supply a specific actor and a specific deed for each spell's effect (see `naming/SKILL.md` Rule 2 on deriving from role).
- **Creatures** → see Section 3, the subtype translation table.
- **Planeswalkers** → named, recurring, larger-than-life figures central to the setting's own mythology (Gandalf, Galadriel, Sauron) — themes without an obvious pantheon of named super-figures should read this type's guidance in Section 7.

A theme without a clean equivalent for one of these types (e.g. a theme with no real concept of "curse" for enchantments) should say so explicitly and give the nearest working substitute, rather than leaving the entry vague — see Section 7 for themes where entire type categories need a non-obvious translation.

### 3. Subtype translation table

This is the section the deck lore doc leans on hardest, because `creature/SKILL.md`'s subtype conventions are keyed to real MTG subtypes, and a themed deck's creatures will be sampled against those exact subtypes. For every subtype that could plausibly appear in a sampled deck, state how that subtype's role, this theme's own equivalent, and — critically — **which of that subtype's signature visual features (per `creature/SKILL.md`'s Part 2) survive the translation**. The translation changes the surface identity, not the visual anchor the corpus work already validated; an Angel translated into this theme must still cash out as something with `creature/SKILL.md`'s Angel signature features (paired wings, a halo-adjacent light, bilateral symmetry) wearing this theme's specific dress, not a wingless figure that merely does angel-shaped things in the plot.

The 34 subtypes `creature/SKILL.md` documents, which this table must cover (skip only a subtype with no plausible occurrence in any deck under this theme, and say so):

Angel, Demon, Devil, Vampire, Zombie, Skeleton, Spirit, Horror, Eldrazi, Phyrexian, Dragon, Sphinx, Hydra, Elemental, Beast, Dinosaur, Elf, Goblin, Merfolk, Faerie, Giant, Dwarf, Human — Knight, Human — Soldier, Human — Cleric, Human — Wizard, Human — Rogue, Human — Warrior, Human — Shaman, Human — Noble, Human — Assassin, Construct, Golem, Insect.

**Worked example (Lord of the Rings, three entries):**
- **Angel → Maiar/Valar in physical, winged manifestation** (e.g. a Balrog-adjacent fallen Maia, or an unfallen messenger spirit): keep the paired wings and halo-adjacent light exactly as `creature/SKILL.md` specifies; reskin the armor/material to Middle-earth's forged-metal-and-cloth register rather than a generic celestial one.
- **Elf → the Elves of Middle-earth directly** (a rare one-to-one translation — see Section 7's note on themes with a literal source match): keep every signature feature (tapering ears, living plant material worked into garments, a woodland-crown accessory) unchanged, since the subtype's corpus convention and the theme's own source material already agree.
- **Dwarf → the Dwarves of Middle-earth directly**: same one-to-one case as Elf — no translation work needed beyond confirming the corpus's braided-beard-with-metal-clasps convention matches Tolkien's dwarves (it does).
- **Zombie → the Barrow-wights or the Dead of Dunharrow**: keep the localized-rot/graveyard-prop signature features, translate the setting-specific prop cluster from a modern graveyard to a barrow-mound or a mountain oath-hall.
- **Construct → the constructed servants of Isengard or Mordor's forges (orc-forges, siege engines given rough sentience)**: keep the exposed-jointed-segmentation and engraved-metalwork signature features, translate the "civilization that crafted it" detail to Isengard's or Mordor's specific industrial register.

A theme where a subtype has no plausible narrative equivalent at all (say, a hard science-fiction theme with no supernatural register for "Spirit") should say so and specify the fallback: either fold it into the nearest neighbor subtype's translation (Spirit → a data-ghost/echo construct, borrowing the Construct entry's translation with the Spirit corpus section's soft-edged dissolving quality layered on top) or state plainly that this subtype is expected not to occur in decks under this theme and give the builder permission to flag it for a one-off translation if it ever does.

### 4. Naming vocabulary

This section is what `naming/SKILL.md` Rule 1 means by "drawn from the theme's own vocabulary" — it must give the naming step enough real material to work from, not just a one-line description of the theme's "feel."

Cover, at minimum:
- **Language flavor**: what real or invented language(s) the theme's names are built from, and what register they carry (formal/archaic, clipped/technical, ornate/ceremonial, etc.).
- **Naming patterns**: the theme's own conventions for how people, places, and things are actually named in the source material — patronymics, epithets tied to a deed or place, title-plus-name constructions, compound descriptive names, and so on.
- **Roots and recurring elements**: specific prefixes, suffixes, or recurring word-parts a name-builder can draw on so that generated names feel native rather than freely invented on the spot.
- **Per-faction register, if factions have distinct naming voices**: this is what feeds `naming/SKILL.md` Rule 5 (faction consistency) — if two factions in this theme should sound different from each other (as Rohan and Lothlórien do), say so here explicitly and give 2-3 example names per faction's register, so a later batch call has ground truth to check a new name against instead of inventing a register on the fly.

**Worked example (Lord of the Rings, abbreviated):** Rohirric names draw on Old English phonology (Éomund, Théoden, Éowyn) and favor patronymics and epithets tied to horses, plains, and oaths ("Rider of the Mark"). Elvish names draw on Tolkien's Sindarin/Quenya roots (soft consonant clusters, vowel-heavy endings — Galadriel, Legolas, Lothlórien) and favor titles tied to realms, ages, or light ("Light of Lothlórien"). Dwarvish names are short, hard-consonant, often with a title-of-craft or hall-name attached (Dáin of the Ancient Halls). A name-builder checking a new Rohirric name against this section's 2-3 examples is doing exactly the cross-check `naming/SKILL.md` Rule 5 asks for.

A theme with no obvious linguistic register of its own (an abstract concept theme, a single-word mood) still needs this section — invent a plausible naming logic for it (e.g. a theme built around "entropy" might name things via degradation-of-an-original-word patterns) rather than leaving naming ungrounded. See Section 7.

### 5. Deck anchor guidance

This section feeds the deck lore doc step (built by the orchestrator) that auto-detects factions per deck and needs to know how to read a specific commander as the "central" faction. State the rule generically here, since it applies the same way to every deck built under this theme: **the commander's own color identity and subtypes point to which of this bible's mapped factions is the deck's anchor**, and every other detected faction in that specific deck should be described, in the deck lore doc, in terms of its relationship *to* the anchor (serves it, opposes it, is bound to it by an old oath, exists independent of it and only incidentally shares a color, etc.) rather than as a free-floating faction with no stated relationship to the commander at all.

Where useful, note any theme-specific wrinkles this rule needs to handle — e.g., a commander whose color identity spans a mapped alliance rather than a single faction (Section 1's multicolor entry) anchors the deck on that alliance itself, not on an arbitrary pick of one of its component colors. Do not try to pre-resolve specific commanders here; that per-deck resolution is the deck lore doc's job, not this bible's.

### 6. Inter-faction relations default

The design spec flags this as a deliberately deferred decision that each new theme bible must make explicitly rather than leave implicit: **default to theme-canon-first** relations between factions. Where the real setting has an established answer for how two factions relate (Gondor and Rohan are sworn allies; Mordor and everyone else is adversarial; the Elves are withdrawing from Middle-earth's affairs rather than actively opposing anyone), use that established answer rather than inventing a new relationship from scratch. Only invent a relationship where the theme's own canon is genuinely silent (e.g. Middle-earth's canon has little to say about how the Ents specifically relate to the Dwarves, since the two barely interact in the source material — a theme bible is free to invent a plausible relationship there).

**This choice must be flagged explicitly in the bible itself**, not left as an unstated assumption — add a short subsection stating which inter-faction relationships in Section 1's map are theme-canon (with a one-clause citation of what in the source material establishes it) and which are invented because canon was silent. This gives a later reviewer, or a later deck's lore doc, a way to tell the difference between "this is Tolkien's own lore" and "this is something this bible's builder made up to fill a gap" — the two should never be presented with equal authority.

## 7. When the theme has no natural faction split

Lord of the Rings has an unusually clean shape for this process: five colors map to five distinguishable factions with little forcing. **Most themes will not be this clean, and this process must not silently assume they will be.** A theme without five natural factions — a single movie with one protagonist faction and one antagonist faction, an abstract concept with no factions at all, a real historical period with dozens of overlapping powers — is still buildable under this skill, using the following adjustments:

- **Fewer than five factions:** it is fine for two or three of Section 1's seven color/multicolor/colorless entries to point at the *same* faction, distinguished by a different facet of that faction rather than a different group entirely (e.g. a single-antagonist movie theme might map both Black and Red to "the antagonist's forces," with Black covering their manipulative/corrupting agents and Red covering their frontline enforcers — same faction, two registers). State this explicitly in Section 1 rather than inventing a fifth faction that doesn't exist in the source material just to fill the grid.
- **More than five natural factions:** pick the five (or fewer) most load-bearing to the theme's own core conflict for the primary color map, and note the remainder as sub-factions nested under one of the five, available for a deck lore doc to surface as a finer-grained faction candidate if a specific deck's subtype density calls for it.
- **No factions at all (an abstract or conceptual theme):** Section 1 still needs seven entries, but they can map to *facets, phases, or aspects* of the concept instead of political factions — a theme built around "the four seasons plus decay and renewal" could map colors to seasonal registers rather than groups of people. The rest of this skill's sections still apply: Section 2 still needs a card-type→motif map, Section 3 still needs subtype translations (creatures under an abstract theme might all translate to personifications of the concept's facets), and Section 4 still needs a naming vocabulary — an abstract theme needs vocabulary grounding *more*, not less, since there's no existing character/place vocabulary to lean on by default.
- **A theme with a genuinely one-to-one match to an existing subtype** (Section 3's Elf/Dwarf note above): don't force a translation that doesn't need to happen. If the theme's own material already is a fantasy setting with elves in it, the "translation" is simply confirming the corpus convention holds, not inventing new signature features to replace ones that already fit.

In every case, the goal is the same: give every downstream skill (naming, deck-lore clustering, per-type art direction) a concrete, specific answer to draw from, sized to what the theme actually supports — never a generic placeholder invented to satisfy this document's shape at the expense of the theme's real content. If a theme genuinely resists a section (e.g. no plausible enchantment-as-curse concept exists anywhere in it), say that plainly and give the nearest working substitute rather than leaving the section thin or silently identical to another theme's answer.
