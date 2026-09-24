# User Prompt Corpus — Source of Truth for `art-template/SKILL.md`

This file is the raw material behind the shared rules in `mtg-reskin/skills/art-template/SKILL.md`. The 10 numbered rules in that file were derived by observing patterns across these prompts, not invented in the abstract — when a rule and a real prompt seem to disagree, treat the corpus as ground truth and revisit the rule.

Note on count: the implementation plan estimated 24 prompts before the exact set was finalized. Only 21 distinct prompt submissions actually exist in the source conversation this corpus was drawn from — prompts 18 and 19 below are word-for-word duplicates of each other, and there is no separate 22nd–24th prompt. Both copies of the duplicate are kept here as legitimate corpus entries (see note on prompt 19) rather than deduplicated, since the repetition itself is informative about how the character-bible pattern was used in practice.

Each prompt below is numbered in original order and followed by a **Demonstrates:** line naming the specific art-template rule(s) it best illustrates, with a concrete detail quoted from that prompt.

## Index by rule

Use this table to jump straight to examples of a given rule instead of scanning all 21 entries.

| Rule | Best-demonstrating entries |
|---|---|
| 1. Who/What/Why/Where brief | 7, 11, 13 |
| 2. Diegetic lighting | 2, 5, 8, 10, 12, 14, 17, 20 |
| 3. Intricacy | 1, 16 |
| 4. Palette discipline | 1, 16 |
| 5. Framing for card crop | 3, 6, 9, 18, 21 |
| 6. Framing tightness | 4, 15, 21 |
| 7. Body-part continuity gotcha | 16 |
| 8. Banned words | — (no entry below is annotated as the primary example; all 21 prompts comply) |
| 9. Closing suffix | — (structural — see the closing sentence of every entry rather than a single standout example) |
| 10. No text, frames, or artist names | — (structural — every entry complies; no single entry stands out as the clearest example) |
| Character-bible reuse pattern (not a numbered art-template rule; flagged for future naming/theme-bible skills) | 15, 16, 17 (exception), 18, 19 |

---

**1.** "The Gilded Chalice - a devil's gift. Half figure Baroque oil painting portrait: an aged, weary aristocrat in heavy embroidered robes and fur trimmed mantle, seated in a carved high backed chair, lifting an ornate gold chalice toward his lips with one ring laden hand, head tilted down so eyes are shadowed beneath a heavy brow, other hand resting loosely on the armrest. The chalice catches warm candlelight on its near side where liquid gleams like red wine; the far inner rim sits in shadow where it reads as black ichor. The chalice bowl bears an engraved frieze of tiny relief figures circling hand to hand as if pulled under. Face and crown occupy the upper vertical center; chalice and raised hand are the focal midpoint; robes fade into shadow in the lower third. Rich warm chiaroscuro from a single unseen candle. Deep reds, aged gold, near black shadows. Heavy textured brushwork. Magic: The Gathering artifact card art style. Intricate, atmospheric, high detail."

**Demonstrates:** Rule 3 (Intricacy) — "an engraved frieze of tiny relief figures circling hand to hand as if pulled under" is a specific, nameable engraved micro-narrative, not a generic "ornate" adjective. Also demonstrates Rule 4 (Palette discipline): "Deep reds, aged gold, near black shadows" is a named 2–3 color list, nearly identical to the exact example phrasing used in the rule itself.

---

**2.** "Extreme close up on a weathered parchment scroll on a dark table. An elegant quill rests mid stroke where an unfinished signature trails off. A pale human hand holds the parchment's edge; a clawed, dark red black hand enters from the opposite side, pressing an ornate signet into glowing wax beside the signature. The wax seal glows hellish red orange — the sole light source — casting warm red gold highlights across both hands and parchment while the background dissolves into near black. A wisp of pale smoke curls from the wax. No faces, no room, nothing else in frame. Wax seal just off center; quill tip clear of the top edge; hands taper into shadow at the bottom. Palette: black, aged parchment gold, hellish red only. Painterly chiaroscuro illustration, Magic: The Gathering artifact card art style. Intimate, ominous, high detail."

**Demonstrates:** Rule 2 (Diegetic lighting) — the wax seal is named explicitly as "the sole light source," with explicit falloff stated: highlights on hands and parchment near it, "background dissolves into near black" further away.

