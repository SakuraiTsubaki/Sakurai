# Migration to v11

Status: active — 2026-09-13.

## Objective

Eliminate the ambiguity where Sakurai held deep ROM-derived analysis while Tsubaki held only a thin catalog/manifest subset. Under v11, Tsubaki is the complete non-ROM superset and Sakurai is the curated knowledge subset.

## Path mapping

```text
legacy: GEN-05/BLACK/SOURCE/NDS-TWL/CART/IRBO-HV0/...
new:    GEN-05/BLACK/RELEASES/NDS-TWL/CART/IRBO-HV0/...

legacy: GEN-05/WHITE/SOURCE/NDS-TWL/CART/IRAO-HV0/...
legacy: LIBRARY/GEN-05/WHITE/SOURCE/NDS-TWL/CART/IRAO-HV0/...
new:    GEN-05/WHITE/RELEASES/NDS-TWL/CART/IRAO-HV0/...
```

Exact dump-specific observations move under `DUMPS/DUMP-SHA256-.../`. Release-wide facts remain at the release root.

## Repository migration

1. Materialize release/dump identity in Sakurai.
2. Mirror those knowledge artifacts to Tsubaki.
3. Put every additional non-ROM extraction/asset/build artifact in Tsubaki at the same coordinate.
4. Verify hashes/counts against the source ROM locally.
5. Mark old SOURCE/LIBRARY locations migration-only; delete them only after content equivalence is verified.

No ROM binary is uploaded during migration.
