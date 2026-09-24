# Corpus Notes — Creature Art Sampling (Scryfall)

Source material behind `mtg-reskin/skills/creature/SKILL.md`. Date run: **2026-09-23**.

## Methodology

For each of 7 colors and 34 creature subtypes, ran Scryfall `cards/search` queries (`unique=art`, creatures printed 2010 or later, excluding digital-only, promo, and joke/`-st:funny` cards). Colors were queried twice (`order=usd` and `order=released`, merged and de-duplicated by illustration ID) per the plan; subtypes were queried once (`order=usd`) since a single page already returned far more than the 10-15 target for nearly every subtype.

**Query counts vs. viewed images — these are two different numbers, both reported honestly below:**
- **`total_cards`** = total Scryfall matches for the query (the underlying population).
- **`unique_arts` (page 1)** = distinct illustrations returned on the first results page. Scryfall paginates at ~175 results; most cells hit that cap, meaning the true unique-art count is `unique_arts` *or more* — a lower bound, not an exact total. Only devil, skeleton, sphinx, hydra, dwarf, human-shaman, human-noble, and human-assassin returned fewer than 175 (i.e., the count shown is their true total).
- **Images downloaded / actually viewed** = the representative subset (6 per color, 4 per subtype) whose `art_crop` images were downloaded and viewed with vision to distill the conventions in `creature/SKILL.md`. This is a deliberate, transparent scoping decision (per the task's own guidance) — not every one of the 68–341 arts per cell was individually viewed; a representative sample was, and the full per-cell count is recorded here regardless.

No cell fell under the 10-art low-confidence threshold on the query-count axis — every color and subtype comfortably cleared it, several by orders of magnitude (e.g. devil at 68, the smallest cell, is still well over 10).

### Universes Beyond crossover contamination and correction

The initial sample-selection filter (a name-keyword blocklist applied before download) missed several Universes Beyond crossover cards — Marvel, Final Fantasy, Assassin's Creed, Warhammer 40K, and Avatar: The Last Airbender crossover cards whose character names aren't obviously non-Magic at a glance (e.g. "Namor the Sub-Mariner," "Ezio Auditore da Firenze," "Kefka, Court Mage," "Bloodthirster"). This was caught mid-sampling and corrected: agents doing the visual distillation were instructed to identify and discount any such image from the conventions they wrote, using only the remaining legitimate original-Magic-fantasy images in that cell.

Lord of the Rings content (`LTR`/`LTC`/`HOB` sets, e.g. Aragorn, Sauron, Smaug) is arguably legitimate precedent — Rodrigo's own proven prompt corpus (`reference/user-prompts.md`, entries 11–14) is built on LOTR characters rendered in Magic's own painterly house style. In practice, the research agents applied a more conservative standard than that precedent strictly requires: several excluded LOTR/Hobbit-set cards (Sauron from Red, Multicolor, and the Horror subtype; Smaug from Red and the Dragon subtype; Aragorn from Human-Noble) as a judgment call, on the reasoning that Universes Beyond LOTR art still skews toward licensed-character-portrait conventions rather than original Magic monster-design conventions. This thinned several cells below what they'd otherwise have (see tables below); the resulting write-ups were flagged and kept conservative rather than silently patched. This is worth surfacing as a genuine judgment call rather than a settled rule — a future pass could reasonably decide to keep LOTR content and re-derive these cells with a larger effective sample.

Beyond the originally-named crossover list, the research agents also caught several additional Universes Beyond cards mid-pass on their own initiative — Astarion, the Decadent (Baldur's Gate 3/D&D) in Vampire; Lulu, Stern Guardian (Final Fantasy) in Human-Wizard; Atla Palani, Nest Tender (a Jurassic World cameo) in Human-Shaman; and an additional Final Fantasy exclusion (Terra, Herald of Hope) in Human-Warrior beyond the two Marvel cards already flagged. All of these are recorded in the per-subtype table below with the specific card and reasoning.

This means the "images actually used" count for several cells is lower than the number downloaded — recorded transparently per cell below. **LOW-CONFIDENCE flags:** Red color (3 usable images); Human-Warrior (1 usable image — recommend re-sampling before treating its skill-file section as a settled convention rather than a hedged best-effort); Human-Assassin (2 nominal but ~1 effective, since one remaining image is an uninformative alternate-art cat portrait); Human-Noble (2 usable images with conflicting signal — one classic crowned-king image, one gothic sword-wielder with no crown — the skill file anchors on the stronger source and flags the mismatch); Human-Cleric (2 usable images, and removing the excluded cards changed the section's whole thematic direction, from devotional prayer to intimate closeness with a monstrous/divine being).

## Per-color sampling

| Color | Query | Scryfall total_cards | unique_arts (page 1) | Images downloaded | Images actually used (post crossover exclusion) | Notes |
|---|---|---|---|---|---|---|
| W | `t:creature c:w year>=2010 -is:digital -is:promo -st:funny` | 4762 | 339 | 6 | 6 | |
| U | `t:creature c:u year>=2010 -is:digital -is:promo -st:funny` | 4380 | 338 | 6 | 6 | |
| B | `t:creature c:b year>=2010 -is:digital -is:promo -st:funny` | 4644 | 341 | 6 | 6 | |
| R | `t:creature c:r year>=2010 -is:digital -is:promo -st:funny` | 4620 | 332 | 6 | **3 — LOW-CONFIDENCE (viewed sample)** | Smaug the Magnificent (HOB), Sauron the Dark Lord (LTR), Mary Read and Anne Bonny (ACR) excluded post-hoc; only 3 legit images remained (Edgar Markov, Fury, Bello, Bard of the Brambles). Conclusions kept conservative. |
| G | `t:creature c:g year>=2010 -is:digital -is:promo -st:funny` | 4852 | 337 | 6 | 6 | |
| Multicolor | `t:creature c>=2 year>=2010 -is:digital -is:promo -st:funny` | 4122 | 333 | 6 | 4 | Sauron the Dark Lord (LTR) and Mary Read and Anne Bonny (ACR) excluded post-hoc; 4 legit images remained (Edgar Markov, Ms. Bumbleflower, Bello Bard of the Brambles, Hazel of the Rootbloom). |
| Colorless | `t:creature id=c year>=2010 -is:digital -is:promo -st:funny` | 789 | 297 | 6 | 6 | |

## Per-subtype sampling

| Subtype | Query | Scryfall total_cards | unique_arts (page 1) | Images downloaded | Images actually used | Notes |
|---|---|---|---|---|---|---|
| angel | `t:angel year>=2010 -is:digital -is:promo` | 360 | 175 | 4 | 4 | |
| demon | `t:demon year>=2010 -is:digital -is:promo` | 281 | 175 | 4 | 4 | |
| devil | `t:devil year>=2010 -is:digital -is:promo` | 68 | 68 | 4 | 4 | |
| vampire | `t:vampire year>=2010 -is:digital -is:promo` | 590 | 175 | 4 | 3 | Astarion, the Decadent (Baldur's Gate 3/D&D Universes Beyond) excluded post-hoc. |
| zombie | `t:zombie year>=2010 -is:digital -is:promo` | 615 | 175 | 4 | 4 | |
| skeleton | `t:skeleton year>=2010 -is:digital -is:promo` | 82 | 82 | 4 | 4 | |
| spirit | `t:spirit year>=2010 -is:digital -is:promo` | 657 | 175 | 4 | 3 | Wan Shi Tong, Librarian (TLA) excluded post-hoc. |
| horror | `t:horror year>=2010 -is:digital -is:promo` | 411 | 175 | 4 | 3 | Sauron, the Dark Lord (LTR) excluded post-hoc (conservative judgment — see LOTR note above; this instance was excluded since Sauron's card art here is closer to a licensed-portrait treatment than original Magic horror iconography). |
| eldrazi | `t:eldrazi year>=2010 -is:digital -is:promo` | 232 | 175 | 4 | 4 | |
| phyrexian | `t:phyrexian year>=2010 -is:digital -is:promo` | 570 | 175 | 4 | 4 | |
| dragon | `t:dragon year>=2010 -is:digital -is:promo` | 627 | 175 | 4 | 3 | Smaug the Magnificent (HOB — The Hobbit) excluded post-hoc. |
| sphinx | `t:sphinx year>=2010 -is:digital -is:promo` | 117 | 117 | 4 | 4 | |
| hydra | `t:hydra year>=2010 -is:digital -is:promo` | 87 | 87 | 4 | 4 | |
| elemental | `t:elemental year>=2010 -is:digital -is:promo` | 672 | 175 | 4 | 4 | |
| beast | `t:beast year>=2010 -is:digital -is:promo` | 460 | 175 | 4 | 4 | |
| dinosaur | `t:dinosaur year>=2010 -is:digital -is:promo` | 290 | 175 | 4 | 4 | |
| elf | `t:elf year>=2010 -is:digital -is:promo` | 776 | 175 | 4 | 4 | |
| goblin | `t:goblin year>=2010 -is:digital -is:promo` | 543 | 175 | 4 | 4 | |
| merfolk | `t:merfolk year>=2010 -is:digital -is:promo` | 319 | 175 | 4 | 3 | Namor the Sub-Mariner (MSH) excluded post-hoc. |
| faerie | `t:faerie year>=2010 -is:digital -is:promo` | 188 | 175 | 4 | 4 | |
| giant | `t:giant year>=2010 -is:digital -is:promo` | 234 | 175 | 4 | 4 | |
| dwarf | `t:dwarf year>=2010 -is:digital -is:promo` | 174 | 174 | 4 | 4 | |
| human-knight | `t:human t:knight year>=2010 -is:digital -is:promo` | 327 | 175 | 4 | 3 | Celes, Rune Knight (FIC) excluded post-hoc. |
| human-soldier | `t:human t:soldier year>=2010 -is:digital -is:promo` | 555 | 175 | 4 | 3 | Captain America, Super-Soldier (MSH) excluded post-hoc. |
| human-cleric | `t:human t:cleric year>=2010 -is:digital -is:promo` | 339 | 175 | 4 | **2 — thin, borderline** | Yuna, Hope of Spira and Aerith, Last Ancient (FIN/FIC) excluded post-hoc; only Shadowborn Apostle and Kaalia of the Vast remained. |
| human-wizard | `t:human t:wizard year>=2010 -is:digital -is:promo` | 646 | 175 | 4 | 3 | Lulu, Stern Guardian (Final Fantasy) excluded post-hoc (judgment call — not on the originally-named list, but the same licensed-IP category). |
| human-rogue | `t:human t:rogue year>=2010 -is:digital -is:promo` | 265 | 175 | 4 | 3 | Locke, Treasure Hunter (FIC) excluded post-hoc. |
| human-warrior | `t:human t:warrior year>=2010 -is:digital -is:promo` | 460 | 175 | 4 | **1 — LOW-CONFIDENCE, recommend re-sampling** | Shang-Chi (Marvel), King T'Challa//Black Panther (Marvel), and Terra, Herald of Hope (Final Fantasy) all excluded post-hoc; only Fynn, the Fangbearer remained, and it reads as a masked duelist/rogue rather than a bare-armed brawler. The skill file's Human-Warrior section is written as a hedged best-effort and flagged for follow-up sampling rather than treated as a confident convention. |
| human-shaman | `t:human t:shaman year>=2010 -is:digital -is:promo` | 172 | 172 | 4 | 3 | Atla Palani, Nest Tender (Jurassic World Universes Beyond cameo) excluded post-hoc (judgment call). |
| human-noble | `t:human t:noble year>=2010 -is:digital -is:promo` | 140 | 140 | 4 | **2 — thin, mixed signal** | King T'Challa//Black Panther (Marvel) and Aragorn, the Uniter (LTR, judgment call — reversed from an earlier pass that kept LOTR content by default) both excluded post-hoc. Only Kenrith, the Returned King (classic crowned-king iconography) and The Wandering Rescuer (a gothic sword-wielder with no crown, closer to Knight/Warrior) remained — these two pull in different directions, so the skill file anchors mainly on Kenrith and flags the mismatch. |
| human-assassin | `t:human t:assassin year>=2010 -is:digital -is:promo` | 125 | 125 | 4 | **2 nominal, ~1 effective — LOW-CONFIDENCE** | Mary Read and Anne Bonny and Ezio Auditore da Firenze (ACR) excluded post-hoc. Of the 2 remaining, Queen Marchesa's actual art crop is a stylized cat portrait (an alternate-art variant) with no usable assassin iconography, leaving Massacre Girl as the only genuinely informative source. |
| construct | `t:construct year>=2010 -is:digital -is:promo` | 288 | 175 | 4 | 4 | |
| golem | `t:golem year>=2010 -is:digital -is:promo` | 163 | 163 | 4 | 4 | |
| insect | `t:insect year>=2010 -is:digital -is:promo` | 267 | 175 | 4 | 4 | |

## Honest scope summary

- **Colors queried:** 7 of 7 (W, U, B, R, G, Multicolor, Colorless). All 7 metadata-sampled; 42 images downloaded and viewed with vision, 37 actually usable in the final write-ups after crossover exclusion (Red down to 3, Multicolor down to 4).
- **Subtypes queried:** 34 of 34 (all subtypes and human-class combinations listed in the task — 16 non-human/non-class subtypes plus 6 races plus 9 human classes plus 3 construct-adjacent types). All 32 metadata-sampled; 128 images downloaded and viewed with vision, 109 actually usable in the final write-ups after crossover exclusion.
- **Total images individually viewed with vision (not just counted from metadata):** all 170 downloaded images (42 color + 128 subtype) were viewed — the exclusions above are a *post-viewing* editorial judgment (a viewed image recognized as licensed IP and then discounted from the written conventions), not images skipped during viewing. Work was split across three parallel research passes: one agent for all 7 colors, two agents for 16 and 18 subtypes respectively.
- No cell's underlying Scryfall query returned fewer than 68 matching arts (devil, the smallest population) — well above the 10-art low-confidence threshold on the query-count axis. Every low-confidence flag in this document is on the *viewed-and-used-sample* axis, caused by the Universes Beyond crossover correction described above, not by a scarcity of real Magic creature art in that cell. Human-Warrior is the one cell weak enough (1 usable image) that its skill-file section is written as a hedged best-effort and explicitly flagged for follow-up re-sampling.
