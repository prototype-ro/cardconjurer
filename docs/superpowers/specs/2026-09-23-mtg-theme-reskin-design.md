# MTG Theme Reskin Environment — Design

## Purpose

Given a Moxfield decklist, a theme (e.g. The Lord of the Rings), and a commander, produce a new in-world name and Midjourney-ready art direction for every card — output that reads as **real, published Magic art**, not generic AI fantasy, and reads as **this specific deck's world**, not a generic theme skin.

This is a prompt/skill environment, not application code, except for one thin Scryfall batch-lookup script. Runtime target: Claude Code in this repo, invoked as a skill.

## Problem statement

AI-written art prompts default to generic. Two failure modes to kill:
1. **Generic-per-card**: vague subject, no decisive moment, no named light source, purple-prose adjectives instead of concrete material/action.
2. **Generic-per-theme**: every card in a themed deck feels like an interchangeable reskin, with no trace of *this* deck's specific story (e.g. a Kaalia, the Vast deck built from Angels + Demons + Dragons under one Mardu commander should read as those three factions in tension, not "generic angel," "generic demon," "generic dragon" cards that happen to share a color identity).

## Non-goals

- No application UI, no batch card-image generation pipeline, no Scryfall image caching beyond one lookup pass.
- No attempt to fully automate theme-bible creation without human review on first build of a new theme.
- Not scoped to build all 8 type skills to equal depth in the first pass (see Build order).

## Architecture

```
/mtg-reskin/
  SKILL.md                     orchestrator: pipeline, modes, output format, quality gate
  skills/
    art-template/SKILL.md      shared prompt skeleton, used by every type skill
    creature/SKILL.md
    artifact/SKILL.md          adapted near-verbatim from anthropic-skills:mtg-artifact-card-art
    instant/SKILL.md
    sorcery/SKILL.md
    enchantment/SKILL.md
    land/SKILL.md
    planeswalker/SKILL.md
    battle/SKILL.md
    naming/SKILL.md
    theme-bible/SKILL.md
  themes/
    lord-of-the-rings.md       first theme bible, worked example
  reference/
    corpus-notes.md            Scryfall sampling queries/dates/counts, per type
    user-prompts.md            Rodrigo's 24 proven prompts, annotated by pattern (see Corpus section)
  scripts/
    scryfall_batch.py          one POST to /cards/collection per deck run
```

## Pipeline

1. **Parse decklist** (Moxfield export text).
2. **Enrich in one call**: `scripts/scryfall_batch.py` posts the full card list to Scryfall's `/cards/collection` endpoint once, returns type line, supertypes, subtypes, color identity, mana value, oracle text, keywords for every card. Replaces the original per-card-call design (was O(n) requests; now O(1)).
3. **Load theme bible** from `/themes/<theme>.md`. If it doesn't exist, invoke `theme-bible/SKILL.md` to build it — this step is interactive/reviewed, not silently generated, since it anchors everything downstream.
4. **Build the deck lore doc** (new step, replaces a single generic "deck-arc brief"):
   - Cluster cards by **subtype density** first, color identity second — color identity alone under-detects (a mono-color-identity deck can still span multiple tribal factions, e.g. Mardu Kaalia = Angels/Demons/Dragons in one color identity).
   - Any subtype appearing ≥3 times, or matching one of the commander's own subtypes, becomes a **faction candidate**.
   - For each faction candidate, pull its theme-bible subtype-translation entry as seed, expand into: identity, territory/domain, what it wants, how it relates to the *other* detected factions in this specific deck.
   - Commander's subtypes/colors anchor which faction is central; the doc must state explicitly how the other detected factions relate to the commander (serve it, oppose it, are bound by it, etc.) — not left implied.
   - Output: ~1 short paragraph per faction + 1 paragraph on inter-faction relations. This whole doc is injected into every batch call, replacing the single deck-arc brief from the original draft.
5. **Init faction ledger**: grows across batches — per faction, established names/vocabulary/motifs/palette. Also holds a **character-bible entry per legendary card** once one is generated (reusable description block, matching the observed pattern of reusing near-verbatim physical description across multiple prompts for the same named character, e.g. Ob Nixilis — only the action/mode clause changes per card).
6. **Batch cards**, ~20 per batch. Each batch call receives: deck lore doc (constant), current faction ledger, used-names list. After each batch, orchestrator appends anything new the batch established to the ledger.
7. **Route each card to its type skill.** Every type skill is built on the shared `art-template/SKILL.md` skeleton (see below) plus its own compositional-mode taxonomy.
8. **Name the card** via `naming/SKILL.md` (see Naming rules).
9. **Output JSON** per card (see Output format).

