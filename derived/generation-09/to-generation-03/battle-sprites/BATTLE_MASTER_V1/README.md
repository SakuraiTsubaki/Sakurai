# Generation IX → Generation III Battle Sprite Master v1

## Status

**Conversion contract fixed. Public-source source census and canonical-visual-source selection in progress.**

This project converts the most original, verifiable Generation IX Pokémon visual sources available for Pokémon Scarlet, Pokémon Violet, The Hidden Treasure of Area Zero, and Pokémon LEGENDS Z-A into reproducible Generation III battle-sprite assets.

The target is not merely a 64×64 PNG. Completion requires a traceable source-to-target pipeline ending in Generation III-compatible indexed graphics, palette data, 4bpp data, compressed graphics, manifests, hashes, deduplication maps, validation, and review evidence.

## Contributing upstream repositories

- `PocketMonsters-Scarlet-Decompilation`
- `PocketMonsters-Violet-Decompilation`
- `PokemonLegends-Z-A-Decompilation`

These game identities remain separate even when a visual source appears identical.

## Fixed baseline

This master inherits the preservation philosophy established by the Generation IV and Generation V `BATTLE_MASTER_V1` work:

- no generative-image tools
- no AI redraw, retouch, or upscaling
- no antialiasing introduced by the conversion pipeline
- no bilinear/bicubic RGB interpolation for indexed-source conversion
- no frequency-only automatic palette reduction as a final decision rule
- preserve source scale, composition, silhouette, identifying details, and representative colors
- preserve logical slots even when rendered results deduplicate to one canonical asset
- deterministic scripts wherever possible
- minimal manual pixel correction only when required to recover source identity lost by the target constraints
- every manual correction must be logged

## Generation IX source reality

Generation IX does not use the Generation III/IV/V model of a canonical indexed 2D Pokémon battle-sprite archive. Scarlet/Violet and LEGENDS Z-A are 3D titles.

Therefore this project must never invent a nonexistent official 2D battle sprite and label it as an original asset.

For Generation IX, the authoritative input is a **canonical visual source set**, selected per Pokémon logical role from the most original and verifiable available material.

## Source priority

Source selection is based on closeness to the actual game asset, not on whether a local ROM is available.

Priority order:

1. Directly decoded game model, texture, material, animation, scene, or related asset when legally and technically available to the project.
2. Verifiable public extraction or preservation data that retains original model/texture/resource structure and provenance.
3. Official game render, official model presentation, official website visual, or official distribution asset.
4. High-quality in-game capture that preserves the real game model, pose, lighting, markings, proportions, and coloration.
5. Verified preservation mirror or other public technical extraction with documented provenance.
6. Enlarged PNG, web preview, fan-site mirror, or screenshot only when nothing closer to the original can currently be obtained.

Lower-priority material may be used for cross-checking even when a higher-priority source exists.

A lower-priority source used as the working source must be marked `provisional` or `reconstructed` and must never be silently promoted to game-native status.

## Known Generation IX container baseline

Current public reverse-engineering evidence identifies Scarlet/Violet and LEGENDS Z-A resource access around `data.trpfs` / `data.trpfd`-style Trinity container infrastructure. Scarlet/Violet public tooling exposes Trinity file exploration and model-view/export workflows.

This is a research baseline, not a declaration that every model/texture member or every Z-A implementation detail is already resolved. Exact archive/member paths, hashes, resource types, materials, texture sets, animation sets, and version differences must be recorded when verified.

## Game separation

The following are separate source families:

### Scarlet
- base game
- every relevant update/revision
- The Teal Mask content
- The Indigo Disk content
- epilogue/additional content
- event/update-delivered visual changes where applicable

### Violet
- same categories as Scarlet, tracked independently
- version-exclusive Pokémon and visual context remain separately attributable

### LEGENDS Z-A
- base game
- updates
- additional content
- Mega Evolution and all Z-A-specific forms/visual states
- Z-A model/render implementation must not be treated as if it were Scarlet/Violet data

## Logical role key

Every source and target record must identify at minimum:

- generation
- game
- game version/update
- region/language when relevant to the visual asset
- National Pokédex number or verified internal species identifier
- form
- sex/gender presentation
- normal/shiny state
- side (`front` / `back`)
- source pose / animation state
- source type (`game_model`, `texture`, `official_render`, `capture`, `menu_sprite`, etc.)
- source status (`native`, `verified_extract`, `official`, `preservation`, `provisional`, `reconstructed`)

Logical roles are never deleted solely because their final pixels match another role.

## Canonical visual source selection

The canonical source is selected per logical role, not globally per species.

Selection must consider:

- body proportions
- silhouette
- head/face shape
- eye placement and color
- markings
- wings, tails, limbs, antennae, horns, crests, accessories, metallic parts, translucent parts, glow/emissive regions
- male/female visual differences
- form-specific geometry and textures
- shiny coloration
- relative scale and battle presentation
- front/back readability
- source pose and whether the pose is representative of actual battle presentation

