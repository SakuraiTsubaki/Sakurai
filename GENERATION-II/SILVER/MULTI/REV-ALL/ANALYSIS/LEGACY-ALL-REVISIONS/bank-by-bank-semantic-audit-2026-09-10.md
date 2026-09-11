# Silver bank-by-bank semantic audit

> Reference labels come from pret/pokegold (English complete disassembly) and the current SakuraiTsubaki/pokegold-kr layout. Labels are a semantic coordinate system, not proof that every regional build has identical content at the same address.

Legend: `D`=data present, `0`=all-zero bank, `–`=bank absent because the 1 MiB JP ROM ends at 3F.

## Banks 00–0F

| Bank | Reference role | KR | JP0 | JPA | EN | DE | FR | IT | ES | Flags |
|---:|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| 00 | ROM0 / interrupts / header / Home | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 01 | bank1 | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 02 | bank2 | D | D | D | D | D | D | D | D |  |
| 03 | bank3 | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 04 | bank4 | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 05 | bank5 | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 06 | Tileset Data 1 | D | D | D | D | D | D | D | D |  |
| 07 | Roofs / Tileset Data 2 / Extra Songs 1 | D | D | D | D | D | D | D | D |  |
| 08 | Clock Reset / Tileset Data 3 / Catch Tutorial / Egg Moves | D | D | D | D | D | D | D | D |  |
| 09 | bank9 | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 0A | bankA | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 0B | bankB | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 0C | Tileset Data 4 | D | D | D | D | D | D | D | D | ALL8_IDENTICAL;WEST5_IDENTICAL |
| 0D | Effect Commands | D | D | D | D | D | D | D | D |  |
| 0E | Enemy Trainers | D | D | D | D | D | D | D | D |  |
| 0F | Battle Core | D | D | D | D | D | D | D | D | JP_REV_CHANGED |

## Banks 10–1F

| Bank | Reference role | KR | JP0 | JPA | EN | DE | FR | IT | ES | Flags |
|---:|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| 10 | bank10 / Evolutions and Attacks | D | D | D | D | D | D | D | D |  |
| 11 | bank11 | D | D | D | D | D | D | D | D |  |
| 12 | Pic Pointers / Pics 1 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 13 | Unmapped in EN/KR layout | 0 | D | D | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 14 | bank14 / Egg Pic | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 15 | Pics 2 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 16 | Pics 3 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 17 | Pics 4 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 18 | Pics 5 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 19 | Pics 6 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 1A | Pics 7 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 1B | Pics 8 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 1C | Pics 9 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 1D | Pics 10 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 1E | Pics 11 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 1F | Unown Pic Pointers / Pics 12 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |

## Banks 20–2F

| Bank | Reference role | KR | JP0 | JPA | EN | DE | FR | IT | ES | Flags |
|---:|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| 20 | Trainer Pic Pointers / Pics 13 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 21 | bank21 / Credits | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 22 | Unmapped in EN/KR layout | 0 | D | D | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 23 | bank23 | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 24 | bank24 | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 25 | Maps / Events | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 26 | Title Screen | D | D | D | D | D | D | D | D |  |
| 27 | Unmapped / localization-specific candidate | 0 | D | D | 0 | D | D | D | D | KR_ZERO_WEST_ACTIVE |
| 28 | Unmapped in EN/KR layout | 0 | D | D | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 29 | Unmapped in EN/KR layout | 0 | D | D | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 2A | Map Blocks 1 | D | D | D | D | D | D | D | D | ALL8_IDENTICAL;WEST5_IDENTICAL |
| 2B | Map Blocks 2 | D | D | D | D | D | D | D | D | WEST5_IDENTICAL |
| 2C | Unmapped in EN/KR layout | 0 | D | D | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 2D | Unmapped in EN/KR layout | 0 | D | D | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 2E | Pics 14 / bank2E | D | D | D | D | D | D | D | D |  |
| 2F | Unmapped in EN/KR layout | 0 | D | D | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |

## Banks 30–3F

| Bank | Reference role | KR | JP0 | JPA | EN | DE | FR | IT | ES | Flags |
|---:|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| 30 | Sprites 1 | D | D | D | D | D | D | D | D | ALL8_IDENTICAL;WEST5_IDENTICAL |
| 31 | Sprites 2 / bank31 | D | D | D | D | D | D | D | D |  |
| 32 | bank32 / The End | D | D | D | D | D | D | D | D |  |
| 33 | Move Animations / Extra Songs 2 | D | D | D | D | D | D | D | D |  |
| 34 | Unmapped in EN/KR layout | 0 | D | D | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 35 | Unmapped in EN/KR layout | 0 | D | D | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 36 | Font Inversed | D | D | D | D | D | D | D | D |  |
| 37 | Map Blocks 3 / Tileset Data 5 | D | D | D | D | D | D | D | D | ALL8_IDENTICAL;WEST5_IDENTICAL |
| 38 | bank38 | D | D | D | D | D | D | D | D |  |
| 39 | Copyright / Title Screen 2 / bank39 | D | D | D | D | D | D | D | D |  |
| 3A | Audio / Songs 1 | D | D | D | D | D | D | D | D |  |
| 3B | Songs 2 | D | D | D | D | D | D | D | D | ALL8_IDENTICAL;WEST5_IDENTICAL |
| 3C | Songs 3 / Sound Effects / Cries | D | D | D | D | D | D | D | D | ALL8_IDENTICAL;WEST5_IDENTICAL |
| 3D | Songs 4 | D | D | D | D | D | D | D | D | ALL8_IDENTICAL;WEST5_IDENTICAL |
| 3E | bank3E / Shrink Pics / bank3E_2 | D | D | D | D | D | D | D | D | JP_REV_CHANGED |
| 3F | bank3F | D | D | D | D | D | D | D | D | JP_REV_CHANGED |

