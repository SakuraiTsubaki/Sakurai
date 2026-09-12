# Repository Structure v3

## Core rule

The repository path is built around **immutable release identity**, not around language, region, revision, or work type as independent ownership layers.

Canonical prefix:

`GAMES/GEN-XX/<GAME-ID>/`

A real ROM / executable / official build is one release unit. Region, language, revision, platform, cartridge flags, update version, hashes, and provenance are attributes of that release and are recorded in its manifest.

Original ROM / executable binaries are never committed.

## Why v3 replaces the old models

The legacy path

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

made locale and revision look universal even though later platforms use patches, title versions, build IDs, multilingual releases, DLC, and other build identities. The v2 draft improved provenance separation but still duplicated release identity as `SOURCE/<RELEASE-ID>/<REV>`.

v3 removes that duplication. **One canonical release ID identifies one exact official build.**

## Root layout

```text
GAMES/
  GEN-01/
    GREEN/
      RELEASES/
      COMPARISONS/
      PROJECTS/
      SHARED/
META/
.github/
README.md
STRUCTURE.md
MIGRATION.md
```

Generation folders are zero-padded: `GEN-01`, `GEN-02`, ... `GEN-10`, `GEN-11`, and onward.

`GAME-ID` is a stable uppercase machine slug. Human-facing official titles belong in metadata, not in the folder grammar.

`_SHARED` may be used as the game ID only for genuinely generation-wide material involving multiple games.

## RELEASES — exact official source builds

```text
GAMES/GEN-XX/<GAME-ID>/RELEASES/<RELEASE-ID>/<WORK-TYPE>/...
```

`RELEASE-ID` is a human-readable unique build identity. Recommended components are platform, market/region, language set, and build/revision identifier.

Examples for the uploaded Japanese Pokémon Green ROMs:

```text
GAMES/GEN-01/GREEN/RELEASES/GB-JP-JA-REV-0/
GAMES/GEN-01/GREEN/RELEASES/GB-JP-JA-REV-A/
```

Their SGB support is release metadata, not another path level. Likewise, hashes and Game Boy header version are recorded in `MANIFESTS/release.json`.

For later platforms, a release ID may use a software/update version instead of `REV-*`, for example `NSW-GLOBAL-MULTI-VER-4.0.0`. The folder grammar does not assume that every platform has cartridge-style revisions.

Duplicate dumps with identical verified content do not create another release tree. Record provenance/dump observations in the manifest.

## COMPARISONS — relationships between releases

```text
GAMES/GEN-XX/<GAME-ID>/COMPARISONS/<COMPARISON-ID>/<WORK-TYPE>/...
```

Use this whenever the subject inherently spans two or more releases. Do not create fake locale/revision owners such as `MULTI`, `REV-ALL`, or `ALL-REV`.

Example:

```text
GAMES/GEN-01/GREEN/COMPARISONS/GB-JP-JA-REV-0--GB-JP-JA-REV-A/DIFFS/
```

The exact member release IDs must also be recorded in comparison metadata.

## PROJECTS — derived work and modernization

```text
GAMES/GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/COMMON/<WORK-TYPE>/...
GAMES/GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/TARGETS/<TARGET-ID>/<WORK-TYPE>/...
```

A project may consume one or many official releases. `PROJECT-ID` describes the activity/product, such as `MODERNIZATION`, `LOCALIZATION-KO`, `ENGINE-EXPANSION`, or `SPRITE-UPGRADE`.

`COMMON` owns work shared by every target. `TARGETS` owns artifacts that differ by target build. Project manifests must state their exact base release IDs; a target is never represented as though it were an official source release.

## SHARED — game-wide reusable material

```text
GAMES/GEN-XX/<GAME-ID>/SHARED/<WORK-TYPE>/...
```

Use only for material genuinely independent of one exact release: common schemas, generic tools, engine terminology, reusable test infrastructure, and equivalent game-wide resources.

Do not move release-specific facts into `SHARED` merely to shorten a path.

## Generation-wide and cross-generation work

Generation-wide material uses:

```text
GAMES/GEN-XX/_SHARED/COMPARISONS/<ID>/<WORK-TYPE>/...
GAMES/GEN-XX/_SHARED/PROJECTS/<ID>/COMMON/<WORK-TYPE>/...
GAMES/GEN-XX/_SHARED/PROJECTS/<ID>/TARGETS/<TARGET-ID>/<WORK-TYPE>/...
GAMES/GEN-XX/_SHARED/SHARED/<WORK-TYPE>/...
```

Repository-wide catalogs, schemas, release registries, and migration metadata belong under `META/`. Cross-generation research should use a clearly named repository-wide study under `META/STUDIES/` unless it becomes its own project repository.

## Sakurai work types

Sakurai is the research / reverse-engineering / documentation source of truth. Canonical work types are:

`ANALYSIS`, `CENSUS`, `STRUCTURE`, `TEXT`, `DATA`, `DIFFS`, `TOOLS`, `TESTS`, `VERIFICATION`, `REPORTS`, `LOCALIZATION`, `DISASSEMBLY`, `MANIFESTS`, `MAPS`, `SYMBOLS`.

Subdirectories below a work type are semantic subjects, not replicas of generation/game/release ownership levels.

## Repository pair contract

`Sakurai` and `Tsubaki` use the same canonical identity prefix:

`GAMES/GEN-XX/<GAME-ID>/<BRANCH>/<IDENTITY>/...`

Sakurai owns research, release manifests, reverse engineering, source maps, specifications, and verification. Tsubaki owns production assets, patches, generated build artifacts, converters, and output manifests. The same `RELEASE-ID`, `COMPARISON-ID`, `PROJECT-ID`, and `TARGET-ID` must mean the same thing in both repositories.

## Migration rule

`GENERATION-*` roots, standalone `GEN-*` roots, and the v1/v2 five-level or `SOURCE/<release>/<rev>` trees are legacy. They may remain temporarily during migration but receive no new project work.

Move each file to the narrowest truthful v3 owner. Do not keep duplicate live copies to preserve an old pathname; Git history is the archive.