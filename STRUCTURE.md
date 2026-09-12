# Repository Structure v9

Status: **proposed cutover** — 2026-09-13.

v9 redesigns the repository around stable game ownership and removes transport/platform/package metadata from canonical paths. Those facts stay in manifests. Structural folder names are English nouns; registered IDs remain uppercase and are shared with Tsubaki.

## 1. Canonical roots

```text
GAMES/
SCOPES/
REGISTRY/
INFRA/
ARCHIVE/
```

Root documentation and `.github/` metadata are also allowed.

Retired after cutover: `GEN-XX/`, `CROSS-GEN/`, `LIBRARY/`, `PROJECTS/`, `GENERATION-IV/`, and live `LEGACY/` roots.

## 2. Game-owned paths

```text
GAMES/GEN-XX/<GAME-ID>/
├── RELEASES/<RELEASE-ID>/
├── TARGETS/<TARGET-ID>/
├── COMPARES/<COMPARISON-ID>/
├── REFERENCES/<REFERENCE-ID>/
└── SHARED/<RESOURCE-ID>/
```

A path exists only when content exists. Unknown language, market, revision, platform, package kind, or build facts are manifest state and never become placeholder directory IDs.

## 3. Official release ownership

Canonical release path:

```text
GAMES/GEN-XX/<GAME-ID>/RELEASES/<RELEASE-ID>/
```

Platform, package/distribution, language, region, revision, product code, title code, checksums, dump identity, and provenance are fields in `IDENTITY/manifest.*`.

Typical Sakurai release leaf:

```text
<RELEASE-ID>/
├── IDENTITY/
├── DUMPS/<DUMP-ID>/
├── NATIVE/
├── STRUCTURE/
├── CODE/
├── TEXT/
├── MAPS/
├── SYSTEMS/
├── RESEARCH/
├── REPORTS/
└── VERIFY/
```

Original ROM/executable binaries are never committed. A dump record is evidence about a release, not a second release identity.

## 4. Derived target ownership

Single-game work:

```text
GAMES/GEN-XX/<GAME-ID>/TARGETS/<TARGET-ID>/
```

Typical Sakurai target leaf:

```text
<TARGET-ID>/
├── MANIFESTS/
├── SOURCE-LOCKS/
├── RESEARCH/
├── CROSSWALKS/
├── SPEC/
├── DESIGN/
├── REPORTS/
└── VERIFY/
```

Implementation source, converted production assets, patches, and build outputs are owned by Tsubaki or their canonical implementation repository; Sakurai records the design, evidence, source locks, and verification.

## 5. Multi-game and cross-generation scope

Same-generation multi-game work:

```text
SCOPES/GEN-XX/TARGETS/<TARGET-ID>/
SCOPES/GEN-XX/COMPARES/<COMPARISON-ID>/
SCOPES/GEN-XX/REFERENCES/<REFERENCE-ID>/
SCOPES/GEN-XX/SHARED/<RESOURCE-ID>/
```

Cross-generation work:

```text
SCOPES/CROSS-GEN/TARGETS/<TARGET-ID>/
SCOPES/CROSS-GEN/COMPARES/<COMPARISON-ID>/
SCOPES/CROSS-GEN/REFERENCES/<REFERENCE-ID>/
SCOPES/CROSS-GEN/SHARED/<RESOURCE-ID>/
```

Do not use a scope root merely because two games share bytes. Shared identity-independent schemas/resources may be shared; release-owned facts remain with each release and equality is recorded by comparison evidence.

## 6. Registry and infrastructure

`REGISTRY/` contains pair-wide stable identifiers and schemas for generations, games, releases, dumps, targets, comparisons, references, and reusable resource IDs.

`INFRA/` contains validators, migration tooling, repository automation, generic parsers, and repository architecture documents.

`ARCHIVE/PRE-V9/` is read-only quarantine for unique material that cannot yet be assigned a live semantic owner. New work never goes to archive.

## 7. Sakurai ↔ Tsubaki invariant

Both repositories use identical values for:

- `GEN-XX`
- `GAME-ID`
- `RELEASE-ID`
- `DUMP-ID`
- `TARGET-ID`
- `COMPARISON-ID`
- `REFERENCE-ID`
- `RESOURCE-ID`

Sakurai is authoritative for identity, native/ROM structure, reverse engineering, comparisons, localization research, technical specification, citations, and verification evidence.

Tsubaki is authoritative for extracted/converted production assets, normalization, implementation helpers, patches, build recipes, and production verification.

A separate implementation repository such as `SakuraiTsubaki/pokegold-kr` may remain authoritative for its engine source; Sakurai/Tsubaki then store role-specific derived artifacts plus an exact source commit lock instead of duplicating the entire implementation tree.

## 8. ROM-derived routing rule

From a ROM/disassembly workflow:

```text
identity / hashes / offsets / bank maps / format notes / research / design / comparison
    → Sakurai

extracted reusable assets / converters / normalized data / insertion-ready data / patches / build scripts
    → Tsubaki

engine source that already has a dedicated canonical repository
    → keep there; reference exact commit from Sakurai/Tsubaki

original or modified full ROM binary
    → never commit
```

## 9. Gold/Silver NatDex examples

```text
GAMES/GEN-02/GOLD/TARGETS/GOLD-KR-NATDEX/
GAMES/GEN-02/SILVER/TARGETS/SILVER-KR-NATDEX/
```

Sakurai examples:

```text
.../RESEARCH/ROM-LIMITS-AND-ARCHITECTURE.md
.../SOURCE-LOCKS/pokegold-kr.json
.../VERIFY/
```

Tsubaki examples:

```text
.../MANIFESTS/
.../TOOLS/
.../PATCHES/
.../BUILD/
.../VERIFY/
```

## 10. Forbidden live labels

Outside `ARCHIVE/PRE-V9/`, do not introduce ambiguous ownership labels such as:

```text
MULTI
ALL
ALL-RELEASES
REV-ALL
REV-UNKNOWN
MULTI-REGION
_SHARED
MISC
OTHER
GENERAL
MIGRATED
```