## Banks 40–4F

| Bank | Reference role | KR | JP0 | JPA | EN | DE | FR | IT | ES | Flags |
|---:|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| 40 | Standard Scripts | D | – | – | D | D | D | D | D |  |
| 41 | Phone Scripts | D | – | – | D | D | D | D | D |  |
| 42 | Map Scripts 1 | D | – | – | D | D | D | D | D |  |
| 43 | Map Scripts 2 | D | – | – | D | D | D | D | D |  |
| 44 | Map Scripts 3 | D | – | – | D | D | D | D | D |  |
| 45 | Map Scripts 4 | D | – | – | D | D | D | D | D |  |
| 46 | Map Scripts 5 | D | – | – | D | D | D | D | D |  |
| 47 | Map Scripts 6 | D | – | – | D | D | D | D | D |  |
| 48 | Map Scripts 7 | D | – | – | D | D | D | D | D |  |
| 49 | Map Scripts 8 | D | – | – | D | D | D | D | D |  |
| 4A | Map Scripts 9 | D | – | – | D | D | D | D | D |  |
| 4B | Map Scripts 10 | D | – | – | D | D | D | D | D |  |
| 4C | Map Scripts 11 | D | – | – | D | D | D | D | D |  |
| 4D | Map Scripts 12 | D | – | – | D | D | D | D | D |  |
| 4E | Map Scripts 13 | D | – | – | D | D | D | D | D |  |
| 4F | Map Scripts 14 | D | – | – | D | D | D | D | D |  |

## Banks 50–5F

| Bank | Reference role | KR | JP0 | JPA | EN | DE | FR | IT | ES | Flags |
|---:|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| 50 | Map Scripts 15 | D | – | – | D | D | D | D | D |  |
| 51 | Map Scripts 16 | D | – | – | D | D | D | D | D |  |
| 52 | Map Scripts 17 | D | – | – | D | D | D | D | D |  |
| 53 | Map Scripts 18 | D | – | – | D | D | D | D | D |  |
| 54 | Map Scripts 19 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 55 | Map Scripts 20 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 56 | Map Scripts 21 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 57 | Map Scripts 22 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 58 | Unmapped in EN/KR layout; active only DE/FR/IT/ES among 2 MiB builds | 0 | – | – | 0 | D | D | D | D | KR_ZERO_WEST_ACTIVE |
| 59 | Map Scripts 23 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 5A | Map Scripts 24 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 5B | Map Scripts 25 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 5C | Map Scripts 26 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 5D | Map Scripts 27 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 5E | Map Scripts 28 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 5F | Map Scripts 29 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |

## Banks 60–6F

| Bank | Reference role | KR | JP0 | JPA | EN | DE | FR | IT | ES | Flags |
|---:|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| 60 | Map Scripts 30 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 61 | Map Scripts 31 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 62 | Map Scripts 32 (EN reference; commented WIP in KR layout) | D | – | – | D | D | D | D | D |  |
| 63 | Unused/zero in all 2 MiB builds | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 64 | Text 1 | D | – | – | D | D | D | D | D |  |
| 65 | Text 2 | D | – | – | D | D | D | D | D |  |
| 66 | Text 3 | D | – | – | D | D | D | D | D |  |
| 67 | Unused/zero in all 2 MiB builds | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 68 | Pokédex entries (EN 001–064; KR 001–128) | D | – | – | D | D | D | D | D |  |
| 69 | Pokédex entries (EN 065–128; KR 129–251) | D | – | – | D | D | D | D | D |  |
| 6A | Pokédex entries 129–192 in EN; zero in KR | 0 | – | – | D | D | D | D | D | KR_ZERO_WEST_ACTIVE |
| 6B | Pokédex entries 193–251 in EN; zero in KR | 0 | – | – | D | D | D | D | D | KR_ZERO_WEST_ACTIVE |
| 6C | Names | D | – | – | D | D | D | D | D |  |
| 6D | Move Descriptions | D | – | – | D | D | D | D | D |  |
| 6E | Item Descriptions | D | – | – | D | D | D | D | D |  |
| 6F | Unused/zero in all 2 MiB builds | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |

## Banks 70–7F

| Bank | Reference role | KR | JP0 | JPA | EN | DE | FR | IT | ES | Flags |
|---:|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| 70 | bank70 / Tileset Data 6 / bank70_2 / Pokégear GFX / Credits Strings | D | – | – | D | D | D | D | D |  |
| 71 | KR-specific bank71; zero in Western builds | D | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL;KR_ONLY_ACTIVE |
| 72 | KR DMG Error Screen; zero in Western builds | D | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL;KR_ONLY_ACTIVE |
| 73 | Unused/zero | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 74 | Unused/zero | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 75 | Unused/zero | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 76 | Unused/zero | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 77 | Unused/zero | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 78 | KR Hangul Tables 1; zero in Western builds | D | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL;KR_ONLY_ACTIVE |
| 79 | KR Hangul Tables 2; zero in Western builds | D | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL;KR_ONLY_ACTIVE |
| 7A | KR Hangul Tables 3; zero in Western builds | D | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL;KR_ONLY_ACTIVE |
| 7B | KR Diploma GFX; zero in Western builds | D | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL;KR_ONLY_ACTIVE |
| 7C | Unused/zero | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 7D | Unused/zero | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 7E | Unused/zero | 0 | – | – | 0 | 0 | 0 | 0 | 0 | WEST5_IDENTICAL |
| 7F | KR bank7F / Western Stadium 2 checksum tail region | D | – | – | D | D | D | D | D |  |
