# Repository Structure v9

Status: **canonical** — 2026-09-13.

v9 keeps generation/game ownership from v8, but makes source-release evidence, dump observations, research products, and production assets unambiguous across the Sakurai/Tsubaki pair.

## 1. Canonical roots

```text
GEN-XX/
CROSS-GEN/
INFRA/
```

Root documentation and `.github/` metadata are allowed. `LIBRARY/`, `PROJECTS/`, `LEGACY/`, `GENERATION-*`, and other pre-canonical roots are migration-only and receive no new work.

## 2. Game ownership

```text
GEN-XX/<GAME-ID>/
├── SOURCE/
├── TARGET/
├── COMPARE/
├── SHARED/
└── REFERENCE/
```

Generation-level `COMPARE/` or `TARGET/` is used only when work intentionally spans multiple games in that generation. Cross-generation work belongs under `CROSS-GEN/`.

## 3. SOURCE identity grammar

```text
GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

Generation V examples:

```text
GEN-05/BLACK/SOURCE/NDS-TWL/CART/IRBO-HV0/
GEN-05/WHITE/SOURCE/NDS-TWL/CART/IRAO-HV0/
```

`RELEASE-ID` identifies the release/build, never a specific dump file. Dump-specific evidence stays below the release.

### Sakurai release leaf

```text
<RELEASE-ID>/
├── IDENTITY/
├── DUMPS/<DUMP-ID>/
│   ├── IDENTITY/
│   ├── HEADER/
│   ├── INDEXES/
│   └── VERIFICATION/
├── NATIVE/
│   ├── HEADER/
│   ├── INDEXES/
│   ├── CODE/
│   ├── TEXT/
│   ├── MAPS/
│   └── DOMAINS/
├── ANALYSIS/
├── SPEC/
├── TOOLS/
├── REPORTS/
└── VERIFICATION/
```

Identity-independent parsers/schemas go under `SHARED`, not duplicated into every release.

## 4. Sakurai responsibility

Sakurai is authoritative for release identity, dump observation metadata, hashes, headers, section/file-system/overlay indexes, research, reverse-engineering, specifications, comparison reports, reproducible analysis tools, and verification evidence. ROM images are never stored here.

## 5. TARGET grammar

```text
GEN-XX/<GAME-ID>/TARGET/<TARGET-ID>/
GEN-XX/TARGET/<TARGET-ID>/
CROSS-GEN/TARGET/<TARGET-ID>/
```

A target manifest must lock exact source `RELEASE-ID` values and exact `DUMP-ID` values when byte-exact reproduction matters.

## 6. COMPARE grammar

```text
GEN-XX/<GAME-ID>/COMPARE/<COMPARISON-ID>/
GEN-XX/COMPARE/<COMPARISON-ID>/
CROSS-GEN/COMPARE/<COMPARISON-ID>/
```

Black/White source comparison:

```text
GEN-05/COMPARE/BLACK-IRBO-HV0--WHITE-IRAO-HV0/
```

## 7. SHARED and REFERENCE

`SHARED` is limited to identity-independent reusable schemas, parsers, terminology maps, codecs, and common algorithms. Byte-identical release-owned artifacts remain release-owned; equality is recorded by hashes/catalogs.

`REFERENCE` contains external/secondary material and never overrides direct observations from official software or a locally inspected source image.

## 8. Pair invariant with Tsubaki

Both repositories use identical generation, game, platform, package, release, dump, target, comparison, and reference/resource IDs. Sakurai owns **knowledge/evidence**; Tsubaki owns **production assets/implementation**.

## 9. ROM exclusion invariant

Never commit original, modified, rebuilt, decrypted, trimmed, padded, patched, or otherwise transformed ROM images. ROM-derived metadata, hashes, manifests, indexes, source code, scripts, patches, reports, and reproducibility data are project artifacts.

## 10. Forbidden new canonical labels

Outside migration/quarantine, do not introduce ambiguous owners such as `MULTI`, `ALL`, `REV-ALL`, `ALL-RELEASES`, `MULTI-REGION`, `MISC`, `OTHER`, `GENERAL`, `REV-UNKNOWN`, or `MIGRATED`. Unknown facts belong in manifests, not vague directory names.
