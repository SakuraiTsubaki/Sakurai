# Generation IX → Generation III Battle Sprite Master v1 — Source Census

Research date: **2026-09-15**

Status: **Phase 1 technical census established; Phase 2 public role census complete for pinned source; native catalog crosswalk continues**

This census records candidate sources for reconstructing Generation IX Pokémon battle visuals for Generation III conversion. A source appearing here does not automatically make it canonical. Canonical selection is performed per logical sprite role and must be recorded in the manifest.

## 1. Game identities

| Source family | Upstream repository | Status |
| --- | --- | --- |
| Pokémon Scarlet | `PocketMonsters-Scarlet-Decompilation` | active public-source reconstruction |
| Pokémon Violet | `PocketMonsters-Violet-Decompilation` | active public-source reconstruction |
| Pokémon LEGENDS Z-A | `PokemonLegends-Z-A-Decompilation` | active public-source reconstruction |

Scarlet and Violet remain separate game identities even when files or rendered results are identical. LEGENDS Z-A is a separate implementation family and is never normalized to Scarlet/Violet structure without evidence.

## 2. Existing upstream source registries

The three upstream decompilation repositories already record the public-source/no-local-ROM research mode and Japanese-origin baseline in `manifests/source-registry.json`.

### Scarlet registry

`PocketMonsters-Scarlet-Decompilation/manifests/source-registry.json`

Already records:

- official Nintendo product/update sources
- `kwsch/pkNX`
- `pkZukan/gftool`
- `KotMatrosk1n/KM-Editor`
- `Pokemon-Project-com/sv-text`
- `TM-C0M8U570RZ/Titan-Re-Docs`

### Violet registry

`PocketMonsters-Violet-Decompilation/manifests/source-registry.json`

Tracks the corresponding Violet identity with the same public technical-source families where applicable.

### LEGENDS Z-A registry

`PokemonLegends-Z-A-Decompilation/manifests/source-registry.json`

Already records:

- official Nintendo/Pokémon product, update, and HOME information
- `kwsch/pkNX`
- `KotMatrosk1n/KM-Editor`
- `projectpokemon/za-textport`
- `Digote/pokedat`
- `zbirow/Pokemon-Legends-Z-A-Tools`
- `Ruimusume/PLZA`

## 3. Resource/container evidence

### pkNX

Source: `https://github.com/kwsch/pkNX`

Public `GameFileMapping.cs` currently maps both Generation IX families to:

- `arc/data.trpfd`
- `arc/data.trpfs`

The older Legends: Arceus `PokeResourceTable` implementation also provides an explicit Trinity resource naming mapping:

`pm{species:0000}_{gender:00}_{form:00}`

This is confirmed as a tool mapping for Legends: Arceus and used only as continuity evidence for Generation IX until native Generation IX rows are observed.

Verification state: **public technical source; exact Generation IX game-version resource inventory remains incomplete**.

### GFTool

Source: `https://github.com/pkZukan/gftool`

The public project describes tools/libraries for Game Freak Trinity files and explicitly includes:

- TRPFS/TRPFD virtual filesystem support for Scarlet/Violet
- Trinity File Explorer
- Trinity Model Viewer
- model view/export/import work
- Trinity scene/object tooling

This makes it a high-priority technical source for locating and understanding model/texture/scene material when original game bytes are not locally available.

Verification state: **public reverse-engineering implementation; member-by-member Pokémon resource map still required**.

### KM Editor

Source: `https://github.com/KotMatrosk1n/KM-Editor`

Public project scope includes Scarlet, Violet, and LEGENDS Z-A and exposes 3D model inspection/editing workflows across supported games.

Verified useful evidence includes:

- Scarlet/Violet catalog: `pokemon/catalog/catalog/poke_resource_table.trpmcatalog`
- Scarlet/Violet model namespace: `pokemon/data/`
- Z-A catalog: `ik_pokemon/catalog/catalog/poke_resource_table.trpmcatalog`
- Z-A model namespace: `ik_pokemon/data/`
- title-aware model/material/shiny handling
- species/form/gender catalog projection
- animation-resource handling

