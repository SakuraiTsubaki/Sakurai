# Repository Migration — v3

## Status

The root cutover is complete. `GAMES/` is the only active game-data root.

Retired path models are frozen for audit at:

- `META/MIGRATION-SNAPSHOTS/V1/` — old `GENERATION-* / GAME / LOCALE / REV / WORK TYPE`
- `META/MIGRATION-SNAPSHOTS/V2/` — intermediate standalone `GEN-XX` provenance model

## Canonical ownership

```text
GAMES/GEN-XX/<GAME-ID>/RELEASES/<RELEASE-ID>/<WORK-TYPE>/...
GAMES/GEN-XX/<GAME-ID>/COMPARISONS/<COMPARISON-ID>/<WORK-TYPE>/...
GAMES/GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/COMMON/<WORK-TYPE>/...
GAMES/GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/TARGETS/<TARGET-ID>/<WORK-TYPE>/...
GAMES/GEN-XX/<GAME-ID>/SHARED/<WORK-TYPE>/...
```

A `RELEASE-ID` identifies one exact official build. Platform, market, language set, revision/update version, hashes, and provenance belong in release metadata.

## Promotion order

1. Register exact source releases and manifests.
2. Promote release-owned material into `RELEASES`.
3. Promote multi-release diffs/audits into `COMPARISONS`.
4. Promote modernization/localization/engine-expansion work into `PROJECTS`.
5. Promote truly release-independent material into `SHARED`.
6. Verify hashes, provenance, target bases, comparison membership, and file counts.

Migration snapshots are frozen audit sources, never parallel live trees.

Sakurai and Tsubaki must use identical `RELEASE-ID`, `COMPARISON-ID`, `PROJECT-ID`, and `TARGET-ID` values for the same real object.
