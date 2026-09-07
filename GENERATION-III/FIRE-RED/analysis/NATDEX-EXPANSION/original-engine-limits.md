# Original FireRed engine limits — National Dex expansion audit

This note records the currently verified limits relevant to expanding FireRed beyond the stock 386 National Dex entries.

## Stock species numbering

Stock FireRed uses:

- `SPECIES_NONE = 0`
- Kanto + Johto: 1–251
- `OLD_UNOWN_B` through `OLD_UNOWN_Z`: 252–276
- Hoenn species: 277–411
- `SPECIES_EGG = 412`

The project removes the 25 obsolete Old Unown reservation slots and remaps stock references so the base-species invariant becomes:

`base SPECIES_* ID == National Dex number`

This gives #252 Treecko = 252, #386 Deoxys = 386, #1025 Pecharunt = 1025, while keeping 1026–4095 available for future generations.

## Identifier width

The stock structures store species IDs as `u16` in the encrypted Pokémon substructure, battle Pokémon and trainer-party records. Therefore the 412-entry stock table size is a software/table-layout limit, not a 9-bit or 10-bit species-ID storage limit.

Project ID plan:

- `0x0000`: NONE
- `0x0001–0x0FFF`: base National Dex species (1–4095)
- `0x1000–0x1FFF`: gameplay-distinct varieties
- `0x2000–0xFFFD`: future extension space
- `0xFFFE`: EGG
- `0xFFFF`: INVALID

Forms use an independent `u16 FormId`.

## Save / Pokédex flags

Stock:

- `DEX_FLAGS_NO = ceil(NUM_SPECIES / 8)`
- stock `NUM_SPECIES = 412`
- 52 bytes Owned + 52 bytes Seen
- `SaveBlock2` size = `0xF24` (3876 bytes)
- one save-sector data area = 3968 bytes
- unused `filler_B20[0x400]` = 1024 bytes

4095 base Dex entries need:

- `ceil(4095/8) = 512` bytes per Seen/Owned set
- extension beyond stock = `512 - 52 = 460` bytes per set
- total extension = `920` bytes
- filler remaining = `1024 - 920 = 104` bytes

So a 4095-base-species Seen/Caught cap can fit without changing `SaveBlock2` size, provided the extension is placed in the unused filler and the accessors are rewritten.

## SpeciesInfo limitations

Stock `SpeciesInfo` is 28 bytes and includes:

- six base stats: `u8`
- two types: `u8`
- catch rate: `u8`
- base EXP yield: `u8`
- EV yield bitfields
- two held items: `u16`
- gender ratio / egg cycles / friendship / growth rate: `u8`
- two egg groups: `u8`
- two abilities: `u8`
- safari flee rate / body color

Required changes:

- **Ability ID:** `u8` is a 255-ID ceiling and is insufficient for a future-proof all-generation engine. Move to `u16` in the expanded runtime/table format.
- **Ability slots:** stored Pokémon use a one-bit `abilityNum`, so stock supports two slots only. Add a representation for Hidden Ability / future slots.
- **Base EXP:** promote `u8` to `u16`.
- Base stats can remain `u8` for current official values.

## Evolution table

Stock layout:

`gEvolutionTable[NUM_SPECIES][5]`

Five entries are already exhausted by stock Eevee's five Gen III evolutions. Modern Eevee requires eight evolutions, and later evolution methods also exceed the stock method set.

Replace with a pointer/index table to variable-length evolution records terminated by an END record.

## Level-up learnsets

Stock constants include:

- move-ID mask: `0x01FF` → 9-bit move IDs, max 511
- level mask occupies the remaining packed bits
- `MAX_LEVEL_UP_MOVES = 20`

For an all-generation engine, replace the packed representation with records such as `(u16 move, u8 level)` and a variable-length terminator/index.

## Forms / varieties

Stock FireRed does not have a general Form ID model. Castform and Deoxys are special-cased around sprite/form behavior.

The expansion must separate:

1. National Dex number
2. gameplay Species/Variety ID
3. cosmetic Form ID

Cosmetic forms may point to the same gameplay variety while using separate graphics/form metadata.

## ROM size and language layouts

Stock ROMs are 16 MiB. The standard GBA ROM address window supports a natural 32 MiB target.

Large unused FF regions exist in stock ROMs, but their locations differ between BPRE/BPRJ and European language builds. The project therefore uses common logical tables plus language-specific link layouts instead of hard-coding one set of offsets for every ROM.

## Verified BPRE Rev0 table anchors

- Pokémon names: `0x245EE0`, 11 bytes/entry
- Species → National Dex: `0x251FEE`, u16 entries
- Base stats: species 0 at `0x254784`, 28 bytes/entry
- Evolutions: species 0 at `0x259754`, 40 bytes/species, five 8-byte slots
- Level-up learnset pointer table: species 0 at `0x25D7B4`, 4 bytes/entry

These anchors are for BPRE Rev0 only and must not be assumed for other languages/revisions.
