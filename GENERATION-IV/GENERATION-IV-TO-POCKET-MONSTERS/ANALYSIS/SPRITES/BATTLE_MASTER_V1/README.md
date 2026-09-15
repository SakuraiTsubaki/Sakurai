# Generation IV battle sprite master v1

## Status

**Active Generation III insertion master contract.**

This directory is the canonical Sakurai analysis location for the Generation IV battle-sprite preservation and Generation III 64×64 insertion pipeline. Historical pre-migration copies under `INFRA/QUARANTINE/` remain provenance snapshots only and do not override this active contract.

## Scope

Generation IV coverage includes Diamond/Pearl, Platinum, and HeartGold/SoulSilver battle-sprite sources, with each game/version identity retained separately even where source archives or rendered results are byte-identical.

The inventory must include:

- complete main species-slot ranges used by each title
- front / back
- logical male / female slots, including shared-slot aliases and explicit empty slots
- animation frames and frame relationships used by the original game
- normal / shiny palettes
- alternate forms addressed by game loading logic
- `otherpoke`/special/auxiliary members, including unreferenced or leftover candidates
- source archive/member relationships and loading mappings

## Project-wide fixed contract

The goal is not merely to create a 64×64 PNG. The complete source-to-Generation-III process must remain reproducible, inspectable, and verifiable from the closest available official or preservation-grade source through final insertion-ready binary assets.

Source priority is evidence-based rather than ROM-presence-based:

1. When accessible, directly decoded game/ROM graphics, palettes, indices, frames, animations, archive/member structures, and loading relationships are preferred.
2. Lack of a ROM or direct extraction path never by itself stops the work. Use the closest verifiable official or preservation-grade source available.
3. If several candidate sources exist, compare native resolution, pixel/index structure, palette, transparency, frame structure, metadata, and SHA-256 before selecting the canonical source.
4. Enlarged PNGs, web previews, mirrors, or screenshots may be used only with limitations and reconstruction status recorded; they are not automatically equivalent to game-native indexed data.

## Generation IV indexed-source rule

Generation IV battle sprites are indexed graphics and therefore must preserve source palette/index structure through conversion whenever possible.

The canonical Generation III insertion transform follows the `preservation-v2` rule:

1. Decode the complete source canvas as palette indices.
2. Preserve the complete native canvas rather than cropping to the Pokémon's opaque bounding box.
3. Map the full source canvas directly to the full 64×64 target canvas.
4. For every target pixel, compute exact geometric overlap with source pixels.
5. Select one of the actually overlapping source palette indices using weighted overlap voting.
6. Apply mild rare-index preservation so thin but species-defining details survive reduction.
7. Apply silhouette protection: when at least 50% of a target pixel's mapped source footprint is opaque, transparency may not win that target pixel.
8. Never average RGB values and never invent a color or palette index.
9. Preserve normal/shiny palette relationships from the source.
10. Visually review source and final side by side before acceptance.

For the common Generation IV 80×80 source battle canvas, this is a full-canvas 80×80 → 64×64 transform. Per-species opaque-bbox fitting, artificial enlargement, and normalized occupied-height scaling are prohibited.

## Forbidden processing

Do not use:

- generative-image tools
- AI redraw, AI retouch, or AI upscaling
- antialiasing
- bilinear or bicubic interpolation
- RGB averaging
- intermediate/new-color generation
- automatic frequency-only palette reduction

A rare palette color may carry an eye, marking, metallic ornament, highlight, or another defining detail. Technical compliance with a 16-color limit is not sufficient if species identity is damaged.

## Automatic processing and manual correction

Prefer deterministic, reproducible scripts.

If deterministic conversion clearly destroys a defining eye, marking, silhouette edge, or other source detail, minimal manual pixel correction is allowed only to restore information lost because of the Generation III constraints. It must not redesign or modernize the sprite.

When manual correction occurs, retain separately:

- automatic output
- corrected output
- changed coordinates/pixels
- reason for each correction
- validator result before and after correction

## Required outputs — no optional items

A battle-sprite task is incomplete unless all applicable outputs exist and are preserved:

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
- conversion scripts and exact settings/configuration
- automatic conversion result
- manual correction result/history when used
- source/final visual comparison material
- validation results and error records
- all metadata needed to rebuild and reproduce the package

PNG-only or palette-only output is not completion. Missing 4bpp, compressed data, manifest, hashes, provenance, or validation leaves the build incomplete.

## Deduplication

Use SHA-256 of the final rendered pixel result as the global visual deduplication key.

When two logical roles render identically, preserve one canonical asset but retain every game/version/form/frame/gender/palette logical reference in the manifest. Deduplication removes redundant file bytes, never logical relationships.

## Provenance requirements

Every logical asset must record at least:

- generation
- game/title
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

Unconfirmed data must remain explicitly unknown/unresolved rather than being guessed.

## Repository split

### Sakurai

Store analysis and reproducibility material:

- source/archive/member analysis
- loading/source mappings
- extraction/conversion scripts
- configuration
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

## Acceptance checks

`BATTLE_MASTER_V1` is accepted only when all of the following pass:

- closest-source provenance is recorded
- direct game data is used when available without making ROM access a universal prerequisite
- native indexed palette/index structure is preserved through conversion
- complete source canvas → complete 64×64 target mapping is used
- no antialiasing, interpolation, generated/new colors, or generative imagery is used
- rare identifying colors/details and silhouette survive visual inspection
- front/back, normal/shiny, gender/alias, frames, and forms are reconciled to source logic
- all special/auxiliary/`otherpoke` members are inventoried rather than silently discarded
- all required PNG/palette/4bpp/compressed/manifest/hash/provenance/validation outputs exist
- every logical role resolves to a valid canonical asset
- dedup mapping loses zero logical references
- rebuild/reproduction metadata can recreate the same output binaries and hashes

## Historical result snapshot

Earlier project passes recorded 25,136 logical rendered records, 11,947 unique 64×64 RGBA assets after global SHA-256 deduplication, 24 atlas pages, and 727 inventoried `otherpoke` members. Those figures are historical evidence and must be revalidated against the active source inventory before being treated as final current counts.

## Historical sources

Earlier versions are retained under `INFRA/QUARANTINE/PRE-V8/...` for auditability. They remain useful for project history but do not override this active contract.
