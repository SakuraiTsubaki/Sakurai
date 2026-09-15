# Generation IX → Generation III Battle Sprite Master v1 — Phase Status

Updated: **2026-09-15**

## Phase 0 — fixed contract

Status: **COMPLETE**

Fixed:

- Generation III target is 64×64 indexed/4bpp-compatible battle graphics.
- PNG-only output is never considered complete.
- Final packages require palette, BGR555, 4bpp, compressed graphics, manifests, SHA-256, dedup, validation and provenance.
- No generative image tools, AI redraw, AI retouch or AI upscaling.
- No automatic frequency-only palette reduction accepted as final.
- Gen IV/V preservation-v2 philosophy is inherited where technically applicable.
- Gen IX 3D/true-color sources require a separate identity-preserving conversion path rather than pretending an official indexed 2D battle sprite exists.
- Scarlet, Violet and LEGENDS Z-A remain separate source families.
- No local ROM/game dump is required to continue public-source research.
- Sakurai owns research/control material; Tsubaki receives production assets after they actually exist.

## Phase 1A — source family census

Status: **COMPLETE FOR INITIAL TECHNICAL BASELINE; EXHAUSTIVE ENUMERATION CONTINUES**

Verified public technical source families currently include:

- `kwsch/pkNX`
- `pkZukan/gftool`
- `KotMatrosk1n/KM-Editor`
- `Aqua-0/sv2za`
- `hYdos/TrinityFormats`
- `freedom12/PokemonModelViewer`
- `sora10pls` public Scarlet/Violet scene-data output
- upstream official/public registries already recorded in the Scarlet/Violet/Z-A decompilation repositories

## Phase 1B — resource-container baseline

Status: **BASELINE VERIFIED FROM MULTIPLE PUBLIC IMPLEMENTATIONS**

Current public reverse-engineering evidence supports:

- Generation IX `arc/data.trpfd`
- Generation IX `arc/data.trpfs`
- Trinity resource handling
- `.trmdl` Pokémon model resources
- resource dependency handling through models/materials/textures/animations

Direct game-byte hashes are unavailable in the current no-local-ROM research mode and therefore remain unverified rather than fabricated.

## Phase 1C — Pokémon catalog identity

Status: **PUBLIC PARSER STRUCTURE VERIFIED**

Current public parsers establish the key:

`(species u16, form u16, gender u8)`

and expose at least:

- model path
- material-table path
- config path
- animation list
- locator list
- icon path
- unresolved numeric id
- defence-resource path

Normal/shiny material relationships are tracked separately from the species/form/gender key.

## Phase 1D — game-specific namespaces

Status: **VERIFIED FROM CURRENT PUBLIC TOOLING**

### Scarlet / Violet

- catalog: `pokemon/catalog/catalog/poke_resource_table.trpmcatalog`
- model namespace: `pokemon/data/`
- model extension: `.trmdl`

### LEGENDS Z-A

- catalog: `ik_pokemon/catalog/catalog/poke_resource_table.trpmcatalog`
- model namespace: `ik_pokemon/data/`
- model extension: `.trmdl`

Identical extension names do not imply identical game implementations.

## Phase 1E — 2D evidence families

Status: **PARTIALLY ENUMERATED; BATTLE-CANONICAL STATUS REJECTED BY DEFAULT**

Current reference families include:

- Scarlet/Violet 256×256 Big menu Pokémon images
- Scarlet/Violet Small/historical menu-image families
- Scarlet/Violet 160×160 item images
- Scarlet/Violet 60×60 type symbols
- Scarlet/Violet 200×40 type-label UI assets
- Scarlet/Violet Pokédex resource/image families
- LEGENDS Z-A 160×160 normal/shiny menu Pokémon images

These are secondary design/cross-check evidence unless a closer source cannot be obtained.

## Phase 2A — exhaustive public model-role census

Status: **COMPLETE FOR PINNED `PokemonModelViewer` CONFIG SOURCE**

Pinned source:

- repository: `freedom12/PokemonModelViewer`
- commit: `c5952930343748e6dcb4cae21ee383e0bd13b75c`