---

**3.** "A hooded devil like figure in a dark tattered cloak, small horns beneath the hood, crouched still over a fallen white pegasus in the underbrush, wings limp. Scene rendered in silhouette and deep shadow — no blood or wounds, only stillness and violation. A mossy log arches across the upper frame; tall dark trunks recede into blue grey mist. Faint cold blue moonlight barely illuminates the pale pegasus and cloak's edge; everything else dissolves into near total darkness. Deep blue and near black desaturated palette. Hooded figure and pegasus centered mid frame; misty forest floor tapers into darkness at the bottom. Composition keeps the log and treetops clear of the top edge, leaving expendable space at bottom for card title and text box. Painterly digital fantasy illustration, Magic: The Gathering card art style, atmospheric and restrained, high detail."

**Demonstrates:** Rule 5 (Framing for card crop) — explicitly names the purpose of the empty space, "leaving expendable space at bottom for card title and text box," the direct precursor to the rule's canonical phrasing.

---

**4.** "Lord Xander, a bearded pale skinned noble wearing a crown of curved pale horn like spikes, a heavy white fur trimmed robe over dark formal clothing, standing in his dim private gallery. Both hands grip an ornate mounted sword upright before him - each hand has five clearly distinct, naturally separated fingers. Calm, possessive expression as he examines the blade. Setting: dark wood paneled gallery vault with framed portraits on easels, a golden winged statue at the edge, trophies and relics in glass cases receding into shadow. Cool, even ambient light catches soft highlights on fur trim and blade; face clearly lit with legible midtones; background fades to soft dark shadow. Composition: dark paneled walls visible at top, face and both hands centered, lower robe and floor tapering into shadow at bottom. Painterly digital fantasy illustration, Magic: The Gathering card art style, high detail."

**Demonstrates:** Rule 6 (Framing tightness) — the shot is close on face and hands but deliberately keeps "dark wood paneled gallery vault with framed portraits... trophies and relics in glass cases receding into shadow" legible in frame, the dim surrounding-environment pocket the rule requires rather than an edge-to-edge crop.

---

**5.** "A single horned demon at the center of a violent magical detonation, multiple translucent duplicate copies exploding outward in all directions, each mid formation at a different solidification stage from ghostly to nearly complete. Setting: a cracked ritual circle carved into dark stone with glowing arcane sigils, weathered cracked pillars at the scene's edges. A stark blue white arcane energy burst at center serves as the primary light source, casting sharp cold highlights on the demon's horns and chest; duplicates grow progressively dimmer and more translucent outward; the stone floor remains legible dark rather than pure black. Composition: exploding copies and energy burst clear the top edge, the demon's face and blast core centered in frame, the ritual circle tapering into shadow at the bottom. Painterly digital fantasy illustration, Magic: The Gathering card art style, high detail."

**Demonstrates:** Rule 2 (Diegetic lighting, falloff clause) — the burst is named as "the primary light source," and falloff is stated as a graduated effect: "duplicates grow progressively dimmer and more translucent outward."

---

**6.** "Besieged fortress city under a fire lit orange and purple sky, tall stone towers burning and breached along the skyline, small clawed winged daemons wheeling through smoke above the flames, a dense horde of daemons and armored cultists clashing at the base of the walls as a readable silhouetted mass, firelight from burning towers casting warm orange highlights on nearest combatants and long dramatic shadows across the battlefield, thick smoke rising into the sky, distant banners jutting from the horde, epic apocalyptic atmosphere. Composition: burning tower tops and thickest smoke clear of the top edge, breached wall and densest clash centered mid frame, foreground battlefield and fallen debris tapering into shadow near the bottom edge. Painterly digital fantasy illustration, Magic the Gathering card art style, chaotic frenzied atmosphere, high detail."

**Demonstrates:** Rule 5 (Framing for card crop) — states explicitly which zones are "clear of the top edge" (tower tops, smoke) versus which "taper into shadow near the bottom edge" (battlefield, debris), matching the rule's upper/lower expendable-space structure.

---

