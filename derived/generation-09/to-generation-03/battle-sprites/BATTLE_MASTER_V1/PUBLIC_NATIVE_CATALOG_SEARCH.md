# Generation IX Native Pokémon Catalog — Public Source Search Log

Search date: **2026-09-15**

Purpose: locate a public Scarlet/Violet or Pokémon LEGENDS Z-A `poke_resource_table.trpmcatalog` row dump, decoded export, or equivalent record set containing both native identity fields and resource paths.

## Required target evidence

A high-value result must expose at least:

```text
species
form
gender
model_path
```

Preferably it also exposes:

```text
material_table_path
config_path
animations
locators
icon_path
defence_path
catalog version
source game/version
```

## GitHub code-search findings

Global searches for `poke_resource_table.trpmcatalog` returned implementation/documentation references rather than a committed complete Generation IX decoded row dump.

High-value implementations found:

### `Aqua-0/sv2za`

Relevant files:

- `src/fb/trpmcatalog.rs`
- `src/backend/catalog.rs`
- `src/bin/catalog_inspect.rs`
- `src/backend/patch_catalog.rs`
- `src/ui/donors.rs`

Value:

- parses the native key `(species, form, gender)`;
- parses `model_path` and other catalog resource fields;
- directly pairs a parsed native key with a parsed `pm_variant` and `model_path`;
- compares Scarlet/Violet and Z-A catalogs by native key;
- provides an inspector capable of printing row details when supplied catalog bytes.

Limitation:

- repository does not currently expose a complete committed retail SV/Z-A catalog row dump in the searched source tree.

### `KotMatrosk1n/KM-Editor`

Relevant files:

- `src/KM.SV/Models/SvModelPreviewService.cs`
- `src/KM.ZA/Models/ZaModelPreviewService.cs`
- `src/KM.ZA/GameModules/ZaPokemonResourceCatalogService.cs`
- `src/KM.ZA/Data/ZaDataPaths.cs`
- `src/KM.Tools/Application/GameModuleProviders.cs`

Value:

- title-aware Scarlet/Violet and Z-A resource-catalog handling;
- explicit species/form/gender projection;
- model/material/shiny/animation loading based on catalog data;
- explicit Z-A catalog path and game-specific namespace.

Limitation:

- expects project/dump data; no complete retail catalog row export located in the searched repository source.

### `TM-C0M8U570RZ/trpmcatalog-anvil`

Value:

- independently identifies the Scarlet/Violet catalog path;
- provides tooling around `trpmcatalog` editing/inspection.

Limitation:

- no complete decoded retail Generation IX row dump located in the searched source.

### `pkZukan/poke-dot`

Value:

- references the Z-A catalog path and catalog-format code.

Limitation:

- no complete decoded retail row set located in the searched source.

### `kwsch/pkNX`

Value:

- verifies Trinity resource-container baseline for Generation IX;
- provides the earlier Legends: Arceus `PokeResourceTable` schema and explicit `pm{species}_{gender}_{form}` tool naming mapping.

Limitation:

- current Gen IX file mapping exposes container support rather than a committed Scarlet/Violet or Z-A catalog row dump.

## Public model/preservation search findings

Public Scarlet/Violet model preservation is useful for asset-identity cross-checking even when it does not contain native catalog keys.

Examples observed:

- Alolan Raichu: `pm0026_00_11`.
- Pikachu: `pm0025_00_00`, `pm0025_01_00`, and special resources `pm0025_11_00` through `pm0025_18_00`.

These examples help test a suffix hypothesis but do not replace native row evidence.

## GitHub issue search

A search for issues containing `poke_resource_table.trpmcatalog` returned no useful public issue result in the connected search surface during this pass.

## General web search

Searches combining:

- `poke_resource_table.trpmcatalog`
- `Scarlet Violet`
- `dump`
- `model_path`
- known resource names such as `pm0026_00_11`

primarily surfaced source-code implementations or model preservation pages. No complete row dump containing native key + model path was located in this pass.

## Current conclusion

**No complete public Scarlet/Violet or Z-A native catalog row dump was located in this search pass.**

This is not evidence that none exists. It means the currently surveyed public indexed/searchable sources did not expose one.

The project therefore continues with:

1. exhaustive public model-resource census already generated;
2. native schema/key/path-pairing evidence from public implementations;
3. suffix-semantic hypotheses kept explicitly provisional;
4. continued search for decoded native rows or equivalent high-confidence evidence;
5. no fabricated native crosswalk rows.

## Revisit triggers

Repeat/extend this search when any of the following appears:

- a new public datamining repository;
- a release/artifact containing catalog reports;
- a tool adds JSON/CSV export examples;
- issue/PR attachments expose decoded tables;
- a public preservation project publishes full resource metadata;
- the project's source registries identify a newly available source.

When a row dump is found, preserve its exact source version, file hash, retrieval date, and decoding tool version before merging it into the crosswalk.
