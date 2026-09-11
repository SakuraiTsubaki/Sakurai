# Sakurai

Pokémon project analysis and research repository.

## Canonical hierarchy

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

The exact naming and placement rules are defined in [`STRUCTURE.md`](STRUCTURE.md). That document is authoritative for all future automatic GitHub reflection.

Key rules:

- GAME contains only one canonical game title, or reserved `_SHARED` for genuinely generation-wide material.
- Group aliases such as `RGBY`, `GSC`, `DPPt-HGSS`, `BW`, and similar synthetic game folders are not used.
- Locale and revision names use the normalized tokens defined in `STRUCTURE.md`.
- Translation directions and cross-generation provenance are metadata/work concerns, not GAME or locale folder names.
- New work must follow the canonical hierarchy even while legacy paths are being migrated.

This repository stores reproducible analysis, census, comparison, verification, reports, manifests, scripts, tables, maps, symbols, tests, and other research outputs.

Distributable work products are reflected here automatically after work is completed. Original ROM binaries and non-redistributable copyrighted binaries are never stored here.