**7.** "A dark red black skinned demon with clawed hands stands over a fallen armored victim, one clawed hand extended in a showman's gesture toward the darkness, head tilted slightly down as if taking a bow. The fallen victim's armor catches dim highlights on the ground at the demon's feet. A ring of torches burns just beyond visibility, implying unseen spectators; faint silhouettes of watching figures linger at the torchlight's edge. Warm torchlight catches sharp highlights along the demon's clawed hand and shoulder while its form stays in legible shadow. The demon's gesture and fallen victim are centered in frame; the raised arm and torch glow stay clear of the top edge; the arena floor tapers into shadow at the bottom. Painterly digital fantasy illustration, Magic: The Gathering card art style, theatrical, self satisfied, cruel atmosphere."

**Demonstrates:** Rule 1 (Who/What/Why/Where — the "What" clause) — the demon is caught in a specific frozen instant, "one clawed hand extended in a showman's gesture... as if taking a bow," rather than a neutral standing pose, dramatizing the card's theatrical-cruelty flavor rather than just depicting the demon at rest.

---

**8.** "An elder human noble with pale gaunt aristocratic features, long flowing white hair, deep set eyes with a faint red tint, wearing ornate black engraved plate armor with a single tall spiked pauldron and dark fur collar, gripping an ornate ceremonial mace held upright at his side. Three quarter turn, gazing coldly to one side. Grand stone hall with tall pillars and narrow vertical window slits behind him; pale daylight as primary light source, catching sharp highlights on his hair and armor edges while his face stays evenly lit with clear midtones. Stone hall fades into soft dim atmosphere behind the pillars. Face and upper armor centered in frame; lower armor and mace taper into shadow at the bottom edge. Pillar tops and window slits clear of the top edge. Painterly digital fantasy illustration, Magic the Gathering card art style, cold regal atmosphere, high detail."

**Demonstrates:** Rule 2 (Diegetic lighting) — "pale daylight as primary light source" is named with explicit falloff: sharp highlights near the source on hair/armor edges, the stone hall behind "fades into soft dim atmosphere" with distance.

---

**9.** "A massive black armored horned demon with twin curling horns, dark leathery bat wings folded behind it, a long tentacle like tail coiling near its feet, standing atop a rock outcrop. It grips a large curved dual edged sword wreathed in swirling purple flame held low at its side. Purple fire is the primary light source, casting cold highlights on dark armor and wing undersides, while its face stays in shadow with glinting eyes. Hazy ash choked dusk sky behind it; two small silhouetted warrior groups visible far below on a smoke filled battlefield. Calm, calculating expression. Composition centered on armored chest and lowered sword, horns and wingtips clear of the top edge, rock and battlefield fading to shadow at the bottom. Painterly digital fantasy illustration, Magic the Gathering card art style, cold cruel atmosphere, high detail."

**Demonstrates:** Rule 5 (Framing for card crop) — "Composition centered on armored chest and lowered sword, horns and wingtips clear of the top edge, rock and battlefield fading to shadow at the bottom" is a direct precursor of the rule's exact vertical-band phrasing.

---

**10.** "Be'lakor, a towering daemon prince with massive black feathered wings bearing pale glowing eye sigils, curved golden horns, ornate gold and white plate armor over a red skinned daemonic lower body and cloven hooves. He stands atop a rock outcrop, arms raised and wings spread wide in a dominant pose. Behind him looms a vast translucent ghostly daemon head wreathed in swirling pink flame, casting warm magenta highlights across his wings and horns. Two small armored cultists stand at his feet; one holds a spectral curved glaive glowing cool pale blue, kept visually separate from the pink glow. Background: hazy violet Chaos landscape with dark jagged standing stones and misty purple peaks. Composition centers Be'lakor's torso, wings and ghostly head clear of the top edge, rock and cultists fading to shadow at the bottom. Painterly digital fantasy illustration, Magic: The Gathering card art style, epic tyrannical atmosphere, high detail."

**Demonstrates:** Rule 2 (Diegetic lighting — two-effects-distinct clause) — the cool pale blue glaive glow is stated to be "kept visually separate from the pink glow," the exact scenario the rule calls out for two magic effects sharing a frame.

---

