# MTG Theme Reskin Environment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code skill environment (`/mtg-reskin/`) that reskins an MTG decklist into a chosen theme, producing per-card names and Midjourney-ready art prompts grounded in real MTG art conventions and the specific deck's own worldbuilding.

**Architecture:** One thin Python script does the only real "application code" (a single batched Scryfall lookup). Everything else is markdown skill content: a shared art-direction skeleton, per-card-type skills that plug into it, a naming skill, a theme-bible skill, and an orchestrator skill that runs the pipeline (parse → enrich → theme bible → deck lore doc → faction ledger → batched card processing → JSON output).

**Tech Stack:** Python 3 (stdlib `urllib`/`json` only — no dependencies to install) for the Scryfall script; Markdown for all skills; this is invoked as a Claude Code skill, not a standalone app.

**Spec:** `docs/superpowers/specs/2026-09-23-mtg-theme-reskin-design.md` — read this first, it's the source of truth for every content requirement below.

---

### Task 1: Scryfall batch enrichment script

**Files:**
- Create: `mtg-reskin/scripts/scryfall_batch.py`
- Test: `mtg-reskin/scripts/test_scryfall_batch.py`

- [ ] **Step 1: Write the failing test for decklist parsing**

```python
# mtg-reskin/scripts/test_scryfall_batch.py
import unittest
from scryfall_batch import parse_decklist

class TestParseDecklist(unittest.TestCase):
    def test_parses_quantity_and_name(self):
        text = "1 Sol Ring\n2 Swamp\n1 Kaalia of the Vast"
        result = parse_decklist(text)
        self.assertEqual(
            result,
            [
                {"quantity": 1, "name": "Sol Ring"},
                {"quantity": 2, "name": "Swamp"},
                {"quantity": 1, "name": "Kaalia of the Vast"},
            ],
        )

    def test_skips_blank_lines_and_comments(self):
        text = "1 Sol Ring\n\n// Commander\n1 Kaalia of the Vast\n"
        result = parse_decklist(text)
        self.assertEqual(
            result,
            [
                {"quantity": 1, "name": "Sol Ring"},
                {"quantity": 1, "name": "Kaalia of the Vast"},
            ],
        )

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd mtg-reskin/scripts && python3 -m pytest test_scryfall_batch.py -v`
Expected: FAIL with `ImportError: cannot import name 'parse_decklist'` (file doesn't exist yet)

- [ ] **Step 3: Write `parse_decklist`**

```python
# mtg-reskin/scripts/scryfall_batch.py
import json
import re
import sys
import urllib.request

SCRYFALL_COLLECTION_URL = "https://api.scryfall.com/cards/collection"
USER_AGENT = "mtg-reskin/1.0"


def parse_decklist(text: str) -> list[dict]:
    """Parse Moxfield-style export text into [{quantity, name}, ...]."""
    entries = []
    line_re = re.compile(r"^(\d+)\s+(.+?)\s*$")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("#"):
            continue
        match = line_re.match(line)
        if not match:
            continue
        quantity, name = match.groups()
        entries.append({"quantity": int(quantity), "name": name})
    return entries
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd mtg-reskin/scripts && python3 -m pytest test_scryfall_batch.py -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Write the failing test for batching into groups of 75**

Scryfall's `/cards/collection` endpoint accepts at most 75 identifiers per request — this test locks that limit in.

```python
# append to test_scryfall_batch.py
from scryfall_batch import chunk_identifiers

class TestChunkIdentifiers(unittest.TestCase):
    def test_chunks_into_groups_of_75(self):
        names = [{"name": f"Card {i}"} for i in range(160)]
        chunks = list(chunk_identifiers(names))
        self.assertEqual(len(chunks), 3)
        self.assertEqual(len(chunks[0]), 75)
        self.assertEqual(len(chunks[1]), 75)
        self.assertEqual(len(chunks[2]), 10)
```

- [ ] **Step 6: Run test to verify it fails**

Run: `cd mtg-reskin/scripts && python3 -m pytest test_scryfall_batch.py -v`
Expected: FAIL with `ImportError: cannot import name 'chunk_identifiers'`

- [ ] **Step 7: Write `chunk_identifiers`**

```python
# append to scryfall_batch.py
def chunk_identifiers(identifiers: list[dict], size: int = 75):
    for i in range(0, len(identifiers), size):
        yield identifiers[i : i + size]
```

- [ ] **Step 8: Run test to verify it passes**

Run: `cd mtg-reskin/scripts && python3 -m pytest test_scryfall_batch.py -v`
Expected: PASS (3 tests)

- [ ] **Step 9: Write `fetch_collection` (one POST per chunk) and `enrich_decklist` (orchestrates parse → chunk → fetch → merge), plus CLI entrypoint**

```python
# append to scryfall_batch.py
def fetch_collection(identifiers: list[dict]) -> list[dict]:
    """POST one chunk (<=75 identifiers) to /cards/collection, return card objects."""
    payload = json.dumps({"identifiers": identifiers}).encode("utf-8")
    request = urllib.request.Request(
        SCRYFALL_COLLECTION_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        body = json.loads(response.read())
    return body.get("data", [])


def enrich_decklist(decklist_text: str) -> list[dict]:
    """Parse decklist, batch-fetch Scryfall data, return one enriched record per card entry."""
    entries = parse_decklist(decklist_text)
    identifiers = [{"name": entry["name"]} for entry in entries]

    by_name = {}
    for chunk in chunk_identifiers(identifiers):
        for card in fetch_collection(chunk):
            by_name[card["name"].lower()] = card

    enriched = []
    for entry in entries:
        card = by_name.get(entry["name"].lower(), {})
        enriched.append(
            {
                "quantity": entry["quantity"],
                "name": entry["name"],
                "type_line": card.get("type_line", ""),
                "color_identity": card.get("color_identity", []),
                "mana_value": card.get("cmc"),
                "oracle_text": card.get("oracle_text", ""),
                "keywords": card.get("keywords", []),
            }
        )
    return enriched


if __name__ == "__main__":
    decklist_text = sys.stdin.read()
    result = enrich_decklist(decklist_text)
    json.dump(result, sys.stdout, indent=2)
```

- [ ] **Step 10: Manual smoke test against the real API**

Run:
```bash
cd mtg-reskin/scripts && printf "1 Sol Ring\n1 Kaalia of the Vast\n" | python3 scryfall_batch.py
```
Expected: JSON array of 2 objects, each with a non-empty `type_line` (e.g. `"Artifact"` for Sol Ring, `"Legendary Creature — Human Cleric"` for Kaalia).

- [ ] **Step 11: Commit**

```bash
git add mtg-reskin/scripts/scryfall_batch.py mtg-reskin/scripts/test_scryfall_batch.py
git commit -m "$(cat <<'EOF'
Add Scryfall batch enrichment script for mtg-reskin

Single POST to /cards/collection per <=75 cards, replacing what
would otherwise be one Scryfall request per card in the deck.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Shared art-direction skeleton (`art-template/SKILL.md`)

**Files:**
- Create: `mtg-reskin/skills/art-template/SKILL.md`
- Reference: `mtg-reskin/reference/user-prompts.md` (created in Task 3, but content for this task is drawn from the 24 prompts already in the design spec)

- [ ] **Step 1: Write `art-template/SKILL.md`**

This file has no code to test — it's the shared skeleton every type skill inherits. It must contain each of the following as its own labeled subsection, using this exact content (from spec section "Shared art-direction skeleton"):

1. **Who/What/Why/Where brief** — run silently before drafting any prompt:
   - Who: decide if a figure/hand/implied second party belongs in frame, or the object/scene carries itself alone.
   - What: name the specific frozen moment. Never describe the subject at rest.
   - Why: the visual metaphor must map onto the card's actual mechanic or the deck's lore.
   - Where: setting + a diegetic light source, positioned per the framing rule below.

2. **Diegetic lighting rule**: name the physical light source explicitly (candle, spell glow, moonlight, forge fire, energy burst — never "dramatic lighting"). State falloff explicitly: what stays legible near the source, what recedes to shadow/haze further away. When two magic effects/colors share the frame, state they are kept visually distinct.

3. **Intricacy rule**: give the subject visible history — engraved micro-narrative, wear pattern, an unusual material choice — so it rewards a second look, not just a first glance.

4. **Palette discipline**: 2-3 dominant colors, stated as an explicit short list (e.g. "deep reds, aged gold, near-black shadows"). Never open-ended ("vibrant colors").

5. **Framing for card crop** — use this exact phrasing pattern in every prompt:
   > "composition composed so the [subject/most detailed part] sits within the vertical middle band of the frame, roughly between 20% and 65% down from the top, well clear of both the top 15% and bottom 35% of the image — [upper area] fading into plain dark atmosphere, expendable space meant to be cropped by the title bar; [lower area] fading into shadow, expendable space meant to be cropped by the text box."

6. **Framing tightness**: default to close-up/medium-tight with a visible pocket of dim surrounding environment. Not extreme/edge-to-edge close-up — leave room for the crop to eat into.

7. **Body-part continuity gotcha**: if a figure's own limb is transforming or fused with an object, describe it as one continuous part. Never phrase it as "gripping/holding" a separate object, or the model reads two distinct objects.

8. **Banned words**: epic, majestic, dramatic, stunning, breathtaking, mystical, ethereal, awe-inspiring — banned as mid-scene description. Exception: allowed once, as a single terminal atmosphere tag at the very end of the prompt (e.g. "...card art style, epic isolated atmosphere, high detail").

9. **Closing suffix**, fixed per deck:
   `Painterly digital fantasy illustration, Magic: The Gathering [artifact] card art style, [2-4 word atmosphere tag], high detail. --ar 5:7`
   Add `--no <specific clutter terms>` only when several generations have converged on the same unwanted clutter — never as a default parameter.

10. **No literal text, card frames, borders, or UI in the described art. No named living artists — style comes from the conventions above, not an artist name.**

Each type skill (Tasks 4-11) references this file and adds only its own compositional-mode taxonomy — it must not restate the 10 rules above.

- [ ] **Step 2: Verify against the design spec**

Open `docs/superpowers/specs/2026-09-23-mtg-theme-reskin-design.md`, section "Shared art-direction skeleton (`art-template/SKILL.md`)". Confirm all 11 numbered points in the spec are present as their own subsection in the file just written (spec has 11 points; this task's Step 1 lists 10 because point 11 in the spec — "no literal text/frames/UI, no named artists" — is combined here as one item; keep it as two sentences under one heading, that's fine, but do not drop the "no named artists" clause).

- [ ] **Step 3: Commit**

```bash
git add mtg-reskin/skills/art-template/SKILL.md
git commit -m "$(cat <<'EOF'
Add shared art-direction skeleton skill for mtg-reskin

Encodes the diegetic-lighting, framing-percentage, palette-discipline,
and banned-word rules every card-type skill inherits, derived from
Rodrigo's proven Midjourney prompt corpus.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Annotated user-prompt corpus (`reference/user-prompts.md`)

**Files:**
- Create: `mtg-reskin/reference/user-prompts.md`

- [ ] **Step 1: Write the file**

Contains all 24 of Rodrigo's original prompts (from this conversation), each followed by a one-line annotation naming which numbered rule from `art-template/SKILL.md` it best demonstrates. Structure:

```markdown
# User Prompt Corpus — Annotated

Source of truth for the shared art-template skeleton. Each entry is a
proven Midjourney prompt, annotated with the art-template rule it best
demonstrates.

## 1. The Gilded Chalice (devil's gift)

> [full prompt text verbatim]

Demonstrates: diegetic lighting (single unseen candle, explicit near/far
falloff on the chalice rim), 2-3 color palette, intricacy rule (engraved
frieze of tiny relief figures).

## 2. Wax-seal scroll (extreme close-up)

> [full prompt text verbatim]

Demonstrates: framing tightness — this is the one prompt that goes
edge-to-edge ("no faces, no room, nothing else in frame") rather than
medium-tight; note as the exception, not the default, when writing the
framing-tightness rule.

...
```

Continue for all 24 prompts in order, pulling the verbatim text from this conversation's transcript. Each of the 5 Ob Nixilis prompts gets annotated as demonstrating the **character-bible reuse pattern** (near-verbatim physical description repeated, only the action/mode clause changes).

- [ ] **Step 2: Commit**

```bash
git add mtg-reskin/reference/user-prompts.md
git commit -m "$(cat <<'EOF'
Add annotated user-prompt corpus for mtg-reskin

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Artifact type skill (port existing skill)

**Files:**
- Create: `mtg-reskin/skills/artifact/SKILL.md`
- Read: `/Users/rodgz_mac/.claude/skills/synced/95820aee-57e2-4ff4-aa04-35aa5332ad2b_1548cc23-11bc-4534-8410-e0dc970dda4e/mtg-artifact-card-art/SKILL.md`

- [ ] **Step 1: Read the existing skill file in full**

Run: read the file at the path above.

- [ ] **Step 2: Write `mtg-reskin/skills/artifact/SKILL.md`**

Port the content near-verbatim, with two edits:
1. Add a header line: `> Built on skills/art-template/SKILL.md — see that file for the shared lighting/framing/palette/banned-word rules. This file adds only the artifact-specific compositional modes below.`
2. Remove the "Technical settings currently in use" section's `--style raw --v 6.1` and `--chaos 10-20` lines (confirmed not in use); keep the `--ar 5:7`, the `--no` negative-list guidance, the palette-discipline line, the anti-repeated-near-black-phrasing line, and the body-part-continuity line (these last two are now also in `art-template/SKILL.md` — keep them here too since Steps 3-5 of the original artifact skill reference them in artifact-specific context, this is acceptable duplication for a ported reference skill, not new authoring).

Keep the 5 compositional modes (caught mid-use, human gesture/2b portrait variant, material duality, minimal iconic object, window into a wider world) and the Who/What/Why/Where step exactly as written.

- [ ] **Step 3: Commit**

```bash
git add mtg-reskin/skills/artifact/SKILL.md
git commit -m "$(cat <<'EOF'
Port artifact card art skill into mtg-reskin

Adapted from the existing mtg-artifact-card-art skill, pointed at
the new shared art-template skeleton, technical-settings section
trimmed to match confirmed Midjourney params (--ar 5:7 only).

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Creature type skill + corpus

**Files:**
- Create: `mtg-reskin/skills/creature/SKILL.md`
- Create: `mtg-reskin/reference/corpus-notes.md`

- [ ] **Step 1: Sample the corpus**

For each color (W, U, B, R, G, multicolor, colorless), run two Scryfall searches and record results:
```
https://api.scryfall.com/cards/search?q=t:creature+c:w+year>=2010+-is:digital+-is:promo+-st:funny&unique=art&order=usd&dir=desc
https://api.scryfall.com/cards/search?q=t:creature+c:w+year>=2010+-is:digital+-is:promo+-st:funny&unique=art&order=released&dir=desc
```
(repeat `c:w` → `c:u`, `c:b`, `c:r`, `c:g`, and use `q=t:creature+c>=2+year>=2010...` for multicolor, `q=t:creature+id=c+year>=2010...` for colorless). Target 15-25 unique arts per color after merging both sort orders and de-duplicating. Respect ~50-100ms between requests.

Also sample key subtypes directly, one query each: `t:angel`, `t:demon`, `t:devil`, `t:vampire`, `t:zombie`, `t:skeleton`, `t:spirit`, `t:horror`, `t:eldrazi`, `t:phyrexian`, `t:dragon`, `t:sphinx`, `t:hydra`, `t:elemental`, `t:beast`, `t:dinosaur`, `t:elf`, `t:goblin`, `t:merfolk`, `t:faerie`, `t:giant`, `t:dwarf`, `t:human+t:knight`, `t:human+t:soldier`, `t:human+t:cleric`, `t:human+t:wizard`, `t:human+t:rogue`, `t:human+t:warrior`, `t:human+t:shaman`, `t:human+t:noble`, `t:human+t:assassin`, `t:construct`, `t:golem`, `t:insect` — each with `year>=2010 -is:digital -is:promo&unique=art&order=usd&dir=desc`, ~10-15 arts each.

For each sampled art, view the `image_uris.art_crop` image and record (never copy the image itself): subject/action, decisive moment shown, composition, light source(s), palette, materials/textures, the one specific unmistakable detail, how the art shows the mechanic.

- [ ] **Step 2: Write `mtg-reskin/reference/corpus-notes.md`**

Record: the exact queries run, the date run, and the count of unique arts collected per color and per subtype cell. Flag any cell that came in under 10 arts (expected for rare subtype/color combos) as low-confidence.

- [ ] **Step 3: Write `mtg-reskin/skills/creature/SKILL.md`**

Header line: `> Built on skills/art-template/SKILL.md.` Then, distilled from the corpus (not a list of cards):
- One subsection per color: palette tendencies, recurring materials, typical lighting register, emotional register — plus 3-5 short worked art-direction examples per color.
- One subsection per sampled subtype: anatomy/silhouette conventions, signature features, what visually separates it from its nearest-neighbor subtype (e.g. Angel vs. Horror, Eldrazi vs. Phyrexian) — plus 3-5 worked examples.
- A **hybrid-subtype rule**: when a creature has multiple subtypes (Angel Horror, Vampire Knight, Zombie Dragon), the art must visibly combine both signature features — never let one erase the other.
- A **compositional-mode list** (per the design spec's per-type taxonomy requirement): at minimum, (1) mid-combat action, (2) static dominant pose for legendary/singular creatures, (3) transformation/corruption-in-progress, (4) group/swarm composition. Each mode gets a 2-3 sentence description of when to use it.
- **Subtype fidelity is mandatory**: state explicitly that subtype visual cues are non-negotiable, cross-reference the art-template's intricacy rule.

- [ ] **Step 4: Commit**

```bash
git add mtg-reskin/skills/creature/SKILL.md mtg-reskin/reference/corpus-notes.md
git commit -m "$(cat <<'EOF'
Add creature card art skill + corpus notes for mtg-reskin

Full-depth Scryfall sampling per color and per key subtype, per the
design spec's decision to build creature (largest, most subtype-heavy
type) at full depth first.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Instant + Sorcery type skills (role-based, reduced corpus)

**Files:**
- Create: `mtg-reskin/skills/instant/SKILL.md`
- Create: `mtg-reskin/skills/sorcery/SKILL.md`

- [ ] **Step 1: Sample reduced corpus**

For each of the two types, run one query per color (skip the double usd/released split — single `order=usd&dir=desc` pass is enough at reduced depth): `q=t:instant+c:w+year>=2010+-is:digital+-is:promo+-st:funny&unique=art&order=usd&dir=desc` etc. Target 8-10 arts per color per type. Record findings inline in each skill file's "worked examples," no separate corpus-notes entry needed at this depth.

- [ ] **Step 2: Write `mtg-reskin/skills/instant/SKILL.md`** and **Step 3: Write `mtg-reskin/skills/sorcery/SKILL.md`**

Header line: `> Built on skills/art-template/SKILL.md.` Both files organize by **role**, not subtype (instants/sorceries have no meaningful subtypes, per design spec): removal, counterspell, board wipe, card draw, ramp, tutor, pump/protection, reanimation, burn. For each role: 1) the decisive-moment convention specific to that role (e.g. removal = the exact instant of exile/destruction; counterspell = the spell being caught/unraveled mid-flight; board wipe = the wave of effect crossing the whole board), 2) a per-color palette/lighting note where the role's color matters, 3) 2-3 worked examples.

