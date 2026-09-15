# BW battle sprite native-format baseline

This baseline records the native source facts that the Generation III insertion pipeline must preserve before conversion.

## Main archive

- NDS path: `/a/0/0/4`
- supplied EUR Black archive SHA-256: `0ef9595f7924f533985515f159c35bdb8fd8015ef50bef2a2f0e08219ed3487e`
- supplied EUR White archive SHA-256: same
- archive size: `7,889,304` bytes
- members: `14,285`
- complete 20-member blocks by arithmetic: `714`
- trailing members: `5`

## Static battle graphics

- resource type: NCGR (`RGCN` Nitro container after decompression)
- native canvas: `96×96`
- indexed source: yes
- nominal color depth: 4bpp / 16 palette indices
- static front slots in each standard block: `+0` default/male, `+1` female
- static back slots in each standard block: `+9` default/male, `+10` female

The static Generation III master must come from these dedicated static members rather than from an arbitrarily frozen multipart animation tick.

## Multipart animated graphics

- animated-parts resource type: NCGR plus NCER/NANR/NMCR/NMAR
- dominant raw NCGR canvas observed directly: `256×128`
- front parts slots: `+2/+3`
- front cell/animation/multicell resources: `+4..+7`
- front auxiliary record: `+8`
- back parts slots: `+11/+12`
- back cell/animation/multicell resources: `+13..+16`
- back auxiliary record: `+17`

Animated resources are a separate preservation track. They remain in scope even where the baseline Generation III engine consumes only the static 64×64 sprite.

## Palettes

- `+18`: normal NCLR
- `+19`: shiny NCLR
- palette-index relationships must be retained; do not render to RGB and then derive a new palette by color frequency

## Conversion target

- Generation III target canvas: `64×64`
- indexed/4bpp-compatible output required
- palette binary required
- raw 4bpp graphics binary required
- compressed Generation III graphics binary required
- final PNG is a review artifact, not the sole deliverable

## Fixed geometric rule

For the BW static path, preservation-v2 maps the complete `96×96` source canvas to the complete `64×64` target canvas. The Pokémon's opaque bounding box is not cropped and fitted independently.

Each output pixel must select an existing source palette index using exact source-area overlap voting, with mild rare-index preservation and the fixed 50% opaque-footprint silhouette rule. RGB interpolation, antialiasing, or creation of new colors is prohibited.

## Unresolved work that remains explicit

- block → species/form mapping for all 714 complete blocks
- semantic resolution of `+8/+17` auxiliary records
- semantics of all 5 trailing members
- exact logical alias behavior for every empty female/static/parts slot
- complete source→target and logical→canonical manifests

No unresolved item is to be silently inferred or discarded.
