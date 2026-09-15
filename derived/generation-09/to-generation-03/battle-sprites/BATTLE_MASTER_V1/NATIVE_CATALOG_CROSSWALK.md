# Generation IX → Generation III Battle Sprite Master v1 — Native Catalog Crosswalk

Research date: **2026-09-15**

Status: **Phase 2B in progress — key/path relation verified by public implementations; complete row-level retail catalog dump not yet located in the public corpus.**

## Objective

Crosswalk the exhaustive secondary public model-role census against the closest available Generation IX native Pokémon resource-catalog semantics.

The required relation is:

```text
native catalog key
(species, form, gender)
        ↓
model_path
        ↓
pmXXXX_YY_ZZ resource directory
        ↓
public config role / preserved model / icon / animation inventory
        ↓
Generation III front/back normal/shiny logical roles
```

No suffix is assigned native semantic meaning merely because its numeric value looks plausible.

## 1. Native key shape — VERIFIED BY PUBLIC PARSERS

`Aqua-0/sv2za` parses `poke_resource_table.trpmcatalog` with:

```text
SpeciesKey {
    species: u16,
    form: u16,
    gender: u8
}
```

The project uses the same key shape for both Scarlet/Violet and LEGENDS Z-A catalog comparison.

Evidence state: `CONFIRMED_TOOL_MAPPING`.

## 2. Native key and model path coexist in the same parsed row — VERIFIED

`sv2za/src/backend/catalog.rs` stores selected Scarlet/Violet catalog entries as:

```text
SelectedMon {
    key: SpeciesKey,
    pm: String,
    pm_variant: String,
    model_path: String
}
```

The code obtains `pm` and `pm_variant` by splitting that entry's `model_path`.

This establishes an important fact without guessing suffix semantics:

> A concrete native `(species, form, gender)` key and a concrete `pmXXXX_YY_ZZ`-family model resource path are directly paired in one catalog entry.

Evidence state: `CONFIRMED_TOOL_MAPPING`.

## 3. Scarlet/Violet and Z-A catalogs are compared by native key — VERIFIED

The public conversion tool independently opens:

Scarlet/Violet:

`catalog/catalog/poke_resource_table.trpmcatalog`

Z-A:

`ik_pokemon/catalog/catalog/poke_resource_table.trpmcatalog`

It builds the Z-A key set from `(species, form, gender)` and checks Scarlet/Violet entries against that set.

This proves that cross-title comparison is keyed semantically, not merely by matching filenames.

Evidence state: `CONFIRMED_TOOL_MAPPING`.

## 4. Earlier Trinity explicit suffix rule — VERIFIED FOR LEGENDS: ARCEUS ONLY

The public pkNX Legends: Arceus `PokeResourceTable` implementation constructs:

`pm{species:0000}_{gender:00}_{form:00}`

while querying the table by `(species, form, gender)`.

Thus for that explicit tool mapping:

```text
pmXXXX_YY_ZZ
       │  │
       │  └─ form
       └──── gender
```

Evidence state for Legends: Arceus: `CONFIRMED_TOOL_MAPPING`.

Evidence state when carried forward to Scarlet/Violet or Z-A: `INFERRED_FROM_CONTINUITY` only.

It is not promoted to `CONFIRMED_NATIVE_ROW` for Generation IX without observed row-level data.

## 5. Generation IX preserved asset examples — PARTIAL SUPPORT

Independent Scarlet/Violet preservation identifies:

- Alolan Raichu as `pm0026_00_11`.
- Pikachu resources include `pm0025_00_00`, `pm0025_01_00`, and `pm0025_11_00` through `pm0025_18_00`.

Consequences:

1. A non-zero second suffix is demonstrably involved in at least one alternate-form distinction (`pm0026_00_11`).
2. The first suffix is not safely describable as a simple binary 0/1 dimension because preserved resources use values beyond 1.
3. The parser field name `gender` must be preserved as a native schema label but must not be collapsed to ordinary male/female semantics without row-level interpretation.
4. Costume/special-presentation/model-role states may share the same low-level identity axis or resource naming space; exact semantics remain to be proven.

Evidence state: `SUPPORTED_BY_ASSET_IDENTITY`.

