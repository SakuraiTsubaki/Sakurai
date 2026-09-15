# Generation VI battle sprite master v1

## Status

**Active Generation III insertion master contract — source research / reconstruction phase.**

This directory defines the cross-title Generation VI battle-sprite reconstruction pipeline for Pokémon X, Pokémon Y, Pokémon Omega Ruby, and Pokémon Alpha Sapphire.

This is a derived cross-repository work item because it combines material and evidence from these Generation VI decompilation namespaces:

- `PocketMonsters-X-Decompilation`
- `PocketMonsters-Y-Decompilation`
- `PocketMonsters-OmegaRuby-Decompilation`
- `PocketMonsters-AlphaSapphire-Decompilation`

Historical `GEN-*`, `GENERATION-*`, `CROSS-GEN`, and `INFRA/QUARANTINE` trees are migration/provenance inputs only. New work follows the current `derived/` architecture.

## Project-wide fixed contract

The goal is not merely to produce a 64×64 PNG. The complete path from the closest verifiable Generation VI source to the final Generation III insertable graphics must be reproducible, inspectable, hashable, and visually validated.

Source priority is evidence-based rather than ROM-presence-based:

1. Directly decoded game data is preferred when available.
2. Lack of a ROM or direct extraction path never by itself stops the work.
3. When direct game data is unavailable, use the closest verifiable official or preservation-grade material: verified extracted models/textures/animations, official renders, in-game captures, official site/distribution graphics, or preservation-project output.
4. Web previews, enlarged PNGs, screenshots, mirrors, and converted exports may be used only with their limitations recorded. They are not automatically byte-equivalent to game-native data.
5. If multiple candidate sources exist, compare geometry/texture identity, dimensions, formats, metadata, member location, hashes, rendering behavior, and visual output before selecting a canonical source.

## Generation VI is not an indexed-2D battle-sprite source

Generation VI mainline battles use 3D Pokémon models rather than Generation III–V style dedicated 2D front/back battle sprites.

Therefore:

- no nonexistent Generation VI 2D battle sprite may be described as an original asset;
- the 40×30 Pokémon box/party icon is not the battle-sprite source;
- web-distributed 120×120 or similar PNG renders are not automatically treated as game-native battle sprites;
- the canonical visual source for this pipeline is the Generation VI 3D Pokémon model/texture/material/animation system plus verified in-game battle presentation evidence.

The final 64×64 front/back sprites are **Generation III-target reconstructions derived from Generation VI official game visuals**, not recovered native Generation VI 2D sprites.

## Known native archive locations

Current public reverse-engineering documentation identifies:

### Pokémon X / Y

- Pokémon model archive: `a/0/0/7`
- Pokémon box/party icons: `a/0/9/3` (40×30; UI asset only, not battle-master source)
- item icons: `a/0/9/4` (30×30; unrelated to Pokémon battle master)

### Omega Ruby / Alpha Sapphire

- Pokémon model archive: `a/0/0/8`
- trainer battle models: `a/1/3/3`
- trainer mugshots: `a/1/6/0`

Public ORAS extraction notes describe recurring Pokémon/form groups containing a model container, normal texture, shiny texture, and animation/material/visibility-related members. These patterns are evidence to inventory, not a license to assume every species/form block is identical. Every member relationship must be verified per archive.

## Known model/resource families

Reverse-engineering tools and preservation projects identify Generation VI Pokémon resources using Game Freak / Nintendo 3DS model families including:

- `PC` / `PS` containers
- BCH/H3D-related containers
- GFModel geometry/skeleton data
- GFTexture texture data
- GFMotion animation data
- material / visibility / skeletal animation tracks

Older extraction tooling commonly labels members with `.pc`, `.pt`, `.pb`, `.pk`, `.pf`, or BCH-derived extensions. These tool-generated extensions must never replace the primary provenance key. The authoritative identifier is the original archive/member coordinate plus file signature/hash.

## Source inventory requirements

Before sprite reconstruction, inventory every battle-relevant logical visual state represented by XY and ORAS, including:

- all species available in Generation VI
- every battle-visible alternate form
- gender-dependent model/texture differences
- Mega Evolutions
- Primal Groudon / Primal Kyogre
- Mega Rayquaza
- special battle-visible states whose geometry or texture changes
- normal texture state
- shiny texture state
- model mesh/skeleton identity
- material state
- visibility animation state
- skeletal animation state where available
- game/version identity even where the underlying source proves identical

Do not collapse X/Y and ORAS identities merely because they appear visually identical. Deduplication occurs only after identity is verified.

## Canonical rendering tracks

Generation III requires distinct front and back battle assets. Generation VI generally uses one 3D model viewed from different battle cameras rather than separate native front/back sprite sheets.

Accordingly the master uses two reconstruction tracks:

### Front track

Represents the opponent-side in-battle view of the Pokémon using the verified Generation VI battle model, textures, materials, visibility state, pose/animation state, and opponent-side camera relationship.

### Back track

Represents the player-side rear battle view of the same official model using the verified player-side camera relationship and battle pose.

Front and back are therefore independently rendered/reconstructed target assets even when they originate from one shared model.

## Pose and animation rule

Do not use an arbitrary pose, arbitrary animation tick, bind pose, export-tool default pose, or marketing render simply because it is convenient.

For each logical asset, record:

- animation/motion identifier if known
- animation frame/timestamp selected
- material/visibility animation state
- camera/view identifier or reconstructed camera transform
- model transform / scale / anchor
- source evidence used to justify that state

The preferred canonical static state is the verified normal in-battle idle presentation for the corresponding side. Until a game-native motion/camera mapping is verified, any externally reconstructed pose or view remains `provisional` and cannot receive final-master status.

## Spatial preservation rule

Generation IV/V full-canvas preservation cannot be copied mechanically because Generation VI does not provide a native 2D battle canvas.

Instead, Generation VI requires a reproducible **canonical render canvas**.

For each source/game/view combination:

1. render or reconstruct the verified battle-facing model state on a transparent reference canvas;
2. preserve a common battle anchor and camera convention across species;
3. do not crop each Pokémon to its opaque bounds and enlarge it independently;
4. do not normalize all species to the same occupied height or width;
5. preserve relative species scale and battle placement as supported by in-game evidence;
6. record the render-canvas dimensions, projection, camera parameters, model transform, and anchor in the manifest;
7. only then convert that canonical render canvas to the Generation III 64×64 target.

A species-specific opaque-bounding-box fit is prohibited because it destroys relative scale and presentation.

## Generation III target

Final Pokémon battle assets target the standard Generation III battle-sprite constraints:

- 64×64 canvas
- indexed/4bpp-compatible graphics
- maximum 16 palette entries per sprite palette, including the transparent entry as required by the target format
- separate front and back graphics
- normal and shiny palette relationships retained as target data
- insertion-ready 4bpp graphics
- insertion-ready compressed graphics data where required by the target engine

The Generation III source projects use 64×64 OAM battle sprites and compressed front/back graphics/palette tables; final assets must be able to enter that pipeline rather than existing only as display PNGs.

## True-color / 3D color reconstruction rule

Generation VI textures and rendered output are not treated as if they were an indexed Generation IV/V sprite.

Do not:

- take a true-color render and automatically keep the 15 most frequent opaque colors;
- quantize only by global frequency;
- bilinear/bicubic resize into a 64×64 RGB image and then accept the result;
- generate antialiased intermediate colors;
- use AI redraw, AI retouch, AI upscaling, or generative-image tools;
- invent colors that are unsupported by the source design.

Instead, identify the Pokémon's visual identity structure before palette reduction, including as applicable:

- principal body colors
- shadow groups
- highlight groups
- eyes and facial details
- species-defining markings
- metallic/ornamental areas
- wing/membrane colors
- glow/emissive accents
- mouth/tongue/claw/horn accents
- other rare but identifying colors

Palette reduction must preserve those semantic color roles even when a role occupies only a small number of pixels.

## Geometric down-conversion rule

