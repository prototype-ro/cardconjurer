# Naming — Card Renaming Rules

This skill governs the one thing every other type skill (`art-template/SKILL.md` and its eight type-specific children) leaves untouched: what the reskinned card is actually *called*. Art direction and naming are separate passes over the same card — a prompt can be perfect and still fail the deck if the name it's attached to breaks uniqueness, drifts from the theme's voice, or silently reuses the printed MTG name. Run this skill's rules on every card, independent of which type skill produced its art prompt.

## 1. Length and vocabulary

Every new name is **2-5 words**, drawn from the theme's own vocabulary — not generic fantasy filler that could belong to any deck. "Native to the theme's vocabulary" means the words themselves should feel lifted from the theme bible: if the theme is Lord of the Rings, a name should read like something out of Tolkien's naming conventions (patronymics, epithets tied to place or deed, elvish/dwarvish/rohirric register depending on faction) rather than a generic "Shadow Blade" that could just as easily be a D&D drop-in. A name outside 2-5 words either reads as a single flat label (too short to carry theme flavor) or as a run-on description masquerading as a name (too long — that belongs in the prompt's `specific_detail`, not the `new_name` field).

## 2. Derive from role, not type

Do not default to a name built off the card's type line. The name has to come from what the card *does* in the game — its role in the oracle text — filtered through the theme's lore.

**Worked example:** "Swords to Plowshares" exiles a creature and gives its controller life equal to its power. The oracle-text role is *merciful removal that transforms a threat into something benign*, not "a sword." A name built off the type/flavor surface would land on something like "Sword of Banishing" or "Blade of Exile" — mechanically plausible but derived from the reprint's own flavor text, not from the mechanic itself, and it also collides with the banned move in Rule 3 (still visibly the same idea as the original card). A name built off the actual role instead lands on something like, for a Lord of the Rings deck, "The Plowshare Oath" or "Absolution of the Falling" — the removal is reframed as an act of forced mercy or redemption, which is the mechanic's real shape (unconditional exile + healing, not just "unconditional removal"). For a different theme's register, the same role could become "Mercy's Verdict" or "The Gentler Blade" — the point is that the role (coercive-but-merciful removal) drives the name, not the sword flavor of the original printing.

Before naming any card, be able to state in one clause what the oracle text actually does, and derive the name from that clause, not from the type line or the original name's imagery.

## 3. Never reuse the original MTG card name

The new name must not be the printed Magic card name, in whole or as a thinly reskinned variant of it. "Swords to Plowshares" cannot become "Blades to Plowshares" or "Swords into Plowshares" — that's the same name with one word swapped, not a new name. If a theme's lore happens to produce a name that coincides with an unrelated real MTG card name, that's fine (it's not the *original* card being reskinned); what's banned is any name still recognizably derived from the card being replaced.

## 4. Unique across the deck

No two cards in the same deck may share a new name, full stop — this is checked against the orchestrator's used-names list (see the pipeline's faction ledger), not just eyeballed per batch.

**Worked example:** a deck has two removal spells with similar oracle text — one exiles a creature, one destroys it. If both get named independently by role (Rule 2) they risk converging on something like "The Ranger's Judgment" for both. The fix is not to weaken either name's fit to its own mechanic; it's to differentiate them along an axis the theme already supports — one becomes "The Ranger's Judgment" (the exile effect, framed as a permanent sending-away) and the other "The Ranger's Reckoning" (the destroy effect, framed as final and violent) — same character-voice, same faction register, but textually distinct strings. If two cards would also collide on evoking the *same specific named character* (not just a similar mechanic), that's not a uniqueness clash to resolve by rewording — it's the canonical-name collision case in Rule 6 below, which has its own resolution path.

## 5. Faction consistency

