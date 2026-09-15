# Generation IX → Generation III Battle Sprite Master v1 — Technical Baseline

Research date: **2026-09-15**

Status: **verified from current public reverse-engineering source code; direct game-byte verification remains pending because this project has no local retail ROM/game dump**

## 1. Scarlet / Violet Pokémon resource catalog

Public KM-Editor source currently identifies the Scarlet/Violet Pokémon model catalog as:

`pokemon/catalog/catalog/poke_resource_table.trpmcatalog`

The catalog parser/model-preview path exposes logical identity fields for:

- species
- form
- gender
- model path
- optional material-table path used to derive shiny material variants

Model paths are resolved relative to:

`pokemon/data/catalog`

and accepted Pokémon model resources resolve under:

`pokemon/data/`

with the model extension:

`.trmdl`

### Consequence for BATTLE_MASTER_V1

Scarlet/Violet canonical-source selection must operate at least at:

`species × form × gender × normal/shiny × game/version`

rather than one model per National Pokédex species.

The material-table relationship means shiny must be tracked as a material/texture variant relationship when that is how the source represents it; it must not be treated as an unrelated painted sprite.

## 2. LEGENDS Z-A Pokémon resource catalog

Public KM-Editor source currently identifies the Z-A Pokémon resource catalog as:

`ik_pokemon/catalog/catalog/poke_resource_table.trpmcatalog`

Z-A model paths are resolved relative to:

`ik_pokemon/data/catalog`

and accepted model resources resolve under:

`ik_pokemon/data/`

with the model extension:

`.trmdl`

The public catalog/model-preview implementation likewise exposes:

- species
- form
- gender
- model path
- material-table path
- shiny material variant relationship

### Consequence for BATTLE_MASTER_V1

Z-A is not merely a Scarlet/Violet path alias. Its Pokémon resource namespace is different and its catalog/parser implementation must remain separately attributable.

Mega Evolutions and any Z-A-specific forms must be enumerated from the Z-A catalog/form data rather than inferred from Scarlet/Violet availability.

## 3. Trinity model structure

Public GFTool source includes a Trinity `.trmdl` model structure (`TRMDL`) with mesh data and model-viewer/file-explorer handling for `.trmdl` files.

This confirms that `.trmdl` is an actionable public technical target for model-source reconstruction rather than only an opaque filename observed in screenshots or fan documentation.

## 4. Materials and texture references

GFTool public model/material code exposes material texture references and renderer-side texture loading from model/material structures.

For the Generation III conversion pipeline this means source provenance should not stop at the `.trmdl` path. Where available, each canonical-source record should preserve:

- model path/hash
- material resource path/hash
- texture resource path/hash
- normal/shiny material relationship
- material-animation relationship where relevant to appearance

A rendered 2D reference without this dependency graph is lower-confidence than a reproducibly resolved model/material/texture source set.

## 5. Animation baseline

Current public KM-Editor model-preview implementations expose animation resources separately from the static model and attempt to select a representative default wait animation with the identifier:

`00000_defaultwait01_loop`

when available.

Scarlet/Violet public code resolves animation-catalog/resource relationships including `.tracn` and `.tracr` resources, then resolves skeletal and material-animation dependencies.

Z-A public code similarly resolves animation resource groups and skeletal/material animation dependencies, but through Z-A-specific catalog logic.

### Consequence for battle sprite composition

A static Generation III front/back sprite must not be created by arbitrarily freezing any available animation frame.

The source-pose decision must record:

- selected animation/pose id
- frame/time selection if a frame is sampled
- camera orientation
- battle-facing orientation
- anchor/ground relationship
- why the pose is representative

A default wait animation is a high-priority candidate for canonical review, not an automatic final choice.

## 6. Source graph hashing requirement

Public model-preview source already hashes loaded source files to detect changes during a preview session. The Generation III pipeline adopts the same reproducibility principle at the asset-package level.

For every canonical render, record SHA-256 for every available dependency used to produce it:

- catalog member
- model
- material table
- textures
- skeleton
- animation resources
- material-animation resources
- rendered intermediate

If the same logical role is rebuilt from different source hashes, it is a new source revision and must not silently overwrite the prior result.

## 7. Current confirmed namespace differences

| Axis | Scarlet/Violet | LEGENDS Z-A |
| --- | --- | --- |
| Pokémon catalog | `pokemon/catalog/catalog/poke_resource_table.trpmcatalog` | `ik_pokemon/catalog/catalog/poke_resource_table.trpmcatalog` |
| model namespace | `pokemon/data/` | `ik_pokemon/data/` |
| model extension | `.trmdl` | `.trmdl` |
| species/form/gender catalog identity | confirmed in public tooling | confirmed in public tooling |
| shiny material relationship | confirmed in public tooling | confirmed in public tooling |
| animation handling | Trinity resources; SV implementation | Trinity resources; Z-A-specific implementation |

Shared file extensions do not prove identical semantics. Parsers and resource relationships remain game-specific until verified equivalent.

## 8. Immediate implementation implication

The next executable research deliverable is not a sprite resize script.

It is a **Pokémon resource-role census** capable of enumerating, from available public evidence and later direct game data when available:

`game/version → species → form → gender → normal/shiny → model → material table → textures → animations`

That table becomes the source of truth for canonical front/back rendering and only then feeds the Generation III 64×64 indexed conversion stage.

## 9. Evidence sources used for this baseline

- `kwsch/pkNX` — Generation IX `data.trpfd` / `data.trpfs` mapping evidence
- `pkZukan/gftool` — Trinity file/model structures, `.trmdl`, model/file explorer and rendering code
- `KotMatrosk1n/KM-Editor` — Scarlet/Violet and Z-A Pokémon resource catalogs, model namespaces, species/form/gender roles, shiny material variants, animation/dependency resolution

These are public third-party reverse-engineering sources. They are not substituted for direct game-byte provenance when direct verification later becomes available.
