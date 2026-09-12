# LeafGreen Path Design v3

## Scope

This design is derived from the currently audited Pokémon LeafGreen source ROM set. Original ROM binaries are never stored in GitHub.

## Core rule

A source path represents a verified official binary lineage, not a filename label or a desired target locale.

Canonical source build identity:

`<GAME-CODE>-<LANGUAGE>`

Canonical source path:

`GEN-03/LEAFGREEN/SOURCE/<BUILD-ID>/<REVISION>/<WORK-TYPE>/...`

For the current ROM set:

- `BPGJ-JA/REV-0`
- `BPGE-EN/REV-0`
- `BPGE-EN/REV-1`
- `BPGD-DE/REV-0`
- `BPGF-FR/REV-0`
- `BPGI-IT/REV-0`
- `BPGS-ES/REV-0`

Distribution labels such as Japan, USA, Europe, Germany, France, Italy, and Spain remain manifest metadata. They are not allowed to create duplicate source identities when the verified binary identity is the same.

## Ownership branches

### SOURCE

Official source-build-specific research only.

`GEN-03/LEAFGREEN/SOURCE/<BUILD-ID>/<REVISION>/<WORK-TYPE>/...`

Examples:

`SOURCE/BPGJ-JA/REV-0/DISASSEMBLY/...`

`SOURCE/BPGE-EN/REV-1/TEXT/...`

### COMPARE

Cross-build or cross-revision work.

`GEN-03/LEAFGREEN/COMPARE/<SCOPE>/<WORK-TYPE>/...`

Canonical scopes include:

- `ALL-BUILDS`
- `BPGE-REVISIONS`
- `LOCALIZATION`
- explicit pair scopes such as `BPGJ-JA__BPGE-EN`

`MULTI` and `REV-ALL` are legacy and must not receive new work.

### SHARED

Release-independent LeafGreen schemas, catalogs, generic tools, symbol conventions, and test infrastructure.

`GEN-03/LEAFGREEN/SHARED/<SCOPE>/<WORK-TYPE>/...`

Recommended scopes include `CATALOG`, `ENGINE`, `PATH-SCHEMA`, `SCHEMAS`, `TOOLS`, and `TEST-INFRA`.

### TARGET

Any modified, modernized, localized, experimental, or reconstructed output.

`GEN-03/LEAFGREEN/TARGET/<PROJECT-ID>/<BASE-BUILD-ID>/<REVISION>/<WORK-TYPE>/...`

The project axis is mandatory so unrelated modifications never collide.

Examples:

`TARGET/MODERNIZED/BPGE-EN/REV-0/...`

`TARGET/MODERNIZED/BPGJ-JA/REV-0/...`

`TARGET/PAST-PARADOX-001-386/BPGE-EN/REV-0/...`

`TARGET/PAST-PARADOX-001-386/BPGJ-JA/REV-0/...`

## Sakurai work types

Sakurai owns research and reverse-engineering artifacts. Preferred work types are:

`ANALYSIS`, `CENSUS`, `STRUCTURE`, `TEXT`, `DATA`, `DIFFS`, `TOOLS`, `TESTS`, `VERIFICATION`, `REPORTS`, `LOCALIZATION`, `DISASSEMBLY`, `MANIFESTS`, `MAPS`, `SYMBOLS`.

Do not nest one work type under another when the artifact can be routed directly. For example, cross-build disassembly belongs under `COMPARE/.../DISASSEMBLY`, not `COMPARE/.../ANALYSIS/.../DISASSEMBLY`.

## Current legacy mapping

`GENERATION-III/LEAFGREEN/MULTI/REV-ALL/ANALYSIS/BANK-SURVEY-64K`

maps to the v3 ownership tree under:

`GEN-03/LEAFGREEN/COMPARE/ALL-BUILDS/ANALYSIS/BANK-SURVEY-64K`

with its nested disassembly content split to:

`GEN-03/LEAFGREEN/COMPARE/ALL-BUILDS/DISASSEMBLY/BANK-SURVEY-64K`

The ROM build manifest belongs under:

`GEN-03/LEAFGREEN/SHARED/CATALOG/MANIFESTS/source-builds.json`

## Migration policy

Move content; do not maintain duplicate live copies. Git history is the archive for legacy paths. Source ROM binaries remain outside GitHub and read-only. Every source-specific artifact must identify its source build and revision through its path and/or manifest metadata.
