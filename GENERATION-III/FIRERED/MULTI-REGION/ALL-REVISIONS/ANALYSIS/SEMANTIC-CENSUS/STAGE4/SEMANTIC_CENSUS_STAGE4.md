# Pokémon FireRed 8-ROM Census — Stage 4 Systems / Metadata / Text Anchors

## Scope
This stage continues the direct whole-ROM census of the eight FireRed project ROMs. No ROM bytes are published.

Covered in this stage:
- embedded Game Freak compatibility header (`GFRomHeader`) at ROM offset `0x00000100`
- save-block sizes and externally exposed offsets
- ability names / description storage anchors
- item table metadata and item descriptions
- Pokédex entry tables and descriptions
- Pokémon icon pointer / palette-index tables
- English Rev0 vs Rev1 text revision audit

## 1. Embedded `GFRomHeader`
All eight ROMs contain the compatibility header at `0x00000100`, with version `4` (FireRed), language IDs matching JP/EN/FR/IT/DE/ES, game name `pokemon red version`, and National Dex count `386`.

The header directly exposes addresses for Pokémon front/back sprites, normal/shiny palettes, icons, icon palette IDs, icon palettes, species names, move names, species info, ability names/descriptions, item data, battle moves, ball graphics/palettes, plus key save offsets.

### Save layout
- `SaveBlock2`: `0x0F24` (3876 bytes) in all eight ROMs.
- `SaveBlock1`: JP = `0x3D40` (15680 bytes); all Western releases = `0x3D68` (15720 bytes).
- Difference: exactly 40 bytes.
- Core exposed offsets such as flags `0x0EE0`, vars `0x1000`, Pokédex `0x0018`, seen1 `0x05F8`, seen2 `0x3A18`, party count `0x0034`, party `0x0038`, external-event data `0x30A7`, and external-event flags `0x30BB` are consistent across the eight headers.

## 2. Ability data
- Ability count: 78.
- Western fixed ability-name stride: 13 bytes (`12 + EOS/padding`).
- Japanese fixed ability-name stride: 8 bytes (`7 + EOS/padding`).
- JP ability names begin with `------- / あくしゅう / あめふらし / かそく / カブトアーマー ...`, confirming correct indexing.
- Western `abilityDescriptions` header target is a 78-entry pointer table.
- Japanese `abilityDescriptions` header target is not a 78-entry pointer table; it points into direct Japanese description data. This is a real build-layout difference and is recorded without forcing the Western interpretation onto JP.
- EN Rev0 and EN Rev1 ability names/descriptions: 0 semantic differences.

## 3. Item data
- Item records: 375.
- Western item record stride: 44 bytes, name field 14 bytes.
- Japanese item record stride: 40 bytes, name field 10 bytes.
- A normalized scalar record was built from item ID, price, hold effect/parameter, importance, registrability, pocket, type, presence of field/battle callbacks, battle usage, and secondary ID.
- The normalized scalar SHA-256 is identical for all eight releases: game-mechanical item metadata is unchanged by localization/revision.
- EN Rev0 vs Rev1 item records and item descriptions: 0 semantic differences.

## 4. Pokédex entry tables
The table was located independently in every ROM from the first three National Dex height/weight tuples, not from a hard-coded English address.

| Release | Table | Stride | Category width |
|---|---:|---:|---:|
| JP Rev1 | `0x409C00` | 28 | 6 |
| JP Rev0 | `0x40E2D0` | 28 | 6 |
| ES | `0x44912C` | 36 | 12 |
| DE | `0x44F73C` | 36 | 12 |
| EN Rev0 | `0x44E850` | 36 | 12 |
| EN Rev1 | `0x44E8B0` | 36 | 12 |
| FR | `0x447F70` | 36 | 12 |
| IT | `0x445868` | 36 | 12 |

All tables contain 387 records (`NONE + National Dex 1..386`).

After excluding localized category/description text and pointer addresses, every release produces the same normalized hash for height, weight, unused field, Pokémon display scale/offset, and trainer display scale/offset. Thus all non-language Pokédex presentation parameters are identical across the eight ROMs.

### English Rev0 -> Rev1 Pokédex text changes
Exactly two description records differ:

1. National Dex 152 — CHIKORITA
   - Rev0: `Its pleasantly aromatic leaves have the\nability to check the humidity and\ntemperature.`
   - Rev1: `Its pleasantly aromatic leaf has the\nability to check the humidity and\ntemperature.`
2. National Dex 248 — TYRANITAR
   - Rev0: `Its body can’t be harmed by any sort of\nattack, so it is very eager to make\nchallenges against enemies.`
   - Rev1: `It has an impudent nature. Having great\nstrength, it can even change surrounding\nlandforms.`

No other English Pokédex category or description record changed in this pass.

## 5. Pokémon icons
The header provides the Pokémon icon table and icon palette-index table directly.

Across all eight ROMs:
- 440 icon-table entries
- 440 valid ROM pointers
- 415 unique icon targets
- the complete 440-entry icon asset hash vector is identical
- the 440-byte icon palette-ID table hash is identical

This establishes that Pokémon menu icons and their palette-ID assignments are shared across all eight releases, even though Stage 3 showed language-family differences in some battle Pokémon palettes and trainer graphics.

## 6. Validation
The Stage 4 validator reruns the following checks for every ROM:
- `GFRomHeader` signature/version/language-family assumptions
- National Dex count = 386
- ability storage layout is recognized
- first item-table anchors are structurally valid
- Bulbasaur Pokédex height/weight = 7 dm / 69 hg
- save-block sizes parse successfully

Result: 8/8 pass.

## Artifacts
Core artifacts:
- `gf_rom_header.csv`
- `pokedex_summary.csv`
- `ability_summary.csv`
- `item_summary.csv`
- `mon_icon_summary.csv`
- `english_revision_pokedex_diffs.csv`
- `stage4_validation.csv`
- `stage4_summary.json`
- `detailed_manifest.csv`
- `fire_red_stage4_census.py`

The deterministic per-ROM detailed CSVs (Pokédex, abilities, items) are generated by the script and covered by SHA-256 in `detailed_manifest.csv`.

## Boundary of Stage 4
Not yet declared globally complete. Remaining semantic layers include font/glyph asset mapping, complete script/text pointer graph, map layouts/tilesets/events at record level, audio tables, full flash-sector serialization, Mystery Gift / wireless / e-Reader semantic tables, and the unresolved JP Rev0 high-ROM region.
