# v10 Migration Plan

Date: 2026-09-13

## Cutover rule

v10 is immediately canonical for all new work. Existing v9 and older material is not deleted in place during the first cutover. It is treated as read-only migration input until mapped to a v10 coordinate.

## Mapping

```text
GEN-XX/<GAME>/SOURCE/<PLATFORM>/<PACKAGE>/<RELEASE>/...
  -> GEN-XX/<GAME>/RELEASES/<PLATFORM>/<PACKAGE>/<RELEASE>/...

GEN-XX/<GAME>/TARGET/<TARGET-ID>/...
  -> GEN-XX/<GAME>/PROJECTS/<PROJECT-ID>/...

GEN-XX/<GAME>/COMPARE/<ID>/...
  -> GEN-XX/<GAME>/COMPARES/<ID>/...

GEN-XX/<GAME>/REFERENCE/<ID>/...
  -> GEN-XX/<GAME>/REFERENCES/<ID>/...
```

Generation-level and cross-generation targets/compares follow the same pluralized v10 vocabulary.

## Migration stages

1. Freeze creation of new v9 `SOURCE`, `TARGET`, `COMPARE`, and `REFERENCE` paths.
2. Register every observed ROM as a v10 `RELEASES/.../DUMPS/<DUMP-ID>` source observation.
3. Create one migration map per legacy subtree with old path, new coordinate, ownership repo, and verification state.
4. Copy or recreate verified artifacts at v10 coordinates; do not blindly rename content whose provenance is unclear.
5. Replace internal links with v10 coordinates.
6. Move unresolved unique leftovers to `INFRA/QUARANTINE/PRE-V10/<original-path-id>/` only when needed.
7. Remove duplicate legacy copies only after hash/provenance verification; Git history remains the archive.

## First registered corpus

The 2026-09-13 baseline contains 25 locally observed ROM images: 7 Generation I, 8 Generation II, and 10 Generation III. Their ROM bytes remain local. GitHub receives only identity metadata, hashes, header/checksum results, and production references/plans.

## Safety invariants

- Never commit a playable ROM image.
- Never infer two releases are identical only because filenames look similar.
- Exact dump identity is SHA-256 based.
- Conceptual release identity and exact dump identity remain separate.
- Header/filename observations are marked as observations until external release verification is performed.
- Sakurai and Tsubaki must point at the same release and dump IDs.
