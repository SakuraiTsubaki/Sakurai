# Generation IX → Generation III Battle Sprite Master v1 — Source Census

Research date: **2026-09-15**

Status: **Phase 1 in progress — public-source census, no local retail ROM/game dump required**

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

This is useful as independent technical evidence that Scarlet/Violet and Z-A expose a Trinity-style resource-container baseline in public reverse-engineering tooling.

Verification state: **public technical source; exact game-version resource inventory still incomplete**.

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

Public project scope includes Scarlet, Violet, and LEGENDS Z-A and exposes 3D model inspection/editing workflows across supported games. It is useful for:

- model availability cross-checks
- texture/material handling evidence
- animation support/limitations
- game-specific Pokémon data references

Verification state: **public technical/modding source; bundled visual assets require per-file provenance/licensing review**.

## 4. Pokémon model-role evidence

### Scarlet/Violet scene-data output

Source: `https://gist.github.com/sora10pls`

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

## 7. Required census axes per Pokémon logical role

The complete census must eventually account for every applicable combination of:

- species/internal species id
- form
- sex/gender presentation
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

## 8. Canonical-source decision states

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

## 9. Immediate research queue

1. Enumerate Scarlet/Violet Pokémon model/texture naming and archive/member conventions from public Trinity tooling/documentation.
2. Enumerate Z-A model/texture naming and resource differences separately.
3. Build the complete form/sex/shiny logical-role table for Scarlet/Violet.
4. Build the complete form/sex/shiny/Mega logical-role table for Z-A.
5. Reconcile DLC/update additions and changed visual resources.
6. Establish reproducible model-render capture settings for front/back canonical review.
7. Only after the above, begin Generation III 64×64 palette/index conversion candidates.

## 10. Provisionality rule

Because the project currently has no local retail ROM/game dump, absence of direct game bytes does **not** stop work. It only changes the provenance status.

Any source later superseded by a closer verified source remains in history and the manifest; it is not silently erased.