- [ ] **Step 4: Commit**

```bash
git add mtg-reskin/skills/instant/SKILL.md mtg-reskin/skills/sorcery/SKILL.md
git commit -m "$(cat <<'EOF'
Add instant and sorcery card art skills for mtg-reskin

Role-based organization (removal, counterspell, board wipe, etc.)
since these types have no meaningful subtypes; reduced-depth corpus
per the design spec's cost trade-off for non-creature types.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Enchantment type skill (subtype-based, reduced corpus)

**Files:**
- Create: `mtg-reskin/skills/enchantment/SKILL.md`

- [ ] **Step 1: Sample reduced corpus**

One query per subtype at reduced depth (8-10 arts each): `t:aura`, `t:saga`, `t:curse`, `t:class`, `t:room`, `t:shrine`, and a general `t:enchantment -t:aura -t:saga -t:curse -t:class -t:room` pass for global/world-altering enchantments — each with `year>=2010 -is:digital -is:promo&unique=art&order=usd&dir=desc`.

- [ ] **Step 2: Write `mtg-reskin/skills/enchantment/SKILL.md`**

Header line: `> Built on skills/art-template/SKILL.md.` One subsection per subtype: Aura (the worn/bound-to-a-subject moment), Saga (a chapter-moment vignette — note this may need 2-3 chapter beats described separately), Curse (affliction taking hold), Class/Room (structural/spatial motif), global enchantments (world-altering wide shot). 2-3 worked examples per subsection.

- [ ] **Step 3: Commit**

```bash
git add mtg-reskin/skills/enchantment/SKILL.md
git commit -m "$(cat <<'EOF'
Add enchantment card art skill for mtg-reskin

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 8: Land type skill (scale-based, reduced corpus)

