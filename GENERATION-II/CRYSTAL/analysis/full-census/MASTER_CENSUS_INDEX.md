# Crystal 7-ROM census index

## Completed layers
1. ROM identity/header/hash validation (7/7).
2. Full 896-bank byte census (7 ROMs × 128 banks).
3. Per-bank entropy/fill-run inventory.
4. Cross-ROM bank identity/difference matrix.
5. EN Rev0↔RevA exact 584-byte / 79-range delta ledger.
6. International bank-role annotation from `pret/pokecrystal` layout.
7. JP upper-bank zero-layout divergence audit.
8. European `75/76/79` overflow-bank relocation evidence.

## Files
- `FULL_CENSUS_PASS1.md`
- `FULL_CENSUS_PASS2_BANK_ROLES.md`
- `FULL_CENSUS_PASS3_OVERFLOW.md`
- `HARDWARE_HEADER_AUDIT.md`
- `EN_REVISION_AUDIT.md`
- `bank_census.csv`
- `bank_role_matrix.csv`
- `cross_rom_bank_matrix.csv`
- `fill_runs_ge64.csv`
- `en_rev0_reva_changed_ranges.csv`
- `same_offset_identical_runs_ge256.csv`
- `rom_structural_summary.csv`
- `european_overflow_alignment.csv`
- `overflow_bank_usage.csv`
- `ascii_heuristic_summary.csv`

## Next reverse-engineering layers
- proper Crystal charmap/font extraction per language
- text command/string/pointer census
- map/event/script object census and semantic cross-language mapping
- Pokédex 251-entry pointer/text census
- Pokémon/move/item/trainer name tables
- graphics/pic pointer and compressed-data census
- save/SRAM and mobile-specific data-structure census
- safe free-space proof by reference/reachability analysis (not fill-byte guessing)
