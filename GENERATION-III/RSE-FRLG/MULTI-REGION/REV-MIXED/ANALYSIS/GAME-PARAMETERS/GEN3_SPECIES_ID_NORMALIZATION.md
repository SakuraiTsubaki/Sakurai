# Gen III Species ID Normalization

Status: project decision confirmed.

## Decision

The legacy Generation III `SPECIES_OLD_UNOWN_B` through `SPECIES_OLD_UNOWN_Z` slots are not retained in the project runtime species namespace.

They are treated as obsolete legacy holes and are removed from the normalized species ID layout.

## Normalized project species IDs

The Generation III target runtime will use National Pokédex order as the canonical base-species ID order:

- `0` = NONE
- `1..251` = Generation I-II species
- `252..386` = Generation III species
- `387..493` = Generation IV species
- `494..649` = Generation V species

Thus the project base-species ID is numerically identical to the National Pokédex number for 001-649.

Examples:

- Treecko = 252
- Chimecho = 358
- Deoxys = 386
- Turtwig = 387
- Arceus = 493
- Victini = 494
- Genesect = 649

## Egg and forms

`EGG` is not allowed to occupy a National Pokédex species number in the normalized namespace. It becomes a special sentinel/state outside the 001-649 base-species range.

Unown B-Z, ! and ? are not represented as independent base species. They are routed through the form system as `(SPECIES_UNOWN, form_id)`.

The same rule applies to other Generation III-V alternate forms: base species ID remains the National Pokédex species, while form identity is stored/routed separately.

## Migration consequences

Original RSE/FRLG internal IDs 252-276 (`OLD_UNOWN_*`) are discarded from the project runtime namespace.

Original Gen III species IDs 277-411 must be remapped to National Pokédex IDs 252-386. This means all species-indexed data and every code path that consumes original internal species IDs must be audited and converted, including at minimum:

- species info / personal data
- names
- Pokédex conversion tables and seen/caught logic
- evolution tables
- level-up and TM/HM learnsets
- wild encounters
- trainer parties
- breeding / daycare
- party / box / save serialization
- battle initialization
- cries
- icons and graphics tables (graphics integration remains deferred)
- footprints
- scripts and event parameters
- Hall of Fame
- link/trade compatibility paths
- any table sized or bounded by the original `NUM_SPECIES`

## Compatibility rule

Original ROM data is preserved in source/reference form, but project runtime data is normalized before use.

Where original Gen III binary data contains a legacy internal species ID, use an explicit legacy-to-project converter rather than assuming the value already equals a National Pokédex ID.

Conceptually:

`Gen3LegacySpeciesId -> ProjectSpeciesId (National Dex 001-649)`

For the original base species:

- legacy 1-251 -> project 1-251
- legacy 252-276 -> invalid/obsolete OLD_UNOWN legacy slots
- legacy 277-411 -> project 252-386
- legacy 412 (`EGG`) -> special egg state, not a base-species ID
- legacy 413+ Unown form IDs -> `(SPECIES_UNOWN, form_id)`

## Project rule

Do not preserve legacy numbering merely to avoid touching dependent tables. The project prefers one canonical 001-649 species namespace and explicit migration of dependent systems.

This decision supersedes the earlier compatibility-hole proposal that kept IDs 252-276 reserved.
