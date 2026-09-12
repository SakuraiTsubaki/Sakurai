# BW battle-sprite animation safety — v5 exact timeline method

## Status

- Source structure: verified against the uploaded BW ROM work and `magical/pokemon-nds-sprites`.
- Geometry method: exact playback path implemented.
- ROM execution result: pending local runtime recovery; do not invent union numbers before execution.

## Why v5 exists

The first preservation prototypes treated a fixed 96×96 crop as the source image. That clipped wide Pokémon such as Reshiram, Zekrom, and Kyurem before downscaling.

v3 removed the fixed crop and used the full frame-0 alpha bbox.

v4 added a conservative animation-space union by enumerating all NANR frames reachable from NMCR elements. This is safe, but it can include frame combinations that are never played together.

v5 follows the actual Generation V playback stack and therefore computes the union of frames that the game really displays.

## Verified BW member layout

For each Pokémon/form block of 20 members in `/a/0/0/4`:

- front: 0..8
  - +2 NCGR sprite parts
  - +4 NCER
  - +5 NANR
  - +6 NMCR
  - +7 NMAR
- back: 9..17
  - +11 NCGR sprite parts
  - +13 NCER
  - +14 NANR
  - +15 NMCR
  - +16 NMAR
- +18 normal palette
- +19 shiny palette

## Exact playback order

The public BW extraction implementation confirms the runtime-style order:

1. `NMAR` selects the current mapped cell / NMCR map and supplies its local timeline.
2. `NMCR` iterates the mapped sprite-part animation entries.
3. For each NMCR entry, `NANR` selects the visible frame at the current map tick.
4. `NCER` supplies the OAM/cell object geometry.
5. `NCGR` supplies the non-transparent source pixels.

The key behavior copied into v5 is that consecutive NMAR frames referencing the same NMCR map keep accumulating `frame_tick`; switching map index resets that local tick to zero.

## v4 vs v5

### v4 conservative union

`scan_bw_animation_union_bbox.py`

Enumerates every NANR frame referenced by NMCR and unions the occupied pixels. Useful as a safety upper bound and corruption detector.

### v5 exact played union

`scan_bw_animation_timeline_v5.py`

For every tick in NMAR animation cell 0:

- resolve NMAR frame;
- resolve NMCR map;
- resolve each NANR part frame at that map-local tick;
- render opaque pixel masks on a large anchor-centered canvas;
- record the actual tick bbox;
- union all tick bboxes.

Front and back are scanned independently.

## Required validation

For each species and side, record:

- NMAR period in 60 Hz ticks;
- NMCR maps actually referenced by the NMAR timeline;
- per-tick bbox relative to battle anchor;
- exact played union bbox;
- conservative v4 union bbox;
- difference between exact and conservative unions;
- any tick touching the temporary analysis canvas edge (must be zero);
- any invalid NCER/NANR/NMCR/NMAR index (must be zero).

The exact union must be contained inside the conservative union. If not, one of the parsers or coordinate transforms is wrong.

## Downscale rule after v5

The representative static image may remain frame 0, but its **scale and anchor placement must be chosen using the exact full-animation union**, not the frame-0 bbox.

Generation III and Generation II candidates must be generated independently from the Generation V reconstruction. Never chain Gen V → Gen III → Gen II.

- Gen III: 64×64 target candidate, preserve silhouette/detail and use GBA-compatible color precision/palette constraints.
- Gen II: 56×56 target candidate, repixel for the target 2bpp sprite grammar rather than blindly retaining all Gen V colors.

One-pixel safety margins are an initial automated guard, not a substitute for species-specific manual pixel cleanup.

## Important distinction

A 96×96 extraction window is not treated as the authoritative Generation V sprite source. The authoritative source for preservation work is the ROM multipart animation plus its real anchor-relative occupied geometry.
