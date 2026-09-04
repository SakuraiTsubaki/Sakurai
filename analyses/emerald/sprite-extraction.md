# Pokémon Emerald — sprite extraction census

## Inputs

Seven supplied filenames resolve to six unique ROM images. `Pokemon - Emerald Version (U).gba` and `Pokemon - Emerald Version (USA, Europe).gba` are byte-identical (SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`). Unique targets: JP, EN, DE, FR, IT, ES.

## Confirmed sprite families extracted per unique ROM

- Pokémon battle still front/back, normal + shiny: 3,574 PNGs
- Pokémon animated front, included above
- Pokémon menu icons: 880 PNGs
- Pokémon footprints: 413 PNGs
- Trainer front + back: 127 PNGs
- Overworld/object-event: 1,777 PNGs from 239 graphics IDs
- Item icons: 378 PNGs
- Total confirmed/table-backed sprite PNGs: 7,149 per unique ROM
- Exhaustive plausible `CompressedSpriteSheet` census: 1,847 unique candidates for JP/EN/DE/FR/IT, 1,848 for ES

## Core table offsets

| Lang | Still front | Animated front | Back | Normal pal | Shiny pal | Trainer front | OW info | Item icons |
|---|---|---|---|---|---|---|---|---|
| JP | 0x2D4CA8 | 0x2DDA1C | 0x2D6148 | 0x2D6F08 | 0x2D7CC8 | 0x2D8EE4 | 0x4DDA74 | 0x5DFCC8 |
| EN | 0x301418 | 0x30A18C | 0x3028B8 | 0x303678 | 0x304438 | 0x305654 | 0x505620 | 0x614410 |
| DE | 0x315D88 | 0x31EAFC | 0x317228 | 0x317FE8 | 0x318DA8 | 0x319FC4 | 0x517350 | 0x6258D8 |
| FR | 0x308F48 | 0x311CBC | 0x30A3E8 | 0x30B1A8 | 0x30BF68 | 0x30D184 | 0x50A50C | 0x618798 |
| IT | 0x300DDC | 0x309B50 | 0x30227C | 0x30303C | 0x303DFC | 0x305018 | 0x502364 | 0x610FAC |
| ES | 0x30767C | 0x3103F0 | 0x308B1C | 0x3098DC | 0x30A69C | 0x30B8B8 | 0x508C7C | 0x617250 |

Additional detected tables include Pokémon icon pointers/palettes, footprints, trainer palettes, and the 8-entry trainer-back picture/palette tables; those are preserved in each extraction manifest and `rom_metadata.json`.

## Cross-language findings

- All 239 overworld/object-event **raw frame payloads** are identical across JP/EN/DE/FR/IT/ES. Differences seen in an early rendered-PNG comparison came from palette auto-resolution and are not classified as source-frame localization differences.
- Pokémon footprints and trainer sprite payloads match across all six unique ROMs.
- Pokémon battle/icon comparison isolates the confirmed JP-vs-Western Jynx difference at internal species ID 124. Battle front/back, animated-front frames, normal/shiny renders and both menu-icon frames are affected.

## Reproducibility

The local extraction package contains PNGs, `.gbapal` files, raw table dumps, CSV manifests, `rom_metadata.json`, SHA-256 checksums, the main extractor, and the broad compressed-sheet census tool. ROM images are intentionally excluded from the asset package.