Verification state: **public technical/modding source; bundled visual assets require per-file provenance/licensing review**.

### sv2za

Source: `https://github.com/Aqua-0/sv2za`

This is currently one of the strongest semantic sources for Phase 2B because it:

- parses both Scarlet/Violet and Z-A `poke_resource_table.trpmcatalog` files;
- defines the native key as `(species:u16, form:u16, gender:u8)`;
- retains `model_path`, material/config paths, animation and locator information;
- directly pairs a parsed native key with `pm`, `pm_variant`, and `model_path`;
- compares Scarlet/Violet and Z-A by native key;
- provides `catalog_inspect` for row-level inspection when catalog bytes are supplied.

Verification state: **strong public reverse-engineering implementation; no complete committed retail SV/Z-A decoded catalog dump located in the current public search pass**.

### trpmcatalog-anvil / poke-dot

Sources:

- `https://github.com/TM-C0M8U570RZ/trpmcatalog-anvil`
- `https://github.com/pkZukan/poke-dot`

These independently reinforce Generation IX catalog paths and format/tooling, but the current searched source trees did not expose a complete decoded retail catalog row set.

## 4. Pokémon model-role evidence

### Pinned PokemonModelViewer configuration corpus

Source: `https://github.com/freedom12/PokemonModelViewer`

Pinned commit:

`c5952930343748e6dcb4cae21ee383e0bd13b75c`

The repository's own generator mechanically scans Generation IX model directories named `pmXXXX_YY_ZZ` and emits per-ID configuration files with source-local fields named:

- `formIndex = YY`
- `variantIndex = ZZ`
- icon path
- animation-name/file inventory

These labels are preserved exactly and are **not** assumed to equal native catalog `form` / `gender` fields.

The deterministic project parser has exhaustively processed the pinned SCVI and LZA configuration trees.

#### SCVI result

- config IDs: **735**
- complete config coverage: **735 / 735**
- resource-role rows: **980**
- unique resource IDs: **980**
- IDs with multiple resource roles: **166**
- animation names: **51,771**
- animation-file references: **103,379**
- parser consistency issues: **0**

#### LZA result

- config IDs: **366**
- complete config coverage: **366 / 366**
- resource-role rows: **590**
- unique resource IDs: **590**
- IDs with multiple resource roles: **142**
- animation names: **41,790**
- animation-file references: **83,580**
- parser consistency issues: **0**

Generated results are under `generated/public-model-role-census/`.

Verification state: **exhaustive for this pinned secondary public configuration source; not equivalent to a retail native catalog dump**.

### Scarlet/Violet scene-data output

Source: public `sora10pls` scene-data output.

The public Scarlet/Violet scene-data Pokémon model output records model-component fields including examples of:

- Pokémon development/internal identifier
- form identifier
- sex
- rare/shiny state
- egg state
- scale
- visibility

This is important because the Generation III conversion manifest must not collapse form/sex/shiny/model roles into a single species-level image.

Verification state: **public extracted/reverse-engineered scene data; use as role-structure evidence, not as a replacement for model/texture bytes**.

### Independent model preservation

Public Scarlet/Violet model preservation provides asset-identity cross-checks, including:

- Alolan Raichu: `pm0026_00_11`
- Pikachu resource family including `pm0025_00_00`, `pm0025_01_00`, and `pm0025_11_00` through `pm0025_18_00`

These examples prove that suffix axes must be preserved raw. They do not by themselves complete the native catalog crosswalk.

Verification state: **secondary preserved-asset identity evidence**.

## 5. 2D image families — secondary evidence only

Generation IX includes many official/game-derived 2D image families, but none is automatically the canonical battle source merely because it is a convenient PNG.

Current confirmed working/reference families include:

### Scarlet/Violet

