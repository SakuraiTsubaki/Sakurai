# Repository Structure v7

Status: **canonical** as of 2026-09-12.

v7 is a generation-first ownership model. It preserves the technical release/dump identity model from v6 while removing the top-level `LIBRARY/` vs `PROJECTS/` split.

Original ROM/executable binaries are never committed.

## 1. Canonical roots

```text
GEN-01/
GEN-02/
...
GEN-XX/
CROSS-GEN/        # only when a target/reference/comparison truly crosses generations
INFRA/
```

Repository metadata and root documentation (`.github`, `.gitignore`, `README.md`, `STRUCTURE.md`, `MIGRATION.md`) are also allowed.

`LIBRARY/`, `PROJECTS/`, and `LEGACY/` are retired as top-level canonical roots in v7.

## 2. Generation layout

```text
GEN-XX/
├── <GAME-ID>/
│   ├── SOURCE/
│   ├── COMPARE/
│   ├── SHARED/
│   └── REFERENCE/
├── TARGET/
├── COMPARE/
├── SHARED/
└── REFERENCE/
```

A game directory owns facts about official releases of that game. Derived modernization/localization/integration/build projects are generation-owned `TARGET`s rather than being split into a separate top-level project tree.

## 3. Official source identity

Canonical source path:

```text
GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

The order is fixed:

```text
generation → game → source → platform/execution profile → package/distribution kind → native release identity
```

`PLATFORM-ID` describes the execution/container family, e.g. `GB`, `GBC`, `GBA`, `NDS-NTR`, `NDS-TWL`, `3DS`, `SWITCH`, `SWITCH2`.

`PACKAGE-KIND` describes the official package/distribution kind, e.g. `CART`, `DIGITAL`, `VC`, or another precise registered value.

`RELEASE-ID` identifies the official build/release. Human region/language/revision labels are metadata unless they are part of, or required to disambiguate, the native technical identity.

Typical Sakurai release leaf:

```text
<RELEASE-ID>/
├── IDENTITY/
├── DUMPS/<DUMP-ID>/
├── NATIVE/
├── DOMAINS/
├── TOOLS/
├── REPORTS/
└── VERIFICATION/
```

`DUMP-ID` identifies an exact observed image and never creates a fake release. Bad dumps, modified images, overdumps, trims, and incomplete images remain dump observations under the correct release or unresolved identity record.

`NATIVE` records physical/software layout. `DOMAINS` records semantic game meaning. Raw offsets are never silently replaced by guessed semantic ownership.

## 4. Targets

Generation-scoped derived work:

```text
GEN-XX/TARGET/<TARGET-ID>/
```

Cross-generation derived work:

```text
CROSS-GEN/TARGET/<TARGET-ID>/
```

Typical Sakurai target sections:

```text
MANIFESTS/
INPUTS/
CROSSWALK/
ANALYSIS/
DESIGN/
DIFFS/
TOOLS/
REPORTS/
VERIFICATION/
```

A target manifest must lock its source game, release IDs, dump IDs where needed, target identity, and provenance. A fan/project target never masquerades as an official `SOURCE` release.

## 5. Compare / Shared / Reference

Game-local relationship:

```text
GEN-XX/<GAME-ID>/COMPARE/<COMPARISON-ID>/
```

Generation-wide relationship:

```text
GEN-XX/COMPARE/<COMPARISON-ID>/
```

Cross-generation relationship:

```text
CROSS-GEN/COMPARE/<COMPARISON-ID>/
```

`SHARED` is only for genuinely identity-independent schemas, parsers, terminology maps, format definitions, or equivalent reusable material. Byte-identical release-owned files remain release-owned and are related by hashes/catalogs rather than moved to `SHARED`.

`REFERENCE` contains external/secondary sources and never overrides facts observed from official source images.

## 6. INFRA

Repository-wide architecture, registries, schemas, validators, tooling, and migration records belong under `INFRA/`.

Read-only migration quarantine is nested under:

```text
INFRA/QUARANTINE/PRE-V7/
```

It is not a canonical work destination. Unique pre-v7 material may remain there temporarily until owner-by-owner migration is verified. Git history remains the permanent archive.

## 7. Sakurai ↔ Tsubaki invariant

Both repositories use identical values for:

- `GEN-XX`
- `GAME-ID`
- `PLATFORM-ID`
- `PACKAGE-KIND`
- `RELEASE-ID`
- `DUMP-ID`
- `TARGET-ID`
- `COMPARISON-ID`
- reference/resource IDs

Sakurai owns identity, reverse engineering, native structure, semantic research, comparisons, citations, extraction/rebuild specifications, and verification evidence.

Tsubaki owns extracted/normalized/converted production assets, implementation inputs, patches, builds, and production catalogs.

## 8. Forbidden canonical labels

New canonical paths under `GEN-*` and `CROSS-GEN` must not contain ambiguous ownership labels such as:

```text
MULTI
REV-ALL
ALL
ALL-RELEASES
MULTI-REGION
_SHARED
MISC
OTHER
GENERAL
REV-UNKNOWN
MIGRATED
```

Unknown facts remain explicit manifest fields; they do not become fake path identities.

## 9. Routing rule

Every artifact has exactly one truthful owner:

- official release fact → `GEN-XX/<GAME-ID>/SOURCE/.../<RELEASE-ID>/`
- exact observed dump fact → `.../DUMPS/<DUMP-ID>/`
- same-game relation → `GEN-XX/<GAME-ID>/COMPARE/`
- same-generation cross-game relation → `GEN-XX/COMPARE/`
- generation-scoped derived work → `GEN-XX/TARGET/`
- cross-generation derived work → `CROSS-GEN/TARGET/`
- reusable identity-independent research → `SHARED/`
- external reference → `REFERENCE/`
- repository-wide rule/tool → `INFRA/`
- pre-v7 unmigrated material → `INFRA/QUARANTINE/PRE-V7/`
