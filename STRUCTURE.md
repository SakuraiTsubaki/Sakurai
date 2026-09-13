# Repository Structure v11

Status: **canonical** — 2026-09-13.

The canonical detailed specification is [`INFRA/ARCHITECTURE/V11.md`](INFRA/ARCHITECTURE/V11.md).

v11 keeps the release-centric coordinates introduced by v10, but corrects the repository split: **Tsubaki is the complete non-ROM project repository.** Sakurai is the knowledge/research subset; anything committed to Sakurai for a project is also eligible and expected to exist in Tsubaki at the same semantic coordinate. Production artifacts exist in Tsubaki and do not need to be duplicated into Sakurai.

## Canonical roots

```text
GEN-XX/
CROSS-GEN/
INFRA/
```

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

`DUMP-ID` is `DUMP-SHA256-<first-16-uppercase-hex>` and the full SHA-256 is recorded in the observation manifest.

## Repository rule

- **Tsubaki:** every project artifact except original/modified/playable ROM images. This includes analysis, reports, tables, manifests, tools, source, extracted assets, normalized/converted assets, translation data, implementation data, patches, build recipes/logs, and verification evidence.
- **Sakurai:** research/control subset: identity, provenance, hashes, analysis, reverse engineering, tables, reports, schemas/specifications, research tools, and verification evidence.
- The old interpretation “Sakurai gets analysis while Tsubaki gets only production” is retired. It caused non-ROM artifacts to be absent from Tsubaki.

## ROM exclusion

Do not commit original ROMs, modified ROMs, playable ROM images, or a lossless bank/chunk decomposition whose only purpose is to reconstruct a copyrighted ROM. Hashes, metadata, patches, extracted functional assets, translation data, and reproducibility information are allowed project artifacts.

## Migration

v10 and older paths are migration inputs. New work uses v11. See [`INFRA/ARCHITECTURE/MIGRATION-V11.md`](INFRA/ARCHITECTURE/MIGRATION-V11.md).
