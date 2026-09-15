# Generation VIII Connected Systems — Official-Source Baseline

**Status:** Reference only  
**Baseline date:** 2026-09-16 (Asia/Seoul)

This document records official-source facts that affect the Generation VIII decompilation/research program but are not, by themselves, proof of internal game implementation. Every item below must later be reconciled with the exact Sword/Shield, Brilliant Diamond/Shining Pearl, or Pokémon Legends: Arceus target revision when lawful extracted project material is available.

## 1. Pokémon HOME compatibility

The official Pokémon HOME product page currently lists all five Generation VIII game targets as supported Nintendo Switch titles:

- Pokémon Sword
- Pokémon Shield
- Pokémon Brilliant Diamond
- Pokémon Shining Pearl
- Pokémon Legends: Arceus

The same official material warns that restrictions may apply when moving particular Pokémon. Therefore this project must not model HOME compatibility as a single unrestricted bidirectional flag.

Official source:
- https://www.pokemon.com/us/pokemon-video-games/pokemon-home
- https://home.pokemon.com/en-us/move/

### HOME game-specific Pokédex behavior

Pokémon HOME version 2.0.0 added game-specific Pokédexes. Official HOME documentation states that the Sinnoh Pokédex for Brilliant Diamond/Shining Pearl, the Galar/Isle of Armor/Crown Tundra Pokédexes for Sword/Shield, and other game-specific Pokédexes register Pokémon based on the game in which the Pokémon was caught rather than treating HOME's National Pokédex as the only registry.

Research consequence:
- keep HOME Pokédex registration behavior separate from the in-game Pokédex implementation;
- record origin/caught-game dependencies;
- preserve historical HOME version behavior instead of applying the current HOME state retroactively.

Official source:
- https://home.pokemon.com/en-gb/features/

### HOME move-state behavior

Pokémon Support documents that move availability can differ between Sword/Shield, Brilliant Diamond/Shining Pearl, Pokémon Legends: Arceus, and other games. When a Pokémon is moved into a title that cannot support its current move set, HOME may replace the moves with moves valid for that destination; HOME also preserves a game-specific move set so returning a Pokémon to a game it previously visited can restore the move set last used there.

The same support material notes a one-way restriction relevant to Let's Go-origin Pokémon: after such a Pokémon has been moved from Pokémon: Let's Go, Pikachu!/Eevee! into Sword/Shield, BDSP, or PLA through HOME, it cannot be returned to the Let's Go titles.

Research consequence:
- do not create one universal Generation VIII move-state record;
- distinguish game-native learnset data, HOME transfer validation, and HOME's per-game remembered move state;
- distinguish game-side transfer eligibility data from service-side HOME behavior.

Official source:
- https://support.pokemon.com/hc/en-us/articles/6372731346452-Why-did-my-Pok%C3%A9mon-s-moves-change

## 2. Brilliant Diamond / Shining Pearl save-record bonuses

The official BDSP website documents two save-record bonuses in Floaroma Town:

- Sword or Shield save records on the same Nintendo Switch system allow the player to receive Jirachi.
- Pokémon: Let's Go, Pikachu! or Let's Go, Eevee! save records allow the player to receive Mew.

The official page also states that multiple qualifying save records do not allow multiple copies of these rewards in one BDSP save: one Jirachi and one Mew can be received.

Official source:
- https://diamondpearl.pokemon.com/en-us/shop/other-games-bonus/

### PLA-linked Arceus distribution path in BDSP

The official Pokémon distribution index records Arceus for Brilliant Diamond/Shining Pearl with `Pokémon Legends: Arceus save records` as the distribution method. This establishes a cross-title save-record linkage that must be matched to the exact BDSP revision, event flag/script, and local save-record check once game data is available.

Official source:
- https://www.pokemon.com/us/pokemon-video-games/pokemon-distributions

## 3. Pokémon Legends: Arceus save-record bonuses

The official Pokémon Legends: Arceus bonus page documents three distinct cross-title save-record groups.

### Brilliant Diamond / Shining Pearl play records

BDSP play records unlock:

- a post-credits research request that can lead to Darkrai;
- the Modern Team Galactic Set from the clothier after joining the Galaxy Expedition Team.

### Sword / Shield play records

Sword or Shield play records unlock:

- a post-credits research request that can lead to Shaymin (Land Forme);
- the Shaymin Kimono Set from the clothier after joining the Galaxy Expedition Team.

### Let's Go play records

Let's Go, Pikachu! or Let's Go, Eevee! play records allow the player to claim both the Pikachu Mask and Eevee Mask from the clothier after joining the Galaxy Expedition Team.

Official source:
- https://legends.arceus.pokemon.com/en-ca/shop/bonus-3/

Research consequence:
- identify the exact local save/application-presence checks used by PLA;
- keep cosmetic unlocks and post-credits research-request unlocks as separate conditions;
- document whether the same flag/check routine is reused across qualifying titles only after local evidence exists.

## 4. Official distributions and HOME gifts

The official Pokémon distribution index contains Generation VIII-linked records that include, among other entries:

- HOME gifts tied to first-transfer/compatibility periods;
- BDSP rewards distributed through save-record linkage;
- Generation VIII Mystery Gifts and event distributions.

These records establish a reference corpus, not a substitute for in-game event tables or server-side event archives.

Official source:
- https://www.pokemon.com/us/pokemon-video-games/pokemon-distributions

Research rule:
1. record distribution date range, region/language, delivery method and required title/update;
2. separately record official web evidence, preserved event files, and game-local receiving/unlock logic;
3. do not infer server implementation details that are not present in lawful project material;
4. distinguish ordinary Mystery Gift, save-record reward, HOME gift, event-table override, serial-code distribution and local-wireless distribution.

## 5. Daybreak and revision-sensitive content

Official Pokémon material identifies Daybreak as Pokémon Legends: Arceus Ver. 1.1.0 and describes it as adding new outbreak investigations and new battles at the training grounds. This must remain a distinct historical revision target rather than being silently absorbed into the final PLA state.

Official source:
- https://www.pokemon.com/us/pokemon-news/pokemon-scarlet-and-pokemon-violet-coming-to-nintendo-switch

Research consequence:
- compare base PLA against Ver. 1.1.0 before comparing against later revisions;
- isolate newly introduced scripts, requests, data tables, encounters and assets;
- record later fixes independently.

## 6. Verification state

Everything in this file is currently **Reference only** because it is sourced from official web material rather than direct local game extraction.

Promotion rules:

- `Observed`: corresponding game-side data/code/script/flag is found in the exact local target.
- `Reproduced`: the behavior or data can be recreated by documented tooling or controlled steps.
- `Matched`: reconstructed output satisfies an explicit comparison criterion against the intended target.

Do not promote HOME service behavior to a claim about game-local implementation unless the relevant local code/data has been observed.

## 7. Active GitHub tracking

This baseline supports these active Generation VIII research tracks:

- Master program: Sakurai issue #122
- Connected systems: Sakurai issue #123
- Official distributions/event data: Sakurai issue #124
- Version/patch/bug/unused-data census: Sakurai issue #126
- Complete data census: Sakurai issue #127
- Official-source linked-bonus/HOME baseline: Sakurai issue #128

Update this document when an official source is superseded, when a historical HOME/game revision is identified, or when local project evidence upgrades a claim from `Reference only` to a stronger verification state.
