# Repository Migration — v2

## Status

v2 path migration is active.

The previous canonical model `GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE` is now legacy because it cannot distinguish official source releases, derived target builds, cross-release research, and game-wide shared material without ambiguous `MULTI/REV-ALL` buckets.

## New root

Roman generation folders migrate to zero-padded numeric folders:

- `GENERATION-I` → `GEN-01`
- `GENERATION-II` → `GEN-02`
- ...
- `GENERATION-IX` → `GEN-09`
- future generations use `GEN-10`, `GEN-11`, etc.

## New ownership routing

Each game moves into one of four branches:

- `SOURCE/<RELEASE-ID>/<REV>/<WORK-TYPE>` — official source builds only
- `TARGET/<TARGET-ID>/<BASE-ID>/<WORK-TYPE>` — derived/localized/modernized targets
- `COMPARE/<SCOPE>/<WORK-TYPE>` — inherently multi-source or multi-revision work
- `SHARED/<SCOPE>/<WORK-TYPE>` — release-independent game-wide material

## Pokémon Red first migration target

The uploaded/source-audited Red ROM set resolves to seven unique source identities:

1. `SOURCE/JP-JA/REV-0`
2. `SOURCE/JP-JA/REV-A`
3. `SOURCE/US-EU-EN/REV-0`
4. `SOURCE/EU-DE/REV-0`
5. `SOURCE/EU-FR/REV-0`
6. `SOURCE/EU-IT/REV-0`
7. `SOURCE/EU-ES/REV-0`

The second English file is byte-identical to the first and is provenance only, not an eighth source path.

Current `GENERATION-I/RED/MULTI/REV-ALL/ANALYSIS/ROM-AUDIT` maps to `GEN-01/RED/COMPARE/ALL-SOURCES/ANALYSIS/ROM-AUDIT`.

Current cross-ROM disassembly pipeline material maps to the appropriate `COMPARE/ALL-SOURCES/DISASSEMBLY`, `COMPARE/ALL-SOURCES/TOOLS`, `COMPARE/ALL-SOURCES/REPORTS`, or `COMPARE/ALL-SOURCES/MANIFESTS` owner instead of keeping nested work-type replicas.

## Migration behavior

Legacy `GENERATION-*` roots are temporarily tolerated by the validator and reported as migration warnings. New work must use v2 paths. Migration must move content rather than keep duplicate live copies. Git history remains the archive for old paths.
