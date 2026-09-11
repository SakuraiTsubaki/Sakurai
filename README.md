# Sakurai

Pokémon project analysis and research repository.

## Canonical hierarchy

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

Only canonical single-game names may appear at the GAME level. Cross-game material within one generation belongs under `_SHARED`.

Legacy material has been physically relocated under canonical game paths. When its finer locale/revision classification has not yet been resolved, it is preserved under `MULTI/REV-ALL/MIGRATED/<legacy-source>/` without changing file contents.

New work must never be written into `MIGRATED`; it goes directly to its canonical locale, revision, and work type.

Sakurai stores analysis, census, structure maps, disassembly notes, comparisons, verification, reports, manifests, tools, tables, and other research outputs. Original ROM binaries and non-redistributable copyrighted binaries are never stored here.

See `STRUCTURE.md` for the enforced schema and `MIGRATION.md` for the legacy relocation map.