## Shared art-direction skeleton (`art-template/SKILL.md`)

Every type skill is built on this base, not a copy of it — type skills override the compositional-mode step and any per-type defaults, everything else is shared so all 8 types stay visually coherent as one deck.

1. **Who/What/Why/Where brief**, run silently before drafting:
   - Who — is a figure/hand/implied second party needed, or does the object/scene carry itself.
   - What — the specific frozen moment. Never a static/at-rest description.
   - Why — the visual metaphor must map onto the card's actual mechanic or the deck's lore, not be decoration.
   - Where — setting + a diegetic light source, positioned relative to the framing band (below).
2. **Compositional mode** — type-specific, see Per-type mode taxonomies below. Never generic "portrait of X."
3. **Diegetic lighting rule**: name the physical light source explicitly, state falloff explicitly (what stays legible near the source, what recedes to shadow/haze further away). When two magic effects/colors are both present in frame, state they're kept visually distinct.
4. **Intricacy rule**: give the subject visible history (engraved micro-narrative, wear pattern, material detail) — reward a second look, not just a first catch.
5. **Palette discipline**: 2-3 dominant colors stated as a short explicit list. Never open-ended ("vibrant colors").
6. **Framing for card crop**, stated with explicit percentages every time:
   > "composition composed so the [subject/most detailed part] sits within the vertical middle band of the frame, roughly between 20% and 65% down from the top, well clear of both the top 15% and bottom 35% of the image — [upper area] fading into plain dark atmosphere, expendable space meant to be cropped by the title bar; [lower area] fading into shadow, expendable space meant to be cropped by the text box."
7. **Framing tightness**: close-up/medium-tight, not extreme close-up — leave a visible pocket of dim environment so there's room for the crop to eat into, rather than edge-to-edge subject.
8. **Body-part continuity gotcha**: if a figure's own limb/body part is transforming or fused with an object, describe it as one continuous part, never as "gripping/holding" a separate object — the model misreads that as two distinct things.
9. **Banned words**: epic, majestic, dramatic, stunning, breathtaking, mystical, ethereal, awe-inspiring — banned as *mid-scene* description. Exception: one of these may appear as a single terminal atmosphere tag at the very end of the prompt (e.g. "...card art style, epic isolated atmosphere, high detail") — matches observed real usage, where the word functions as a mood label, not purple prose.
10. **Closing suffix**, fixed per deck:
    `Painterly digital fantasy illustration, Magic: The Gathering [artifact] card art style, [2-4 word atmosphere tag], high detail. --ar 5:7`
    Add `--no <specific clutter terms>` only as a targeted fix when several generations have converged on the same unwanted clutter — not a default parameter.
11. No literal text, card frames, borders, or UI in the described art. No named living artists.

## Per-type mode taxonomies

Each type skill enumerates its own numbered compositional modes — not slot-filled defaults. Confirmed shape from the existing `artifact` skill (adopt near-verbatim):

- **Artifact** (existing skill, reuse as-is): 1) caught mid-use, 2) human gesture implying ritual (2b: painterly half-figure portrait variant), 3) material duality as concept, 4) minimal iconic object, 5) window into a wider world.
- **Creature**: modes driven by pose + subtype anatomy (e.g. mid-combat action, static dominant-pose portrait for legendaries, transformation/corruption-in-progress, group/swarm). Subtype fidelity is mandatory here — an Angel Horror must visibly read as both, never erasing one for the other.
- **Instant/Sorcery**: no meaningful subtypes; modes driven by **role** — removal, counterspell, board wipe, card draw, ramp, tutor, pump/protection, reanimation, burn. Each role gets its own decisive-moment convention (e.g. removal = the exact instant of exile/destruction, counterspell = the spell being caught/unraveled mid-flight).
- **Enchantment**: modes by subtype — Aura (worn/bound to a chosen subject), Saga (a chapter-moment vignette), Curse (affliction taking hold), Class/Room (structural/spatial motif), global enchantments (world-altering wide shot).
- **Land**: modes by scale — wide establishing shot with small/absent figures (basics, named locations), utility land close on a specific feature, legendary location as an iconic landmark shot.
- **Planeswalker/Battle**: rarer types, fewer samples expected — modes center on the character's iconic pose/ability-in-use (planeswalker) or the contested-territory moment (battle, siege-in-progress).

