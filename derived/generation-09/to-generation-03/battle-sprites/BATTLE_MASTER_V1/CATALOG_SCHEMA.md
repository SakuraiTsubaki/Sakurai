# Generation IX Pokémon Resource Catalog Schema Notes

Research date: **2026-09-15**

Status: **public reverse-engineering baseline; direct retail-byte verification pending**

## Purpose

The Generation IX → Generation III battle-sprite master must enumerate logical Pokémon visual roles before conversion. Public reverse-engineering code shows that `poke_resource_table.trpmcatalog` is the key resource table for this purpose.

## Verified public parser fields

Current public parser implementations expose each catalog entry with the following identity/resource fields:

| Field | Meaning / current interpretation |
| --- | --- |
| `species` | internal species identifier (`u16`) |
| `form` | catalog field named `form` (`u16`); exact semantic mapping to resource-path suffixes must be observed, not guessed |
| `gender` | catalog field named `gender` (`u8`); do **not** assume it is limited to ordinary biological male/female presentation until observed values are reconciled |
| `model_path` | model resource path |
| `material_table_path` | material-table path used for material variants including shiny relationships |
| `config_path` | Pokémon model/config resource path |
| `animations[]` | animation-group references, each with a form number and path |
| `locators[]` | locator references, each with a form number, locator index, and locator path |
| `icon_path` | icon resource path |
| `unk_id` | currently unresolved `u32` field in the public parser |
| `defence_path` | defence-related resource path |

The catalog document itself also exposes a version value.

## Species key

The public parser key is:

`(species: u16, form: u16, gender: u8)`

This key is the minimum identity axis for model-role enumeration. Normal/shiny is layered on top through material-table handling rather than assumed to be a second independent species key.

### Semantic caution for `gender`

`gender` is the field name used by current public parsers and schemas. The project preserves that field name because changing it would destroy traceability to the source implementation.

However, it must currently be treated as a **catalog identity component whose complete value semantics are still under verification**, not as a promise that only ordinary male/female values occur.

Generation III logical-role manifests therefore retain both:

- `native_gender_field` — exact numeric catalog value when observed;
- `interpreted_presentation_role` — separately verified semantic label such as male/female/costume/other, never inferred from the field name alone.

## Scarlet / Violet namespace

Catalog:

`pokemon/catalog/catalog/poke_resource_table.trpmcatalog`

Model namespace:

`pokemon/data/`

Public examples and tooling support Pokémon resource names of the general `pm####` family. One public TrinityFormats code example references the Eevee skeleton path:

`pokemon/data/pm0133/pm0133_00_00/pm0133_00_00.trskl`

This naming example is evidence of the resource naming family only. The exact meaning/range of every numeric subfield must be derived from catalog/resource relations rather than guessed.

## LEGENDS Z-A namespace

Catalog:

`ik_pokemon/catalog/catalog/poke_resource_table.trpmcatalog`

Model namespace:

`ik_pokemon/data/`

Public tooling resolves Z-A `.trmdl` model paths under this namespace and treats the Z-A catalog separately from Scarlet/Violet.

## Native catalog ↔ resource-path relationship

Current public `Aqua-0/sv2za` code reads both the Scarlet/Violet and Z-A `poke_resource_table.trpmcatalog` files and stores each selected row as:

```text
SelectedMon {
    key: SpeciesKey { species, form, gender },
    pm,
    pm_variant,
    model_path
}
```

`pm` and `pm_variant` are parsed from the first two path components of the catalog's own `model_path`.

Therefore the public implementation directly establishes that **a native `(species, form, gender)` catalog key and a concrete `pmXXXX_YY_ZZ`-family resource path coexist in the same catalog row**.

What is still missing from the currently available public corpus is a committed retail catalog dump containing the complete observed row-by-row numeric values. Without those bytes/rows, suffix semantics must not be declared fully verified.

## Historical Trinity naming evidence

The public pkNX Legends: Arceus `PokeResourceTable` implementation constructs a default resource name as:

`pm{species:0000}_{gender:00}_{form:00}`

and separately queries the table with `(species, form, gender)`.

Evidence status for Generation IX work:

- **CONFIRMED_AS_TOOL_MAPPING for Legends: Arceus**
- **continuity evidence only for Scarlet/Violet and Z-A until row-level native catalog confirmation**

This historical mapping is highly useful for forming a crosswalk hypothesis, but it does not override an observed Generation IX catalog row.

## Current Generation IX suffix evidence

The pinned public `freedom12/PokemonModelViewer` configuration source mechanically parses model directory names:

