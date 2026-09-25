# mtg-reskin — Orchestrator

This is the top-level skill. It wires every other file in `/mtg-reskin/` into one pipeline: given a pasted Moxfield decklist, a theme name, and (implicitly) the deck's commander, it produces one Midjourney-ready JSON object per card. Nothing in this file re-derives rules that live elsewhere — it sequences calls to `scripts/scryfall_batch.py`, `skills/theme-bible/SKILL.md`, `skills/naming/SKILL.md`, `skills/art-template/SKILL.md`, and the 9 type skills, and it owns the two artifacts that persist across the whole run: the **deck lore doc** and the **faction ledger**.

Two data structures recur throughout and must never be conflated (see naming/SKILL.md Rule 4):

- **Used-names list**: a flat, append-only list of every `new_name` string committed so far, across every faction. This is the uniqueness check (Rule 4).
- **Faction ledger**: a structured, per-faction map of established names/vocabulary/motifs/palette, plus a separate per-character physical-description map. This is the consistency and collision-tiebreak check (Rules 5, 7, 8).

Both are passed into every batch call. They are not the same object and not interchangeable — the used-names list answers "has this exact string been used," the ledger answers "what voice/character does this faction/character already have."

## Inputs

- **Decklist text**: pasted Moxfield export, one `<quantity> <name>` per line.
- **Theme**: a name matching (or to become) a file under `themes/<theme>.md`.
- **Output mode**: one of `prompt`, `pinterest`, `both` (see Output modes below). Ask the user if not stated.
- **Commander**: identify from the decklist itself (Moxfield exports typically mark it, e.g. a `Commander` section header, or it's the sole legendary creature named outside the 99). If ambiguous, ask.

## Pipeline

### Step 1 — Parse and enrich the decklist

Take the user's pasted decklist text as-is (do not hand-parse it yourself) and pipe it directly to the enrichment script in one call:

```bash
python3 mtg-reskin/scripts/scryfall_batch.py <<'EOF'
<decklist text, one "<quantity> <name>" per line>
EOF
```

This is **one invocation for the whole deck**, not one per card — the script itself batches Scryfall's `/cards/collection` endpoint internally (chunks of ≤75 identifiers). Capture its JSON stdout: an array of objects, each shaped exactly:

```json
{
  "quantity": 0,
  "name": "",
  "type_line": "",
  "color_identity": [],
  "mana_value": 0,
  "oracle_text": "",
  "keywords": []
}
```

Use these exact keys downstream (`type_line`, `oracle_text`, `color_identity`, `keywords`, `mana_value`) — do not invent alternate field names. Note: the script preserves one enriched record **per decklist line's quantity as a single record with a `quantity` field**, not one record per physical copy. Basic lands with `quantity: 10` arrive as **one** record with `"quantity": 10` — Step 6 (batching) and Step 8 (output) are responsible for expanding that into 10 distinct per-copy entries; do not treat a quantity-10 record as one card going forward.

If any line failed to resolve (script prints a `Warning: skipping unparseable line` to stderr, or a record comes back with an empty `type_line`), surface this to the user before proceeding — a card with no Scryfall data can't be routed or subtyped.

### Step 2 — Load or build the theme bible

Look for `mtg-reskin/themes/<theme>.md`.

- **If it exists**: load it in full. Its six required sections (color→faction map, card-type→motif map, subtype translation table, naming vocabulary, deck anchor guidance, inter-faction relations default) are the seed material for Steps 3 and 4.
- **If it does not exist**: invoke `skills/theme-bible/SKILL.md` to draft one now. **This is never silent.** Present the drafted bible to the user for review before treating any of it as final — per that skill's own instructions, a first draft is a proposal, not a deliverable. **End your turn and wait for the user's explicit confirmation before invoking Step 3** — do not treat silence, an unrelated reply, or your own judgment that the draft "looks fine" as confirmation. Once confirmed (or corrected and re-confirmed), save the bible to `mtg-reskin/themes/<theme>.md` for reuse on future runs.

### Step 3 — Build the deck lore doc

Using the enriched card list from Step 1 and the loaded bible from Step 2:

1. **Count subtype occurrences.** For every enriched card, parse `type_line` to extract its subtypes (the words after the em dash, e.g. `"Legendary Creature — Human Cleric"` → subtypes `Human`, `Cleric`; `"Artifact Creature — Golem"` → subtype `Golem`). Basic lands' implicit subtype is their own name (Plains/Island/Swamp/Mountain/Forest) — count these too. Tally counts across the whole deck (each quantity-N record counts N times toward its subtype tally, even though it hasn't been split into N output rows yet).
2. **Identify faction candidates**: any subtype with a tally ≥3, plus any subtype that also appears in the commander's own `type_line`, regardless of that subtype's deck-wide tally (per the design spec's commander-anchor rule).
3. **Fallback — no subtype clears the threshold.** A generic control/superfriends/spells-matter commander can easily have no subtype at tally ≥3 and no reusable commander subtype, which would otherwise leave zero faction candidates, an empty ledger, and no faction for any downstream card to populate. If sub-step 2 above produces zero candidates, **cluster by color identity instead**: treat each color present anywhere in the deck's cards (plus multicolor and colorless, if either is present) as its own faction candidate, and resolve each one directly against the bible's Section 1 color→faction map rather than Section 3's subtype table. Proceed with the rest of this step (anchor determination, relations paragraph) exactly as if these were subtype-derived candidates — the rest of the pipeline does not need to know which path produced them.
4. **For each faction candidate**, look up its entry in the loaded bible's Section 3 (subtype translation table). Expand it into one short paragraph covering: identity (who they are under this theme), territory/domain, and what they want. If the bible's Section 3 has no entry for a surfaced subtype (shouldn't happen for the 34 documented subtypes, but can for an edge case like a changeling or an un-translated basic-land type), fall back to the bible's Section 1 color→faction map for that card's color identity instead, and note the fallback inline in the lore doc.
5. **Determine the anchor faction** using the bible's Section 5 (deck anchor guidance): the commander's color identity and subtypes point to which mapped faction/alliance is "home." Every other detected faction is described in relation to the anchor.
6. **Write the inter-faction relations paragraph**: one paragraph stating how every detected faction relates to the commander (serves/opposes/bound-by/independent-but-adjacent) and to each other, pulling from the bible's Section 6 (theme-canon-first citations where they exist, invented-and-flagged only where the bible's Section 6 says canon is silent). Do not invent a relation the bible already resolved, and do not silently treat an invented relation as canon.

Output of this step: a single doc, ~1 short paragraph per faction candidate + 1 relations paragraph. This doc is a constant passed unmodified into every batch in Step 7 — it is not rebuilt or re-derived per batch.

### Step 4 — Initialize the faction ledger and used-names list

Before any card is processed, initialize:

```json
{
  "<faction_name>": {
    "names": [],
    "vocabulary": [],
    "motifs": [],
    "palette": []
  }
}
```

— one entry per faction candidate identified in Step 3 (add new faction keys later only if a card's routing surfaces a faction the subtype count missed, which should be rare given Step 3's ≥3 threshold).

Also initialize a separate, parallel structure:

```json
{ "<character_name>": "<fixed physical-description paragraph>" }
```

— empty at start, populated the first time a legendary/named-character card establishes a bible entry (naming/SKILL.md Rule 8).

Also initialize the **used-names list** as an empty flat array. This is distinct from the ledger's per-faction `names` arrays (which exist for voice/register consistency, Rule 5) — the used-names list is the single global uniqueness source of truth (Rule 4). A name enters both simultaneously when committed, but they are checked for different reasons and neither substitutes for the other.

**Persistence during the run.** The deck lore doc, faction ledger, used-names list, and character-bible map must not live only as unstated in-context assumptions across a multi-batch run — a long run risks context compaction silently dropping or corrupting append-only state the naming system depends on being exact. Maintain all four as a single JSON scratch file (e.g. `mtg-reskin-run-state.json` in the working directory, or the session's scratchpad directory) that is written out after Step 4's initialization and re-written after every batch completes in Step 7. Before starting each new batch, re-read this file from disk rather than trusting whatever is still in context, and pass its current contents into that batch's context. This file is run-scoped working state, not a deliverable — it is not part of the final output and can be discarded once Step 8 emits the full deck array.

### Step 5 — Expand quantities and batch the card list

Before batching, expand every enriched record into its actual per-copy count: a `quantity: 10` Forest record becomes 10 separate working entries (each still carrying the same `type_line`/`oracle_text`/etc., since Scryfall doesn't distinguish copies), a `quantity: 1` record becomes 1. **Every individual physical copy is its own card going forward** — this matters most for basic lands, which will otherwise look like a single entry to dedupe. Do not deduplicate identical-name entries at any later step; each keeps its own row through naming, art direction, and final output.

Split the fully-expanded per-copy list into batches of **~20 cards each**, preserving decklist order within and across batches (order matters for the naming collision tiebreak, Rule 7).

### Step 6 — Determine each card's type-skill route

Before naming or art-directing a card, decide which of the 9 type skills handles it, from its `type_line`:

1. **If "Creature" appears anywhere in `type_line`** (including hybrid types like "Artifact Creature," "Enchantment Creature," "Legendary Creature") → route to `skills/creature/SKILL.md`. This check runs **first**, before any other type check, per the design spec's priority rule.
2. Else if `type_line` contains "Planeswalker" → `skills/planeswalker/SKILL.md`.
3. Else if `type_line` contains "Battle" → `skills/battle/SKILL.md`.
4. Else if `type_line` contains "Land" (including "Legendary Land," "Basic Land," snow-covered variants) → `skills/land/SKILL.md`.
5. Else if `type_line` contains "Artifact" (including "Legendary Artifact," "Artifact — Equipment," etc., and *not* already caught by rule 1) → `skills/artifact/SKILL.md`.
6. Else if `type_line` contains "Enchantment" (including "Enchantment — Aura/Saga/Curse/Class/Room," and *not* already caught by rule 1) → `skills/enchantment/SKILL.md`.
7. Else if `type_line` contains "Instant" → `skills/instant/SKILL.md`.
8. Else if `type_line` contains "Sorcery" → `skills/sorcery/SKILL.md`.

Worked disambiguation per the design spec: "Artifact Creature — Golem" → creature (rule 1 fires before rule 5). "Enchantment Creature — Human Cleric" → creature (rule 1 before rule 6). "Legendary Land" → land (no creature type present, rule 4 fires cleanly). A card can only ever match one route — rules 2-8 are mutually exclusive once rule 1 has already claimed every creature-typed card, so evaluate them in the order above and stop at the first match.

### Step 7 — Process each batch

For each batch, in order:

**Context passed into the batch** (all three, every batch):
- The deck lore doc (Step 3 output) — constant across all batches, never regenerated.
- The current faction ledger and character-bible map (Step 4, updated after each prior batch).
- The current used-names list (Step 4, updated after each prior batch).

**Per card within the batch**, in decklist order:

1. **Route** the card per Step 6.
2. **Name the card** by applying `skills/naming/SKILL.md` in full:
   - Derive the name from the card's role (parsed from `oracle_text`), per Rule 2 — never from `type_line` alone.
   - Check the bible's Section 4 (naming vocabulary) for the card's faction register.
   - Check the **used-names list** for exact-string uniqueness (Rule 4).
   - Check the **faction ledger's** `names`/`vocabulary` entries for register consistency with already-committed names in the same faction (Rule 5).
   - Check the **character-bible map** for an existing canonical-name claim (Rule 7). If this card plausibly evokes a character already committed to the character-bible map by an earlier batch, that earlier claim wins outright regardless of this card's narrative centrality — this card gets an epithet/title variant, full stop, per the append-only ledger semantics below. If the collision is between two-or-more cards newly discovered within *this same batch*, and neither has been committed to the character-bible map yet, resolve by decklist order (or commander-centrality if tied) before committing either.
   - Basic lands: each individual copy (already split out in Step 5) gets its own distinct named location within its faction — never the same name repeated, never a numbered variant of one base name.
   - **Commit rule**: as soon as a card's name is finalized within this batch, immediately append it to the used-names list and to its faction's ledger entry (and to the character-bible map if applicable) **before** moving to the next card in the batch. Do not defer all of a batch's commits to the end of the batch — a later card in the *same* batch must see the earlier card's name as already committed, exactly as a later batch must see an earlier batch's commits as already committed. The ledger is append-only at every granularity (within-batch and across-batch): once written, a name is never revisited or reassigned.
3. **Art-direct the card** by applying the routed type skill's compositional-mode taxonomy on top of `skills/art-template/SKILL.md`'s shared skeleton (Who/What/Why/Where brief, diegetic lighting + falloff, intricacy, palette discipline, framing-band language, framing tightness, body-part continuity, banned words, closing suffix, no-text/no-artist rule). **Before writing the Who clause, check the character-bible map for this card's character** (same lookup as Step 7.2's naming check, same map). If an entry already exists and this card is not a deliberate transformation of that character, reuse its fixed physical-description paragraph near-verbatim in the prompt per naming/SKILL.md Rule 8 — do not invent a new physical description for a character who already has one. Only depart from the bible paragraph when this card is itself establishing a new bible entry (the character's first appearance) or is a flagged deliberate transformation (per Rule 8's Ob Nixilis exception), in which case the departure should be signaled in the name too, not just the art. Ground the specific decisive moment and detail in **this deck's faction** as described in the deck lore doc (Step 3), not a generic theme-level treatment of the card's type/color. Use the type skill's own closing-suffix aspect ratio exactly as that skill specifies it — **do not assume every card uses `--ar 4:3`**; `battle/SKILL.md` overrides this to `--ar 3:1` by default (with `--ar 16:9` as its documented fallback), and that override must be preserved verbatim in the final prompt for any battle card. The other 8 type skills use the shared `--ar 4:3` default from `art-template/SKILL.md` Rule 9 unmodified (corrected 2026-09-24 from an earlier, wrong `--ar 5:7` assumption). Per Rule 5, every prompt should describe the full subject fully contained within its frame with margin, not bled to the edge for an assumed post-crop.
4. **Build the output object** for this card per the Output format below, populating fields according to the active output mode.

**After the batch finishes** (all ~20 cards processed): append every new name/vocabulary/motif/palette entry and every new character-bible entry established during this batch to the persistent faction ledger and used-names list, so the *next* batch receives the fully updated state. (In practice, per the commit rule above, this will already be true incrementally — this is the checkpoint to confirm nothing was missed before moving on.)

**Run the quality gate** (below) against every card in the batch before returning its results. Rewrite any card that fails any check, then re-check it, before including it in the batch's output.

### Step 8 — Emit output

Collect every batch's card objects, in original decklist order, into a single JSON array. This is the full-deck output.

## Output modes

- **`prompt`**: only the `prompt` field is populated; omit the `pinterest` field entirely from each object.
- **`pinterest`**: only the `pinterest` field is populated; omit the `prompt` field entirely from each object.
- **`both`**: both `prompt` and `pinterest` are populated.

Ask the user which mode applies if not already specified before Step 1.

## Output format

One object per card (per physical copy — see Step 5), collected into one JSON array for the full deck:

```json
{
  "original": "",
  "type_line": "",
  "role": "",
  "faction": "",
  "new_name": "",
  "decisive_moment": "",
  "specific_detail": "",
  "prompt": "",
  "pinterest": ["", "", "", "", ""]
}
```

- `original` — the printed Scryfall/Moxfield card name (never the new name).
- `type_line` — as returned by `scryfall_batch.py`, unmodified.
- `role` — the one-clause statement of what the card does (naming/SKILL.md Rule 2's required first step), e.g. "merciful removal that transforms a threat into something benign."
- `faction` — the faction (from the deck lore doc / ledger) this card was attributed to.
- `new_name` — the committed name from Step 7.2.
- `decisive_moment` — the specific frozen instant chosen per the Who/What/Why/Where brief's "What."
- `specific_detail` — the one nameable intricacy-rule detail (engraved micro-narrative, wear pattern, or unusual material).
- `prompt` — the full Midjourney prompt text, including the type skill's own closing suffix and aspect ratio. Populated per output mode.
- `pinterest` — 5 short search queries (subject, composition/pose, lighting, textures/props, environment), in that order. Populated per output mode.

## Quality gate (run before returning any batch's results)

For every card in the batch, verify all of the following. Rewrite before output if any check fails, then re-verify the rewritten card.

- Name is unique (checked against the used-names list), fits the faction's theme vocabulary (checked against the ledger), and resolves any canonical-collision per the tiebreak rule (Rule 7) — including respecting any earlier batch's already-committed claim.
- Art direction matches the card's role, and — for creatures — subtype fidelity is preserved (the card's signature visual features per `creature/SKILL.md` and the theme bible's Section 3 translation both survive).
- A decisive moment and a specific, unique detail are both present and are not generic placeholders.
- No banned words (art-template Rule 8's list) appear outside the single allowed terminal atmosphere tag.
- A physical, named light source with explicitly stated falloff is present (art-template Rule 2).
- Framing states the full subject is entirely contained within the frame with an even margin on all sides, per art-template Rule 5 — not bled to the edge or described as if the app will crop into it.
- The prompt reflects the deck lore doc's relevant faction specifically — a reader familiar with the deck lore doc should be able to tell which faction this card belongs to from the prompt's content, not just from the `faction` field label — never a generic theme-level reskin that could belong to any faction or any deck under this theme.

## Notes on scope

- This file does not restate any type skill's compositional-mode taxonomy, `art-template/SKILL.md`'s shared rules, `naming/SKILL.md`'s rules, or `theme-bible/SKILL.md`'s section requirements — it sequences calls to them. When in doubt about a specific rule's exact wording or edge case, read the source skill file directly rather than relying on this summary.
- Split cards, MDFCs, and Adventure cards are not yet covered by an explicit rule anywhere in this environment (flagged as an open item in the design spec). If one appears in a real decklist, pause and ask the user how to handle its two names/faces before generating output for that card, rather than guessing silently.
