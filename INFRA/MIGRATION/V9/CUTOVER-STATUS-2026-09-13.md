# Repository v9 cutover status — 2026-09-13

## Canonical architecture

Active new work uses only:

```text
GEN-XX/
CROSS-GEN/
INFRA/
```

Generation/game source ownership is `GEN-XX/<GAME>/SOURCE/...`; intentional cross-generation project work is `CROSS-GEN/TARGET/...`.

## Generation V source anchors

```text
GEN-05/BLACK/SOURCE/NDS-TWL/CART/IRBO-HV0/
GEN-05/WHITE/SOURCE/NDS-TWL/CART/IRAO-HV0/
GEN-05/COMPARE/BLACK-IRBO-HV0--WHITE-IRAO-HV0/
```

Observed local dumps:

- Black: `SWEETNDS-a68b3bed`
- White: `SWEETNDS-f94d4578`

ROM images are excluded.

## Completed in this cutover

- `STRUCTURE.md` promoted to v9 canonical rules.
- `MIGRATION.md` promoted to v9 active cutover rules.
- machine-readable `INFRA/repository-path-v9.yaml` added.
- Generation V Black/White native summaries expanded with exact hashes and execution-region hashes.
- Black/White source snapshot report added.
- reproducible NDS inventory/parser tool added.
- current cross-generation project `release-lock.yaml` and `artifact-routing.yaml` migrated to canonical roots.
- v9 ROM-set registry added.

## Historical paths intentionally retained

Old `INFRA/PATH-SPECS/V*`, migration records, and `INFRA/QUARANTINE/**` may contain `LIBRARY/`, `PROJECTS/`, or older path grammar. These are historical evidence and are not rewritten.

## Physical legacy-root retirement

A top-level legacy `LIBRARY/` tree may still contain pre-cutover copies. It is now read-only/migration-only. It must be deleted only after every unique blob is proven represented in its canonical `GEN-*` owner or explicitly quarantined. No blind bulk deletion is permitted.
