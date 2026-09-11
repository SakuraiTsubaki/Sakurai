# Giratina sprite preservation v2 audit

## Source
- Supplied Korean Pokémon Platinum ROM
- NDS game code: `CPUK`
- ROM version byte: `0`
- Species: Giratina #487
- Current scope: base species-slot front/back battle sprite, frame 0

## Method
The 80×80 source sprite was reduced to a 64×64 Generation III-style target canvas using deterministic area-weighted sampling. No generative image tool, anti-aliasing, or interpolated RGB color was used. Each output pixel selects a color already present in the source sprite palette. A mild rarity term is used only to reduce accidental loss of small accent colors.

## Results

| Side | Variant | Opaque pixels | Palette colors | BBox |
|---|---:|---:|---:|---|
| Front | source80 | 3984 | 14 | 0,1–79,78 |
| Front | nearest64 | 2545 | 14 | 0,1–63,62 |
| Front | preserve_v1_64 | 2637 | 14 | 0,1–63,62 |
| Front | preserve_v2_64 | 2555 | 14 | 0,1–63,62 |
| Back | source80 | 3546 | 12 | 0,8–79,79 |
| Back | nearest64 | 2266 | 12 | 0,6–63,63 |
| Back | preserve_v1_64 | 2335 | 12 | 0,6–63,63 |
| Back | preserve_v2_64 | 2279 | 12 | 0,6–63,63 |

The 80→64 area ratio is 0.64. That gives expected occupied areas of 2549.76 px for the front and 2269.44 px for the back. v2 lands at 2555 and 2279 px respectively, while v1 remains visibly and numerically over-retentive.

## Critical review points
- Front: wing/spike tips, head spikes, leg separation, red/yellow accent boundaries, internal silhouette gaps.
- Back: shoulder/wing readability, top protrusions, dark-body/armor separation, bottom-edge battle composition.

## Form handling
Giratina has multiple formes in Platinum. This audit intentionally does **not** assume that the base species slot covers every forme. Origin Forme must be located in the Platinum form-specific sprite data and audited separately. No form data should be merged merely because the National Dex species ID is shared.

## Asset location
The current v2 front/back 64×64 drafts are stored in `SakuraiTsubaki/Tsubaki` under:
`GENERATION-IV/PLATINUM/KOREA/REV-0/GRAPHICS/SPRITE-PRESERVATION-V2/GIRATINA/`
