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

## Authoritative source for the 64×64 static master

BW stores **dedicated static battle NCGRs separately from the multipart animated parts**. Within each 20-member Pokémon/form block:

### Front group (+0..+8)
- `+0` NCGR male static front
- `+1` NCGR female static front
- `+2` NCGR male animated parts
- `+3` NCGR female animated parts
- `+4` NCER
- `+5` NANR
- `+6` NMCR
- `+7` NMAR
- `+8` unresolved/auxiliary member

### Back group (+9..+17)
- `+9` NCGR male static back
- `+10` NCGR female static back
- `+11` NCGR male animated parts
- `+12` NCGR female animated parts
- `+13` NCER
- `+14` NANR
- `+15` NMCR
- `+16` NMAR
- `+17` unresolved/auxiliary member

### Palettes
- `+18` normal NCLR
- `+19` shiny NCLR

Therefore the **static 64×64 insertion master uses the ROM's dedicated static NCGR slots (+0/+1/+9/+10) as its authoritative source**. We do not freeze an arbitrary animated tick and call it the static master.

Female static/parts slots that are empty because the species has no visual sexual dimorphism are recorded explicitly and represented as logical aliases to the canonical static source where appropriate; empty ROM slots are never silently discarded.

## Static preservation-v2 conversion

The Generation IV master used fixed 80×80 → 64×64 weighted index selection. BW static battle sprites are nominally 96×96, so the same selection rule is generalized to the actual decoded static source dimensions:

1. Decode the dedicated static NCGR directly from the project BW ROM `/a/0/0/4` archive.
2. Keep the source as palette **indices**, not interpolated RGB.
3. Fit the complete opaque source extent into a 62×62 safe inner area on a 64×64 target, preserving aspect ratio and a 1-pixel safety margin.
4. For every target pixel, calculate exact source-pixel area overlap.
5. Select one of the overlapping source palette indices using weighted overlap voting.
6. Apply the same mild rare-index preference used by the Generation IV preservation-v2 strategy.
7. If at least half of a target pixel's mapped source footprint is opaque, transparency cannot win that target pixel; this is the generalized form of the Generation IV `0.78125 / 1.5625 = 50%` silhouette rule.
8. Never average RGB and never invent a palette index or color.
9. Render normal and shiny from the original `+18` / `+19` BW palettes after index selection.
10. Deduplicate identical 64×64 RGBA results globally by SHA-256 while retaining every logical role in the manifest.

Implementation kernel: `preservation_v2_generalized.py`.

## Separate animation-preservation track

The multipart animation data remains fully preserved, but it is **not** the source for the static insertion master. Animated sprites are handled as a parallel track:

1. decode `male/female parts + NCER + NANR + NMCR + NMAR` from the ROM;
2. reconstruct the complete animation on a safe canvas;
3. follow the actual NMAR timeline;
4. retain the common battle anchor;
5. compute exact played union envelopes and conservative data unions;
6. when/if a target engine supports Gen V-style animation, down-convert all animation frames with one common scale/anchor per animation set using the same source-index-only preservation rule.

This separation fixes the earlier prototype mistake where an animated frame was cropped/frozen and treated as if it were the canonical static sprite.

## Scope

The master covers the complete BW battle-sprite archive, not only National Dex 001–649:

- all standard 20-member Pokémon/form blocks identified in `/a/0/0/4`
- front / back
- logical male / female slots, including aliases and empty slots recorded explicitly
- normal / shiny palettes
- all alternate forms represented in the archive
- tail/special battle-sprite data and additional palettes inventoried separately rather than ignored
- animation parts/timelines preserved in the separate animation track

Black and White remain separate game identities in the manifest even when the underlying `/a/0/0/4` archive is byte-identical.

## Repository split

- **Sakurai**: analysis, source mappings, manifests, validation, extraction/conversion scripts, dedup tables, archive hashes.
- **Tsubaki**: rendered/insertable 64×64 assets and atlases.

## Acceptance checks

A result is not called `BATTLE_MASTER_V1` unless all of the following pass:

- ROM-primary provenance recorded
- dedicated static NCGR used for the static 64×64 master
- source-index-only color selection
- no antialiasing/interpolation/new colors
- front/back and normal/shiny coverage verified
- male/female slot/alias state recorded
- form/special-slot inventory reconciled against the ROM archive
- SHA-256 dedup mapping preserves every logical role
- generated asset count and manifest references cross-check with zero missing files
- animation data remains preserved separately rather than being discarded or conflated with the static master
