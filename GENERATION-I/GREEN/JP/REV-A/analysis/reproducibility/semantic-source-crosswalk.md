# Semantic source crosswalk — Pokémon Green JP REV-0 / REV-A

## Exact external disassembly match

Cross-check repository: `Narishma-gb/pokegreen` (master).

Its `roms.sha1` declares:

- `pokegreen.gb` = `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` — exact match for our REV-0 input.
- `pokegreen11.gb` = `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` — exact match for our REV-A input.

The Makefile builds Green with revision-specific assembler defines:

- REV-0: `_GREEN` + `_REV0` → `pokegreen.gb`
- REV-A: `_GREEN` + `_REV1` → `pokegreen11.gb`

It uses RGBDS (`rgbasm`, `rgblink`, `rgbfix`, `rgbgfx`) and fixes the Green headers as `POKEMON GREEN`, MBC1+RAM+BATTERY, SGB-enabled, version 0 or 1.

## Semantic categories available for cross-mapping

The source tree supplies structured areas for at least:

- `audio/` and `audio.asm` — music and sound
- `constants/` — IDs, hardware, charmap, maps, Pokémon, moves, items, trainers, battle, text, audio, etc.
- `data/` — structured game data tables
- `engine/` — executable game logic
- `gfx/` — graphics and converted assets
- `home/` / `home.asm` — fixed-bank engine code
- `maps/` / `maps.asm` — map structures
- `scripts/` — event/text/script data
- `ram/` / `ram.asm` — WRAM/HRAM layout and symbols
- `garbage/` / `garbage.asm` — preserved unused/padding/garbage bytes required for byte-identical reconstruction
- top-level `main.asm`, `includes.asm`, `layout.link` — build composition and bank layout

`includes.asm` provides explicit semantic constant/macro families for charmap, hardware, RAM, graphics, serial, scripts, types, battle, moves, move effects, items, Pokémon, Pokédex, trainers, sprites, palettes, maps, events, text, menus, audio, music and tilesets.

## Integration rule for this project

The uploaded ROMs remain the primary truth. The external disassembly is a semantic labeling/build reference, not a replacement source ROM. Every imported symbol, range or semantic classification should be checked against our canonical input hashes and, where possible, against generated bank/page hashes.

For each semantic range we add to our project, record:

1. revision(s), bank, file offset start/end and CPU address range;
2. source symbol/path in the disassembly;
3. category (code/data/text/map/gfx/audio/etc.);
4. whether REV-0 and REV-A are identical, relocated, or content-changed;
5. byte/hash verification result against the canonical ROM;
6. rebuild verification status.

## Current status

The byte-perfect reproducibility baseline is complete locally and regression-tested. This crosswalk establishes a verified path to the next layer: full semantic source mapping and RGBDS rebuild verification for both exact Green revisions.
