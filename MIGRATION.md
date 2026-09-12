# Repository Migration — v9

Status: **cutover design**, 2026-09-13.

v9 completes the v8 ownership migration by enforcing the Sakurai/Tsubaki payload split and registering `RGBY-KANTO-TO-GSC` as a first-class cross-generation target.

## Canonical roots

```text
GEN-XX/
CROSS-GEN/
INFRA/
```

## Repository split

```text
ROM-derived identity / provenance / research / spec / mapping / verification
  → Sakurai

extraction / conversion / implementation / patch / build / production reports
  → Tsubaki

original ROM / complete patched ROM / non-redistributable full extraction
  → local only
```

## Root cleanup map

Non-canonical live roots are removed from the canonical namespace. Unique material is retained read-only under quarantine when semantic migration is not yet complete.

```text
GENERATION-IV/... → INFRA/QUARANTINE/PRE-V9/ROOT/GENERATION-IV/...
LIBRARY/...       → INFRA/QUARANTINE/PRE-V9/ROOT/LIBRARY/...
PROJECTS/...      → semantic TARGET owner, otherwise quarantine
LEGACY/...        → INFRA/QUARANTINE/PRE-V9/ROOT/LEGACY/...
```

Existing `INFRA/QUARANTINE/PRE-V8/` remains historical and is not re-nested.

## v8 semantic mappings retained

```text
GEN-01/GREEN-MODERNIZATION                 → GEN-01/GREEN/TARGET/GREEN-MODERNIZATION
GEN-01/RED-MODERNIZATION                   → GEN-01/RED/TARGET/RED-MODERNIZATION
GEN-01/YELLOW-MODERNIZATION                → GEN-01/YELLOW/TARGET/YELLOW-MODERNIZATION
GEN-01/RBY-ENGLISH-RELOCALIZATION          → GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION
GEN-02/CRYSTAL-LOCALIZATION-KO             → GEN-02/CRYSTAL/TARGET/CRYSTAL-LOCALIZATION-KO
GEN-02/SILVER-MODERNIZATION                → GEN-02/SILVER/TARGET/SILVER-MODERNIZATION
GEN-03/FIRERED-KR-LOCALIZATION             → GEN-03/FIRERED/TARGET/FIRERED-KR-LOCALIZATION
GEN-03/FIRERED-MODERNIZATION               → GEN-03/FIRERED/TARGET/FIRERED-MODERNIZATION
GEN-03/LEAFGREEN-MODERNIZATION             → GEN-03/LEAFGREEN/TARGET/LEAFGREEN-MODERNIZATION
GEN-03/LEAFGREEN-PAST-PARADOX-001-386      → GEN-03/LEAFGREEN/TARGET/LEAFGREEN-PAST-PARADOX-001-386
```

## New v9 target registration

```text
Project: RGBY カントー地方 → GSC
Target ID: RGBY-KANTO-TO-GSC
Owner path: CROSS-GEN/TARGET/RGBY-KANTO-TO-GSC/
```

The path exists in both repositories with identical target ID but repository-specific contents.

## Cutover invariants

1. No original or complete patched ROM image is committed.
2. `SOURCE` release and dump identities are preserved.
3. Path-only moves preserve blob bytes where possible.
4. One live semantic owner exists per artifact.
5. Sakurai contains reviewable facts/specifications; Tsubaki contains reproducible production implementation.
6. Cross-generation work lives under `CROSS-GEN/TARGET`.
7. Quarantine receives no new production work.
8. No force-update or history rewrite of `main` during cutover.