**11.** "Wounded armored Aragorn lying half collapsed on a muddy rocky riverbank at the base of a tall cliff. Face turned toward viewer, clearly lit, eyes closed, brow furrowed in pain. One hand open palm up in the mud, fingertips catching light. Other arm limp beside a fallen sword. A dark brown horse stands over him, head lowered, nose nudging his shoulder. Shaft of pale morning light falls through a cliff gap across his face and chest; softer overcast dawn light fills the rest. Warm highlight along the horse's mane and shoulder. Steep shadowed cliff behind; shallow river beyond the bank; scattered debris and disturbed mud suggest a fall. Composition: cliff top clear of frame's upper edge; man's lit face and horse's lowered head centered; muddy hand tapers into shadow at bottom. Painterly digital fantasy illustration, Magic: The Gathering card art style, quiet tender atmosphere, high detail."

**Demonstrates:** Rule 1 (Who/What/Why/Where — the "What" clause) — the frozen moment chosen is the aftermath of a fall (horse nudging a collapsed, wounded figure), not Aragorn at rest or idle, and "scattered debris and disturbed mud suggest a fall" implies the preceding action rather than depicting it directly.

---

**12.** "The One Ring hanging from a heavy linked chain, half sunk in snow, its polished surface catching cold side lit sunlight in bright specular highlights while the underside stays in soft shadow. A lone hooded figure stands small and distant on a windswept snow ridge behind it, dwarfed by jagged snow capped mountains fading into pale atmospheric haze under a cold winter sky. Snow takes a faint warm gold cast near the ring, cooling to blue white further away. Ring centered as clear focal point; chain and foreground snow taper into soft shadow at the bottom edge. Mountain peaks and sky kept clear at the top. Painterly digital fantasy illustration, Magic: The Gathering artifact card art style, epic isolated atmosphere, high detail."

**Demonstrates:** Rule 2 (Diegetic lighting, falloff clause) — falloff is stated as a color shift with distance: "Snow takes a faint warm gold cast near the ring, cooling to blue white further away."

---

**13.** "Arwen, pale Elven noblewoman with dark flowing hair and pale hooded cloak billowing behind her, astride a rearing white horse on a rock outcrop at the right of the frame, one arm raised commanding the flood. A massive cascade of glowing white floodwater pours down the gorge, sculpting mid flow into charging horse shapes of foam and rushing water, galloping left toward nine Nazgûl — black cloaked Ringwraiths on black horses — massed and fleeing along the near bank. Floodwater glows with pale luminous light, casting cool highlights on Arwen and her horse; Nazgûl remain dark silhouettes with thin cold rim light. Steep pine covered cliffs frame the gorge, fading into misty haze. Arwen and the leading flood horses centered together; churning rapids taper into shadow at the bottom. Painterly digital fantasy illustration, Magic: The Gathering card art style, epic dramatic atmosphere, high detail."

**Demonstrates:** Rule 1 (Who/What/Why/Where — the "Why" clause) — the flood is not decorative water but a visual metaphor sculpted into "charging horse shapes," mapping the scene's magic directly onto the lore beat it dramatizes (the river itself becoming an army against the Nazgûl).

---

**14.** "Galadriel, tall and ethereal, pale silver gold hair, simple silver circlet, flowing white silver gown, kneeling beside a wide shallow silver basin on a carved stone pedestal, one hand near the silver ewer she poured from, gazing into water where an opalescent vision swirls. Moonlight filters through silver birch trunks and hanging moss; the basin's cool inner glow lights her face and hands from below while moonlight catches her hair and birch bark in blue white — two light sources kept distinct. Expression calm but faintly troubled. Faint mist pools at the pedestal's base. Composition centered on her face and glowing basin; circlet and birch canopy clear of the top edge; gown and mist taper into soft shadow at the bottom. Painterly digital fantasy illustration, Magic: The Gathering artifact card art style, hushed mystical atmosphere, high detail."

**Demonstrates:** Rule 2 (Diegetic lighting, two-sources-distinct clause) — the prompt states outright that the basin's glow and the moonlight are "two light sources kept distinct," the clearest verbatim precursor to that specific clause in the rule.

---