**Files:**
- Create: `mtg-reskin/skills/land/SKILL.md`

- [ ] **Step 1: Sample reduced corpus**

Queries at reduced depth: `t:land+t:basic`, `t:land+-t:basic+-is:funny` filtered to legendary lands via `is:legendary+t:land`, and a general non-basic utility-land pass — 8-10 arts each, `year>=2010 -is:digital -is:promo&unique=art&order=usd&dir=desc`.

- [ ] **Step 2: Write `mtg-reskin/skills/land/SKILL.md`**

Header line: `> Built on skills/art-template/SKILL.md.` Note that the framing-percentage rule from art-template still applies, but lands more often have **no figure at all** or a small distant one — state this explicitly as the land-specific override of the Who/What/Why/Where "Who" step. Three modes: (1) wide establishing shot, small/absent figures (basics, named locations), (2) utility land close on one specific feature, (3) legendary location as an iconic landmark shot. 2-3 worked examples per mode.

- [ ] **Step 3: Commit**

```bash
git add mtg-reskin/skills/land/SKILL.md
git commit -m "$(cat <<'EOF'
Add land card art skill for mtg-reskin

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 9: Planeswalker + Battle type skills (rare types, minimal corpus)

**Files:**
- Create: `mtg-reskin/skills/planeswalker/SKILL.md`
- Create: `mtg-reskin/skills/battle/SKILL.md`

- [ ] **Step 1: Sample minimal corpus**

`t:planeswalker+year>=2010+-is:digital+-is:promo&unique=art&order=released&dir=desc` and `t:battle+year>=2010+-is:digital+-is:promo&unique=art&order=released&dir=desc` — take whatever comes back (battle is a small, recent card type; expect well under 25 total unique arts). No color split needed at this volume — pool all colors together and note color as a per-example detail instead.

- [ ] **Step 2: Write `mtg-reskin/skills/planeswalker/SKILL.md`**

Header line: `> Built on skills/art-template/SKILL.md.` Mode: character's iconic pose/ability-in-use, always a static dominant-pose portrait (planeswalkers are always a specific named character — never a generic figure). 3-5 worked examples pooled across colors.

- [ ] **Step 3: Write `mtg-reskin/skills/battle/SKILL.md`**

Header line: `> Built on skills/art-template/SKILL.md.` Mode: contested-territory moment — the siege/assault in progress, camera positioned to show both attacking and defending sides implied in frame. 3-5 worked examples.

- [ ] **Step 4: Commit**

```bash
git add mtg-reskin/skills/planeswalker/SKILL.md mtg-reskin/skills/battle/SKILL.md
git commit -m "$(cat <<'EOF'
Add planeswalker and battle card art skills for mtg-reskin