`pmXXXX_YY_ZZ`

into source-local fields named:

- `formIndex = YY`
- `variantIndex = ZZ`

Those names are properties of that preservation/viewer project and are **not** promoted to native catalog semantics.

Independent public Scarlet/Violet model preservation demonstrates examples such as:

- `pm0026_00_11` for Alolan Raichu, proving that at least one non-zero **second suffix** participates in an alternate-form/resource distinction;
- Pikachu resources including `pm0025_00_00`, `pm0025_01_00`, and `pm0025_11_00` through `pm0025_18_00`, demonstrating that the **first suffix** can take values beyond a simple binary 0/1 set in real preserved model resources.

Consequently:

- do not rename `YY` to `gender` globally yet;
- do not rename `ZZ` to `form` globally yet;
- do not assume parser field `gender` means only biological sex;
- preserve exact raw suffixes and exact native catalog fields independently until a row-level crosswalk proves their relation.

## Crosswalk evidence levels

Every proposed native-key ↔ resource-suffix relation uses one of these states:

| State | Meaning |
| --- | --- |
| `CONFIRMED_NATIVE_ROW` | observed directly in a Generation IX catalog row with key and path |
| `CONFIRMED_TOOL_MAPPING` | explicitly constructed/mapped by a trusted public implementation for that title |
| `SUPPORTED_BY_ASSET_IDENTITY` | suffix meaning supported by independently identified preserved asset(s) |
| `INFERRED_FROM_CONTINUITY` | plausible from an earlier Trinity title or naming continuity, not yet title-native proof |
| `UNRESOLVED` | no safe semantic assignment yet |

Final manifests never silently upgrade a lower evidence state.

## Model / material / config extension evidence

Current public tools expose or generate the following resource extensions around the Pokémon catalog:

- `.trmdl` — model
- `.trmmt` — material table in current public SV→ZA tooling
- `.trpokecfg` — Pokémon config in current public SV→ZA tooling
- `.trskl` — skeleton
- `.tracn` — animation-name/catalog relation in current Scarlet/Violet tooling
- `.tracr` — animation resource/group relation
- `.tranm` and `.gfbanm` — animation formats recognized by public Trinity tooling

These extension labels are technical evidence from public implementations, not permission to assume every Generation IX title/version uses every extension identically.

## Catalog comparison rule

Public `sv2za` tooling demonstrates a catalog-diff axis based on the `(species, form, gender)` key and compares at least:

- model path
- material table path
- config path
- icon path
- defence path
- unresolved id
- animation count
- locator count

`BATTLE_MASTER_V1` adopts this comparison shape for cross-title and cross-version catalog research.

## Required project census row

Every discovered catalog role should normalize to at least:

```text
game
version
catalog_version
species
form
gender
interpreted_presentation_role
model_path
model_path_suffix_a
model_path_suffix_b
material_table_path
config_path
icon_path
defence_path
unknown_id
animation_count
locator_count
normal_material_status
shiny_material_status
source_class
source_hash
verification_state
suffix_mapping_evidence_state
```

Animation and locator details belong in child tables/arrays rather than flattened comma-separated strings when exact reconstruction is required.

## Why this matters for Generation III conversion

A 64×64 output is downstream of this catalog identity.

The conversion pipeline must never:

- collapse distinct `(species, form, gender)` catalog keys because they look similar;
- assume shiny is a hand-painted recolor unrelated to source materials;
- discard animation/locator relations before canonical battle pose/anchor research;
- infer Z-A paths from Scarlet/Violet by simple prefix replacement without validation;
- infer form/gender semantics from file names alone;
- treat public-viewer `formIndex` / `variantIndex` labels as equivalent to native catalog field names without crosswalk evidence.

## Public evidence sources

- `KotMatrosk1n/KM-Editor` — Scarlet/Violet and Z-A catalog/model preview implementations
- `Aqua-0/sv2za` — direct SV/Z-A catalog parser, key/path pairing, diff tooling and resource-path construction
- `kwsch/pkNX` — earlier Trinity `PokeResourceTable` schema and explicit Legends: Arceus naming mapping
- `pkZukan/gftool` — Trinity model/material/animation structures and viewers
- `hYdos/TrinityFormats` — public Scarlet/Violet resource-path example
- `freedom12/PokemonModelViewer` — pinned public SCVI/LZA directory/config inventory used for exhaustive secondary census
- The Models Resource Scarlet/Violet preservation pages — independently named model-resource examples used only as secondary asset-identity evidence

All claims in this note remain tagged by evidence level until direct Generation IX catalog-row verification is possible.
