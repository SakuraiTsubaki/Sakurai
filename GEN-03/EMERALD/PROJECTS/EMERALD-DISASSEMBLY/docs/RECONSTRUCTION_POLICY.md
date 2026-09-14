# Reconstruction Policy

## Core rule

This repository stores the reproducible source representation of Pokémon Emerald, not the original or reconstructed full ROM binaries.

## Source-of-truth references

Reference ROMs are treated as read-only inputs during reverse engineering. Their identities are recorded in `manifests/roms.json`. They are never committed.

## Reconstruction target

The final repository should be sufficient to produce each supported target from source and repository assets alone. A local `baserom.gba` dependency is not part of the final design.

During early reverse engineering, a local reference ROM may be used by analysis/extraction tools. Every such dependency must be progressively eliminated by replacing ROM slices with reconstructed source or repository assets.

## Preferred representations

Use the most editable and semantically useful representation that can reproduce the original bytes:

- code: C and/or labeled assembly
- tables: structured source, CSV/JSON where useful, generated assembly only when appropriate
- text: decoded strings plus exact encoding/charmap metadata
- Pokémon/trainer/UI graphics: PNG plus palette/layout metadata
- tiles/maps: editable tiles, palettes, layouts, events and map scripts
- audio: song/event source, voicegroups, samples and conversion metadata
- compressed data: keep decompression/recompression tooling and canonical source asset

Opaque `INCBIN` data is allowed only as an explicitly tracked intermediate state. It should be replaced as its format becomes understood.

## Multi-language policy

Shared engine/code/data should be represented once when it is byte- and semantics-equivalent. Language- or region-specific material must remain traceable to its target release. Do not merge distinct data merely because it looks visually similar.

## Verification

Each reconstructed target must eventually pass:

1. expected file size
2. GBA header fields
3. exact SHA-1/SHA-256 match
4. byte-for-byte comparison
5. build-from-clean-tree regression test

Any intentional modernization belongs outside the exact-reconstruction baseline or in a clearly separated branch/configuration.
