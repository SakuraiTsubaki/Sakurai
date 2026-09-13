# Pokémon Blue 6-ROM bank-by-bank exhaustive survey

Date: 2026-09-10

## Inputs
- **JP** — `Pocket Monsters - Ao (Japan) (SGB Enhanced).gb` — 512 KiB — 32 banks — SHA-1 `0da501e3e5c51ab8fef55b092dcdd7e6b050e424`
- **EN** — `Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb` — 1024 KiB — 64 banks — SHA-1 `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`
- **FR** — `Pokemon - Version Bleue (France) (SGB Enhanced).gb` — 1024 KiB — 64 banks — SHA-1 `47faa910d0e073c600665bf9c83b6bd17babdf8a`
- **DE** — `Pokemon - Blaue Edition (Germany) (SGB Enhanced).gb` — 1024 KiB — 64 banks — SHA-1 `20e72dc6f41493eee1fdd0cef54214e6c3389688`
- **IT** — `Pokemon - Versione Blu (Italy) (SGB Enhanced).gb` — 1024 KiB — 64 banks — SHA-1 `f69ed1a1332f04c24c7db899a09019bb045fa8b3`
- **ES** — `Pokemon - Edicion Azul (Spain) (SGB Enhanced).gb` — 1024 KiB — 64 banks — SHA-1 `7715e7b133e8634df48918b9138374110212a108`

## Global findings
- Western ROMs have content through bank `$2C`; banks `$2D-$3F` are 19 fully-zero 16 KiB banks in all five Western releases.
- Bank `$1B` is byte-identical across all six ROMs.
- Japanese Blue ends at bank `$1F`; Western localizations add `$20-$2C` for large text/Pokédex/move-name regions and reserve `$2D-$3F`.

## Bank-by-bank map

