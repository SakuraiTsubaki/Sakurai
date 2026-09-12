# BW sprite preservation v3 — uncropped source pipeline

## Problem confirmed

The earlier v1/v2 experiments used a fixed 96×96 extraction window (`(48,16)–(144,112)`) after composing the BW multipart battle sprite on a 192×128 canvas. This window is useful for a DS-style view, but it is not a lossless source envelope for preservation work.

Measured frame-0 alpha bounding boxes from the existing ROM reconstruction:

| Dex | Pokémon | full composed bbox | bbox size | extent outside old 96×96 window |
|---:|---|---|---|---|
| 643 | Reshiram | (56,30)–(152,112) | 96×82 | rightmost 8 columns |
| 644 | Zekrom | (59,21)–(154,112) | 95×91 | rightmost 10 columns |
| 646 | Kyurem | (41,38)–(135,112) | 94×74 | leftmost 7 columns |

Therefore v1/v2 output PNGs remain useful as algorithm experiments, but they must not be treated as final porting sources.

## v3 source rule

The preservation source is now `*_rom_frame0_crop.png`, i.e. the complete non-transparent alpha bounding box produced from the 192×128 multipart composition. The fixed `*_rom_frame0_96.png` image is no longer accepted as the downscale source.

Pipeline:

1. BW ROM `/a/0/0/4` multipart data
2. NCGR + NCER + NANR + NMCR + palette composition on a large canvas
3. full alpha bounding-box extraction
4. preserve original aspect ratio
5. independently fit the complete silhouette to target generation canvas
6. one-pixel safety margin
7. bottom-safe placement for battle-sprite baseline stability
8. target-specific palette treatment

There is no 96→64→56 chain. Gen III and Gen II candidates are independently produced from the complete BW composition.

## Target rules used in the automatic v3 candidate

### Gen III candidate

- 64×64 output canvas
- complete source silhouette fitted inside 62×62 maximum envelope (1 px safety margin)
- nearest/pixel-footprint preservation; no RGB interpolation
- RGB converted to GBA-style 5-bit channel precision
- horizontal centering and bottom-safe placement
- this is an automatic candidate; species-specific repixel cleanup is still required

### Gen II candidate

- 56×56 output canvas
- complete source silhouette fitted inside 54×54 maximum envelope (1 px safety margin)
- same source-footprint preservation stage
- reduced to four visible luminance/chroma representatives as an automatic 2bpp-style candidate
- horizontal centering and bottom-safe placement
- final Gen II-authentic sprite still requires manual per-species pixel-art editing

## Important distinction

"Pixel preservation" does not mean retaining every source pixel after reducing dimensions. It means that no source information is lost *before* the generation-specific redesign begins. The complete Gen V silhouette, distinguishing structures and palette relationships are the preservation master; the Gen III/II versions are deliberate reinterpretations under their target constraints.

## Status

- clipping cause: confirmed
- old 96×96 preservation master: rejected
- full alpha-bbox source policy: confirmed
- v3 script: implemented as `preserve_downscale_v3_uncropped.py`
- final rendered v3 PNG validation: pending local execution because the current file-execution runtime timed out during this session
