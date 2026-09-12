# Repository Migration — v4

## Status

v4 is canonical. Legacy `GENERATION-*`, standalone `GEN-*`, `GAMES/`, `MULTI`, `REV-ALL`, `ALL`, and `MULTI-REGION` paths are migration inputs only and receive no new work.

## Canonical ownership

```text
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/RELEASES/<RELEASE-ID>/...
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/COMPARISONS/<COMPARISON-ID>/...
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/SHARED/...
PROJECTS/<PROJECT-ID>/...
INFRA/...
```

Exact supplied ROM images are dump observations below a release:

```text
LIBRARY/.../RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/...
```

## Classification before moving

- Official release fact -> `LIBRARY/.../RELEASES/`
- Exact dump/file observation -> `.../DUMPS/`
- Cross-release relationship -> `LIBRARY/.../COMPARISONS/`
- Port/integration/modernization/localization/rebuild -> `PROJECTS/`
- Repository-wide registry/schema/validator/migration data -> `INFRA/`

Do not infer ownership from a legacy directory name; classify each artifact by what it actually describes.

## Generation V -> Pocket Monsters

The old BW baseline owner:

```text
GENERATION-V/_SHARED/MULTI/REV-ALL/ANALYSIS/BW-EUR-REV-UNKNOWN/ROM-BASELINE-SWEETNDS/
```

splits into:

```text
LIBRARY/GEN-05/NDS/BLACK/RELEASES/IRBO-R0/DUMPS/SWEETNDS-a68b3bed/
LIBRARY/GEN-05/NDS/WHITE/RELEASES/IRAO-R0/DUMPS/SWEETNDS-f94d4578/
LIBRARY/GEN-05/NDS/_SHARED/COMPARISONS/BLACK-IRBO-R0--WHITE-IRAO-R0/
```

Generation V-owned integration work formerly hidden below `GENERATION-V/...` moves to:

```text
PROJECTS/GEN5-TO-POCKET-MONSTERS/CROSSWALK/...
PROJECTS/GEN5-TO-POCKET-MONSTERS/DESIGN/...
PROJECTS/GEN5-TO-POCKET-MONSTERS/IMPLEMENTATION/_SHARED/...
PROJECTS/GEN5-TO-POCKET-MONSTERS/IMPLEMENTATION/<TARGET-ID>/...
PROJECTS/GEN5-TO-POCKET-MONSTERS/VERIFICATION/...
```

Pure facts about original target ROMs remain in their own `LIBRARY/.../RELEASES/...` trees and are referenced by the project.

## Cross-generation dispatch rule

A cross-generation artifact belongs to the project that actually owns the transformation, not to whichever source/target generation folder happened to contain the legacy file.

```text
Generation V -> Pocket Monsters work -> PROJECTS/GEN5-TO-POCKET-MONSTERS/...
Generation IV -> Pocket Monsters work -> PROJECTS/GEN4-TO-POCKET-MONSTERS/...
```

A Gen IV import/conversion artifact found under a Gen III legacy target tree remains Gen IV-project work. Shared target ROMs do not merge project identities.

## Migration order

1. Freeze legacy paths for new writes.
2. Register all supplied releases and dump observations in `INFRA/REGISTRY/`.
3. Lock each project's sources/targets in its own `MANIFESTS/release-lock.yaml`.
4. Build an old-path -> v4-owner equivalence manifest.
5. Migrate exact single-release material first.
6. Split pseudo-release trees (`MULTI`, `REV-ALL`) into comparisons or projects by semantics.
7. Move cross-generation work to its correct project root, splitting shared and target-specific implementation.
8. Verify hashes, file counts, references, and target bases.
9. Remove obsolete live copies only after equivalence checks pass; Git history is the archive.
10. Make CI/path validators reject new legacy paths.

## Safety invariant

Do not blindly rename whole legacy directories. They frequently mix release facts, comparisons, dump observations, and project outputs. Every migrated file needs one truthful v4 owner.