# Generation X battle sprite master v1

## Status

**Pre-release source census / canonical-source selection in progress. No Generation III insertion master is approved yet.**

This master covers Pokémon Winds / Pokémon Waves and follows the shared Generation III battle-sprite preservation contract established by the Generation IV `BATTLE_MASTER_V1` preservation-v2 work and the Generation V BW static-master rules.

The goal is not merely to make a 64×64 PNG. The goal is a provenance-complete, reproducible source → Generation III asset pipeline with human-viewable PNG, palette, 4bpp graphics, compressed graphics, manifests, hashes, deduplication, validation, and comparison evidence.

## Upstream identities

- `PocketMonsters-Winds-Decompilation`
- `PocketMonsters-Waves-Decompilation`

Winds and Waves remain separate logical game identities even when a public source asset is byte-identical between them.

## Highest-level source rule

ROM ownership is not a prerequisite for continuing the work.

Source priority is:

1. directly extracted game-internal model / texture / sprite / palette / archive data when available and verifiable;
2. official downloadable source assets that preserve original pixels or model/render information;
3. official in-game footage / captures and official transparent artwork;
4. verified preservation-project extracts;
5. official web images or other recoverable official distribution assets;
6. mirrors / previews / screenshots only when nothing closer to the source exists.

A lower-priority source is never silently described as game-internal original data. Source class, limitations, transformations, and confidence must be recorded in the manifest.

## Current pre-release finding — 2026-09-15

No official Generation X 2D indexed battle-sprite format has been publicly established from the material currently available to this project.

The currently preserved Japanese official Pokémon PNG batch consists of:

- `image_101.png` — ハブロウ
- `image_102.png` — ポムケン
- `image_103.png` — ミオリー
- `image_104.png` — ピカチュウ（カゼピカくん） / ピカチュウ（ナミピカちゃん） combined official image

The same four Git blobs are present in both Winds and Waves upstream repositories, so they are shared public-source candidates rather than version-exclusive source images.

For `image_101.png` through `image_103.png`, the preserved PNG headers confirm a 960×960, 8-bit-per-channel RGBA PNG canvas. `image_104.png` is confirmed as a PNG in the upstream repository but its complete header/pixel inspection remains pending in this master and must not be guessed.

These files are **official public Pokémon artwork**, not proven game-internal battle sprites. They are therefore recorded as pre-release canonical-visual-source candidates, not native battle-sprite originals.

The official 1st Trailer (2026-02-27) is an additional official pre-release game-footage cross-check. Its footage is explicitly development footage, so final-game geometry, materials, poses, lighting, and scale remain provisional until later official builds or game data can be inspected.

## Generation III target contract

Every approved static battle asset must ultimately provide:

- 64×64 target canvas;
- transparent background with target palette index 0 reserved for transparency;
- no more than 16 palette entries including transparency;
- GBA-compatible BGR555 palette representation;
- GBA OBJ-style 4bpp tiled graphics (2048 bytes uncompressed for a complete 64×64 frame);
- Generation III-compatible compressed graphics, using the project-supported GBA LZ77 path where applicable;
- front/back logical roles when a valid source or reconstruction basis exists;
- normal/shiny roles when official color-state evidence exists;
- gender/form/frame roles preserved independently rather than collapsed;
- deterministic source-to-target mapping and full validation.

PNG-only output is never complete.

## Indexed-source rule

If later Generation X game data exposes indexed 2D battle sprites, the native palette/index structure takes priority over RGB reconstructions.

For indexed sources:

- preserve the complete native source canvas rather than cropping the opaque Pokémon bounding box;
- map complete source canvas → complete 64×64 target canvas;
- calculate exact source-pixel area overlap for each target pixel;
- choose only among palette indices already present in the source;
- do not RGB-average, interpolate, antialias, or invent new colors;
- apply mild rare-index preservation for eyes, markings, outlines, highlights, ornaments and other identity-critical details;
- apply silhouette protection so transparency cannot erase a target pixel when at least half of its mapped source footprint is opaque;
- retain every logical role in manifests even when rendered assets deduplicate by SHA-256.

