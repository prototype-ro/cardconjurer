> Built on skills/art-template/SKILL.md.

This file adds instant-specific art direction on top of the shared rules in `art-template/SKILL.md` (diegetic lighting, palette discipline, intricacy, framing, banned words, closing suffix, etc. — all apply unmodified). It does not repeat those rules.

Instants and sorceries have no meaningful subtypes to organize by (unlike creatures), so this file organizes by **role** instead — what the card actually does at the table. Each role gets: the decisive-moment convention specific to that role, a per-color note on how the role's staging shifts with color identity, and 2-3 worked examples.

This is a **reduced-depth sample**, per the design spec's cost trade-off for non-creature types: one Scryfall pass per color (`t:instant c:<color> year>=2010 -is:digital -is:promo -st:funny`, `order=usd&dir=desc`), roughly 15-20 unique cards read per color rather than the full multi-pass corpus used for creatures, plus a handful of targeted oracle-text queries to fill gaps a plain price-sort didn't surface (e.g. `o:"damage to any target"` for red burn). A representative subset of resulting art was actually viewed in full (roughly 14 images across both instant and sorcery combined) rather than every card in every cell — sufficient at this depth to ground the conventions below, not an exhaustive per-role-per-color grid. No separate corpus-notes.md file was produced at this depth, per the plan.