## 6. Public viewer suffix labels are deliberately kept separate

The pinned `freedom12/PokemonModelViewer` generator scans actual directories named:

`pmXXXX_YY_ZZ`

and labels them locally as:

```text
formIndex = YY
variantIndex = ZZ
```

These are source-project labels generated from directory position. They are not assumed to equal native catalog `form` or `gender`.

Therefore the current generated census retains:

- `config_form_index`
- `config_variant_index`

and separately leaves:

- `game_form = UNRESOLVED`
- `game_gender = UNRESOLVED`

until crosswalk evidence exists.

## 7. Why the complete crosswalk is not yet declared finished

The public implementations contain parsers and code that operate on retail catalog files supplied by the user, but the currently surveyed repositories do not commit the complete Scarlet/Violet or Z-A retail `poke_resource_table.trpmcatalog` bytes or a full decoded row dump.

Therefore this project currently has:

- the parser schema;
- the native key shape;
- code proving key ↔ model-path pairing;
- the public model-directory/config inventory;
- independent preserved asset identities;

but does not yet have a public complete table of:

```text
species,form,gender,model_path,...
```

for every retail Generation IX entry.

The missing public dump is recorded as a provenance limitation, not silently filled with guesses.

## 8. Crosswalk row schema

Every future observed native row is normalized to:

```text
game
version
catalog_version
native_species
national_dex_number
native_form
native_gender_field
interpreted_presentation_role
model_path
pm_root
pm_variant
suffix_a
suffix_b
material_table_path
config_path
icon_path
defence_path
normal_material_status
shiny_material_status
public_config_id
public_config_form_index
public_config_variant_index
crosswalk_state
crosswalk_evidence
source_reference
source_sha256
notes
```

## 9. Crosswalk states

- `CONFIRMED_NATIVE_ROW` — observed Generation IX catalog row directly pairs key and path.
- `CONFIRMED_TOOL_MAPPING` — mapping explicitly generated/used by title-aware public implementation.
- `SUPPORTED_BY_ASSET_IDENTITY` — independently identified asset supports the semantic interpretation.
- `INFERRED_FROM_CONTINUITY` — earlier Trinity naming continuity only.
- `CONFLICT` — sources disagree; retain both until resolved.
- `UNRESOLVED` — no safe interpretation yet.

## 10. Current mapping hypothesis — NOT YET A FIXED RULE

The strongest current hypothesis is:

```text
pmXXXX_YY_ZZ
XXXX -> species/resource number
YY   -> native gender/presentation-like catalog axis
ZZ   -> native form-like catalog axis
```

Reasoning:

- pkNX explicitly uses `species_gender_form` for Legends: Arceus;
- `sv2za` directly pairs native `(species, form, gender)` with Generation IX `pm_variant` paths;
- Alolan Raichu is preserved as `pm0026_00_11`, supporting a form-like role for the second suffix;
- first-suffix values beyond 1 demonstrate that the corresponding axis must not be reduced to a simple male/female boolean.

Current evidence state for applying this rule across all Scarlet/Violet and Z-A rows: `INFERRED_FROM_CONTINUITY + SUPPORTED_BY_ASSET_IDENTITY`.

It remains a hypothesis until an observed Generation IX native catalog row supplies the actual key and path together.

## 11. Next research actions

1. Continue searching public repositories, datamining archives, technical write-ups, issue attachments, generated reports, and preserved outputs for a full or partial decoded Generation IX catalog row set.
2. Prefer sources containing both numeric key fields and `model_path` in the same record.
3. Cross-check Scarlet and Violet separately before declaring equality.
4. Cross-check Z-A separately; do not inherit SV mappings automatically.
5. When a decoded table is found, produce `generated/native-catalog-crosswalk/*.csv` and compare all public census rows automatically.
6. Preserve any rows that do not obey the historical suffix hypothesis as first-class exceptions rather than forcing them into it.

## 12. Generation III consequence

No `front/back × normal/shiny` target role is finalized from a public model-directory suffix alone.

The 64×64 conversion begins only after the relevant resource role has either:

- a confirmed native row; or
- an explicitly marked provisional canonical-source decision supported by the strongest available public evidence.
