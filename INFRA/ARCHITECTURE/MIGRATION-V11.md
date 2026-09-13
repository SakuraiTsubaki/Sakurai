# Migration to v11

Status: **active cutover** — 2026-09-13.

v11 keeps v10 semantic coordinates (`RELEASES`, `PROJECTS`, `COMPARES`, `REFERENCES`, `SHARED`) and changes repository ownership semantics.

## v10 → v11 ownership cutover

- Tsubaki changes from a production/data-only plane into the **complete non-ROM superset**.
- Sakurai remains the curated knowledge/research view.
- Existing Tsubaki production artifacts stay where they are.
- Existing Sakurai-only non-ROM artifacts must be mirrored into Tsubaki at the same semantic coordinate.
- v9 and older `SOURCE/TARGET/COMPARE/REFERENCE` paths remain migration inputs and must be mapped into v11 pluralized coordinates.

## Migration order

1. Lock release/dump coordinates and exact hashes.
2. Mirror `RELEASE.json` and `DUMPS/<DUMP-ID>/OBSERVATION.json` from Sakurai into Tsubaki.
3. Mirror Sakurai analysis/tables/schemas/reports/tools/verification into Tsubaki.
4. Keep/add Tsubaki production catalogs, extracted assets, conversions, implementation, patches, build metadata/logs and tests at the same coordinate.
5. Migrate project and comparison trees to `PROJECTS` and `COMPARES`.
6. Verify that no Sakurai-only non-ROM artifact remains for the migrated scope.
7. Retire legacy paths only after unique content and references are verified.

## ROM rule

Never commit a complete original or modified/playable ROM image. This is the only blanket artifact-class exclusion from Tsubaki.