**Universes Beyond exclusions caught mid-sampling:** Legolas's Quick Reflexes, Galadriel's Dismissal, Olórin's Searing Light (all Lord of the Rings, set `ltc`); And They Shall Know No Fear, Blood for the Blood God! (Warhammer 40K, set `40k`); Vivi's Persistence (Final Fantasy, set `fic`); Everybody Lives!, Nanogene Conversion, Ensnared by the Mara (Doctor Who, set `who`); Spirit Water Revival, Water Whip, Avatar's Wrath (Avatar: The Last Airbender, sets `tla`/`tle`). Note that set code alone isn't a reliable signal — `tle` ("Avatar: The Last Airbender Eternal") is a Universes Beyond *reprint* set that also carries plenty of legitimate original-Magic reprints (Enlightened Tutor, Worldly Tutor, Eladamri's Call all appear there and are fine to use); the actual card name and mechanic is what determines a crossover, not the product it was reprinted into.

**Not every role spans every color evenly**, and this file doesn't force it. Counterspell is overwhelmingly blue (with rare red/white splashes that answer it rather than cast it) — sampled almost entirely from blue. Ramp and reanimation are both genuinely rare at instant speed across all colors; where the sample turned up only one or two legitimate cards for a cell, that's stated rather than padded out.

## Contents

**Roles:** [Removal](#removal) · [Counterspell](#counterspell) · [Board Wipe](#board-wipe) · [Card Draw](#card-draw) · [Ramp](#ramp) · [Tutor](#tutor) · [Pump / Protection](#pump--protection) · [Reanimation](#reanimation) · [Burn](#burn)

---

## Removal

**Decisive moment:** the exact instant the threat stops existing or stops mattering — not the creature menacing beforehand, not an empty battlefield afterward. Exile removal should show the subject actively dissolving, unmaking, or being pulled out of the world *as it happens*; destroy/bounce removal should show the moment of impact or displacement, weapon or effect still touching the target.

**Per-color notes:**
- **White** (exile-as-judgment): the removal effect reads as verdict, not violence — a holy light, a field of consecrated weapons, or a banishing glyph doing the work with no visible struggle from the target. Cool white/gold light against a darker, receding threat.
- **Black** (exile/destroy-as-cost): removal here often costs the caster something (life, sacrifice) — stage a visible price alongside the effect (a hand losing color, a ritual mark) rather than a clean, free banishing. Sickly green or rust-red glow against black.
- **Green** (destroy target artifact/enchantment, rarer at instant speed): the destruction reads as overgrowth or explosive natural force breaking something unnatural — roots cracking metal, a chord-summoned burst tearing through a rigid structure. Moss-green and splintering brown against the broken material's own color.
- **Blue** (bounce, tempo removal rather than permanent answer): the target is caught mid-flight and yanked backward through space, not destroyed — a visible rip or fold in the air is the tell that this is displacement, not death.

**Worked examples:**
1. *(White, based on Swords to Plowshares.)* A ring of swords angled inward around a captured creature transfigures mid-shot, blades already softening into curved plowshare edges at the tip, a pale butterfly-shaped glow blooming at the point where the transformation completes, grass and hill fading to soft haze beyond the ring.
2. *(Black, based on Deadly Rollick.)* A gauntleted hand closes around a struggling figure's throat as the figure's lower body has already gone translucent and is peeling away into black smoke, the caster's own knuckles cracking with a hairline red glow — the cost made visible on the caster's own hand.
3. *(Green, based on Force of Vigor.)* A cracked stone construct's chestplate is mid-shatter, roots erupting explosively from within the crack and forcing the metal apart from the inside, moss-green light spilling from the widening fracture.

---

## Counterspell

**Decisive moment:** the targeted spell caught and unraveled *mid-flight*, on the way to its target — never a spell that has already resolved, and never a static magical duel with no travelling projectile. The countered spell should have a distinct color/texture of its own (per art-template Rule 2) that visibly comes apart or reverses direction under the counter's separate light.

**Per-color notes:** almost exclusively blue in this sample — counterspell is one of the roles that doesn't spread across the wheel; red and white occasionally *answer* a counter-adjacent effect but rarely counter outright, so this section stays blue-only rather than force other colors into it. Blue counterspell staging: cool indigo/teal caster's-own magic (per art-template's Blue color conventions in `creature/SKILL.md`, which apply to any blue caster regardless of card type) meeting the incoming spell's unrelated color, the two kept visually distinct exactly per art-template Rule 2 — the counter should never just be "more blue," it should be a different-colored intrusion cancelling a different-colored spell.

**Worked examples:**
1. *(Based on Counterspell.)* A hooded caster's raised palm catches an incoming white-hot bolt inches from impact, cyan-white counter-light spider-webbing outward from the point of contact and visibly overpowering the bolt's own warmer glow, the bolt's leading edge already flickering out.
2. *(Based on Force of Will.)* A caster exiles a card from their own hand in the same motion as raising a hand toward an incoming spell, the sacrificed card's pages disintegrating into pale motes that get pulled into the counter's cyan wall, the original spell's color guttering out against it.
3. *(Based on Mana Drain.)* A counter-glyph closes around an incoming spell like a fist, faint teal light draining backward from the collapsing spell into the caster's own open hand — describe as a slower, "of course" containment rather than the desperate/frantic energy of examples 1-2, since this counter transfers power rather than just erasing it.

---

## Board Wipe

**Decisive moment:** genuinely rare at instant speed — most true "destroy/exile all" board wipes are sorceries (see the Sorcery skill's Board Wipe section for the primary treatment). At instant speed the closest analog is a mass-bounce or mass-displacement effect. The convention: the wave of the effect crossing the *entire visible battlefield/skyline* in one continuous motion, not a localized blast — scale is what separates this from Removal.

**Per-color note:** sampled only from blue in this pass (Cyclonic Rift, overloaded). Treat as a single-color starting hypothesis for the instant-speed version of this role rather than a full per-color convention — a true multi-color board-wipe treatment belongs in the Sorcery file.

**Worked examples:**
1. *(Based on Cyclonic Rift, overloaded.)* A colossal dark maroon storm-funnel tears across an entire city skyline at once, lightning forking down into spires on both the near and far horizon simultaneously, structures and loose debris already lifting into the funnel's leading edge — the scale reads as "everything on the board," not one target.

---

## Card Draw

**Decisive moment:** the moment of taking in more than was there before — a hand closing on cards that weren't in it a beat ago, an eye or mind's-eye opening onto revealed information. Avoid a static "person reading a book" pose; there should be a visible instant of acquisition, not idle study.

**Per-color notes:**
- **Blue** (card draw as pure information/insight): a spell effect visibly pulling cards or knowledge toward the caster, light sourced from the drawn material itself.
- **Black** (card draw with a cost — sacrifice, life, discard): stage the cost and the gain in the same frame, per Removal's black convention above — a sacrificed creature's essence visibly flowing into the cards being drawn.

**Worked examples:**
1. *(Blue, based on Wheel and Deal.)* A caster's hand fans open as seven cards simultaneously slide into it from a spinning cyan vortex hovering at chest height, the vortex's far edge still visibly drawing in loose motes of light.
2. *(Black, based on Village Rites.)* A sacrificed creature's body is mid-dissolve into black-red smoke at a stone altar, the smoke visibly redirecting upward and condensing into two card-shaped motes of pale light near the caster's waiting hand.

---

## Ramp

**Decisive moment:** genuinely rare at instant speed — ramp is overwhelmingly a sorcery-speed effect (see the Sorcery skill's Ramp section for the primary treatment, with land-out-of-the-ground staging). The one common instant-speed analog is a mana ritual (a burst of mana rather than a permanent land). The decisive moment there: the burst of raw mana being torn free in a single instant, not a land calmly entering play.

**Per-color note:** sampled from black only (Dark Ritual) — this is a black-specific effect at instant speed; other colors' ramp is sorcery-speed and belongs in that file.

**Worked examples:**
1. *(Based on Dark Ritual.)* A processional line of hooded figures climbs stone steps toward a twin-horned brazier at the top, both horns erupting into a single shared column of violet-black flame at the exact moment the ritual completes, the flame's light throwing the entire staircase into stark silhouette.

---

## Tutor

**Decisive moment:** the search rendered as *reaching into* something — a library represented not as a bookshelf but as a physical space (a void, a graveyard, a crowd) the caster's hand or gaze plunges into, with the found card's location marked by a distinct glow or shape the moment before it's grasped. Never depict a card popping cleanly out of thin air with no visible reaching motion.

**Per-color notes:**
- **Black** (tutoring as a bargain with death/darkness): the thing being reached toward is skeletal, infernal, or otherwise mortal-cost-coded — a skull, a horned figure looming above.
- **Blue** (tutoring as a precise mental search): a shelf/current of glowing runic cards the caster's fingers sort through with visible selectivity, cooler and more clinical than black's version.
- **Green** (tutoring as calling out to nature/kin): the found card answers a summons rather than being physically grasped — a creature already stepping forward from tall grass or a tree line toward the caster.
- **White** (tutoring as invoking sanctioned lore): a specific tome or relic-shelf lit by a single beam, the found item the only thing in focus.

**Worked examples:**
1. *(Black, based on Vampiric Tutor.)* A pale hand reaches up past a dagger-pierced skull toward something unseen above the frame, alchemical vessels bubbling with dim red light at the hand's elbow, the reach itself — not the found card — the visual subject.
2. *(Blue, based on Mystical Tutor.)* A caster's fingers trail through a vertical current of faintly glowing rune-backed cards suspended in the air before them, one card already brightening distinctly from the others as it's about to be pulled free.
3. *(Green, based on Worldly Tutor.)* A caster's raised hand catches late daylight at a tree line's edge as a half-seen creature shape already steps forward out of the shadowed brush toward the summons, the rest of the grove staying dark and unresolved.

---

## Pump / Protection

**Decisive moment:** the instant the buff takes hold — visible surging musculature, a hardening shell, or a ward snapping into place around the subject an eyeblink before an incoming blow would have landed. The "before" state (the vulnerability) should be legible in the same frame as the "after" (the ward/growth), not shown as a separate panel.

**Per-color notes:**
- **Green** (raw physical growth): the growth itself is the spectacle — visibly swelling muscle, a jaw stretching wider than it should, bark-like growths hardening in real time across skin. This sample skewed grotesque/monstrous rather than heroic — a Giant Growth-style pump reads as feral overgrowth, not a clean power-up glow.
- **White** (protective ward): a barrier or hexproof/indestructible effect renders as a hard-edged, geometric light-shell forming around the subject, distinct in texture from green's organic growth per the two-effects-distinct principle if both appear in the same deck.

**Worked examples:**
1. *(Green, based on Giant Growth.)* A creature's jaw and forelimb are mid-swell, muscle visibly bulging past its own skin's normal limits in the same instant, eyes flaring yellow-hot as the surge peaks — grotesque and overwhelming rather than a clean glow-up.
2. *(White, based on Flawless Maneuver.)* A line of soldiers braces as a hard-edged translucent shell snaps into place around them a fraction of a second before a falling weapon connects, the weapon already deflecting off the shell's outer face with a bright spark at the point of contact.
3. *(Green, based on Heroic Intervention.)* A tree-bound guardian's bark visibly thickens and closes over an open wound in real time as an axe blade, already swinging, is caught mid-strike against the newly hardened surface.

---

## Reanimation

**Decisive moment:** genuinely rare at instant speed — most reanimation effects are sorceries (see the Sorcery skill's Reanimation section for the primary, wider-sampled treatment). The one legitimate instant-speed example found (Goryo's Vengeance) stages reanimation as a *haunting* rather than a triumphant return: the returned creature is translucent, still half-caught between graveyard and battlefield, rather than a solid body standing fully restored.

**Per-color note:** sampled from black only, and from a single card — treat as a starting hypothesis, not a settled convention.

**Worked examples:**
1. *(Based on Goryo's Vengeance.)* A translucent, ghost-pale figure rises through a haze of reeds at dusk, hair and sleeve-edges dissolving into mist rather than holding a hard outline, fangs bared but the whole form still visibly semi-transparent — reanimated, but not yet fully "arrived."

---

## Burn

**Decisive moment:** the projectile or bolt of damage *in transit*, already loosed and mid-flight toward its target, or at the exact moment of impact — never a caster merely charging up an attack that hasn't left their hand yet.

**Per-color note:** red only — burn is red's signature role and doesn't meaningfully appear in other colors at instant speed. Two registers showed up in the sample: a raw elemental bolt (fire/lightning, loosed from an empty hand or a simple mechanical housing) and a caster whose own body is the visible conduit (a chest-mounted core, a cracked-open ribcage) for a larger, more dangerous burst — reserve the second register for the deck's bigger burn spells (X damage, board-scale), and the first for small direct-damage bolts.

**Worked examples:**
1. *(Small bolt, based on Galvanic Blast.)* A robed figure's outstretched arm ends in a simple metal housing mid-discharge, a crisp white-cyan bolt already several feet clear of the housing and crossing warm ochre haze toward an unseen target, the housing's edge still sparking from the initial release.
2. *(Small bolt, based on Gut Shot.)* A single narrow line of red-white energy crosses a dim alley at head height, its point of origin already dark and spent, the target-end still crisp and bright — the bolt caught partway through its flight rather than at either end.
3. *(Larger/board-scale burn, contrast case.)* A figure's own chest has cracked open along a jagged seam, molten light pouring out as the visible source of the spell's damage rather than a hand-cast bolt — reserve this register for X-damage or multi-target burn where the scale of the spell should read as costing the caster something physically, not a clean ranged attack.
