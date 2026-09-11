# Giratina Origin Forme sprite preservation v2

## Source
- Game: Pokémon Platinum (project-supplied Korean ROM)
- ROM SHA-256: `51050f65776f402f86b8b2b2d3b84ab5bbe80dbec75129c86f8bd9b447f11d7b`
- NARC: `poketool/pokegra/pl_otherpoke.narc`

## Verified member mapping
- Character 152: Giratina Origin Forme back sprite
- Character 153: Giratina Origin Forme front sprite
- Palette 246: normal palette
- Palette 247: shiny palette

The Platinum loading logic in `pret/pokeplatinum` resolves Giratina alternate forms through `PL_OTHERPOKE`, with character index `150 + (face / 2) + form * 2` and palette index `244 + shiny + form * 2`. For Origin Forme (`form = 1`) this gives character members 152/153 and palette members 246/247.

## Conversion prototype
Target: 80×80 Gen IV frame → 64×64 preservation draft.

Rules:
- no generative image tools
- no anti-aliasing
- no new/interpolated RGB colors
- output pixels select only from the source palette
- uniform 80×80 → 64×64 geometry
- area-weighted sampling with mild rare-color retention
- front/back remain independent assets
- both animation frames remain independent
- normal/shiny palettes remain independent

## Frame-0 normal-palette metrics
| Side | Variant | Opaque pixels | Colors used | Bounding box |
|---|---|---:|---:|---|
| Front | source 80×80 | 3941 | 15 | [1, 1, 79, 79] |
| Front | nearest 64×64 | 2511 | 15 | [1, 1, 63, 63] |
| Front | preserve v2 64×64 | 2527 | 15 | [1, 1, 63, 63] |
| Back | source 80×80 | 2643 | 11 | [4, 11, 79, 79] |
| Back | nearest 64×64 | 1688 | 11 | [3, 10, 63, 63] |
| Back | preserve v2 64×64 | 1698 | 11 | [3, 9, 63, 63] |

For reference, the geometric area factor from 80×80 to 64×64 is 0.64. The front source occupancy therefore predicts ~2522 pixels and the back ~1692 pixels; v2 remains close while preserving all palette colors used by the source frame.

## Status
This is an automated preservation draft, not final ROM-ready artwork. Final work must validate target-generation battle placement and manually inspect tendrils, spikes, facial features, silhouette corners, and narrow negative spaces.

Origin Forme is deliberately tracked separately from Altered Forme and must not be merged into the base species sprite record.
