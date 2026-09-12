# v8 → v9 migration for GEN4-TO-POCKET-MONSTERS

1. Keep generation/game ownership and the `SOURCE / TARGET / COMPARE / SHARED / REFERENCE` semantics.
2. Preserve the repository-wide v9 technical release-ID grammar (`HV5`, `HV0`, etc.) so this project does not fork global identity rules.
3. Replace source-labelled dump IDs (`LGC-*`, `UPLOAD-*`) with `DUMP-<12-char SHA1>`. Preserve former labels as `legacy_dump_id` metadata where useful.
4. Rewrite any live manifest that still points at retired `LIBRARY/...` roots to `GEN-XX/...`.
5. Register all 19 currently supplied ROM observations as release/dump records, but mark the 19-ROM set as `SUPPLIED-20260913`, not as the full official corpus.
6. Keep original ROMs local/read-only. Only metadata, research, scripts, indexes, extracted/converted production assets, patches and verification outputs are eligible for GitHub.

## Migration stance

Existing v8 data is preserved until its v9 equivalent is verified. New work must use v9 canonical references. Legacy source labels are evidence/provenance fields, not canonical identities.