Minimal corpus depth — both are small/recent card types with limited
real-art sample pools available on Scryfall.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 10: Naming skill

**Files:**
- Create: `mtg-reskin/skills/naming/SKILL.md`

- [ ] **Step 1: Write `mtg-reskin/skills/naming/SKILL.md`**

Must contain, verbatim in substance from the design spec's "Naming rules" section:
- 2-5 words, native to the theme's vocabulary.
- Derived from the card's role in the oracle text, not just its type (worked example: "Swords to Plowshares" → a name about merciful exile, not "Sword of X").
- Never reuse the original MTG card name.
- Unique across the deck.
- Basic lands: each copy gets a distinct named location within its faction.
- Same faction reads consistent in naming style across its cards.
- **Canonical-name collision rule**: first-claim wins (decklist order, or the card most central to the commander's story if tied) gets the bare canonical name; every other card mapping to that same character gets an epithet/title variant of that character (worked example: "Aragorn" claimed by one card; others become "Aragorn, Ranger of the North," "Strider's Blade," "Oath of the Ranger-King" — never a fully unrelated name for the same evoked character).

- [ ] **Step 2: Commit**

```bash
git add mtg-reskin/skills/naming/SKILL.md
git commit -m "$(cat <<'EOF'
Add naming skill for mtg-reskin

Includes the first-claim-wins tiebreak rule for canonical-name
collisions between cards that evoke the same theme character.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 11: Theme-bible skill

**Files:**
- Create: `mtg-reskin/skills/theme-bible/SKILL.md`

- [ ] **Step 1: Write `mtg-reskin/skills/theme-bible/SKILL.md`**

Explains how to build `/themes/<theme>.md` for any theme. Must specify each required section a theme bible must contain:
- **Color → faction/region map** (one line per color + multicolor + colorless).
- **Card type → motif map** (artifacts = forged relics, enchantments = oaths/wards/curses, lands = named locations, etc.).
- **Subtype translation table**: how each sampled MTG subtype (from `creature/SKILL.md`'s subtype list) exists in this world, keeping the subtype's visual essence intact.
- **Naming vocabulary**: language flavor, naming patterns, roots.
- **Deck anchor guidance**: how a commander's colors/subtypes should be read as the "central" faction when the deck lore doc (built by the orchestrator, Task 12) auto-detects factions.
- **Inter-faction relations default**: per the design spec's deferred item, instruct the builder to default to **theme-canon-first** relations (use the real setting's established lore for how factions relate) and only invent relations where the theme is silent — flag this choice explicitly when building a new theme bible.

This skill is deliberately about *process*, not a specific theme's content — Task 12 uses it to produce the LOTR bible.

- [ ] **Step 2: Commit**

```bash
git add mtg-reskin/skills/theme-bible/SKILL.md
git commit -m "$(cat <<'EOF'
Add theme-bible skill for mtg-reskin

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 12: Lord of the Rings theme bible (worked example)

**Files:**
- Create: `mtg-reskin/themes/lord-of-the-rings.md`

- [ ] **Step 1: Write `mtg-reskin/themes/lord-of-the-rings.md`** following the structure defined in Task 11's theme-bible skill

Content, per the design spec's worked-example starting point:
- Color → faction map: W → Gondor / elves of light, U → Rivendell / wizards / the sea, B → Mordor / Nazgûl / the Barrow, R → dwarves / Balrog / dragons, G → Ents / the Shire / Rohan's plains, multicolor → alliances/border regions, colorless → ancient relics and forgotten works.
- Card type → motif map: artifacts = forged relics, enchantments = oaths/wards/curses, lands = named locations from the setting.
- Subtype translation table covering at minimum every subtype listed in `creature/SKILL.md`'s sampled list (e.g. Angel → Maia-like radiant beings, Zombie → Barrow-wights or the Dead Men of Dunharrow, Eldrazi → Morgoth-era horrors from the deep, Demon → Balrog-kin, Dragon → literal Middle-earth dragons, Elf/Human/Dwarf → direct 1:1 mapping).
- Naming vocabulary: Sindarin/Westron-flavored naming patterns and example roots.
- Deck anchor guidance applied: note that a Fellowship-anchored deck reads differently from a Sauron/Mordor-anchored deck even with identical card pools — the commander decides which faction is "home."
- Inter-faction relations: theme-canon-first (real LOTR lore governs how Gondor/Rohan/Mordor/etc. relate), per Task 11's default rule.

- [ ] **Step 2: Commit**

```bash
git add mtg-reskin/themes/lord-of-the-rings.md
git commit -m "$(cat <<'EOF'
Add Lord of the Rings theme bible as worked example for mtg-reskin

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 13: Orchestrator skill

**Files:**
- Create: `mtg-reskin/SKILL.md`

- [ ] **Step 1: Write `mtg-reskin/SKILL.md`**

Must specify the full pipeline as concrete, orderable steps (per design spec "Pipeline" section):

1. Parse decklist text (user-pasted Moxfield export).
2. Run `scripts/scryfall_batch.py` (pipe decklist text to stdin, capture JSON stdout) — one call for the whole deck.
3. Load `themes/<theme>.md`. If missing, invoke `skills/theme-bible/SKILL.md` and pause for human review of the generated bible before continuing — this step is never silent.
4. Build the **deck lore doc**:
   - From the enriched card list, count subtype occurrences (parse from `type_line`, e.g. "Legendary Creature — Human Cleric" → subtypes `Human`, `Cleric`).
   - Any subtype with count ≥3, or any subtype shared with the commander's own type line, becomes a faction candidate.
   - For each faction candidate, look up its entry in the loaded theme bible's subtype translation table; expand into identity/territory/want (1 short paragraph).
   - Add 1 paragraph stating how all detected factions relate to the commander (serves/opposes/bound-by) and to each other, using the theme bible's inter-faction-relations guidance (theme-canon-first per Task 11).
5. Initialize the **faction ledger** as an empty structure: `{faction_name: {names: [], vocabulary: [], motifs: [], palette: []}}`, plus a separate `{character_name: description_block}` map for legendary-card character bibles, populated as cards are processed.
6. Split the enriched card list into batches of ~20.
7. For each batch: pass the deck lore doc (constant), current faction ledger, and the running list of already-used `new_name` values into context; process each card in the batch by (a) routing to its type skill based on `type_line`'s primary type — creature takes priority if "Creature" appears anywhere in the type line, per the design spec's multi-type handling — (b) applying `skills/naming/SKILL.md` including the collision tiebreak, (c) applying the routed type skill's compositional modes on top of `skills/art-template/SKILL.md`. After the batch, append any new names/vocabulary/motifs/palette entries and any new character-bible entries to the ledger.
8. Emit one JSON object per card per the Output format below; collect into a single array for the full deck.

Also specify:
- **Output modes**: `prompt` (only `prompt` field populated, `pinterest` omitted), `pinterest` (only `pinterest` field, `prompt` omitted), `both` (both present).
- **Output format** (copy exactly from spec):
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
- **Quality gate**, run before returning any batch's results (copy exactly from spec):
  - Name is unique, fits theme vocabulary, resolves any canonical-collision per the tiebreak rule.
  - Art direction matches the card's role and (for creatures) subtype fidelity.
  - A decisive moment and a specific unique detail are both present.
  - No banned words outside the single allowed terminal atmosphere tag.
  - A physical, named light source with stated falloff is present.
  - Framing includes the explicit 20-65% band language.
  - Prompt reflects the deck lore doc's relevant faction, not a generic theme-level reskin.
  - Rewrite before output if any check fails.

- [ ] **Step 2: Commit**

```bash
git add mtg-reskin/SKILL.md
git commit -m "$(cat <<'EOF'
Add mtg-reskin orchestrator skill

Wires decklist parsing, Scryfall enrichment, theme-bible loading,
deck lore doc + faction ledger construction, batched card routing,
and the quality gate into one pipeline.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 14: End-to-end test run

**Files:** none created — this is a manual verification pass using everything built in Tasks 1-13.

- [ ] **Step 1: Assemble a 10-card sample decklist covering every type**

Create a scratch file (not committed) with 10 cards: at least one creature, one instant, one sorcery, one artifact, one enchantment, one land, one planeswalker, and pad to 10 with any extra creatures/instants. Use a real, well-known commander with clear multi-faction subtype spread if possible (e.g. Kaalia of the Vast, matching the design spec's worked example) to exercise the deck-lore-doc faction detection.

- [ ] **Step 2: Run the orchestrator skill against the sample deck, theme = Lord of the Rings, mode = `both`**

Invoke `mtg-reskin/SKILL.md`'s pipeline manually, following its steps in order, using the 10-card sample and the LOTR theme bible from Task 12.

- [ ] **Step 3: Check every output card against the quality gate in `mtg-reskin/SKILL.md`**

For each of the 10 output cards, verify all 7 quality-gate checks pass. Any failure means the corresponding type skill or the orchestrator step that produced it needs a fix — go back and correct the relevant skill file, not just the one bad output.

- [ ] **Step 4: Verify deck-lore-doc faction detection worked as designed**

Confirm the output's per-card `faction` field correctly groups cards by the auto-detected factions (e.g. if using Kaalia, confirm Angels/Demons/Dragons appear as distinct factions with distinct vocabulary in their `new_name`/`prompt` fields, not homogenized).

- [ ] **Step 5: No commit for this task** (verification only — if fixes were needed in Step 3, commit those fixes individually with a message describing what was wrong, e.g. `git commit -m "fix: creature skill missing hybrid-subtype rule application in test run"`)

---

## Self-review notes

- **Spec coverage**: every numbered section of the design spec (architecture, pipeline steps 1-9, shared skeleton points 1-11, per-type mode taxonomies for all 8 types, naming rules + collision tiebreak, corpus strategy for creature vs. reduced types, output format, quality gate, build order) maps to a task above. The two "Open items deferred" in the spec are resolved concretely in Task 11 (theme-canon-first default) and left correctly unaddressed for split/MDFC cards (no task references them, since the spec explicitly deferred that until a real test deck surfaces one — Task 14's sample deck should avoid split/MDFC cards for this reason).
- **Type consistency**: `scryfall_batch.py`'s `enrich_decklist` output keys (`quantity`, `name`, `type_line`, `color_identity`, `mana_value`, `oracle_text`, `keywords`) are the same keys Task 13's orchestrator step 4 reads from (`type_line` for subtype parsing). Output JSON field names in Task 13 match the design spec's Output format section exactly.
- **No placeholders**: every task specifies exact file paths and either runnable code (Task 1) or the concrete required content/subsections (Tasks 2-13, each quoting the spec's own already-concrete language rather than saying "add appropriate content").
