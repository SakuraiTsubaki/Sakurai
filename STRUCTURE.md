# Repository Structure v12

Status: **canonical** — 2026-09-13; project-closure repair 2026-09-14.

v12 makes the live tree match the ownership model. Transitional v2–v11 path families are no longer valid live coordinates.

## Canonical live root

```text
.github/
GEN-XX/
CROSS-GEN/
INFRA/
README.md
STRUCTURE.md
MIGRATION.md
```

Repository metadata files such as `.gitignore` and `.gitattributes` may also exist at root.

## Generation/game coordinates

```text
GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/
GEN-XX/<GAME-ID>/COMPARES/<COMPARE-ID>/
GEN-XX/<GAME-ID>/REFERENCES/<REFERENCE-ID>/
GEN-XX/<GAME-ID>/SHARED/
```

Research/verification domains may also live directly below a game when they genuinely belong to that game:

```text
KNOWLEDGE/
VERIFY/
CATALOGS/
REPORTS/
TABLES/
ANALYSIS/
TOOLS/
```

Generation-wide ownership uses:

```text
GEN-XX/PROJECTS/<PROJECT-ID>/
GEN-XX/COMPARES/<COMPARE-ID>/
GEN-XX/REFERENCES/<REFERENCE-ID>/
GEN-XX/SHARED/
```

Cross-generation ownership uses:

```text
CROSS-GEN/PROJECTS/<PROJECT-ID>/
CROSS-GEN/COMPARES/<COMPARE-ID>/
CROSS-GEN/REFERENCES/<REFERENCE-ID>/
CROSS-GEN/SHARED/
```

## Project closure invariant

A live artifact with exactly one project owner **must live below that project's canonical `PROJECTS/<PROJECT-ID>/` root**. Analysis, comparisons, reports, tables, tools, manifests, verification evidence, design material, inputs, build metadata, implementation material, patches, assets, and other project-owned outputs are part of that project closure and must move with the project during every repository migration.

Game-, generation-, and cross-generation-level `COMPARES`, `ANALYSIS`, `REPORTS`, `TABLES`, `TOOLS`, `KNOWLEDGE`, and similar domains are reserved for genuinely shared or scope-level material. They must not be used merely to split one project's work by artifact type.

A migration is not complete merely because the old copy exists below `INFRA/MIGRATION/`. Every still-active project must have a live canonical owner containing its complete eligible closure. Historical migration trees remain evidence only.

Canonical live project coordinates and legacy-to-live ownership mappings are indexed at `INFRA/PROJECTS/INDEX.md` and `INFRA/PROJECTS/MIGRATION-MAP.json`.

## Generation V → ポケットモンスター single-home override

All live work for `GEN5-TO-POCKET-MONSTERS` is stored directly under:

```text
CROSS-GEN/PROJECTS/GEN5-TO-POCKET-MONSTERS/
```

This includes its `BLACK/`, `WHITE/`, `COMPARES/`, `SHARED/`, project analysis, tools, manifests, reports, crosswalks, design and verification work. Do not recreate a repository-root `GEN-05/` tree or a nested project `GEN-05/` mirror for this project. Version upgrades move/merge the current work into this single live root instead of retaining duplicate historical/current trees.

## Release and dump identity

Official release identity is represented by the `RELEASES` coordinate. Exact observed images are registered below that release as:

```text
DUMPS/DUMP-SHA256-<FIRST-16-UPPERCASE>/
```

The complete digest and observation metadata belong in the dump manifest. ROM image bytes themselves are never committed.

## Repository-pair invariant

- **Sakurai** is the curated research/control subset: identity, provenance, analysis, reverse engineering, comparisons, localization research, schemas, technical design, reports, research tooling, citations, and verification evidence.
- **Tsubaki** is the complete non-ROM superset. Every eligible Sakurai project artifact is also eligible for Tsubaki at the same semantic coordinate; production assets and implementation outputs may exist only in Tsubaki.
- Shared generation, game, release, dump, project, comparison, reference, and target IDs must match between repositories.

## Retired live paths

The following are forbidden in the live ownership tree:

```text
LIBRARY/
projects/
workspaces/
STRUCTURE-V2.md
SOURCE/
TARGET/
COMPARE/
REFERENCE/
```

Historical copies may exist only below `INFRA/MIGRATION/` and remain read-only migration evidence. The Generation V → ポケットモンスター single-home override above does not retain duplicate current project trees for historical purposes.

## ROM policy

Only complete playable ROM image files are excluded from GitHub. Source, analysis, documentation, scripts, patches, manifests, hashes, logs, tests, extracted/reconstructed graphics, sprites, PNGs, tiles, maps, text, fonts, audio, tables, binary non-ROM assets, build metadata, reproducible intermediates, and other project artifacts belong in the appropriate repository.