## True-color / 3D-source rule

If Generation X has no native 2D indexed battle sprite, do not invent a nonexistent native sprite and call it original.

Instead:

1. identify the best verifiable official canonical visual source for the Pokémon;
2. document whether it is model/texture data, in-game rendering, official transparent artwork, official capture, or another source class;
3. analyze silhouette, body-color regions, dark regions, highlights, eyes, markings, ornaments, metallic/emissive areas, wings, tail and other species-defining features;
4. construct the Generation III palette deliberately around visual identity rather than selecting the 15 most frequent RGB colors;
5. preserve source-relative scale and placement as far as the available evidence permits;
6. mark any reconstruction as reconstructed/provisional until stronger source evidence supersedes it.

Generative-image tools, AI redraw/retouch/upscale, bilinear/bicubic interpolation, antialiasing, arbitrary RGB averaging, and automatic frequency-only palette reduction are prohibited.

## Web/enlarged-image rule

Official web PNGs may be used, but filtered/enlarged/true-color web images are not assumed to preserve an original indexed palette.

Intermediate RGB colors introduced by filtering or compositing must not be mistaken for native palette colors. If a better source cannot be found, the asset remains explicitly `reconstructed/provisional` and the limitations are recorded.

## Visual acceptance

Automated conversion success is not approval.

Every asset must be visually compared against its strongest source evidence for:

- silhouette;
- head/face/eyes;
- limbs/wings/tail;
- markings and ornaments;
- representative colors;
- light/dark contrast;
- overall recognizable impression;
- source-relative scale and placement.

A technically valid 64×64/4bpp asset that no longer reads as the same Pokémon fails validation.

Minimal manual pixel correction is allowed only to restore source information lost by Generation III constraints. Automatic output and corrected output must be preserved separately, and every manual change must be documented.

## Required outputs

For every final logical asset, preserve all applicable items below:

- original/source PNG or source reconstruction;
- source palette/index data when available;
- Generation III final PNG;
- Generation III palette data;
- Generation III 4bpp data;
- compressed graphics data;
- source-to-target manifest;
- provenance and source location/archive/member data;
- source SHA-256;
- intermediate SHA-256;
- final PNG SHA-256;
- final rendered-pixel SHA-256;
- final palette SHA-256;
- final 4bpp SHA-256;
- final compressed-binary SHA-256;
- logical-slot → canonical-asset mapping;
- dedup relationships;
- deterministic scripts/configuration;
- automatic result;
- manual-correction result/history when used;
- source/final visual comparison;
- validation report and errors.

## Deduplication

Rendered identity is deduplicated globally by final rendered-pixel SHA-256. A single canonical binary/image asset may serve multiple games, forms, genders, frames, palettes or logical slots only when the rendered result is actually identical.

Logical provenance is never discarded when physical files are deduplicated.

## Repository roles

- **Sakurai** — source census, source ranking, mappings, archive/member research, conversion scripts, manifests, provenance, hash tables, dedup tables, validation, comparisons, reports.
- **Tsubaki** — eligible non-ROM source/production assets and the actual Generation III-use final PNG/palette/4bpp/compressed/canonical graphics package.
- Complete playable ROM images are never committed.

## Initial acceptance gate for Generation X

Before the first Generation X Pokémon can be marked complete:

- [ ] native Generation X sprite/model/texture situation investigated and source class recorded;
- [ ] strongest available official/preservation source selected with confidence status;
- [ ] source dimensions, alpha/index/palette properties and hashes recorded;
- [ ] source-relative scale/placement evidence reviewed;
- [ ] 64×64 target generated without prohibited resampling or invented detail;
- [ ] <=16-entry target palette including transparency validated;
- [ ] 4bpp binary generated and decoded back losslessly to the intended indexed target;
- [ ] compressed binary generated and decompressed back losslessly;
- [ ] PNG/palette/4bpp/compressed SHA-256 values recorded;
- [ ] visual comparison approved;
- [ ] logical-slot/canonical-asset mapping written;
- [ ] Tsubaki insertable asset package present.

Until all applicable checks pass, the asset is not complete.
