# Repository Structure v10

Status: **canonical** — 2026-09-13.

The canonical detailed specification is [`INFRA/ARCHITECTURE/V10.md`](INFRA/ARCHITECTURE/V10.md). v10 is a deliberate breaking redesign from v9: new canonical work no longer uses `SOURCE`, `TARGET`, `COMPARE`, or `REFERENCE` as ownership branches.

## Canonical roots

```text
GEN-XX/
CROSS-GEN/
INFRA/
```

Root documentation and `.github/` metadata are allowed. Legacy roots remain migration-only and receive no new work.

## Game ownership

```text
GEN-XX/<GAME-ID>/
├── RELEASES/
├── PROJECTS/
├── COMPARES/
├── REFERENCES/
└── SHARED/
```

## Release identity

```text
GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
└── DUMPS/<DUMP-ID>/
```

`RELEASE-ID` identifies a conceptual official release/build. `DUMP-ID` identifies an exact observed image and is content-addressed as `DUMP-SHA256-<first-16-uppercase-hex>`; the full SHA-256 stays in the observation manifest.

Language, market, region, revision, hashes, title, and checksum status are manifest fields rather than arbitrary path levels.

## Repository split

**Sakurai** is the knowledge/control plane: release and dump identity, provenance, hashes, headers/indexes, research, reverse engineering, schemas, mappings, specifications, analysis tools, reports, and verification evidence.

**Tsubaki** is the production/data plane: source references, extraction plans, catalogs, ROM-derived working assets, normalized/converted assets, implementation data, patches, build recipes/logs, production tools, and production verification.

Both repositories use the same generation/game/platform/package/release/dump/project/compare/reference IDs.

## Projects

```text
GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/
GEN-XX/PROJECTS/<PROJECT-ID>/
CROSS-GEN/PROJECTS/<PROJECT-ID>/
```

Every project pins its input release coordinates and exact dump IDs when byte-exact behavior matters.

## Comparisons and references

```text
GEN-XX/<GAME-ID>/COMPARES/<COMPARE-ID>/
GEN-XX/COMPARES/<COMPARE-ID>/
CROSS-GEN/COMPARES/<COMPARE-ID>/
```

`REFERENCES` contains secondary/external material and never overrides direct software observations. `SHARED` is only for genuinely release-independent reusable resources.

## ROM binary exclusion

Original and modified/playable ROM images are never committed. Hashes, manifests, source, scripts, tables, reports, extracted/normalized assets, patches, build recipes, logs, and reproducibility metadata are tracked.

See [`INFRA/POLICY/ROM-BINARY-EXCLUSION.md`](INFRA/POLICY/ROM-BINARY-EXCLUSION.md).

## Migration

v9 and older `SOURCE`, `TARGET`, `COMPARE`, and `REFERENCE` paths are migration inputs only. New work must use v10 paths. Migration rules are defined in [`INFRA/ARCHITECTURE/MIGRATION-V10.md`](INFRA/ARCHITECTURE/MIGRATION-V10.md).

Do not create new canonical catch-all labels such as `MULTI`, `ALL`, `REV-ALL`, `ALL-RELEASES`, `MULTI-REGION`, `MISC`, `OTHER`, `GENERAL`, `REV-UNKNOWN`, or `MIGRATED`.
