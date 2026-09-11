# BW battle sprite animation union-bbox method

## Status

Implemented scanner: `scan_bw_animation_union_bbox.py`.

This step supersedes the assumption that a reconstructed Generation V battle sprite can safely be treated as a fixed 96x96 source image.

## Problem being solved

The first preservation-downscale prototypes cropped a reconstructed multipart BW sprite to a fixed 96x96 window before converting it to older-generation envelopes. That can clip wide/extreme geometry before the preservation stage begins.

Frame 0 is also insufficient for a fully animated BW sprite: a wing, tail, horn, arm, or other cell can occupy a more extreme coordinate in another NANR frame.

## ROM members scanned

Within the 20-member per-species/form block in `/a/0/0/4`:

- Front geometry: `+2 NCGR`, `+4 NCER`, `+5 NANR`, `+6 NMCR`
- Back geometry: `+11 NCGR`, `+13 NCER`, `+14 NANR`, `+15 NMCR`

For species `dex`, the block base is `dex * 20` in the current BW archive mapping used by this project.

## Method

1. Parse the multipart NCGR graphics.
2. Parse NCER cells/OAM objects.
3. Parse every NANR animation cell and every frame referenced by NMCR map 0.
4. Apply the frame's translation/rotation/scale data.
5. Render each legal animation-element frame on a large safety canvas around a fixed logical battle anchor.
6. Record each occupied pixel bounding box.
7. Compute the spatial union across every legal frame for the front sprite and back sprite separately.
8. Store both canvas coordinates and anchor-relative coordinates.

The scanner does not need to invent synchronized combinations of unrelated animation elements. For clipping safety, the spatial union of each referenced element's legal positions is sufficient: every pixel position that can ever be occupied is included in the union.

## Outputs when executed

For each species:

- `<dex>_animation_union.json`
  - front union bbox
  - back union bbox
  - anchor-relative bounds
  - union size
  - NMCR element count
  - NANR animation/frame records
  - frame duration/type/cell/map offset/cell offset
- `manifest.json`
  - combined species results

Default test species:

- 643 Reshiram
- 644 Zekrom
- 646 Kyurem

## Integration rule for preservation downscale

The target-generation conversion must not read a fixed BW 96x96 crop as its authoritative source.

The authoritative geometric source is:

`BW multipart ROM data -> full legal animation geometry -> union bbox + battle anchor`

For a static Gen III/Gen II conversion, choose a representative pose/frame for artwork, but fit/position it using the verified union/baseline constraints so that the chosen target representation does not inherit accidental clipping from the BW extraction stage.

Front and back sprites must be processed independently.

## Verification state

- Multipart frame-0 reconstruction: confirmed on uploaded BW ROM in the earlier prototype.
- Fixed 96x96 clipping issue: confirmed for the tested frame-0 reconstructions.
- Full-animation union scanner implementation: complete.
- Full-animation numeric results for the uploaded ROM: pending execution because the current local runtime is returning `TransportTimeout` before file access. Do not treat union sizes as confirmed until the scanner has run successfully against the uploaded NARC.
