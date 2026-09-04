# Pokémon LeafGreen Text / Name-Table Census — Stage 4

This stage upgrades the earlier string heuristics into confirmed fixed-table structure. Offsets are ROM offsets (not `0x08xxxxxx` bus addresses).

## Confirmed cross-version tables

### Species names

- **412 records exactly** in every build.
- JP record width: **6 bytes**.
- International record width: **11 bytes**.
- Entry 0 is the dummy question-mark name. Entry 1 begins Bulbasaur (`フシギダネ` in JP; localized name in each international build).
- The move-name table begins **immediately after record 411**, which independently confirms the record count and width.

### Move names

- **355 records exactly** in every build (indices 0–354).
- JP record width: **8 bytes**.
- International record width: **13 bytes**.
- Entry 0 is the dash placeholder; data following entry 354 is not another fixed-width move-name record.

### Type names

- **18 records exactly** in every build.
- JP record width: **5 bytes**.
- International record width: **7 bytes**.
- Index 9 is the `???` sentinel in both JP and international layouts, giving an additional structural anchor.

### Item records (international builds)

- **375 records exactly**, each **44 bytes**.
- The item name is the first **14-byte** field in each record.
- Entry 0 is the dummy item, entry 1 is Master Ball / localized equivalent, and entry 374 is Sapphire / localized equivalent.
- Record 375 is non-item data, confirming the boundary.
- JP item-record layout remains a separate target because the Japanese compile-time name-field width changes the structure size.

## English fixed text tables

Both English revisions contain the same fixed table shapes, shifted by `+0x70` in Rev 1:

- Ability names: **78 × 13 bytes**.
  - Rev 0: `0x024FC1C`
  - Rev 1: `0x024FC8C`
- Trainer class names: **92 × 13 bytes**.
  - Rev 0: `0x023E604`
  - Rev 1: `0x023E674`

The ability table begins with the dummy `-------` followed by STENCH, DRIZZLE, SPEED BOOST, etc. The trainer-class table begins with BLACK BELT and ends with the final blank slot before a zero-filled region.

## Exact table offsets

See `text_table_anchors_stage4.csv`. Important examples:

| Build | Species | Move | Type | Item (if confirmed) |
|---|---:|---:|---:|---:|
| JP `BPGJ` | `0x0203C94` | `0x020463C` | `0x020C050` | pending JP struct pass |
| EN Rev 0 `BPGE` | `0x0245EBC` | `0x0247070` | `0x024F17C` | `0x03DAE64` |
| EN Rev 1 `BPGE` | `0x0245F2C` | `0x02470E0` | `0x024F1EC` | `0x03DAED4` |
| DE `BPGD` | `0x0245D8C` | `0x0246F40` | `0x024F04C` | `0x03DA354` |
| FR `BPGF` | `0x02402C8` | `0x024147C` | `0x0249588` | `0x03D3160` |
| IT `BPGI` | `0x023EF60` | `0x0240114` | `0x0248220` | `0x03D1D24` |
| ES `BPGS` | `0x0241628` | `0x02427DC` | `0x024A8E8` | `0x03D4D8C` |

## Pointer-referenced international text pass

A stricter second pass scans aligned 32-bit ROM pointers, follows each target to an `0xFF` terminator, and accepts only segments with high Generation III international-character density and high letter/digit density. This is substantially stricter than the Stage 3 raw text heuristic.

| Build | Strict referenced text targets | Aligned references | 64 KiB regions |
|---|---:|---:|---:|
| DE | 3,410 | 3,722 | 39 |
| ES | 2,971 | 3,350 | 44 |
| EN Rev 1 | 3,403 | 3,761 | 39 |
| EN Rev 0 | 3,414 | 3,780 | 39 |
| FR | 3,380 | 3,751 | 38 |
| IT | 3,417 | 3,784 | 38 |

These remain **direct-pointer text candidates**, not a claim that every script string uses a direct aligned pointer. Script engines can use indirect tables, relative structures, or pointers to control blocks; those are separate passes.

## Key structural conclusion

JP is not just an international ROM with different glyphs. The fixed name fields are physically narrower:

- Species: **6 vs 11 bytes**
- Moves: **8 vs 13 bytes**
- Types: **5 vs 7 bytes**

Therefore any cross-language patcher must be table-aware and version-aware. Hard-coded international record widths cannot safely operate on JP, and hard-coded JP widths cannot safely operate on international builds.

## Next census targets

1. JP item / ability / trainer-class record geometry.
2. Font sheets and character-code → glyph mapping.
3. Text rendering/control codes (`0xFA`–`0xFE`) and variable expansion.
4. Script pointer tables and indirect text references.
5. Pokédex species/category/description tables.
6. Map names, NPC/event scripts, battle/system messages, menus, PC/shop/link text.
