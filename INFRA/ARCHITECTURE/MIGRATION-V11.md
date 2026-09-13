# Migration to Repository Architecture v11

Status: active — 2026-09-13.

## Required changes from v10

1. Keep the v10 release-centric coordinate model and content-addressed dump IDs.
2. Retire the exclusive repository split. Tsubaki now receives **all non-ROM artifacts**, including analyses/tables/reports also stored in Sakurai.
3. Move active project work from legacy `GEN-01/TARGET/...` or root-like `TARGET/...` paths to `GEN-01/PROJECTS/<PROJECT-ID>/...`.
4. Move legacy `SOURCE/...` release material into `RELEASES/<PLATFORM>/CART/<RELEASE-ID>/...`.
5. Move legacy `COMPARE/...` work into `COMPARES/...`.
6. Preserve history: old paths may remain temporarily as read-only migration inputs, but new commits must target v11 paths.
7. Never migrate a ROM binary. Replace it with identity/provenance/hash observations and reproducible patch/build metadata.

## RBY cutover

The RBY English relocalization project moves to:

```text
GEN-01/PROJECTS/RBY-ENGLISH-RELOCALIZATION/
```

Existing non-ROM implementation, translation, patch, tool, report, and verification artifacts are preserved by reattaching their existing Git objects under the canonical project coordinate where possible; this avoids rewriting binary assets and retains byte identity.
