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
| `form` | form identifier (`u16`) |
| `gender` | gender/sex presentation key (`u8`) |
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

Public `sv2za` tooling already demonstrates a useful catalog-diff axis based on the `(species, form, gender)` key and compares at least:

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
model_path
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
```

Animation and locator details belong in child tables/arrays rather than flattened comma-separated strings when exact reconstruction is required.

## Why this matters for Generation III conversion

A 64×64 output is downstream of this catalog identity.

The conversion pipeline must never:

- collapse distinct `(species, form, gender)` catalog keys because they look similar;
- assume shiny is a hand-painted recolor unrelated to source materials;
- discard animation/locator relations before canonical battle pose/anchor research;
- infer Z-A paths from Scarlet/Violet by simple prefix replacement without validation;
- infer form semantics from file names alone.

## Public evidence sources

- `KotMatrosk1n/KM-Editor` — Scarlet/Violet and Z-A catalog/model preview implementations
- `Aqua-0/sv2za` — catalog parser/diff tooling and resource-path construction
- `pkZukan/gftool` — Trinity model/material/animation structures and viewers
- `hYdos/TrinityFormats` — public Scarlet/Violet resource-path example

All claims in this note remain tagged as public reverse-engineering evidence until direct game-byte verification is possible.
