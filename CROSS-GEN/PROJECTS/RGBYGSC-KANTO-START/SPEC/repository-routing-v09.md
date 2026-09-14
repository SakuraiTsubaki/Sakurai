# Repository routing — RGBYGSC Kanto Start

This target is intentionally cross-generation and therefore lives at:

`CROSS-GEN/TARGET/RGBYGSC-KANTO-START/`

It must not be placed under `GEN-02/SILVER/TARGET/` merely because Korean Silver is the runtime anchor: the target semantically incorporates Generation I RED/GREEN/BLUE/YELLOW source material and Generation II GOLD/SILVER/CRYSTAL material.

## Sakurai ownership

- source release and dump identities
- ROM header observations and cryptographic hashes
- bank/section fingerprints and comparisons
- map, tileset, sprite, script, event, text and object research
- preservation/integration specifications
- verification evidence and reproducible research tools

## Tsubaki ownership

- source-lock consumers and materialization recipes
- production asset catalogs
- normalized and converted assets
- implementation source and relocation tables
- patches and build recipes
- non-ROM build metadata/results
- production/play verification

## Source ownership stays local to each game

Official source identity remains at `GEN-01/<GAME>/SOURCE/...` or `GEN-02/<GAME>/SOURCE/...`. The cross-generation target references those identities; it does not duplicate or redefine them.

## Binary invariant

Original ROMs, modified ROMs, rebuilt ROMs, and raw ROM-byte slices are excluded from GitHub. Hashes, manifests, indexes, tools, patches, source, specifications and reproducibility metadata are versioned.
