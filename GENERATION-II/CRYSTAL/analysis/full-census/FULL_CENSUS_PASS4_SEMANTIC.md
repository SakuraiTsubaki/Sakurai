# Pokémon Crystal 7-ROM semantic census — pass 4

## Verified named tables
- Pokémon names: 251/251 extracted in all seven ROMs.
  - JP: `0x05341A`, fixed 5-byte records.
  - EN0/EN1: `0x053384`, fixed 10-byte records.
  - DE `0x05336E`; FR `0x053377`; IT `0x053393`; ES `0x05338D`, all fixed 10-byte records.
- Move names: 251/251 extracted in all seven.
  - JP: `0x04163B` (bank 10).
  - EN0/EN1: `0x1C9F29` (bank 72).
  - DE `0x1C9E9D`; FR `0x1C9F96`; IT `0x1C9E86`; ES `0x1CA045`.
  - This is a major JP/international relocation: JP keeps move names next to move data; international localizations move the names into the high text bank.
- Item names: 255/255 extracted in all seven.
  - JP: `0x0070FA`.
  - Every international image: exact table start `0x1C8000` (bank 72).
- Trainer class display names: 67/67 extracted in all seven.
  - JP: `0x02D319`.
  - Every international image: exact table start `0x02C1EF`.

## Core parameter identity
Two core gameplay tables are byte-identical across **all seven ROMs** despite relocation:
- Pokémon `BaseData`: 251 × 32 = 8,032 bytes, SHA-1 `33b3dad88e67289252d419cc56248dfbf4ae7887`.
- Move parameter table: 251 × 7 = 1,757 bytes, SHA-1 `88aec41b405babe450cb766530344fed58803b19`.

This proves that, for these two tables, localization changes storage location around the data but does not alter the gameplay parameter bytes.

## Pokédex: all 251 entries recovered
### International architecture
- One 251×2-byte pointer table in bank 11.
- EN0/EN1 pointer table: `0x044378`.
- DE/FR/IT/ES pointer table: `0x04436C`.
- Data is selected across banks `60`, `6E`, `73`, `74` in 64-species groups.
- Each international entry uses:
  1. category/species-class string terminated by `0x50`
  2. 4 raw height/weight bytes
  3. page 1 text terminated by `0x50`
  4. page 2 text terminated by `0x50`

### Japanese architecture
- All 251 JP Pokédex entries are packed into **bank 11**.
- JP uses two verified pointer blocks:
  - 99 pointers at `0x044337`, pointing exactly to entries 1–99 beginning at `0x0443FD`.
  - 152 pointers at `0x0458B3`, pointing exactly to entries 100–251 beginning at `0x0459E3`.
- Both pointer blocks were checked entry-for-entry against the decoded record starts: 251/251 exact matches.
- JP entry metadata is more compact: category string + **3 raw height/weight bytes**, followed by description text ending with `<DEXEND>` (`0x5F`), rather than the international two-page representation.

## Produced ledgers
- `pokemon_names_7rom.csv`
- `move_names_7rom.csv`
- `item_names_7rom.csv`
- `trainer_class_names_7rom.csv`
- `semantic_table_locations.csv`
- `core_parameter_tables.csv`
- `pokemon_base_data_251.csv`
- `move_parameters_251.csv`
- `pokedex_pointer_layout.csv`
- `pokedex_entries_251_7rom.csv`

Each language string ledger contains decoded text **and raw hex**, so characters not yet assigned in a language-specific extended charmap are still losslessly preserved.

## Remaining semantic census
- language-specific extended glyph/font maps and exact font ROM ranges
- all general/NPC/battle/system text commands and pointer graphs
- map headers, map events, object events, scripts and conditional text
- trainer parties/names, wild encounters, item placements
- graphics/picture pointer tables and compressed asset boundaries
- audio pointer/data census
- SRAM/save/mobile structure census
- reference/reachability-based proof of truly safe expansion space
