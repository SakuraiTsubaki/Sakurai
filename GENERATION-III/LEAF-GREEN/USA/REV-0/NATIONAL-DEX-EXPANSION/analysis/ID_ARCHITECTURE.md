# LeafGreen National Dex Expansion — ID architecture

## Current data scope

- National Dex Species: **1025**
- PokéAPI Pokémon varieties: **1351**
- Pokémon Form records: **1579**
- Generation 10+ growth is expected, so IDs must remain appendable without renumbering existing base species.

## Runtime ID plan

```text
0           SPECIES_NONE
1..2047     Base / National Species reservation
2048..8191  Battle varieties / alternate battle parameter records
8192+       Project/custom expansion space
0xFFFF      reserved special sentinel candidate (Egg only after a full engine audit)
```

Current National Dex entries #1..#1025 use the same numeric base Species ID. #1026..#2047 stay reserved for future official generations. Battle varieties do not consume future National Dex numbers.

## Form layer

Visual-only forms are separate Form records and do not automatically allocate a battle Species ID. A form maps to a battle variety, and the battle variety maps to a National species.

`FormRecord -> BattleVariety -> NationalSpecies`

## Original LeafGreen constraints that require hooks

- Stock species tables contain 412 entries.
- Stock Egg handling aliases the old `SPECIES_EGG = 412` boundary and must be audited before moving Egg.
- Hall of Fame stores species in 9 bits (stock ceiling 511).
- Level-up learnset encoding stores move ID in 9 bits (stock ceiling 511).
- Pokédex save flags/UI assume the stock species/dex range and must be separated from battle-species count.
- English and Japanese species-name tables have fixed stock widths; modern names require a renderer/table redesign.

This document describes the target architecture. It supersedes the archived layout-v0 design that preserved the 25 legacy Old Unown dummy species slots.