**15.** "Ob Nixilis, a horned demon lord with purple grey skin and large dark red brown membranous bat wings, wearing ornate bronze gold armor with sculpted pauldrons and a crested horned helm with jagged spikes. Caught mid cast, one clawed hand thrust forward unleashing a concentrated violet black energy bolt toward an off frame target, other hand braced back. Expression sharp and merciless. Hazy battlefield background with drifting smoke and indistinct ruined shapes. The energy bolt is the primary light source, casting hard violet tinted highlights across his gold armor and face while wings and background recede into charcoal grey haze. Muted teal grey and bronze palette, violet black energy as the sole saturated accent. Tight dynamic composition for an instant spell card: hand and bolt in lower middle frame, face and helm spikes clear of the top edge. Painterly digital fantasy illustration, Magic: The Gathering card art style, high detail."

**Demonstrates:** Character-bible reuse pattern (5-prompt Ob Nixilis set, #1 of 5) — introduces the fixed physical description ("purple grey skin... bronze gold armor... crested horned helm with jagged spikes") that prompts 16, 18, and 19 repeat near-verbatim, varying only the action clause ("Caught mid cast... unleashing a... energy bolt"). (Prompt 17 is the deliberate exception to this bible — see its own annotation.) Also demonstrates Rule 6 (Framing tightness): "Tight dynamic composition for an instant spell card: hand and bolt in lower middle frame" adapts the standard framing band to an instant-speed shot.

---

**16.** "Ob Nixilis, a horned demon lord with purple grey skin and large membranous bat wings spread wide in dark red brown, wearing ornate bronze gold armor with sculpted pauldrons and a crested horned helm with jagged spikes. His forearm is fused with the Infinity Gauntlet, golden knuckles set with all six Infinity Stones, raised clenched at chest height as the focal point; other clawed hand braced at his side. Background: ancient carved stone and gold temple wall with faint reliefs, plain and uncluttered. Lighting: soft even temple light with hard specular highlights on gold armor; six Stones emit soft overlapping glows — purple, blue, red, orange, green, yellow — radiating cleanly across his chest, no shattered glass or crystal effects. Face and horns legible in cool shadow rimmed by mixed colored light. Muted teal grey and bronze palette; gauntlet colors as sole saturated accents. Symmetrical frontal composition, face and gauntlet centered. Painterly digital fantasy illustration, Magic: The Gathering card art style, high detail."

**Demonstrates:** Character-bible reuse pattern (#2 of 5) — repeats the same fixed physical description as #15/18/19 near-verbatim ("purple grey skin and large membranous bat wings... bronze gold armor with sculpted pauldrons and a crested horned helm with jagged spikes"; wording drifts slightly, e.g. "sculpted pauldrons" here vs. "sculpted shoulder pauldrons" in #18/19), changing only the mode clause to the Infinity Gauntlet fusion. (Prompt 17 is the deliberate exception to this bible — see its own annotation.) Also demonstrates Rule 3 (Intricacy): "golden knuckles set with all six Infinity Stones" is a specific, nameable detail (not a generic "ornate"), Rule 7 (Body-part continuity): the gauntlet is described as "fused with" his forearm rather than "gripping" it, and Rule 4 (Palette discipline): "Muted teal grey and bronze palette; gauntlet colors as sole saturated accents" is an explicit, closed color list.

---

**17.** "Ob Nixilis mid transformation: corrupted demon with dark reptilian black skin, cracked blackened horns, and a bioluminescent Eldrazi lure jutting from his skull pulsing with sickly light. Black Eldrazi energy tendrils coil up his outstretched arms into his chest as he violently absorbs power from the ground, face contorted between agony and ecstasy. Setting: Eldrazi scarred Zendikar wastes — cracked colorless ground with black veins, broken hedron fragments, ash choked sky. The lure and energy tendrils are primary light sources, casting sickly greenish white light on his chest and face; wasteland remains dark ash grey shadow with legible midtone detail. Composition: horns and lure clear of top edge, face and chest energy centered in frame, cracked ground tapering into shadow at bottom. Painterly digital fantasy illustration, Magic: The Gathering card art style, high detail."

**Demonstrates:** Character-bible reuse pattern (#3 of 5) — deliberately breaks from the fixed bronze-armored description used in #15/16/18/19 to depict the same character mid-corruption ("dark reptilian black skin, cracked blackened horns" replacing "purple grey skin... bronze gold armor"), showing the bible can be intentionally overridden for a specific card's transformation state. Also demonstrates Rule 2 (Diegetic lighting): "the lure and energy tendrils are primary light sources," with the wasteland receding into "dark ash grey shadow" as falloff.

---

**18.** "Ob Nixilis, a horned demon lord with purple grey skin and large membranous bat wings spread wide in dark red brown, wearing ornate bronze gold armor with sculpted shoulder pauldrons and a crested horned helm with jagged spikes, standing in a symmetrical frontal pose with one clawed hand on his chest. Background: ancient carved stone and gold temple wall with faint decorative reliefs. Lighting: soft even temple light casting hard specular highlights on gold armor and warm translucent glow on thin wing membrane edges, deeper shadows in armor recesses and face. Muted teal grey and bronze palette. Composition: wingtips and helm spikes clear of the top edge, face and chest centered, lower armor tapering toward the bottom. Painterly digital fantasy illustration, Magic: The Gathering card art style, high detail."

**Demonstrates:** Character-bible reuse pattern (#4 of 5) — reverts to the fixed base description used in #15/16 ("purple grey skin... bronze gold armor with sculpted shoulder pauldrons and a crested horned helm with jagged spikes"), this time with no special mode/action clause at all — a plain frontal "portrait" use of the bible. Also demonstrates Rule 5 (Framing for card crop): "wingtips and helm spikes clear of the top edge, face and chest centered, lower armor tapering toward the bottom."

---

**19.** "Ob Nixilis, a horned demon lord with purple grey skin and large membranous bat wings spread wide in dark red brown, wearing ornate bronze gold armor with sculpted shoulder pauldrons and a crested horned helm with jagged spikes, standing in a symmetrical frontal pose with one clawed hand on his chest. Background: ancient carved stone and gold temple wall with faint decorative reliefs. Lighting: soft even temple light casting hard specular highlights on gold armor and warm translucent glow on thin wing membrane edges, deeper shadows in armor recesses and face. Muted teal grey and bronze palette. Composition: wingtips and helm spikes clear of the top edge, face and chest centered, lower armor tapering toward the bottom. Painterly digital fantasy illustration, Magic: The Gathering card art style, high detail."

**Demonstrates:** Character-bible reuse pattern (#5 of 5) — an exact word-for-word repeat of #18. This is the clearest possible instance of the pattern: once a character bible plus mode is dialed in and produces the desired result, the identical prompt is resubmitted verbatim rather than rewritten, confirming the bible-plus-mode split is treated as a reusable, literal template rather than just a descriptive habit.

---

**20.** "A horned demon in dynamic three-quarter pose, pale curling ram-like horns crowning its head, bare pale muscular torso, one clawed hand raised in a striking gesture, a single massive black tattered wing sweeping down and back like a torn cape dwarfing the body, a swirling warm orange-gold ember glow burning at the hip as the primary light source, casting warm light up across the chest and the near edge of the wing while the wing's far side and surroundings fall into cool violet-pink haze, a silhouetted ruined structure distant in the misty background, composition framed with the horns and raised hand kept well clear of the top edge and the wing/legs tapering into simple haze near the bottom edge so both the card's title bar and text box crop only expendable space, painterly digital fantasy illustration, Magic the Gathering card art style, high detail"

**Demonstrates:** Rule 2 (Diegetic lighting, falloff clause) — "ember glow burning at the hip as the primary light source" lights the chest and near wing edge, while "the wing's far side and surroundings fall into cool violet-pink haze" as an explicit falloff away from the source.

---

**21.** "A towering legless demon rising from glowing white pink mist, crowned head and gold trimmed chest filling the upper frame with little empty sky above. Crown of dark gnarled horns, gaunt pale face with hollow eyes, gold trimmed dark breastplate. Huge dark furred wings spread wide, filled with curling tendrils and small glowing motes. One long clawed arm reaching down with a banded cuff. Lower body tapering into mist at the frame's bottom edge. Three small robed and armored figures at the very bottom reaching upward toward a smoking cauldron between them. Glowing mist as the primary light source, cool blue violet haze in the background. Indigo and bone palette with gold accents. Painterly digital fantasy illustration, Magic: The Gathering card art style, high detail, imposing close crop with the demon dominating the upper frame."

**Demonstrates:** Rule 6 (Framing tightness) — explicitly named as "imposing close crop with the demon dominating the upper frame," while still keeping the three robed figures and cauldron as a legible pocket of environment at the bottom rather than filling the canvas edge-to-edge with the subject alone.
