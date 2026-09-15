# Generation V BW battle sprite master v1

## Status

**Active Generation III insertion master contract.**

This directory is the canonical Sakurai analysis location for the Generation V Black/White battle-sprite preservation and Generation III 64×64 insertion pipeline. Historical pre-migration copies under `INFRA/QUARANTINE/` are retained only as provenance snapshots and are not the active contract.

## Project-wide fixed contract

The goal is not merely to create a 64×64 PNG. The complete source-to-Generation-III process must remain reproducible, inspectable, and verifiable from the closest available official or preservation-grade source through the final insertable binary assets.

Source priority is evidence-based, not ROM-presence-based:

1. When accessible, directly decoded game/ROM graphics, palettes, indices, frames, animation data, archive/member structure, and loading relationships are the preferred source.
2. Lack of a ROM or direct extraction path is never by itself a reason to stop. Use the closest verifiable official or preservation-grade source available: official assets, verified extractions, archival projects, official renders/models/textures, in-game captures, official web assets, or official distribution material.
3. When the same asset exists from multiple sources, compare native resolution, pixel/index structure, palette, transparency, frames, metadata, and SHA-256 before selecting the canonical source.
4. Web previews, enlarged PNGs, mirrors, and screenshots may be used only with their limitations recorded. They are never automatically treated as byte-equivalent game assets.

## BW native source structure

For the current EUR Black/White source set, Pokémon battle graphics are sourced from `/a/0/0/4`.

Each standard Pokémon/form block uses 20 members:

### Front group (+0..+8)

- `+0` NCGR male/default static front
- `+1` NCGR female static front
- `+2` NCGR male/default animated parts
- `+3` NCGR female animated parts
- `+4` NCER
- `+5` NANR
- `+6` NMCR
- `+7` NMAR
- `+8` auxiliary/unresolved member; preserve and inventory, do not discard

### Back group (+9..+17)

- `+9` NCGR male/default static back
- `+10` NCGR female static back
- `+11` NCGR male/default animated parts
- `+12` NCGR female animated parts
- `+13` NCER
- `+14` NANR
- `+15` NMCR
- `+16` NMAR
- `+17` auxiliary/unresolved member; preserve and inventory, do not discard

### Palettes

- `+18` normal NCLR
- `+19` shiny NCLR

Dedicated static NCGR members are the authoritative source for the static Generation III insertion master. Animated multipart resources are preserved on a separate animation track and must not be frozen arbitrarily and substituted for the canonical static sprite.

Empty female slots are preserved as explicit logical slot states and may alias the canonical default sprite where the original loading behavior does so. Empty members are never silently dropped.

## Native canvas and target

For the static BW battle-sprite track, the normal source canvas is 96×96 indexed/4bpp graphics. The Generation III target is a 64×64 indexed/4bpp-compatible battle sprite.

The entire native source canvas is mapped to the entire target canvas. Never crop to each Pokémon's opaque bounding box and never normalize every species to a common occupied height/width. Relative scale, placement, and transparent margins from the source game must be preserved proportionally.

## preservation-v2 conversion

For indexed source graphics:

1. Decode the complete source canvas as palette indices.
2. Preserve palette indices through geometric conversion; do not convert to RGB and then guess a new palette.
3. Map the entire source canvas to the complete 64×64 target canvas.
4. For each target pixel, calculate the exact geometric overlap with source pixels.
5. Select one of the overlapping source palette indices by weighted overlap voting.
6. Apply mild rare-color/index preservation so thin but identifying details such as eyes, markings, highlights, and ornaments are not disproportionately erased.
7. Apply silhouette protection: when at least 50% of a target pixel's mapped source footprint is opaque, transparency may not win that target pixel.
8. Never create an RGB average, interpolated color, new palette index, or antialiased edge.
9. Render normal and shiny variants from the source normal/shiny palettes after index selection.
10. Perform visual review against the source before acceptance.

Forbidden processing includes generative-image tools, AI redraw/retouch/upscaling, bilinear/bicubic interpolation, antialiasing, RGB averaging, intermediate-color creation, and automatic frequency-only palette reduction.

## Color and identity preservation

A technical 16-color pass is not sufficient for acceptance. Rare colors may be visually essential. Eyes, stripes, symbols, metallic decorations, small highlights, and species-defining accent colors must not be removed merely because they occupy few pixels.

The final 64×64 result must still read immediately as the same Pokémon while meeting Generation III constraints.

If deterministic conversion damages a defining feature, minimal manual pixel correction is allowed only to restore source information lost during conversion. It must not redesign the sprite. The automatic result, corrected result, changed coordinates, and reason for every manual correction must be retained separately in the manifest/validation history.

## Animation preservation track

BW multipart animation is preserved independently from the static insertion master:

1. decode animated NCGR parts plus NCER/NANR/NMCR/NMAR;
2. retain source palette/index relationships;
3. reconstruct the animation on a safe canvas;
4. follow the actual NMAR timeline and source anchors;
5. preserve played union envelopes and conservative data unions;
6. if a target engine later supports the animation set, down-convert all frames with one common scale/anchor and the same source-index-only rules.

Animation resources are never discarded just because Generation III's baseline battle sprite is static.

## Required outputs — no optional items

A sprite task is incomplete unless all applicable outputs are generated and preserved:

- inspectable final PNG
- original source PNG or faithful source reconstruction image
- original/source palette data
- Generation III palette data
- Generation III 4bpp graphics data
- Generation III compressed graphics data
- source-to-target manifest
- source provenance record
- source archive/member or original-asset location mapping
- source SHA-256
- intermediate SHA-256
- final PNG SHA-256
- final rendered-pixel SHA-256
- final palette SHA-256
- final 4bpp SHA-256
- final compressed-binary SHA-256
- source → target correspondence table
- logical slot → canonical asset table
- duplicate/canonical SHA-256 dedup table
- conversion scripts and exact configuration values
- automatic conversion result
- manual correction result and correction history, when used
- source/final visual comparison material
- validation results and error records
- all metadata required to rebuild and reproduce the package

A PNG-only package is not complete. A palette-only package is not complete. Missing 4bpp, compressed data, manifest, hash records, validation, or provenance is a failed/incomplete build.

## Deduplication

Deduplicate globally using SHA-256 of the final rendered pixel result. Different games, versions, regions, revisions, genders, forms, frames, or palette slots may point to one canonical asset when the rendered result is identical.

Deduplication must never erase logical relationships. Every logical game/version/form/frame/gender/palette role continues to exist in the manifest and resolves to its canonical asset.

## Provenance requirements

Every logical asset records at minimum:

- generation
- game
- version
- region
- language
- revision or explicit unresolved revision state
- source type
- archive/member or source-asset identifier
- native canvas size
- palette structure
- transparent index
- frame
- gender/logical gender slot
- normal/shiny state
- form
- conversion method/version
- manual-edit status
- source SHA-256
- intermediate/final hashes
- canonical dedup target

Unknown information must remain explicitly `unknown`/`unresolved`; never invent a value to make the table look complete.

## Repository split

### Sakurai

Store analysis and reproducibility material here:

- source/archive/member analysis
- source mappings
- extraction/conversion scripts
- conversion configuration
- manifests
- provenance
- SHA-256 inventories
- dedup tables
- validation
- visual comparison/review records
- reconstruction/rebuild documentation

### Tsubaki

Store actual Generation III insertable graphical assets:

- canonical 64×64 final PNGs
- Generation III palettes
- Generation III 4bpp graphics
- Generation III compressed graphics binaries
- canonical sprite assets and insertion-ready graphics

Original ROM/cartridge/ISO binaries are excluded from GitHub. Project-generated, reconstructed, extracted, converted, and validated non-ROM work products are preserved.

## Current BW source identity rule

Black and White remain distinct game identities in provenance and logical-slot manifests even when a sprite archive proves byte-identical. Deduplication may share canonical assets, but it never merges the game identities themselves.

`REV-UNKNOWN` in this path is historical naming and must not be used as evidence that the actual cartridge revision is unknown. Revision, region, language set, game code, archive hashes, and ROM hash provenance are established from the source evidence and recorded in manifests. If the active path is later migrated to a confirmed revision-specific path, this directory must leave a redirect/provenance note rather than silently disappearing.

## Acceptance checks

`BATTLE_MASTER_V1` is accepted only when all of the following pass:

- closest-source provenance is recorded
- ROM/direct game data is used when available, without making ROM access a universal prerequisite
- dedicated static BW NCGR members are used for the static master
- complete source canvas → complete 64×64 target mapping is used
- palette-index-only conversion is used for indexed source
- no antialiasing, interpolation, generated/new colors, or generative imagery is used
- rare identifying colors/details and silhouette survive visual inspection
- front/back and normal/shiny coverage is reconciled
- male/female slot/alias/empty state is recorded
- all forms and special/tail members are inventoried rather than ignored
- animation resources remain preserved on their separate track
- all required PNG/palette/4bpp/compressed/manifest/hash/provenance/validation outputs exist
- every logical role resolves to a valid canonical asset
- dedup mapping has zero lost logical references
- rebuild/reproduction metadata is sufficient to recreate the same binaries and hashes

## Historical sources

Earlier versions of this contract are retained under `INFRA/QUARANTINE/PRE-V8/...` as migration evidence. They remain useful for auditing project history but do not override this active contract.