Cards belonging to the same faction (per the deck lore doc's faction clustering) must read as coming from the same voice — same register, same naming conventions, same class of vocabulary — even though each individual name is still derived independently from its own card's role.

**Worked example:** in a Lord of the Rings deck, a Rohirric faction's cards should consistently draw on the same naming conventions as each other: patronymics and epithets tied to horses, plains, and oaths ("Éomund's Vow," "Rider of the Mark," "Oath at the Hornburg"), while an Elvish faction in the same deck draws on a visibly different register — softer phonology, nature/light imagery, titles tied to realms or ages ("Light of Lothlórien," "Warden of the Golden Wood," "Galadriel's Herald"). If a Rohirric card were named "Light of the Mark-Wood" it would read like it wandered in from the Elvish faction's naming conventions even though the words are technically about Rohan — the *style*, not just the subject matter, has to stay consistent within a faction. When in doubt, check a new name against 2-3 already-established names from the same faction in the ledger and confirm it could plausibly sit in the same list.

## 6. Basic lands: distinct named locations

Each copy of a basic land within a faction gets its own distinct named location, not the same name repeated across copies or a generic "Faction Plains #2." A faction's basic lands should read as an actual gazetteer of places within that faction's territory — e.g. a Rohirric Plains might spread across "The Westfold," "Eastfold Downs," and "The Fords of the Entwash" rather than three cards all called "Plains of Rohan." This keeps a full basic-land count from flattening into repeated, uninformative naming, and gives the faction's territory a sense of real geographic breadth.

## 7. Canonical-name collision: first-claim wins

When two or more cards in the deck plausibly evoke the **same specific theme-canon character** (not just a similar role or a similar vibe — the same named figure), only one of them gets to claim that character's bare canonical name. This is different from Rule 4's ordinary uniqueness check: two cards can fail to collide on the exact name string while still both clearly being "Aragorn," and that's the case this rule exists for.

**Resolution — first-claim wins:**
- Process cards in decklist order (or, if the collision needs to be resolved out of order, whichever card is most central to the commander's own story wins the tie).
- The **first** card to map to that character gets the **bare canonical name** — just "Aragorn," no qualifier.
- **Every other card** that maps to the same character gets an **epithet or title variant of that same character** — never a fully unrelated name. The point of the rule is to keep the connection to the evoked character legible across every card that represents them, while still giving each card a textually unique name.

**Worked example:** a deck has three cards that all plausibly represent Aragorn — a legendary creature, an equipment, and a saga. Decklist order (or commander-centrality) gives the legendary creature first claim: it becomes simply "Aragorn." The equipment does not become an unrelated sword name like "Andúril" in isolation (that would sever the visible link for a reader who doesn't already know the lore) — it becomes "Strider's Blade," an epithet-anchored variant that still reads as *his* weapon. The saga becomes "Oath of the Ranger-King" — again anchored to an epithet ("Ranger-King") rather than a generic saga title. All three remain uniquely named per Rule 4, all three remain legible as depicting Aragorn, and none of them is a disconnected alias that would require outside knowledge to tie back to the character.

## 8. Interaction with the character bible: name and visual description move together

`planeswalker/SKILL.md` documents the **character-bible reuse pattern**: when a named character appears across multiple cards in a deck — multiple printings, a creature/planeswalker pair representing "the same" reskinned figure, or the collision case in Rule 7 above — that character's *physical description* is fixed once and reused near-verbatim across every prompt for them, varying only the action/mode clause. `reference/user-prompts.md`'s five-prompt Ob Nixilis set is the demonstrated example: the same "purple grey skin... bronze gold armor... crested horned helm with jagged spikes" bible paragraph is repeated across prompts #15, 16, 18, and 19, with #17 as a deliberate mid-transformation exception.

Naming and the character bible are two halves of the same consistency requirement and must be kept in sync:

- **The name identifies the character; the bible describes the character.** When a card maps to a character who already has an established bible entry in the faction ledger, that card must (a) use a name that is legible as the same character per Rule 7 (the bare canonical name if this card claimed it first, or an epithet variant if not), and (b) pull its physical description from that same character's existing bible entry rather than inventing a new appearance. Two cards can't be "the same Aragorn" if one calls him a grizzled ranger in worn leathers and the other calls him a young golden-armored prince — the visual drift breaks the identity the epithet-naming was trying to preserve.
- **A transformation is the one deliberate exception, on both sides at once.** Prompt #17's mid-transformation Ob Nixilis breaks the physical bible on purpose (reptilian black skin replacing the fixed purple-grey/bronze-armor look) to depict a specific narrative moment. If a card in the deck does this — a walker-flip, a corruption, a saga's final chapter — its *name* should also signal the departure (an epithet like "Ob Nixilis, the Corrupted" or a title distinct from the character's other cards) rather than silently reusing the bare canonical name as if nothing changed. Name drift and bible drift should happen together, deliberately, and only when the card is actually depicting a transformation — not as an accident of two different sessions naming or describing the same character independently.
- **Practically:** before finalizing a new card's name and prompt, check the faction ledger for an existing bible entry under that character. If one exists and this card isn't a deliberate transformation, reuse the name (per Rule 7) and the bible paragraph (per the planeswalker skill's pattern) together. If no entry exists yet and this card is the character's first appearance in the deck, this card's resolution of Rule 7 and its physical description together *become* that ledger entry for every later card to draw on.
