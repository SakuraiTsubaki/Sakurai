# Gen III internal species order — exact ROM-derived mapping

Status: **confirmed from all uploaded Gen III targets; supersedes the earlier +25 simplification.**

## Correction

The earlier assumption that every real Gen III species after the OLD_UNOWN range could be converted by `canonical = legacy - 25` is false.

The uploaded ROMs contain an explicit `internal species ID -> National Dex` u16 table. For IDs 1..251 it is identity, but the Hoenn block is not National-Dex ordered. OLD_UNOWN internal IDs 252..276 map to the old dummy Pokédex constants and are discarded by this project.

Representative confirmed mappings:

- internal 277 -> National 252 Treecko
- internal 304 -> National 276 Taillow
- internal 392 -> National 280 Ralts
- internal 301 -> National 290 Nincada
- internal 315 -> National 300 Skitty
- internal 313 -> National 320 Wailmer
- internal 308 -> National 327 Spinda
- internal 318 -> National 343 Baltoy
- internal 385 -> National 351 Castform
- internal 317 -> National 352 Kecleon
- internal 411 -> National 358 Chimecho
- internal 410 -> National 386 Deoxys

Thus the project must use a complete lookup table, never an arithmetic offset, when migrating original Gen III species IDs.

## Uploaded-ROM verification

All ten inspected RSE/FRLG JP/EN targets contain the same logical 411-entry mapping table. The table bytes have SHA-1:

`db9b54ca7185810df7a928e775c84cc99b127c5c`

ROM-specific mapping-table addresses and SpeciesInfo bases:

| ROM | map | SpeciesInfo |
|---|---:|---:|
| Pocket Monsters Ruby (Japan) | 0x1CE2CA | 0x1D09E8 |
| Pokémon Ruby USA/Europe Rev 2 | 0x1FC52E | 0x1FEC4C |
| Pocket Monsters Sapphire (Japan) | 0x1CE25A | 0x1D0978 |
| Pokémon Sapphire USA/Europe Rev 2 | 0x1FC4BE | 0x1FEBDC |
| Pocket Monsters Emerald (Japan) | 0x2EE60A | 0x2F0D70 |
| Pokémon Emerald USA/Europe | 0x31DC82 | 0x3203E8 |
| Pocket Monsters FireRed (Japan) Rev 1 | 0x20A20E | 0x20C9C0 |
| Pokémon FireRed USA/Europe Rev 1 | 0x25205E | 0x254810 |
| Pocket Monsters LeafGreen (Japan) | 0x20E9D2 | 0x211184 |
| Pokémon LeafGreen Europe Rev 1 | 0x25203A | 0x2547EC |

For every ROM, the real National Dex values 1..386 occur exactly once in the table: 386/386 present, no duplicates, no missing species.

## Project canonical species policy

- 0 = NONE
- 1..386 = original Gen I–III Pokémon, physically reordered to exact National Dex order
- 387..649 = Gen IV/V additions
- 650 = EGG pseudo token when a species-like token is required
- OLD_UNOWN 252..276 = discarded from canonical species space
- Unown forms = species 201 + form ID

## Canonical SpeciesInfo rebuild

A canonical 28-byte Gen III SpeciesInfo table was generated for each uploaded target:

- records 1..386: target-original records copied through the exact ROM mapping table
- records 387..649: BW-derived Gen III compatibility records
- total: 650 records including NONE, 18,200 bytes

The six RSE outputs are byte-identical with SHA-256 `680abb617e3ae8c36754ebc22c499890148ecf7edc615d9d2e3addcd45858023`.

The four FRLG outputs are byte-identical with SHA-256 `669352b9031648adb362ba7d390b3cdd1e2aa3dc6a626bdbc9b39ce65cdc3c18`.

New-species compatibility caveats remain explicit: native Gen III `expYield` is u8 and is only a fallback (u16 Base EXP accessor is authoritative), Gen V held-item IDs are not copied before target item-ID translation, and hidden abilities remain in the project third-ability layer.

## Consequence

All earlier project code that used `legacy = national + 25` or `national = legacy - 25` for the Hoenn block is obsolete and must be replaced by the exact lookup tables before further runtime integration.
