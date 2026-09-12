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

```text
GEN-01/
GEN-02/
CROSS-GEN/
INFRA/
LIBRARY/
PROJECTS/
LEGACY/
```

Existing files under retired roots are **migration sources**, not new-work destinations. Move unique content by meaning; do not mechanically preserve the old nesting.

## Cutover rules

1. Register all local source images in `catalog/roms/manifest.json` first.
2. Give research data stable Kanto-domain IDs before moving it.
3. Separate observations (`research/`) from desired end state (`spec/`).
4. Move implementation/tooling material to Tsubaki instead of keeping production mirrors in Sakurai.
5. Do not migrate ROM images or bulk/raw extracted asset dumps.
6. After unique content is migrated and references are updated, remove obsolete roots in a dedicated cleanup change; Git history remains the archive.

## Tsubaki routing counterpart

Production material formerly nested under generation/game source/target leaves is routed by function:

- input identity → `config/roms/`
- extraction/conversion utilities → `tools/rom/`
- final project implementation → `src/kanto/` and `src/engine/`
- verification → `tests/`
- local source images → ignored `local/roms/`
- regenerated working data → ignored `generated/`
- build products/reports → ignored or selectively versioned under `build/`
