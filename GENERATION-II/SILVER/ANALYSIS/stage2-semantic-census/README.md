# Pokémon Silver 8-ROM Stage 2 Semantic Census

## Scope

This pass moves from bank-level statistics to named structures. It covers all eight project ROMs and produces a semantic bank atlas plus direct extraction of the Western bank 6C name corpus.

## 1. Bank 6C: exact Western name structure

Direct ROM parsing confirms that each Western Silver ROM begins bank `6C` with four consecutive name tables:

1. `ItemNames`: 256 variable-length `@`-terminated records
2. `TrainerClassNames`: 66 variable-length `@`-terminated records
3. `PokemonNames`: 256 fixed 10-byte records padded with `@`
4. `MoveNames`: 251 variable-length `@`-terminated records

Total records per Western ROM: **829**. Across EN/DE/FR/IT/ES this pass extracts **4,145 records** directly from ROM.

This corrects the earlier provisional 830 count; the binary boundary count is 829 (= 256 + 66 + 256 + 251).

### Exact table boundaries

| Lang | Item bytes | Trainer bytes | Pokémon start | Move start | Move end |
|---|---:|---:|---|---|---|
| EN | 2389 | 543 | `0x1B0B74` | `0x1B1574` | `0x1B1EE1` |
| DE | 2374 | 549 | `0x1B0B6B` | `0x1B156B` | `0x1B1F86` |
| FR | 2453 | 560 | `0x1B0BC5` | `0x1B15C5` | `0x1B1F81` |
| IT | 2458 | 568 | `0x1B0BD2` | `0x1B15D2` | `0x1B1FD3` |
| ES | 2443 | 557 | `0x1B0BB8` | `0x1B15B8` | `0x1B1FFA` |

The different byte lengths quantify localization pressure inside the same bank. Pokémon names always occupy exactly 2,560 bytes because the table is fixed-width; item/trainer/move tables expand or shrink by language.

## 2. Western decode completeness

Language-specific extra glyph mappings were resolved for the name bank:

- Spanish: `Á É Í Ñ Ó Ú`
- German: `Ä Ö Ü ä ö ü` (standard Gen II slots)
- French: `+` special glyph used in item names
- Italian: `À È Ù`

Unresolved byte placeholders after this pass: **0**.

## 3. Japanese and Korean Pokémon-name tables

Structural fixed-width detection finds:

- JP-Rev0: bank `14`, `0x0539F0`–`0x053EF0`, width 5 bytes, 256 records, 256/256 structurally valid.
- JP-RevA: bank `14`, `0x0539F0`–`0x053EF0`, width 5 bytes, 256 records, 256/256 structurally valid.
- KR: bank `6C`, `0x1B0C4A`–`0x1B164A`, width 10 bytes, 256 records, 256/256 structurally valid.

The JP Rev0 and RevA Pokémon-name table bytes are **identical**.

## 4. Semantic bank atlas

`semantic_bank_atlas.csv` contains one row for every physical ROM bank (896 rows total), combining direct ROM metrics with public linker-layout labels and two verified European overflow overrides:

- bank `27`: localized landmark/location-name overflow in DE/FR/IT/ES
- bank `58`: localized map-script/dialogue overflow in DE/FR/IT/ES

Each row records bank SHA-1, entropy, non-zero span, zero-bank status, semantic class, and provenance.

## 5. Outputs

- `semantic_bank_atlas.csv` — all 896 physical banks with semantic class
- `semantic_class_summary.csv` — per-ROM semantic class totals
- `western_name_table_locations.csv` — exact 6C table boundaries for EN/DE/FR/IT/ES
- `western_name_inventory_829x5.csv` — 4,145 directly extracted localized records
- `western_name_matrix_829.csv` — aligned 829-row five-language comparison matrix
- `western_name_decode_unknowns.csv` — unresolved decoder bytes (zero after this pass)
- `jp_kr_pokemon_name_table_locations.csv` — structurally detected JP/KR Pokémon-name tables
- `jp_kr_pokemon_name_records_raw.csv` — raw fixed-width records for JP Rev0, JP RevA, KR
- `stage2_semantic_census.py` — reproducible analyzer

## 6. Next semantic census targets

The next pass should parse text-command streams and pointer tables for:

1. Pokédex entries (`68`–`6B` Western, `68`–`69` KR, `11` JP)
2. move/item descriptions (`6D`/`6E` Western/KR)
3. general text (`64`–`66` Western/KR)
4. map-script dialogue banks and European bank `58`
5. Korean bank `71` and Hangul tables `78`–`7A`
6. unused/debug/garbage strings with verified references
