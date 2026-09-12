# Repository Migration — v3

## Status

v3 is the canonical path model.

The old five-level tree and the intermediate v2 `SOURCE/<release>/<rev>` model are migration sources only. New work must use v3.

## Canonical ownership

```text
GAMES/GEN-XX/<GAME-ID>/RELEASES/<RELEASE-ID>/<WORK-TYPE>/...
GAMES/GEN-XX/<GAME-ID>/COMPARISONS/<COMPARISON-ID>/<WORK-TYPE>/...
GAMES/GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/COMMON/<WORK-TYPE>/...
GAMES/GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/TARGETS/<TARGET-ID>/<WORK-TYPE>/...
GAMES/GEN-XX/<GAME-ID>/SHARED/<WORK-TYPE>/...
```

The source release is the immutable identity unit. Locale, language, platform, revision/update version, hashes, and provenance are release metadata rather than mandatory independent path levels.

## Pokémon Green source-ROM mapping

Verified uploaded sources:

```text
Pocket Monsters - Midori (Japan) (SGB Enhanced).gb
  -> GAMES/GEN-01/GREEN/RELEASES/GB-JP-JA-REV-0/

Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb
  -> GAMES/GEN-01/GREEN/RELEASES/GB-JP-JA-REV-A/
```

The two exact ROM identities are recorded in `MANIFESTS/release.json`. Raw ROM binaries remain outside GitHub.

## Direct path mapping examples

```text
OLD
GENERATION-I/GREEN/JP-JA/REV-0/ANALYSIS/ROM-INVENTORY/...

V3
GAMES/GEN-01/GREEN/RELEASES/GB-JP-JA-REV-0/ANALYSIS/ROM-INVENTORY/...
```

```text
OLD
GENERATION-I/GREEN/JP-JA/REV-A/ANALYSIS/ROM-INVENTORY/...

V3
GAMES/GEN-01/GREEN/RELEASES/GB-JP-JA-REV-A/ANALYSIS/ROM-INVENTORY/...
```

Cross-revision material must not use `REV-ALL`:

```text
GAMES/GEN-01/GREEN/COMPARISONS/GB-JP-JA-REV-0--GB-JP-JA-REV-A/<WORK-TYPE>/...
```

Derived modernization work is project-owned:

```text
GAMES/GEN-01/GREEN/PROJECTS/MODERNIZATION/COMMON/<WORK-TYPE>/...
GAMES/GEN-01/GREEN/PROJECTS/MODERNIZATION/TARGETS/<TARGET-ID>/<WORK-TYPE>/...
```

## Migration order

1. Register exact source releases and manifests.
2. Move release-specific research/assets under `RELEASES`.
3. Move multi-release diffs and audits under `COMPARISONS`.
4. Move derived modernization/localization/build work under `PROJECTS`.
5. Move genuinely release-independent material under `SHARED`.
6. Remove empty legacy trees after their files have moved and verification passes.

Never create a duplicate live copy merely to preserve a legacy path. Git history preserves the previous location.

## Repository pair

Apply the same canonical IDs in `Sakurai` and `Tsubaki`. A release or project must not acquire a different identity simply because the repository contains a different artifact class.