Menu icons are valid evidence but are not automatically the canonical battle source.

## Generation III target contract

Every completed static battle sprite target must provide:

- 64×64 canvas
- indexed palette suitable for Generation III
- at most 16 palette entries including transparency where the target engine requires it
- Generation III BGR555 palette representation
- 4bpp graphics data
- Generation III-compatible compressed graphics data using the selected insertion pipeline (normally GBA BIOS LZ77 type `0x10` unless the target integration explicitly documents another native path)
- human-viewable PNG rendered from the exact final indexed result

The PNG is a review artifact; the indexed/binary representation is the insertion master.

## True-color / 3D → indexed conversion rule

Generation IX sources are commonly true-color textures and 3D geometry, so Generation IV/V source-index-only voting cannot be applied mechanically.

For each logical role:

1. Preserve the official model/design silhouette and proportions.
2. Establish a representative front/back battle composition from verifiable game presentation.
3. Identify semantically important color roles before palette reduction.
4. Preserve species-identifying rare colors even when they occupy few pixels.
5. Build the smallest Generation III-compatible palette that preserves visual identity; do not select colors solely by pixel frequency.
6. Do not create antialiased fringe colors.
7. Use hard pixel clusters and deliberate index assignment suitable for the Generation III visual language.
8. Compare the result against the canonical visual source at native review scale and nearest-neighbor enlarged scale.
9. Reject technically valid output that no longer reads clearly as the same Pokémon/form.

## Prohibited shortcuts

The following are not acceptable final-master methods:

- resizing a Scarlet/Violet 256×256 menu icon to 64×64 and calling it the battle master
- resizing a Z-A 160×160 menu icon to 64×64 and calling it the battle master
- automatic `top 15 colors` / median-cut / k-means output accepted without semantic review
- AI-generated sprite reconstruction
- AI cleanup or detail invention
- opaque-bounding-box normalization that destroys source-relative scale without an explicitly justified target rule
- silently merging forms, sexes, shiny states, games, versions, or source roles

## Required deliverables

No logical sprite role is complete until all applicable deliverables exist:

- source image/render or reproducible source reconstruction
- source provenance record
- source archive/member or public-source location
- source/native dimensions when known
- source model/texture/material/animation identifiers when known
- source SHA-256 where bytes are available
- intermediate working-source SHA-256
- automatic 64×64 result
- final corrected 64×64 PNG
- final rendered-pixel SHA-256
- final palette data and SHA-256
- final 4bpp data and SHA-256
- final compressed graphics data and SHA-256
- source → target manifest
- logical role → canonical asset mapping
- global dedup relation
- conversion script and settings
- manual-correction record when applicable
- visual comparison/review material
- validation output
- reproducibility metadata

PNG-only output is not complete.

## Deduplication

Final assets are deduplicated by exact rendered-pixel identity and, where relevant, exact binary identity.

A canonical asset may be referenced by multiple games, versions, forms, sexes, sides, or source roles only after equality is verified.

Deduplication removes duplicate storage, not logical provenance.

## Repository routing

### Sakurai
Stores research/control material:

- source census
- source mapping
- archive/resource analysis
- canonical-source decisions
- conversion scripts
- manifests
- SHA-256 inventories
- dedup tables
- validation
- comparison/review material
- provenance and uncertainty records

### Tsubaki
Stores eligible production/archive material once generated:

- final 64×64 PNGs
- final indexed palettes
- 4bpp graphics
- compressed graphics
- canonical battle-sprite assets
- insertion-ready packages
- required non-ROM intermediates needed for exact rebuild/review

No complete playable ROM image is committed.

## Acceptance checks

A logical role is not accepted into `BATTLE_MASTER_V1` unless all applicable checks pass:

- canonical source provenance recorded
- source status and confidence recorded
- game/version/form/sex/shiny/side identity recorded
- source design and silhouette preserved
- representative colors and rare identifying details preserved
- 64×64 target confirmed
- palette-limit compliance confirmed
- no prohibited antialias/interpolation residue
- 4bpp output verified
- BGR555 palette verified
- compressed binary round-trip verified
- final PNG rendered from the exact indexed target
- every required SHA-256 present
- dedup mapping retains every logical role
- visual comparison reviewed
- manual edits, if any, fully logged
- zero missing manifest references

## Current phase

### Phase 0 — contract and source-family definition

Status: **fixed**.

### Phase 1 — exhaustive public-source census

Status: **in progress**.

The first census must enumerate, separately for Scarlet, Violet, and LEGENDS Z-A:

- public model/resource tools
- model/texture extraction or viewing evidence
- resource-container documentation
- official renders and official game visual references
- menu/Pokédex/UI images useful only as secondary evidence
- normal/shiny coverage
- sex differences
- alternate forms
- battle poses/animations
- update/DLC differences
- source licensing/redistribution constraints
- provenance quality and verification state

No species sprite conversion is promoted to final-master status before its canonical source decision is recorded.