Deterministic parser/workflow:

- `tools/build_public_model_role_census.py`
- `.github/workflows/gen9-battle-master-public-census.yml`

### Scarlet / Violet (`SCVI`)

- public config IDs: **735**
- config coverage: **735 / 735**
- missing configs: **0**
- model-resource role rows: **980**
- unique resource IDs: **980**
- IDs with multiple resource roles: **166**
- icon references: **980 / 980**
- animation names: **51,771**
- animation-file references: **103,379**
- consistency errors found by parser: **0**

### Pokémon LEGENDS Z-A (`LZA`)

- public config IDs: **366**
- config coverage: **366 / 366**
- missing configs: **0**
- model-resource role rows: **590**
- unique resource IDs: **590**
- IDs with multiple resource roles: **142**
- icon references: **590 / 590**
- animation names: **41,790**
- animation-file references: **83,580**
- consistency errors found by parser: **0**

The generated CSVs preserve the public source's `formIndex` and `variantIndex` names exactly. They are not silently relabeled as native game `form` / `gender` fields.

Detailed results: `PUBLIC_MODEL_ROLE_CENSUS.md` and `generated/public-model-role-census/`.

## Phase 2B — game-native catalog semantic crosswalk

Status: **IN PROGRESS / REQUIRED BEFORE FINAL LOGICAL ROLE CLAIMS**

The public model-role census is secondary evidence and is not treated as the retail `poke_resource_table.trpmcatalog`.

Required crosswalk fields include:

- native species identifier
- National Pokédex mapping where applicable
- native form field
- native gender field
- public config `formIndex` / `variantIndex` relationship
- model path
- material-table path
- config path
- icon path
- animation catalog paths
- normal/shiny material relationship
- Scarlet vs Violet ownership/difference
- update/DLC ownership
- Z-A-specific ownership/difference

Some public config numeric identifiers exceed the established National Pokédex range, so numeric config IDs are **not** automatically treated as National Pokédex numbers.

## Phase 2C — final Generation III logical-role population

Status: **PENDING PHASE 2B CROSSWALK**

The final role census must be keyed by game/version/native species/form/gender/shiny/source role and preserve:

- Scarlet vs Violet identity
- Z-A identity
- DLC/update ownership
- model/material/texture dependencies
- animation/pose candidates
- front/back target roles
- provisional/verified source state

Template: `logical-role.template.json`

## Phase 3 — canonical battle-view reconstruction

Status: **NOT YET PROMOTED**

No sprite is promoted to final conversion until its canonical source and battle composition are recorded.

Required decisions include:

- canonical model/material/texture set
- normal/shiny relationship
- pose/animation id
- frame/time when sampled
- front camera orientation
- back camera orientation
- ground/anchor relationship
- scale rule
- source review evidence

## Phase 4 — Generation III pixel conversion

Status: **BLOCKED BY DESIGN UNTIL PHASE 2/3 ROLE DECISIONS EXIST; RESEARCH ITSELF IS NOT BLOCKED**

Final conversion requires:

- 64×64 indexed result
- <=16 target palette entries as required by the engine path
- BGR555 palette
- 4bpp graphics
- compressed graphics
- deterministic rebuild
- visual identity review
- SHA-256 chain
- dedup mapping

## Current repository artifacts

- `README.md` — fixed master contract
- `SOURCE_CENSUS.md` — public-source census
- `TECHNICAL_BASELINE.md` — model/catalog/animation baseline
- `CATALOG_SCHEMA.md` — normalized Pokémon resource catalog schema notes
- `PUBLIC_MODEL_ROLE_CENSUS.md` — first exhaustive public config census report
- `logical-role.template.json` — per-role provenance/conversion/validation manifest template
- `tools/build_public_model_role_census.py` — deterministic public config parser
- `generated/public-model-role-census/` — generated CSV/summary/provenance outputs
- `PHASE_STATUS.md` — this status record

## Acceptance principle

The project does not count progress by the number of PNGs produced.

Progress is counted only when a logical role becomes more reproducible, more attributable, and closer to a validated Generation III insertion asset without losing the original Pokémon's visual identity.