## Naming rules (`naming/SKILL.md`)

Carried over from the original spec, plus one resolved gap:

- 2-5 words, native to the theme's vocabulary.
- Derived from the card's role in the oracle text, not just its type.
- Never reuse the original MTG card name.
- Unique across the deck.
- Basic lands: each copy gets a distinct named location within its faction.
- Same faction reads consistent in naming style across its cards.
- **Canonical-name collision** (two cards both plausibly map to the same theme-canon character, e.g. two cards both evoke "Aragorn"): **first-claim wins** — whichever card is processed first (decklist order, or the card most central to the commander's story if tied) gets the bare canonical name; every other card mapping to that character gets an epithet/title variant of the same character (e.g. "Aragorn, Ranger of the North," "Strider's Blade," "Oath of the Ranger-King") rather than a fully different name — keeps the connection to the character legible without violating uniqueness.

## Corpus strategy

- **Creature type**: full Scryfall sampling as originally scoped (15-25 arts per color, key subtypes sampled directly), built first — largest and most subtype-heavy type.
- **All other types**: reduced sample size (~8-10 per cell) rather than full depth, to control upfront cost; accepted trade-off is lower fidelity on rare cells (battle, planeswalker) in this first pass.
- **`reference/user-prompts.md`**: Rodrigo's 24 existing proven Midjourney prompts, kept verbatim, annotated against the shared skeleton above — this is stronger ground truth than Scryfall-derived descriptions alone and is the primary source for the shared skeleton's rules (diegetic lighting, framing percentages, palette discipline, banned-word exception, body-part gotcha, character-bible reuse pattern all originate here).
- Scryfall sampling queries follow the original rules: `year>=2010`, half by `order=usd`, half by `order=released`, `unique=art`, excluding digital/promo/funny and showcase/crossover treatments that depart from standard Magic art.

## Output format

Unchanged from the original spec — JSON array per card:
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
`prompt` follows the shared skeleton + type mode + `--ar 5:7` suffix. `pinterest` (5 short search queries: subject, composition/pose, lighting, textures/props, environment) included when mode is `pinterest` or `both`; omit fields per mode.

## Quality gate (before returning any batch)

For every card, verify:
- Name is unique, fits theme vocabulary, and resolves any canonical-collision per the tiebreak rule.
- Art direction matches the card's role and (for creatures) subtype fidelity.
- A decisive moment and a specific unique detail are both present.
- No banned words outside the single allowed terminal atmosphere tag.
- A physical, named light source with stated falloff is present.
- Framing includes the explicit 20-65% band language.
- Prompt reflects the deck lore doc's relevant faction, not a generic theme-level reskin.

Rewrite before output if any check fails.

## Build order

1. `scripts/scryfall_batch.py`.
2. `art-template/SKILL.md` (shared skeleton, derived from `user-prompts.md` analysis).
3. `creature/SKILL.md` with full corpus + `reference/corpus-notes.md`.
4. `artifact/SKILL.md` — port from existing `anthropic-skills:mtg-artifact-card-art` skill.
5. Remaining type skills (reduced corpus).
6. `naming/SKILL.md`, `theme-bible/SKILL.md`.
7. `themes/lord-of-the-rings.md` as worked example.
8. `SKILL.md` orchestrator wiring the full pipeline, including deck lore doc + faction ledger logic.
9. Test run: reskin a 10-card sample covering every type, both modes, checked against the quality gate.

## Open items deferred past this spec

- Whether inter-faction relations in the deck lore doc should default to theme-canon-first (e.g. real LOTR lore for how factions relate) versus invented-per-deck was raised but not resolved — default to theme-canon-first where the theme has an established answer, invent only where the theme is silent, and flag this explicitly in `theme-bible/SKILL.md` for the builder to decide per theme.
- Split cards, MDFCs, and Adventure cards have two names/two faces; `naming/SKILL.md` needs an explicit rule for these once encountered in a real test deck — not designed here since no sample deck has surfaced one yet.
