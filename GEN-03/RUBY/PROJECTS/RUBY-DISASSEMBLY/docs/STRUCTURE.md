# Repository Structure

This repository is organized around reproducible reconstruction rather than raw ROM dumps.

## Core source

- `src/` — decompiled C source.
- `asm/` — assembly source and low-level reconstructed sections.
- `include/` — headers and declarations.
- `constants/` — IDs, enums, flags, and other constants.

## Game data

- `data/` — structured gameplay data and source tables.
- `data/versions/` — language/revision-specific overrides or source data.
- `maps/` — map/layout/event source when maintained separately from `data/`.
- `text/` — decoded text/localization source when maintained separately from `data/`.

## Assets

- `graphics/` — reconstructed sprites, tiles, palettes, interface graphics, fonts, and human-viewable PNGs.
- `sound/` — music, cries, samples, MIDI/WAV/source tables, and sound-engine data.

## Reproducibility

- `config/versions/` — build definitions for each supported language/revision.
- `manifests/` — source-ROM inventories, checksums, extraction manifests, and reconstruction status.
- `symbols/` — symbols, address maps, labels, and cross-version mappings.
- `tools/` — extraction, conversion, analysis, build, and verification utilities.
- `tests/` — regression tests and byte-identity verification.
- `docs/` — reverse-engineering notes, formats, provenance, and implementation documentation.

## Version model

Common data should live once. Version-specific differences should be represented explicitly through configuration or scoped overrides rather than wholesale copies.

Initial target identifiers:

```text
japan
usa
usa_europe_rev2
europe_rev1
germany
germany_rev1
germany_debug
france
france_rev1
italy
italy_rev1
spain
spain_rev1
```

Identifiers may be refined after ROM-header/hash verification.

## Binary policy

Complete game ROM binaries are never committed. A source ROM may be used locally during extraction and verification, but the completed repository must contain the reconstructed material required to rebuild the supported target without that local ROM.

Opaque binary regions should be treated as temporary reconstruction debt and documented in manifests until replaced with source-form data or code.
