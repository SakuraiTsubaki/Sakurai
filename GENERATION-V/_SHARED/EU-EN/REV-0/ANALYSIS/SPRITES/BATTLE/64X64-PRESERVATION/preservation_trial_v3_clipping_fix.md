# BW sprite preservation downscale v3 — unclipped source correction

## Confirmed issue in v1/v2

The v1/v2 trials used a fixed 96×96 diagnostic window cut from the reconstructed BW battle frame: `(48,16)-(144,112)` on the 192×128 composition canvas.

The actual reconstructed frame-0 alpha bounds are:

| Dex | Pokémon | full-frame alpha bbox | visible size | relation to old 96×96 window |
|---:|---|---|---|---|
| 643 | Reshiram | `(56,30)-(152,112)` | 96×82 | 8 px of right-side extent outside the window |
| 644 | Zekrom | `(59,21)-(154,112)` | 95×91 | 10 px of right-side extent outside the window |
| 646 | Kyurem | `(41,38)-(135,112)` | 94×74 | 7 px of left-side extent outside the window |

There is no confirmed vertical clipping in these three frame-0 samples: all visible bottoms end at y=112, which is the old window's bottom edge, and all tops are inside its upper edge. The confirmed loss is horizontal.

Therefore the 96×96 diagnostic crops used by v1/v2 are invalid as master sources for preservation downscaling. Those assets remain useful only as algorithm experiments.

## v3 source rule

1. Reconstruct the BW frame on a large composition canvas first (currently 192×128 for the tested frame path).
2. Preserve the original BW composition coordinates and frame anchor while composing NCGR + NCER + NANR + NMCR.
3. Determine the alpha bounding box only after all parts are composed.
4. Use the complete alpha crop as the pixel source; never crop to an assumed 96×96 source canvas before conversion.
5. Produce Gen III 64×64 and Gen II 56×56 independently from this complete source.
6. Fit the complete silhouette inside the target canvas without clipping; preserve aspect ratio and bottom alignment. Do not chain 96→64→56.
7. Treat final target-generation positioning/ground-contact review separately from source reconstruction.

## Status

- Full-frame bboxes: confirmed from uploaded Pokémon Black (EUR), `/a/0/0/4`, reconstructed frame 0.
- Horizontal clipping in v1/v2 source crops: confirmed.
- v1/v2 converted PNGs: superseded as final candidates.
- v3 target PNGs: must be regenerated from `*_rom_frame0_crop.png` / full reconstructed frame, not `*_rom_frame0_96.png`.
