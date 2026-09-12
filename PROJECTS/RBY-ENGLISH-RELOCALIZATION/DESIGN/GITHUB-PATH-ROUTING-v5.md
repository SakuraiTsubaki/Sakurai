# RBY English Relocalization — GitHub routing v5

Status: **canonical** for this project.

## Source identity

Every official source build is owned by one concrete v5 source path:

```text
LIBRARY/GEN-01/<GAME-ID>/SOURCE/GB/CART/<RELEASE-ID>/
├── IDENTITY/
├── DUMPS/
├── NATIVE/
├── DOMAINS/
├── TOOLS/
├── REPORTS/
└── VERIFICATION/
```

`RELEASE-ID` uses the supported GB identity key `<MARKET>-<LANGUAGE>-HV<n>`. Preservation labels remain explicit metadata; Japanese Pikachu Rev 0A/B/C/D correspond to HV0/HV1/HV2/HV3 without losing those preservation labels.

Japanese Red/Green/Blue/Pikachu releases are `TRANSLATION-ORIGINAL` + `BUILD-BASE`. English Red/Blue/Yellow releases are `IMPLEMENTATION-REFERENCE` only. Green remains an independent target and no fictitious English Green release is created.

## Exact supplied dumps

```text
.../<RELEASE-ID>/DUMPS/USER-UPLOAD-<SHA1-PREFIX>/IDENTITY/dump.json
```

Dump identity never replaces release identity. Full ROM binaries are not committed.

## Cross-game ROM research

```text
LIBRARY/GEN-01/COMPARE/RBY-ROM-CENSUS-2026-09-12/
```

The census stores bank fingerprints, exact-equality groups and guarded padding candidates. Identical banks remain owned by their original releases; comparison data records only the relationship.

## Project ownership

```text
PROJECTS/RBY-ENGLISH-RELOCALIZATION/
├── MANIFESTS/
├── CROSSWALK/
├── DESIGN/
├── IMPLEMENTATION/
├── PATCHES/
├── BUILD/
├── TOOLS/
├── REPORTS/
└── VERIFICATION/
```

The project consumes canonical Japanese source releases and, where available, the corresponding official English implementation-reference release. All nine target IDs are locked by `MANIFESTS/release-lock.json`.

## Repository split

- **Sakurai** owns source/dump identity, ROM maps, reverse engineering, text/data research, comparisons, provenance, tools and verification evidence.
- **Tsubaki** owns extracted release assets, production catalogs, normalized/converted resources, project implementation, patches and build outputs.
- Exact official-release bytes in Tsubaki remain under that release's `ASSETS`; byte equality across Red/Blue/Yellow is recorded under `LIBRARY/GEN-01/COMPARE`, not by moving ownership to a pseudo-shared source.

## Forbidden legacy ownership

Do not create new RBY work under old v4 paths such as:

```text
LIBRARY/GEN-01/GB/<GAME>/RELEASES/...
LIBRARY/GEN-01/GB/_SHARED/...
```

or under `GAMES`, `MULTI`, `REV-ALL`, `_SHARED`, `MISC`, `OTHER`, `GENERAL`.

Git history preserves retired paths; live canonical work uses v5 only.
