# v8 → v9 migration map

v9 changes ownership from a duplicated generation/game tree to repository-specific responsibilities.

## Sakurai routing

| v8 semantic content | v9 destination |
| --- | --- |
| release/dump identity, hashes, header observations | `catalog/roms/` |
| Gen I Kanto map/geography observations | `research/gen1/kanto/` |
| Gen II Kanto map/system/event observations | `research/gen2/kanto/` |
| RGBY ↔ GSC comparisons | `research/comparisons/kanto/` |
| desired restored behavior/geography | `spec/kanto/` |
| portable data contracts | `schemas/` |
| repository architecture/decisions | `docs/` |

## Retired as canonical roots

`GEN-01/`, `GEN-02/`, `CROSS-GEN/`, `INFRA/`, `LIBRARY/`, `PROJECTS/`, and `LEGACY/` become migration sources rather than destinations for new work.

## Cutover rules

1. Register local source images in `catalog/roms/manifest.json`.
2. Give research data stable Kanto-domain IDs before moving it.
3. Separate observations (`research/`) from desired end state (`spec/`).
4. Move implementation/tooling material to Tsubaki rather than mirroring production trees in Sakurai.
5. Do not migrate ROM images or bulk/raw extracted asset dumps.
6. Remove obsolete roots only after unique content and references are migrated; Git history remains the archive.

## Tsubaki routing counterpart

- input identity → `config/roms/`
- extraction/conversion utilities → `tools/rom/`
- final project implementation → `src/kanto/`, `src/engine/`
- verification → `tests/`
- local source images → ignored `local/roms/`
- regenerated working data → ignored `generated/`
- build products/reports → `build/`
