# Generation VII -> Generation III battle sprite fixed contract

Status: **fixed**

This contract governs the Generation VII `BATTLE_MASTER_V1` work. It inherits the verified Generation IV/Generation V preservation lineage and extends it to Generation VII's 3D-source games.

## Objective

Investigate the closest verifiable official/original graphical source available for every Generation VII Pokémon battle visual, preserve its form, color, placement, gender/form distinctions, animation information and provenance as completely as practical, and reconstruct a Generation III-compatible 64x64 battle-sprite asset package.

The target is not merely a 64x64 PNG. The target is a reproducible chain from source provenance through the final Generation III insertable binary assets.

## Source selection

1. Prefer direct decoded game data when legitimately available to the project.
2. ROM possession is not a prerequisite. If direct game data is unavailable, continue with the closest verifiable source: preserved extractions, official model/texture material, official in-game renders, official captures, official web/distribution material, and well-documented preservation projects.
3. Do not silently treat web previews, resized PNGs or screenshots as equivalent to the game's native data.
4. Compare dimensions, pixel structure, alpha, palette/texture behavior, metadata and hashes whenever multiple copies exist.
5. Record uncertainty explicitly. Unknown values remain `TBD`/`unknown`; they are not guessed.

## Native structure first

Before conversion, document each game's actual native structure: model or sprite format, canvas/render target, front/back behavior, normal/shiny source, gender differences, forms, textures, materials, transparency, animation groups, archive/member mapping, logical slots, and load/render relationships.

Do not assume all Generation VII games share one graphics system. Sun/Moon, Ultra Sun/Ultra Moon and Let's Go Pikachu/Eevee are separate source families until equivalence is proven.

## Indexed-source preservation lineage

When a source is genuinely indexed, preserve the original palette/index structure wherever possible.

Generation IV/V `preservation-v2` rules remain fixed for such sources:

- full source canvas -> full 64x64 target canvas;
- no opaque-bounding-box normalization;
- no generative-image tools;
- no antialiasing;
- no RGB interpolation;
- no bilinear/bicubic resampling;
- no invented intermediate colors;
- target pixels select existing source indices/colors;
- exact source-pixel area-overlap voting;
- mild rare-color preservation for visually identifying details;
- silhouette protection: if at least half of a target pixel's mapped source footprint is opaque, transparency cannot win solely by area voting;
- normal/shiny and every logical role remain represented;
- rendered duplicates are globally deduplicated only after cryptographic identity is verified.

## True-color / 3D-source rule

Generation VII 3DS/Switch Pokémon battle visuals are not to be falsely described as native Generation III-style 2D indexed battle sprites.

For a true-color/3D source:

1. Establish the canonical model, texture/material set, battle animation/pose and battle-view orientation first.
2. Preserve the Pokémon's visual identity: silhouette, face/eyes, body colors, markings, appendages, wings, tail, emissive/metallic/transparent features and other identifying details.
3. Do not reduce color by automatic frequency ranking alone.
4. Do not create a new design. Any manual pixel correction is limited to restoring source information lost by the Generation III constraints.
5. Do not use AI redraw, AI retouch, AI upscaling or generative-image tools.
6. Record the automatic result separately from any manually corrected result and document every manual correction.
7. A technically valid 64x64/4bpp result fails acceptance if it no longer reads unmistakably as the source Pokémon.

## Generation III target

Every accepted final battle asset must provide all required deliverables:

- human-viewable final 64x64 PNG;
- preserved/reconstructed source PNG or source render used for review;
- source palette data where applicable;
- Generation III palette data;
- Generation III 4bpp graphics data;
- Generation III-compressed graphics data;
- source-to-target manifest;
- provenance record;
- source archive/member or source-asset location;
- source SHA-256;
- intermediate SHA-256 values;
- final PNG SHA-256;
- final rendered-pixel SHA-256;
- final palette SHA-256;
- final 4bpp SHA-256;
- final compressed-binary SHA-256;
- source -> target mapping;
- logical slot -> canonical asset mapping;
- deduplication mapping;
- deterministic scripts and settings;
- automatic conversion result;
- manual-correction result/history when applicable;
- visual comparison material;
- validation/error records;
- all metadata necessary to rebuild the result.

PNG alone is not completion. Palette alone is not completion. Missing 4bpp, compression, manifests, hashes or validation is not completion.

## Deduplication

Deduplicate only when the final rendered result is cryptographically identical. Keep one canonical binary asset, but retain every game/version/region/revision/form/gender/shiny/frame/logical-slot relationship in the manifest.

Never erase logical relationships merely because the stored pixels are shared.

## Provenance fields

At minimum record:

- generation;
- game;
- version;
- region;
- language;
- revision;
- source kind;
- source archive/member or external asset identifier;
- native model/canvas/texture dimensions as applicable;
- palette/texture format;
- transparent index/alpha behavior where applicable;
- frame/pose;
- gender;
- normal/shiny state;
- form;
- conversion method;
- manual-edit state;
- source and final hashes;
- verification state.

## Visual validation

Every final conversion requires side-by-side source/final inspection. Check silhouette, head/face/eyes, wings, tail, limbs, markings, identifying colors, value contrast, highlights, ornaments and overall impression.

Automatic pipeline success is not visual acceptance.

## Repository boundary

- **Sakurai**: research, source mapping, archive/member analysis, scripts, manifests, validation, hashes, dedup tables, provenance, comparison evidence and verification records.
- **Tsubaki**: actual source/reconstruction PNGs retained for production, final 64x64 PNGs, palettes, 4bpp, compressed binaries, canonical sprite assets and other insertable graphics.
- Complete playable ROM/cartridge/ISO images are excluded from GitHub.

## Batch discipline

Assets are committed in small reviewable batches. Do not dump an entire generation in one unreviewable commit. Identical assets are stored once after hash verification and referenced by all relevant logical slots.

## Fixed top-level rules

- Do not stop solely because a ROM is unavailable.
- Use the closest verifiable original/official/preservation source available.
- Preserve native indexed structure when it actually exists.
- For true-color/3D sources, prioritize species identity and source-faithful rendering under Generation III constraints.
- Never finalize a 16-color asset by naive frequency-only color reduction from a resized RGB image.
- Never use generative-image tools.
- Completion requires the entire reproducible asset package, not a preview PNG.
