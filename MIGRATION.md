# Repository Migration — v6

Status: **active canonical migration**, started 2026-09-12.

v6 is a path-ownership redesign, not a content rewrite. Existing Git objects are reused wherever possible; original ROM binaries remain outside GitHub.

## Completed in the v6 cutover

1. `LIBRARY`, `PROJECTS`, `INFRA`, and `LEGACY` are the only data roots.
2. Flat `PROJECTS/<PROJECT-ID>` is retired in favor of `PROJECTS/GEN-XX/<PROJECT-ID>` or `PROJECTS/CROSS-GEN/<PROJECT-ID>`.
3. Pre-v6 top-level roots and platform-first library remnants are quarantined under `LEGACY/PRE-V6-2026-09-12/`.
4. New writes to legacy names are rejected by CI.
5. v5 release/dump identity rules remain valid and are not renumbered merely for migration.

## Canonical source path

```text
LIBRARY/GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

Exact dumps stay below the release:

```text
.../<RELEASE-ID>/DUMPS/<DUMP-ID>/
```

## Canonical project path

```text
PROJECTS/GEN-XX/<PROJECT-ID>/
PROJECTS/CROSS-GEN/<PROJECT-ID>/
```

Generation is determined by the project's target/source scope, not by a guessed filename. Cross-generation projects use `CROSS-GEN`; `MULTI` is forbidden.

## Legacy quarantine

```text
LEGACY/PRE-V6-2026-09-12/
```

This tree is read-only. It may contain older root layouts and platform-first v4/v5 remnants while equivalence is being checked. It is not a valid destination for new analysis, assets, builds, or project outputs.

## Migration order

1. Freeze pre-v6 paths.
2. Quarantine old live roots without changing blob contents.
3. Group projects by generation.
4. Keep already-canonical game-first v5 source trees live.
5. Classify each quarantined subtree by owner: release, dump, comparison, reference, shared, project, or infra.
6. Re-home files into v6 canonical owners using the existing release/dump/project IDs.
7. Rewrite internal path references and release locks.
8. Verify file counts, blob hashes, provenance links, and target bindings.
9. Remove verified redundant quarantine copies from `LEGACY`; Git history remains available permanently.

## Non-destructive invariant

No pre-v6 tree is discarded merely because its path is obsolete. A legacy subtree leaves `LEGACY` only after its canonical owner is established and equivalence is verified.

## Forbidden new canonical labels

`MULTI`, `REV-ALL`, `ALL`, `ALL-RELEASES`, `MULTI-REGION`, `_SHARED`, `MISC`, `OTHER`, `GENERAL`, `REV-UNKNOWN`, and `MIGRATED` are forbidden outside `LEGACY` historical content.