The canonical render must be reduced deterministically to 64×64 without antialiasing or RGB interpolation.

The preferred reconstruction pipeline is:

1. establish the canonical transparent render canvas and common battle anchor;
2. establish the target Generation III palette through documented semantic source analysis;
3. map source/render pixels to source-supported target color roles without creating intermediate colors;
4. reduce geometry using deterministic area/coverage logic rather than bilinear/bicubic filtering;
5. preserve thin identity features with mild rare-detail protection;
6. apply silhouette protection so coverage does not collapse narrow limbs, ears, wings, horns, tails, or outline edges solely because of transparent majority;
7. validate the automatic 64×64 result against the canonical source render;
8. permit only minimal documented manual pixel correction when Generation III constraints erase a clearly source-supported defining feature.

For true-color/3D inputs, unlike indexed Gen IV/V, the final palette is a documented reconstruction palette; it must not be mislabeled as an original Generation VI palette.

## Normal / shiny rule

When game-native normal and shiny texture resources are available, both must be preserved independently at source level.

Do not create the shiny result by hue-shifting or recoloring the final normal 64×64 sprite if the original Generation VI shiny texture exists.

Normal and shiny assets may share target geometry/index topology only if validation demonstrates that doing so preserves the source-supported color structure without losing shiny-specific detail.

## Form and gender rule

A form/gender state receives an independent logical record whenever Generation VI loading logic or source assets distinguish it, even if the final 64×64 result deduplicates to another asset.

This includes logical aliases and identical-result states. Never remove a form/gender relationship merely because its rendered pixels match another record.

## XY / ORAS separation

X, Y, Omega Ruby, and Alpha Sapphire remain four separate game identities in provenance.

- XY source members come from the XY archive structure.
- ORAS source members come from the ORAS archive structure.
- A model/texture/render may deduplicate only after hash/structure/visual equivalence is verified.
- ORAS-only Mega Evolutions, Primal Reversion assets, and other additions remain ORAS-specific logical records where applicable.
- Version-exclusive availability does not imply a different model by itself; availability and asset identity are recorded separately.

## Automatic processing and manual correction

Prefer deterministic scripts for every repeatable stage.

Minimal manual pixel correction is allowed only when the deterministic Generation III conversion clearly damages source-supported identity information such as an eye, marking, silhouette edge, horn, small appendage, or other defining detail.

Manual correction must never redesign or modernize the Pokémon.

For every manual correction preserve:

- automatic output
- corrected output
- pixel coordinates changed
- previous and replacement palette indices
- reason for the correction
- source evidence
- validation before/after state

## Required outputs — no optional items

A logical battle-sprite record is incomplete unless all applicable outputs and evidence exist:

- source model/container reference
- source texture reference
- source normal texture or faithful reconstruction
- source shiny texture or faithful reconstruction
- source animation/material/visibility references where applicable
- canonical source render PNG (front)
- canonical source render PNG (back)
- exact render metadata (camera, projection, pose/timestamp, transform, anchor, canvas)
- automatic 64×64 PNG
- final validated 64×64 PNG
- reconstructed Generation III palette data
- Generation III 4bpp graphics data
- Generation III compressed graphics data
- source-to-target manifest
- source provenance record
- source archive/member mapping
- source SHA-256 values for every retained source/intermediate file
- canonical-render SHA-256
- automatic-output SHA-256
- final PNG SHA-256
- final rendered-pixel SHA-256
- final palette SHA-256
- final 4bpp SHA-256
- final compressed-binary SHA-256
- logical slot → canonical asset table
- duplicate/canonical SHA-256 dedup table
- conversion scripts and exact configuration
- automatic conversion output
- manual correction output/history when used
- source/final side-by-side comparison material
- validation results and error records
- all metadata needed to reproduce the same outputs and hashes

PNG-only output is not completion.

## Deduplication

Use SHA-256 of the final rendered-pixel result as the global visual deduplication key for final 64×64 assets.

Additionally retain hashes for source models, source textures, canonical renders, palettes, 4bpp data, and compressed binaries so source-level identity is not confused with visual-output identity.

