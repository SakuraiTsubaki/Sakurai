# Batch 001 / #001 BULBASAUR — Generation III adaptation v2 candidate

This candidate replaces the rejected fixed 80x80->64x64 full-canvas reduction as the working final-adaptation model.

## Core correction

`64x64` is a target canvas, not a scale factor.

- Decode and retain original Gen IV palette indices.
- Compute a common opaque union envelope for the related side/animation set.
- If that union fits 64x64, keep source sprite pixels at **1:1** and translate/crop only transparent source-canvas margins. No resize occurs.
- Never upscale to fill 64x64.
- Only if the common union exceeds 64x64, apply the minimum common reduction needed to fit, using exact source-index area-overlap voting, rare-index protection and the 50% silhouette rule.
- Use one common transform for related animation frames; do not independently recenter each frame.
- Derive Generation III `MonCoords`/y-offset metadata from the adapted result instead of forcing the sprite into the original species' historical Gen III presentation box.
- Any minimally reduced exception remains a visual/pixel-correction candidate until eyes, markings, outline and silhouette are inspected.

## Bulbasaur result

- Diamond/Pearl front: native-pixel crop, scale 1.0; union 39x41 -> recommended MonCoords 40x48.
- Diamond/Pearl back: native-pixel crop, scale 1.0; union 63x44 -> recommended MonCoords 64x48.
- Platinum front: native-pixel crop, scale 1.0; union 39x41 -> recommended MonCoords 40x48.
- Platinum back: animation union 71x46, therefore minimal common fit scale 64/71 = 0.901408...; result union 64x41 -> recommended MonCoords 64x48.
- HeartGold/SoulSilver front: native-pixel crop, scale 1.0; union 39x36 -> recommended MonCoords 40x40.
- HeartGold/SoulSilver back: animation union 71x46, minimal common fit scale 0.901408...; result union 64x41 -> recommended MonCoords 64x48.

The official Pokémon Emerald Bulbasaur front/back assets and coordinate tables are used only as a Generation III presentation sanity reference. They are not copied into the Gen IV-derived assets. Emerald records Bulbasaur front as `MON_COORDS_SIZE(32, 40), y_offset 14` and back as `MON_COORDS_SIZE(48, 32), y_offset 16`; the v2 candidate intentionally allows new coordinate metadata when preserving the Gen IV pose requires it.

## Acceptance status

- ROM/source decode: PASS
- source-index preservation: PASS
- no-resize path for fitting sprites: PASS
- minimal-fit path for oversized animation unions: PASS (mechanical)
- Gen III 4bpp/LZ/palette packaging: PASS
- visual/manual pixel acceptance of scaled exceptions: **PENDING**

This directory is a candidate until the scaled exceptions complete visual/pixel review. It must not silently replace source evidence or the rejected v1 diagnostic pass.
