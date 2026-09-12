# Repository Migration — v9

Status: **active cutover** — 2026-09-13.

v9 is a path/ownership normalization. Existing unique data is preserved; ROM images remain excluded.

## Canonical root mapping

```text
LIBRARY/GEN-XX/...                      → GEN-XX/...
GENERATION-XX/...                       → GEN-XX/...
PROJECTS/GEN-XX/<single-game-project>   → GEN-XX/<GAME-ID>/TARGET/<TARGET-ID>/...
PROJECTS/GEN-XX/<multi-game-project>    → GEN-XX/TARGET/<TARGET-ID>/...
PROJECTS/CROSS-GEN/<project>            → CROSS-GEN/TARGET/<TARGET-ID>/...
LEGACY/...                              → INFRA/QUARANTINE/PRE-V9/LEGACY/...
```

## Generation V cutover applied first

```text
GEN-05/BLACK/SOURCE/NDS-TWL/CART/IRBO-HV0/
GEN-05/WHITE/SOURCE/NDS-TWL/CART/IRAO-HV0/
GEN-05/COMPARE/BLACK-IRBO-HV0--WHITE-IRAO-HV0/
```

The inspected local images are dump observations only:

```text
Black: SWEETNDS-a68b3bed
White: SWEETNDS-f94d4578
```

They do not alter release IDs, and the `.nds` files remain local/uncommitted.

## Cross-repository reference repair

Tsubaki manifests must reference canonical Sakurai paths without retired `LIBRARY/` prefixes:

```text
Sakurai:GEN-05/BLACK/SOURCE/NDS-TWL/CART/IRBO-HV0/IDENTITY/release.yaml
Sakurai:GEN-05/WHITE/SOURCE/NDS-TWL/CART/IRAO-HV0/IDENTITY/release.yaml
```

## Cutover rules

1. Preserve exact blob contents when a change is path-only.
2. Never create a new release identity from a dump hash.
3. Keep clean-reference identity and observed-dump identity separate.
4. Do not promote dump-bound extracted data to release-level verified assets until provenance/clean-reference checks pass.
5. Keep one semantic owner per artifact; duplicates are tracked through hashes/catalogs.
6. New work uses v9 paths immediately.
7. Old roots are read-only until migrated, then removed when no unique content remains.
8. No ROM image is committed at any stage.
