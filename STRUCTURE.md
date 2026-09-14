# Repository Structure v12

Status: **canonical** — 2026-09-14.

The live repository represents the current structure only.

## Canonical live root

```text
.github/
GEN-XX/
CROSS-GEN/
INFRA/
README.md
STRUCTURE.md
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

## Single-owner project rule

A live artifact with exactly one project owner must live below that project's canonical `PROJECTS/<PROJECT-ID>/` root. Project-specific analysis, comparisons, reports, tables, tools, manifests, verification evidence, design material, inputs, build metadata, implementation material, patches, assets, and other outputs move together with the project.

Game-, generation-, and cross-generation-level domains are reserved for material genuinely shared by multiple projects or owned by that scope itself.

## Version update rule

Version changes update the current tree directly. If a canonical path changes, merge all unique current work into the new path and remove the old live path in the same change. Do not create parallel `MIGRATION`, `LEGACY`, `PRE-V*`, snapshot, redirect, quarantine, or version-history trees. Git commits, tags, and pull requests are the history and recovery mechanism.

Canonical live project coordinates are indexed at `INFRA/PROJECTS/INDEX.md`.

## Generation V → ポケットモンスター

All live work for `GEN5-TO-POCKET-MONSTERS` is stored directly under:

```text
CROSS-GEN/PROJECTS/GEN5-TO-POCKET-MONSTERS/
```

This includes `BLACK/`, `WHITE/`, `COMPARES/`, `SHARED/`, project analysis, tools, manifests, reports, crosswalks, design, and verification work. Do not recreate a repository-root `GEN-05/` tree or a nested project `GEN-05/` mirror.

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
MIGRATION.md
INFRA/MIGRATION/
```

## ROM policy

Only complete playable ROM image files are excluded from GitHub. Source, analysis, documentation, scripts, patches, manifests, hashes, logs, tests, extracted/reconstructed graphics, sprites, PNGs, tiles, maps, text, fonts, audio, tables, binary non-ROM assets, build metadata, reproducible intermediates, and other project artifacts belong in the appropriate repository.
