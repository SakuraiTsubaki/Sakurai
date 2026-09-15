# Generation IV → Generation III battle sprite master — Batch 001 (#001 BULBASAUR)

> **STATUS: REJECTED AS FINAL / RETAINED AS INTERMEDIATE EVIDENCE**
>
> This batch proved the ROM decoding, palette-index preservation, 4bpp/LZ packaging, hashing and dedup pipeline, but its fixed `80x80 -> 64x64` full-canvas transform was incorrectly promoted to a final Generation III sprite. It reduces every source pixel scale to 0.8 and therefore does not perform the required Generation III battle-presentation adaptation. Do not use the generated 64x64 images from this batch as canonical insertion sprites.

## Source

Five supplied Generation IV ROM observations are read directly and never modified: Diamond USA Rev.05, Pearl USA Rev.05, Platinum Korea Rev.00, HeartGold Korea Rev.00, SoulSilver Korea Rev.00. The active base battle archives are read through NitroFS and species 001 uses the `species * 6` member block.

Diamond/Pearl scanned NCGR payloads use the DP back-to-front LCRNG-XOR decode direction. Platinum/HGSS use the front-to-back direction. The decoded source canvas is 160x80 containing two 80x80 frames. Palette index 0 is transparent.

## What this rejected pass did

- complete 80x80 source frame -> complete 64x64 target canvas
- preservation-v2 exact area-overlap voting
- source palette indices only; no RGB interpolation/new colors
- rare-index and silhouette protection
- Gen III 4bpp / palette / LZ10 packaging

Those mechanics remain useful as a **minimal-fit fallback** when a real sprite/animation envelope cannot fit inside 64x64. They are no longer the default final transform.

## Corrected final-adaptation rule

1. `64x64` is the target canvas, not an instruction to scale an 80x80 canvas by 0.8.
2. Determine a common opaque union envelope for the relevant side/animation set.
3. If the union fits within 64x64, preserve source pixels **1:1** and remove/translate only transparent margins. No resampling is performed.
4. Never upscale merely to fill the canvas.
5. If the common union exceeds 64x64, reduce it only by the minimum amount required to fit, using source-index-only exact area-overlap selection; no RGB interpolation or invented colors.
6. Use one common transform for related animation frames so frame motion/anchoring is not destroyed.
7. Perform visual/pixel inspection and minimal corrective pixel work when a required fit reduction damages eyes, markings, silhouette, or identifying details.
8. Generate/update the matching Generation III `MonCoords` / y-offset metadata instead of forcing the new sprite into the old species' presentation box.
9. Only after adaptation approval are PNG, palette, 4bpp, LZ, hashes, manifest and canonical dedup assets considered final.

## Historical batch result

- logical source roles: 80
- canonical raw NCGR members: 5
- canonical raw NCLR members: 2
- canonical 80x80 rendered source images: 15
- canonical 64x64 fixed-downscale assets: 8
- validation of binary mechanics: PASS
- **visual/adaptation acceptance: FAIL**

All source/provenance records are retained so this rejected pass remains reproducible and auditable rather than silently deleted.
