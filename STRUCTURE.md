# Repository Structure v6

Status: **canonical** as of 2026-09-12.

v6 keeps the proven v5 release/dump identity model, but removes live path ambiguity. Current work is split into four explicit ownership roots:

```text
LIBRARY/
PROJECTS/
INFRA/
LEGACY/
```

Original ROM/executable binaries are never committed.

## 1. LIBRARY — source-of-truth research

Canonical source path:

```text
LIBRARY/GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

Order is fixed: generation → game → source → platform/execution profile → package kind → native release identity.

Human language/market labels belong in manifests unless the platform lacks a stronger technical identity.

Examples:

```text
LIBRARY/GEN-05/BLACK/SOURCE/NDS-TWL/CART/IRBO-HV0/
LIBRARY/GEN-05/WHITE/SOURCE/NDS-TWL/CART/IRAO-HV0/
```

Release leaves separate official release identity from exact observed dumps:

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

`NATIVE` records physical/software layout. `DOMAINS` records semantic game meaning. Raw ROM paths are never silently replaced by guessed semantic names.

Same-game comparisons:

```text
LIBRARY/GEN-XX/<GAME-ID>/COMPARE/<COMPARISON-ID>/
```

Cross-game comparisons:

```text
LIBRARY/GEN-XX/COMPARE/<COMPARISON-ID>/
```

`SHARED` is only for genuinely identity-independent schemas, parsers, terminology maps, or format descriptions. Byte-identical release files remain release-owned and are related through comparison/hash indexes.

External/secondary material belongs under `REFERENCE` and never overrides source-ROM facts.

## 2. PROJECTS — derived work

v6 removes the flat project namespace. Every project is generation-scoped unless it truly crosses generations:

```text
PROJECTS/GEN-XX/<PROJECT-ID>/
PROJECTS/CROSS-GEN/<PROJECT-ID>/
```

Project manifests lock source release/dump IDs and target IDs. Derived modernization, localization, integration, porting, patching, and rebuild work never lives inside an official source-release tree.

Typical Sakurai project sections:

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

Tsubaki uses the same project IDs and target IDs for production implementation.

## 3. INFRA — repository-wide rules

Canonical classes:

```text
INFRA/
├── ARCHITECTURE/
├── PATH-SPECS/
├── REGISTRIES/
├── SCHEMAS/
├── VALIDATORS/
├── TOOLING/
└── MIGRATION/
```

Repository-wide schemas, routing rules, validators, registries, migration maps, and generic tools belong here rather than inside a game.

## 4. LEGACY — read-only migration quarantine

```text
LEGACY/PRE-V6-2026-09-12/
```

This is the only allowed home for pre-v6 live trees that have not yet passed owner-by-owner equivalence migration. No new project work may be written there.

Git history remains the permanent archive. `LEGACY` is temporary compatibility/quarantine, not a second canonical tree; migrated copies are removed from `LEGACY` after equivalence verification.

## 5. Repository-pair invariant

Sakurai and Tsubaki share the same:

- `GEN-XX`
- `GAME-ID`
- `PLATFORM-ID`
- `PACKAGE-KIND`
- `RELEASE-ID`
- `DUMP-ID`
- `COMPARISON-ID`
- `PROJECT-ID`
- target IDs

Sakurai owns identity, reverse engineering, native structure, semantic research, comparisons, citations, extraction/rebuild specifications, and verification evidence.

Tsubaki owns extracted/normalized/converted production assets, implementation inputs, patches, builds, and production catalogs.

## 6. Forbidden canonical labels

New canonical paths must not contain:

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

## 7. Routing rule

Every artifact must have exactly one truthful owner:

- official release fact → `LIBRARY/.../SOURCE/.../<RELEASE-ID>/`
- exact observed dump fact → `.../DUMPS/<DUMP-ID>/`
- same-game relation → `<GAME-ID>/COMPARE/`
- cross-game relation → `GEN-XX/COMPARE/`
- identity-independent reusable research → `SHARED/`
- external reference → `REFERENCE/`
- derived work → `PROJECTS/GEN-XX/...` or `PROJECTS/CROSS-GEN/...`
- repository-wide rule/tool → `INFRA/`
- pre-v6 unmigrated material → `LEGACY/PRE-V6-2026-09-12/`
