# Pokémon Crystal bank-role and localization census — pass 2

International bank roles are mapped from `pret/pokecrystal` `layout.link`; this is a reference annotation for the international disassembly, not an assumption that JP has the same bank layout.

## Exact structural facts from project ROMs
- Banks identical across EN Rev0 + DE + FR + IT + ES: **31**
  - 0C, 2A, 2B, 30, 31, 35, 37, 3B, 3C, 3D, 48, 49, 4A, 4B, 4C, 4D, 4E, 4F, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 5A, 7A, 7C
- Banks identical across all six international images including EN RevA: **31**
  - 0C, 2A, 2B, 30, 31, 35, 37, 3B, 3C, 3D, 48, 49, 4A, 4B, 4C, 4D, 4E, 4F, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 5A, 7A, 7C
- JP all-zero banks: **29**
  - 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 6A, 6B, 6C, 6D, 6E, 6F, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 7A, 7B, 7C
- EN Rev0 all-zero banks: **4**
  - 75, 76, 79, 7A

## Strong JP/international layout divergence
- JP banks `60`–`7C` are entirely `0x00` in this project ROM, while the international builds use much of the same range for map scripts, Pokédex entries, general text, European mail, Battle Tower data, etc.
- Therefore JP↔international work must not use blind same-bank/same-offset substitution in the upper ROM. Semantic alignment and pointer/reference reconstruction are mandatory.

## Highest localization delta banks among EN Rev0/DE/FR/IT/ES
| bank | mean differing bytes | max pair diff | international role |
|---|---:|---:|---|
| 14 | 14516 | 15328 | bank14; Unused Egg Pic |
| 62 | 14266 | 15217 | Map Scripts 15 |
| 67 | 14241 | 15529 | Map Scripts 20 |
| 16 | 14173 | 15148 | Map Scripts 2 |
| 1C | 13976 | 14958 | Map Scripts 7 |
| 65 | 13899 | 15002 | Map Scripts 18 |
| 04 | 13897 | 14621 | bank4 |
| 64 | 13822 | 14722 | Map Scripts 17 |
| 1F | 13807 | 14798 | Map Scripts 10 |
| 1B | 13766 | 14643 | Map Scripts 6 |
| 1E | 13737 | 14929 | Map Scripts 9 |
| 6A | 13572 | 14112 | Map Scripts 23 |
| 33 | 13544 | 15450 | Move Animations; Extra Songs 2 |
| 63 | 13504 | 14231 | Map Scripts 16 |
| 24 | 13494 | 13781 | bank24 |
| 6D | 13481 | 13850 | Special Phone Text |
| 66 | 13474 | 14323 | Map Scripts 19 |
| 15 | 13448 | 13936 | Map Scripts 1 |
| 5D | 13435 | 14153 | Crystal Phone Text 2; Pics 22 (unused pics section) |
| 69 | 13336 | 14460 | Map Scripts 22 |

## Low but nonzero localization delta banks (<100 mean differing bytes)
- `06` mean 66.4: Tileset Data 1
- `07` mean 1.8: Roofs; Tileset Data 2; Extra Songs 1
- `08` mean 16.3: Clock Reset; Tileset Data 3; Egg Moves
- `23` mean 84.3: bank23
- `2C` mean 49.4: Map Blocks 3
- `2D` mean 33.6: Tileset Data 5
- `34` mean 18.1: Pic Animations 1
- `3A` mean 5.9: Audio; Songs 1
- `44` mean 1.0: Mobile Adapter SDK
- `5E` mean 27.7: UpdateBattleHUDs; Songs 5; Crystal SFX; mobile5E; Pics 23 (unused pics section)
- `7D` mean 9.8: Mobile News Data

## Reference limits
- Role names come from the public international disassembly layout. They are used only to label likely function/data families in EN/European builds.
- JP requires a separate Japanese-specific role map; the project ROM itself already proves a major upper-bank relocation/omission pattern.
