# BW 64×64 preservation-v2 external cross-check

This cross-check exists only so the visual result of the fixed preservation-v2 contract can be inspected while the project ROM execution runtime is unavailable.

It is **not** the authoritative `BATTLE_MASTER_V1` source. The final master must be rebuilt directly from the uploaded BW ROM `/a/0/0/4` static NCGR slots and ROM palettes.

## Rules used

- complete source canvas -> complete 64×64 canvas
- no opaque-bbox normalization
- no generative-image tools
- no antialiasing
- no RGB interpolation
- output colors selected only from colors occurring in the source sprite
- weighted source-pixel area-overlap voting
- mild rare-color preservation (`0.08` exponent, matching the Generation IV preservation-v2 philosophy)
- transparency cannot win when mapped source footprint is at least 50% opaque
- global SHA-256 deduplication for the full cross-check build

## Tsubaki locations

- sample: `GENERATION-V/BW/EUR/REV-UNKNOWN/SPRITE_ASSETS/64x64_PRESERVATION_V2_EXTERNAL_CROSSCHECK/SAMPLE_643_646/`
- full cross-check: `GENERATION-V/BW/EUR/REV-UNKNOWN/SPRITE_ASSETS/64x64_PRESERVATION_V2_EXTERNAL_CROSSCHECK/`

The sample contains #643–646 front/back normal/shiny files and a gallery. The full build is designed to contain 001–649 front/back normal/shiny logical roles, four atlases, `roles.csv`, `summary.json`, and SHA-256-deduplicated assets.

## Final ROM-primary acceptance

The external cross-check never satisfies ROM-primary acceptance by itself. Final acceptance still requires direct BW ROM provenance, static NCGR slot mapping, +18/+19 palette verification, male/female slot handling, forms/special-tail inventory, and zero missing manifest references.