Deduplication removes duplicate bytes only. It must retain every logical relationship across:

- game
- version
- region/language/revision
- species
- form
- gender
- normal/shiny
- front/back
- source archive/member
- pose/view state

## Provenance requirements

Every logical record must include at least:

- generation
- game/title
- version
- region
- language
- revision or explicit unresolved state
- species identifier / National Dex number
- form identifier
- gender/logical gender state
- normal/shiny state
- front/back target role
- source type (`game-model`, `verified-extraction`, `official-render`, `in-game-capture`, `reconstructed`, etc.)
- source archive/member coordinate when available
- original file signature/container type
- model identifier/hash
- texture identifier/hash
- animation/material/visibility identifiers
- canonical camera/view evidence
- canonical pose/frame/timestamp
- render-canvas size
- anchor/scale/camera/projection parameters
- conversion method/version
- target palette construction record
- manual-edit status
- every intermediate/final SHA-256
- canonical dedup target
- evidence/verification level

Unknown values remain explicitly `unknown` or `unresolved`. Do not guess to fill a table.

## Repository split

### Sakurai

Store research/control and reproducibility material:

- source/archive/member analysis
- model/texture/animation mappings
- camera/pose research
- source provenance
- conversion specifications
- scripts/configuration
- manifests
- SHA-256 inventories
- dedup tables
- validation
- visual review/comparison records
- reconstruction/rebuild documentation

### Tsubaki

Store eligible production/archive assets:

- retained/extracted/reconstructed non-ROM source assets when permitted by the project rules
- canonical source renders
- automatic 64×64 renders
- final validated 64×64 PNGs
- Generation III palettes
- Generation III 4bpp graphics
- Generation III compressed graphics binaries
- insertion-ready canonical sprite assets
- required intermediates and complete reproducibility package

Original ROM/cartridge/ISO images are excluded from GitHub.

## Acceptance checks

`BATTLE_MASTER_V1` is accepted only when all of the following pass:

- closest-source provenance is recorded
- direct game data is preferred when available, without making ROM access a prerequisite
- no nonexistent native Gen VI 2D battle sprite is claimed
- XY and ORAS archive identities are retained
- model/texture/form/gender/normal/shiny inventory is reconciled
- canonical front/back camera and pose state is evidence-backed
- relative battle scale/placement is preserved; no per-species opaque-bbox normalization
- no generative imagery is used
- no antialiasing or RGB interpolation is used in final pixel conversion
- palette construction preserves species identity rather than frequency alone
- normal/shiny source relationships are respected
- all forms and special battle-visible states are inventoried
- required PNG/palette/4bpp/compressed/manifest/hash/provenance/validation outputs exist
- every logical record resolves to a canonical asset
- dedup loses zero logical references
- visual validation confirms the final result still reads immediately as the original Pokémon
- rebuild metadata can reproduce the same final binaries and hashes

## Initial evidence references

Public technical references used to establish the initial archive/format baseline include:

- Project Pokémon — X/Y File System: https://projectpokemon.org/home/docs/gen-6/xy-file-system-r89/
- Project Pokémon — ORAS File System: https://projectpokemon.org/home/docs/gen-6/oras-file-system-r32/
- Project Pokémon — Consolidated Tutorial for X/Y ROM Data Extraction: https://projectpokemon.org/home/forums/topic/36499-consolidated-tutorial-for-xy-rom-data-extraction/
- Project Pokémon — Listing the Pokémon models extracted from ORAS: https://projectpokemon.org/home/forums/topic/34387-listing-the-pokemon-models-extracted-from-oras/
- Ohana3DS Rebirth BCH parser: https://github.com/gdkchan/Ohana3DS-Rebirth
- Nintendo 3DS GFModel/GFTexture/GFMotion importer research: https://github.com/sxrmss/n3ds_importer
- pret/pokeemerald Generation III target implementation reference: https://github.com/pret/pokeemerald

These references establish a working baseline only. Game/archive/member mapping and render-state claims must still be verified per asset before final-master acceptance.