| Bank | Japanese Blue | Western Blue | Western mean similarity | Exact-equal groups |
|---:|---|---|---:|---|
| `$00` | ROM0: vectors/header/home engine | ROM0: vectors/header/home engine | 45.29% | — |
| `$01` | bank1 + garbage | bank1: core engine/events/menus | 17.07% | — |
| `$02` | audio 1 + garbage | audio 1 | 99.95% | — |
| `$03` | overworld/core engine + garbage | overworld/core engine | 48.38% | — |
| `$04` | move names + NPC sprites 1 + font + battle engine 1 + garbage | NPC sprites 1 + font + battle engine 1 | 70.41% | — |
| `$05` | NPC sprites 2 + battle engine 2 + garbage | NPC sprites 2 + battle engine 2 | 98.56% | — |
| `$06` | maps 1-2 + play time + doors/ledges + garbage | maps 1-2 + play time + doors/ledges | 86.67% | — |
| `$07` | maps 3-4 + clear save + hidden events 1 + garbage | maps 3-4 + Pokémon names + hidden events 1 | 68.78% | — |
| `$08` | audio 2 + Bill PC | audio 2 + Bill PC | 39.22% | — |
| `$09` | Pokémon pics 1 + battle engine 3 + garbage | Pokémon pics 1 + battle engine 3 | 97.24% | — |
| `$0A` | Pokémon pics 2 + battle engine 4 + garbage | Pokémon pics 2 + battle engine 4 | 99.92% | — |
| `$0B` | Pokémon pics 3 + battle engine 5 + garbage | Pokémon pics 3 + battle engine 5 | 99.86% | — |
| `$0C` | Pokémon pics 4 + battle engine 6 + garbage | Pokémon pics 4 + battle engine 6 | 99.93% | — |
| `$0D` | Pokémon pics 5 + slot machines + garbage | Pokémon pics 5 + slot machines | 89.82% | — |
| `$0E` | battle engine 7 + garbage | battle engine 7 / Pokémon+move data | 49.79% | — |
| `$0F` | battle core | battle core | 30.94% | — |
| `$10` | Pokédex/menu/trade/intro + garbage | Pokédex/menu/trade/intro | 49.65% | — |
| `$11` | maps 5-6 + Pokédex rating + hidden events core + garbage | maps 5-6 + Pokédex rating + hidden events core | 95.32% | — |
| `$12` | maps 7-8 + screen effects + garbage | maps 7-8 + screen effects | 65.08% | — |
| `$13` | trainer pics + maps 9 + predefs + garbage | trainer pics + maps 9 + predefs | 99.36% | — |
| `$14` | maps 10 + battle engine 8 + hidden events 2 + garbage | maps 10 + battle engine 8 + hidden events 2 | 64.40% | — |
| `$15` | maps 11-12 + battle engine 9 + diploma/trainer sight + garbage | maps 11-12 + battle engine 9 + diploma/trainer sight | 90.95% | — |
| `$16` | maps 13-14 + battle engine 10 + Saffron guards + garbage | maps 13-14 + battle engine 10 + Saffron guards | 95.05% | — |
| `$17` | maps 15-16 + starter dex + hidden events 3 + garbage | maps 15-16 + starter dex + hidden events 3 | 62.06% | — |
| `$18` | maps 17-18 + fossils + hidden events 4 + garbage | maps 17-18 + Cinnabar fossils + hidden events 4 | 95.51% | — |
| `$19` | tilesets 1 + garbage | tilesets 1 | 99.83% | — |
| `$1A` | battle engine 11 + version gfx + tilesets 2 + garbage | battle engine 11 + tilesets 2 | 37.58% | — |
| `$1B` | tilesets 3 | tilesets 3 | 100.00% | JP=EN=FR=DE=IT=ES |
| `$1C` | splash/Hall of Fame/animations/palettes/save + garbage | splash/Hall of Fame/animations/palettes/save | 22.85% | — |
| `$1D` | maps 19-21 + itemfinder/vending + garbage | maps 19-21 + itemfinder/vending | 41.54% | — |
| `$1E` | battle animations/evolution/TM prices + garbage | battle animations/evolution/TM prices | 98.93% | — |
| `$1F` | audio 3 + garbage | audio 3 | 99.99% | — |
| `$20` | — | text 1 | 24.77% | — |
| `$21` | — | text 2 | 24.37% | — |
| `$22` | — | text 3 | 22.76% | — |
| `$23` | — | text 4 | 26.04% | — |
| `$24` | — | text 5 | 27.11% | — |
| `$25` | — | text 6 | 27.84% | — |
| `$26` | — | text 7 | 25.56% | — |
| `$27` | — | text 8 | 29.04% | — |
| `$28` | — | text 9 | 27.72% | — |
| `$29` | — | text 10 | 26.49% | — |
| `$2A` | — | text 11 | 94.96% | — |
| `$2B` | — | Pokédex text | 18.49% | — |
| `$2C` | — | move names | 90.31% | — |
| `$2D-$3F` | — | zero-filled reserved/padding banks | 100.00% | EN=FR=DE=IT=ES |

## Disassembly interpretation
- Do **not** linearly decode an entire bank as SM83 code. Large regions are graphics, maps, text, audio, or tables.
- Use the ROM bytes as the source of truth. Existing exact-build disassemblies are only symbol/structure guides and cross-checks.
- For each bank, convert known executable ranges to instructions, known structured data to typed macros/tables, and leave unresolved bytes losslessly represented until classified.
- Acceptance criterion per ROM: RGBDS build output must be byte-identical to the uploaded source ROM and match its SHA-1.

## Recommended semantic pass order
1. `$1B` — identical six-way data bank; validate cross-region asset mapping.
2. High-similarity engine/data banks (`$02`, `$0A-$0C`, `$13`, `$19`, etc.) to establish stable labels.
3. Mixed engine/map banks `$00-$1F`.
4. Localization-heavy Western text banks `$20-$2C`.
5. Mark `$2D-$3F` explicitly as zero-filled reserved/padding banks, not executable code.
