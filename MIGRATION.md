# Repository Migration — v7

Status: **canonical cutover**, 2026-09-12.

v7 is a path-ownership redesign. File payloads are not rewritten merely to move them; existing Git tree/blob objects are reused wherever possible. Original ROM/executable binaries remain outside GitHub.

## v6 → v7 mapping

```text
LIBRARY/GEN-XX/...                    → GEN-XX/...
PROJECTS/GEN-XX/<PROJECT-ID>/...      → GEN-XX/TARGET/<PROJECT-ID>/...
PROJECTS/CROSS-GEN/<PROJECT-ID>/...   → CROSS-GEN/TARGET/<PROJECT-ID>/...
LEGACY/...                            → INFRA/QUARANTINE/PRE-V7/V6-LEGACY/...
```

The v6 `SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>` identity grammar is retained inside each game. This cutover changes ownership placement, not the meaning of release IDs or dump IDs.

## Canonical v7 roots

```text
GEN-XX/
CROSS-GEN/    # optional; created only when required
INFRA/
```

`LIBRARY`, `PROJECTS`, and `LEGACY` are retired as top-level roots.

## Migration invariants

1. Preserve blob bytes when only the pathname changes.
2. Keep exactly one live canonical owner for each artifact.
3. Do not promote a project target into `SOURCE`.
4. Do not convert region/language/revision labels into fake release identities.
5. Preserve exact release/dump identity and provenance.
6. Quarantined pre-v7 material receives no new work.
7. Remove quarantine copies only after equivalence/ownership verification; Git history remains permanent.
8. ROM/executable binaries remain excluded.

## Repository-pair rule

Sakurai and Tsubaki cut over together and retain identical generation/game/platform/package/release/dump/target/comparison identifiers. Sakurai remains authoritative for research and identity; Tsubaki remains authoritative for production assets and implementations.
