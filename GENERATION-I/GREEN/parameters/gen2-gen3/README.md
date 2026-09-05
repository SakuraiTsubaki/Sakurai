# Green generation-parameter stack: Generation II -> III

This directory is the base parameter layer that must exist **before** regional-dex expansion work.

Order is fixed:

1. Original Pokémon Green / Generation I compatibility layer
2. Generation II parameter layer, sourced from `pret/pokecrystal`
3. Generation III parameter layer, sourced from `pret/pokeemerald`
4. Later generations are appended on top of this stack

The regional Pokédex (e.g. Expanded Johto) is a consumer of this global parameter registry, not the owner of species data.

## Generation II layer

Native National Dex range: **#152-251 (100 species)**.

Imported fields include six battle stats (Special split into Sp. Atk/Sp. Def), type pair, catch rate, base EXP, two held-item slots, gender ratio, hatch cycles, friendship baseline, growth rate, egg groups and TM/HM compatibility tokens.

Engine capabilities represented by this layer include Steel/Dark, six-stat personal data, held items, gender, friendship and breeding/egg metadata.

## Generation III layer

Native National Dex range: **#252-386 (135 species)**.

Because Generation III adds abilities and the modern EV/IV model to old species as well, the generated Gen III overlay contains **all #001-386 species**. It adds two ability slots, six EV-yield fields and explicit Generation III personal metadata while retaining the six-stat/type/breeding fields.

Generation III also introduces the 25 natures. Emerald's ability constants occupy IDs **#1-77**: `CACOPHONY` is the unused ID #76 and `AIR_LOCK` is #77, so the source numbering is preserved rather than compacted. Exact Emerald personal data is extracted from `src/data/pokemon/species_info.h` and joined to the National Dex names from `include/constants/pokedex.h`; Emerald internal species order is never assumed to equal National Dex order.

## Generated outputs

The workflow generates and commits:

- `gen2_native_personal_152_251.csv`
- `gen3_native_personal_252_386.csv`
- `gen3_personal_overlay_001_386.csv`
- `gen3_abilities_001_077.csv`
- `gen3_natures_25.csv`
- `green_gen2_gen3_parameter_layer.bin`
- `MANIFEST.json`

The `.bin` is a **non-ROM parameter data layer**. Runtime activation inside Green is a separate engine migration step. Original ROM files are never committed.

## Source policy

Data is extracted automatically from pinned source checkouts during the workflow, then count/range assertions are applied. Hand-entering hundreds of personal records is intentionally avoided.
