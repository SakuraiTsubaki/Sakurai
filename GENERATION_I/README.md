# Generation I — Master Index

This directory is the cross-version research/index layer for the complete Pokémon Generation I project.

## Primary originals

Japanese originals are investigated independently before commonality is claimed:

- Pocket Monsters Aka — Rev 0 / Rev 1
- Pocket Monsters Midori — Rev 0 / Rev 1
- Pocket Monsters Ao — Japanese Blue
- Pocket Monsters Pikachu — Rev 0 / Rev 1 / Rev 2 / Rev 3

Dedicated active source-reconstruction repositories:

- `SakuraiTsubaki/PocketMonsters-Aka-Disassembly`
- `SakuraiTsubaki/PocketMonsters-Midori-Disassembly`
- `SakuraiTsubaki/PocketMonsters-Ao-Disassembly`
- `SakuraiTsubaki/PocketMonsters-Pikachu-Disassembly`

## Required repository hierarchy

Cross-version analysis stored here follows:

`GENERATION_I/<GAME>/<LANGUAGE_OR_REGION>/<REVISION>/<WORK_TYPE>/`

Examples:

- `GENERATION_I/AKA/JAPAN/REV_0/DISASSEMBLY/`
- `GENERATION_I/MIDORI/JAPAN/REV_1/MAPS/`
- `GENERATION_I/AO/JAPAN/REV_0/TEXT/`
- `GENERATION_I/PIKACHU/JAPAN/REV_3/BUGS/`

Regional/localized releases get their own language/region and revision paths. They are never substituted for Japanese originals.

## Full workstream coverage

Every target is tracked across all of these categories:

1. ROM identity, revisions, hashes and bank inventory
2. LR35902 code and symbols
3. Pokémon/species/internal IDs/base data/evolution/learnsets
4. moves, types and type-effectiveness data
5. items, TM/HM, key items, shops and hidden items
6. maps, interiors, connections, warps, blocks, tilesets and collision
7. NPCs, trainers, parties, AI and dialogue
8. wild encounters, fixed encounters, gifts and trades
9. events, scripts, flags and progression
10. text encoding, fonts, control codes, menus and UI
11. graphics, sprites, tiles, effects and title/battle assets
12. audio, BGM, SFX and cries
13. battle mechanics
14. field mechanics
15. save/SRAM data structures
16. link trade/battle systems and compatibility
17. unused/dummy/debug/inaccessible data
18. bugs, glitches and special behavior
19. regional/localization/revision differences
20. later-generation Kanto/system comparisons
21. preservation-first integration candidates

## Verification policy

Allowed evidence levels:

- Hypothesis
- Observed
- Reproduced
- Matched

Addresses, hashes and data claims must identify the target version/revision. Unknown bytes remain byte-exact `INCBIN` in source-reconstruction repositories until verified source replaces them.

## Preservation policy

- Original ROM binaries are never committed.
- No single RGBY game is treated as a representative replacement for the others.
- Version/revision differences are preserved rather than normalized away.
- Later-generation behavior is never presented as Generation I original behavior.
- Later official additions and project-created expansions are recorded separately from Generation I originals.

## Active master issues

- #125 — full disassembly / research master tracker
- #130 — regional / localization / revision inventory
- #132 — maps, events, NPCs, trainers and progression
- #134 — Pokémon, moves, types, items and systems
- #135 — text, fonts, UI, graphics and audio
- #136 — unused/debug/bugs/special behavior
- #137 — later Kanto/system comparison and integration backlog
- #138 — evidence, symbols, address maps and verification
- #139 — completion matrix
- #140 — repository organization

Status: Generation I full-program work has started.