- Pokémon menu `Big` images: commonly exposed as **256×256** PNGs in public preservation/export sets
- separate `Small` and historical pre-update menu-image families exist; exact source/native specifications must be verified independently before use
- bag/item image family: examples verified at **160×160**
- type-symbol image family: examples verified at **60×60**
- rectangular type-label UI family: examples verified at **200×40**
- Pokédex artwork resource references publicly documented at **1024×1024**
- Pokédex cover/thumbnail resource references publicly documented at **204×238**
- current Scarlet repository Star Mobile public-GitHub sample images: **94×94**; these are not a universal Pokémon battle-sprite specification

### LEGENDS Z-A

- Pokémon menu image family publicly preserved at **160×160** for normal and shiny menu sprites

### Rule

These assets may be used for:

- design cross-checking
- markings/color reference
- form/sex/shiny enumeration
- comparison against rendered model output
- provisional source only when a closer source is unavailable

They may **not** be automatically downscaled to 64×64 and promoted as the battle master.

## 6. Source-selection evidence ladder

Each candidate gets one of these source classes:

| Class | Meaning | Canonical preference |
| --- | --- | --- |
| `game_native` | directly decoded game resource with verified path/version | highest |
| `verified_extract` | public extraction preserving original structure and provenance | very high |
| `official_render` | official render/site/distribution visual | high |
| `game_capture` | verified in-game capture of the actual model/state | high for pose/presentation |
| `preservation_mirror` | public preserved asset with sufficient provenance | medium/high depending on verification |
| `web_preview` | resized/re-encoded preview or mirror | low |
| `reconstructed` | project reconstruction based on multiple lower-level sources | provisional until validated |

The highest available class is not blindly accepted: completeness, form correctness, pose, texture/material accuracy, update version, and reproducibility must also be checked.

## 7. Native crosswalk evidence ladder

Native-key/resource-path semantics use a separate state machine:

- `CONFIRMED_NATIVE_ROW`
- `CONFIRMED_TOOL_MAPPING`
- `SUPPORTED_BY_ASSET_IDENTITY`
- `INFERRED_FROM_CONTINUITY`
- `CONFLICT`
- `UNRESOLVED`

The current strongest whole-family suffix hypothesis remains provisional. See `NATIVE_CATALOG_CROSSWALK.md`.

## 8. Required census axes per Pokémon logical role

The complete census must eventually account for every applicable combination of:

- native species/internal species id
- National Pokédex mapping where applicable
- native form
- native gender/catalog presentation field
- interpreted sex/costume/presentation role
- normal/shiny
- Scarlet/Violet/Z-A game identity
- update/revision
- DLC/additional-content ownership
- model geometry source
- texture source
- material source
- relevant animation/pose source
- front battle interpretation
- back battle interpretation
- menu/Pokédex/official-render cross-checks
- source availability state
- source redistribution state
- source hash availability
- canonical-source decision state

## 9. Canonical-source decision states

Every role must be one of:

- `UNRESEARCHED`
- `SOURCES_FOUND`
- `CROSSCHECK_PENDING`
- `CANONICAL_PROVISIONAL`
- `CANONICAL_VERIFIED`
- `CONVERSION_IN_PROGRESS`
- `CONVERTED_AUTO`
- `MANUAL_REVIEW_REQUIRED`
- `FINAL_VALIDATED`

No role skips directly from `UNRESEARCHED` to `FINAL_VALIDATED`.

## 10. Current research queue

1. Continue native catalog row search and semantic crosswalk (`Phase 2B`).
2. Reconcile public `pmXXXX_YY_ZZ` roles against native `(species, form, gender)` without silently renaming suffix axes.
3. Split Scarlet vs Violet update/DLC ownership where evidence differs.
4. Complete Z-A Mega/form/presentation role mapping separately.
5. Resolve normal/shiny material-table relationships per role.
6. Establish reproducible front/back model-render capture settings and battle anchor/scale rules.
7. Only after canonical source decisions, begin Generation III 64×64 indexed conversion candidates.

Search coverage and the current missing-native-dump limitation are recorded in `PUBLIC_NATIVE_CATALOG_SEARCH.md`.

## 11. Provisionality rule

Because the project currently has no local retail ROM/game dump, absence of direct game bytes does **not** stop work. It only changes the provenance status.

Any source later superseded by a closer verified source remains in history and the manifest; it is not silently erased.
