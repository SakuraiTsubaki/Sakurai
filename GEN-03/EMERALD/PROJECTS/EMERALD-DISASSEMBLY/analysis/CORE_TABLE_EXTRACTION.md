# Core table extraction — Phase 1

This pass follows semantic roots recovered from the Game Freak ROM header and converts high-value table families into reproducible source data. No ROM image is stored in the repository.

## Reference set

Six unique Emerald payloads are SHA-1 verified before extraction: JPN, ENG_USA_EUR (`ENG_U` is a byte-identical alias), FRA, DEU, ITA and ESP.

## SpeciesInfo

`gSpeciesInfo` is 412 records × `0x1C` (28) bytes = 11,536 bytes. The complete table is byte-identical in all six unique releases, SHA-1 `cdac81dc5f81aa165042d490935335f4e0d21a85`. The first 26 bytes are semantic data and the final two bytes are zero padding. All 412 internal slots are stored in `data/species_info/species_info_*.csv` with decoded fields and exact `raw_hex` records.

## BattleMove

`gBattleMoves` is 355 records × `0x0C` (12) bytes = 4,260 bytes. The first 9 bytes are semantic fields and the final 3 bytes are zero padding. The complete table is byte-identical in all six unique releases, SHA-1 `63a1fe0825ad09a1d3f0d0ba812c56a06f0a53bc`. The source is split into review-sized CSV ranges under `data/battle_moves/`.

## Items

There are 377 item slots. JPN uses a 10-byte embedded name and 40-byte compiled record; western releases use a 14-byte name and 44-byte record. After localized text and relocated pointers are separated, all semantic item fields are identical in all six releases. The canonical semantic table is `data/items/items_core.csv`.

## Abilities

There are 78 abilities. JPN uses 8-byte names and 78 consecutive EOS-terminated descriptions; western releases use 13-byte names plus a 78-entry description pointer table.

## Localized full-analysis archive

`analysis/localized_tables_full.tar.xz` stores the complete per-release ability and item extraction results for all six unique releases. It contains localized text, original encoded text bytes, ROM offsets and item function-pointer metadata. Archive SHA-1: `8efa8dbc1668ce1e766d78ec7d2c10235c6f062c`.

The archive members are `abilities/<RELEASE>.csv` and `items/<RELEASE>.csv`. `analysis/localized_tables_full_manifest.json` documents the schema. `tools/package_localized_tables.py` creates the archive deterministically from extractor outputs.

All ability and item strings in this pass decode with zero unknown source bytes. The Italian five-byte Pokémelle glyph sequence is represented semantically as `<POKEMELLE>` while the exact encoded bytes remain preserved in the archive.

## Reproducibility tools

- `tools/extract_species_info.py`
- `tools/extract_battle_moves.py`
- `tools/extract_items.py`
- `tools/extract_abilities.py`
- `tools/emerald_text.py`
- `tools/package_localized_tables.py`

Every extractor verifies the source ROM SHA-1 before following a semantic root.

## Next

1. convert species/move fixed-width name tables into reusable assembler/C source while retaining every localization
2. assign symbolic species, move, ability and item identifiers
3. follow the Pokémon front/back sprite, normal/shiny palette, icon and icon-palette roots
4. decompress graphics and export viewable PNG plus reconstruction metadata
5. continue executable lifting and Block 01 semantic classification
