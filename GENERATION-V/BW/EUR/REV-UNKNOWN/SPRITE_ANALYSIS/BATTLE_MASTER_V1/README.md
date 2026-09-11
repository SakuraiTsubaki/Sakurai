# Generation V battle sprite master v1

## Status

**Conversion contract fixed. ROM-primary 64×64 master rebuild required.**

The existing Tsubaki directory `64x64_PREVIEW_EXTERNAL` is an external visual preview only and is explicitly **not** this master.

## Baseline contract

This master inherits the Generation IV `BATTLE_MASTER_V1` preservation-v2 rules:

- no generative-image tools
- no antialiasing
- no RGB interpolation
- no interpolated/new colors
- every output pixel selects an index/color that already exists in the source ROM palette
- weighted source-pixel overlap selection rather than naive image resampling
- mild rare-color preservation so thin/rare identifying details are less likely to disappear
- identical rendered results are merged globally by SHA-256 rather than duplicated

## Generation V adaptation

Generation V cannot use the Generation IV fixed `80×80 -> 64×64` geometry verbatim. BW battle sprites are multipart animated compositions driven by NCGR + NCER + NANR + NMCR + NMAR, and their legal rendered envelope can exceed 96 pixels.

Therefore the preservation-v2 **selection rule** is retained, while the geometry stage is generalized:

1. Decode the sprite parts directly from the project BW ROM `/a/0/0/4` archive.
2. Reconstruct the complete front/back composition on a safe canvas; never use a fixed 96×96 source crop.
3. Follow the NMAR timeline and retain the common battle anchor.
4. Compute one union envelope for each logical animation set.
5. Choose one uniform source-to-target scale from that union envelope so every frame in that animation uses the same scale and anchor.
6. For every target pixel, evaluate overlap against source **palette-index pixels** and select one of those source indices using preservation-v2 weighted voting plus the same mild rare-color preference.
7. Do not average RGB values and do not invent colors.
8. Render normal and shiny from their respective original BW palettes after index selection.
9. Deduplicate identical 64×64 rendered results by SHA-256 while keeping every logical role in the manifest.

## Scope

The master is intended to cover the complete BW battle-sprite archive, not only National Dex 001–649:

- all standard 20-member sprite/form blocks identified in `/a/0/0/4`
- front / back
- logical male / female data where present, including aliases/empty source slots recorded rather than silently discarded
- normal / shiny palettes
- all official alternate forms represented in the archive
- all actually referenced animation states/ticks from NMAR
- tail/special battle-sprite data and additional palettes inventoried separately rather than ignored

Black and White remain separate game identities in the manifest even when the underlying `/a/0/0/4` archive is byte-identical.

## Repository split

- **Sakurai**: analysis, source mappings, manifests, validation, extraction/conversion scripts, dedup tables, archive hashes.
- **Tsubaki**: rendered/insertable 64×64 assets and atlases.

## Acceptance checks

A result is not called `BATTLE_MASTER_V1` unless all of the following pass:

- ROM-primary provenance recorded
- no fixed-96 source clipping
- source-index-only color selection
- no antialiasing/interpolation/new colors
- common animation scale/anchor preserved per animation set
- front/back and normal/shiny coverage verified
- form/special-slot inventory reconciled against the ROM archive
- SHA-256 dedup mapping preserves every logical role
- generated asset count and manifest references cross-check with zero missing files
