# GSCRGBY

Generation II Kanto rebuilt for a Generation I engine, while preserving RGBY and GSC version/event differences as separate content rather than collapsing them.

## Repository role

This public tree contains reproducible source, conversion tools, patch data, tests, schemas, and documentation. Original `.gb`/`.gbc` ROM images are local inputs and are never committed.

## Canonical path

`projects/gscrgby/` is the canonical project root. Legacy `GEN-01`, `GEN-02`, and `CROSS-GEN` paths remain read-only migration sources until their material is moved or retired.

## Main directories

- `engine/gen1/` — Generation I-side engine adapters and data-format definitions.
- `sources/gen1/` — RGBY extraction/import descriptors and version-difference tables.
- `sources/gen2/` — GSC Kanto extraction/import descriptors and version-difference tables.
- `integration/` — GSCRGBY merged event/map/tileset/object model.
- `patches/` — distributable patch data only, never full ROM images.
- `manifests/` — ROM fingerprints, build manifests, migration maps.
- `tools/` — reproducible extraction/conversion/validation tools.
- `tests/` — structure, map, warp, collision, event and regression tests.
- `docs/` — architecture and reverse-port design notes safe for public release.

See `docs/repository-layout-v2.md` for the migration rules.
