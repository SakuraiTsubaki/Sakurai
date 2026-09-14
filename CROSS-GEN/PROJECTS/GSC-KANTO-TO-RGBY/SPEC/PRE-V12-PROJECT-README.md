# GSCRGBY

Generation II Kanto rebuilt for a Generation I engine, while preserving RGBY and GSC version/event differences as separate content rather than collapsing them.

## Repository role

This public tree contains **promoted, reproducible** source/data definitions, conversion tools, patch data, tests, schemas, manifests, and documentation. Original `.gb`/`.gbc` ROM images are local inputs and are never committed.

Private reverse-engineering evidence lives in `SakuraiTsubaki/Tsubaki/workspaces/gscrgby/` and is promoted here only after input identity, transform, schema, and validation are fixed.

## Canonical path

`projects/gscrgby/` is the canonical public project root. Legacy `GEN-01`, `GEN-02`, and `CROSS-GEN` paths remain read-only GSCRGBY migration sources until their material is moved or retired.

## Main directories

- `engine/gen1/` — Generation I-side engine adapters and data-format definitions.
- `sources/gen1/` — promoted RGBY source descriptors and version-difference data.
- `sources/gen2/` — promoted Gold/Silver/Crystal source descriptors and version-difference data.
- `integration/` — validated GSCRGBY map/tileset/block/object/warp/event/script/text/localization model.
- `patches/` — distributable delta patch data only, never full ROM images.
- `manifests/` — ROM fingerprints, source locks, promotion records, build manifests, migration maps.
- `tools/` — reproducible extraction/conversion/validation tools.
- `tests/` — structure, map, warp, collision, event and regression tests without commercial ROM bytes.
- `docs/` — public architecture and reverse-port design documentation.

See `docs/repository-layout-v3.md` and `manifests/promotion/routing-v3.json` for the current path/promotion contract.
