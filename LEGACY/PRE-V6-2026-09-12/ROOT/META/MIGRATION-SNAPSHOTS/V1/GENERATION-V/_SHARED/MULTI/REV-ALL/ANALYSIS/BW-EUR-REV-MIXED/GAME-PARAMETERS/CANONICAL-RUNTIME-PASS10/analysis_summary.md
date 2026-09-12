# Generation V → Gen III canonical runtime — Pass 10

## Confirmed from uploaded Pokémon Black EUR ROM

- `a/0/1/8`: 668 level-up members. Members 0..649 are used for canonical real species 0..649.
- Level-up entry format: `u16 move, u8 level, u8 aux`; terminator `FF FF FF FF`.
- `a/0/1/9`: 668 evolution members; every member is 42 bytes = 7 × `{u16 method, u16 param, u16 target}`.
- Evolution method IDs actually used by species 1..649: 1 through 27.
- `a/0/1/6`: TM/HM compatibility bytes used here are offsets `0x28..0x37`, 16 bytes / 128 bits per species.

## Canonical Gen III species namespace

- Real Pokémon: `001..649 == National Dex`.
- `OLD_UNOWN_B..Z`: discarded.
- Unown forms: represented as `(species=201, form=0..27)`, not extra species IDs.
- `EGG`: pseudo-species 650; not a real `SpeciesInfo` record.

## Source migration rule

Stock Gen III tables that use C designated initializers such as `[SPECIES_TREECKO]` can follow the new canonical IDs automatically after species constants are rewritten. Positional/raw tables and serialized data cannot; they require explicit reindexing/migration.

## Cry rule

Stock `SpeciesToCryId()` contains OLD_UNOWN-hole compensation and therefore cannot remain after canonical IDs are enabled. For species 1..386, preserve target-original cry behavior through an explicit canonical lookup. For 387..649, do not invent or alias cries; leave them unassigned until the Gen IV/V audio port is implemented.

## Runtime gate

Canonical IDs are still intentionally gated. Before live storage can switch, save migration, link/trade protocol translation, wild/trainer data, remaining positional species tables, and pseudo-species/form call sites must be converted.
