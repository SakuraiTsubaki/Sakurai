# Repository Structure v2

## Why v2 exists

The old fixed path `GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE` mixed three different ownership concepts: official source ROM builds, derived/target localizations, and cross-build research. That forced ambiguous buckets such as `MULTI/REV-ALL` and could place a target locale in the same structural role as an official source release.

v2 separates those concepts before the work-type layer.

## Canonical generation root

Use zero-padded numeric generation folders:

`GEN-01`, `GEN-02`, ... `GEN-10`, `GEN-11`.

This replaces Roman-numeral roots such as `GENERATION-I` and keeps lexical ordering correct as the project grows beyond Generation IX.

## Canonical game root

`GEN-XX/<GAME>/`

GAME is a stable uppercase slug such as `RED`, `GREEN`, `BLUE`, `YELLOW`, `GOLD`, `SILVER`, `CRYSTAL`, `FIRERED`, `LEAFGREEN`, or `LEGENDS-Z-A`.

`_SHARED` is allowed only for material genuinely owned by multiple games within one generation.

## Four ownership branches

Every game is divided by provenance/scope before locale or revision:

### SOURCE

Official source builds only.

`GEN-XX/<GAME>/SOURCE/<RELEASE-ID>/<REV>/<WORK-TYPE>/...`

`RELEASE-ID` describes the actual release/build identity, not a desired target language. Examples for Pokémon Red from the current source set:

- `JP-JA`
- `US-EU-EN`
- `EU-DE`
- `EU-FR`
- `EU-IT`
- `EU-ES`

Use explicit revision labels such as `REV-0`, `REV-A`, `REV-1`.

Do not upload original ROM binaries. Store ROM identity, hashes, header data, bank maps, and provenance in `MANIFESTS` / research files.

### TARGET

Derived outputs, modernization targets, fan/localization targets, rebuilds, and ports that do not represent an official source build.

`GEN-XX/<GAME>/TARGET/<TARGET-ID>/<BASE-ID>/<WORK-TYPE>/...`

Example: a Korean target derived from an English Red source belongs under `TARGET/KR-KO/...`, not under `SOURCE/KR-KO`.

### COMPARE

Artifacts whose subject is inherently multi-source or multi-revision.

`GEN-XX/<GAME>/COMPARE/<SCOPE>/<WORK-TYPE>/...`

Examples:

- `COMPARE/ALL-SOURCES/ANALYSIS/ROM-AUDIT/`
- `COMPARE/JP-JA-REVISIONS/DIFFS/`
- `COMPARE/LOCALIZATION-FAMILIES/DATA/`

This replaces the ambiguous `MULTI/REV-ALL` pattern.

### SHARED

Game-wide material that is not owned by one source release or one target.

`GEN-XX/<GAME>/SHARED/<SCOPE>/<WORK-TYPE>/...`

Examples include common schemas, generic tools, engine-wide symbol conventions, and reusable test infrastructure.

## Sakurai work types

Sakurai is the research / reverse-engineering / documentation repository. Canonical work types are:

`ANALYSIS`, `CENSUS`, `STRUCTURE`, `TEXT`, `DATA`, `DIFFS`, `TOOLS`, `TESTS`, `VERIFICATION`, `REPORTS`, `LOCALIZATION`, `DISASSEMBLY`, `MANIFESTS`, `MAPS`, `SYMBOLS`.

## Pokémon Red source routing confirmed from the current ROM set

The current source set resolves to these canonical homes:

- Japanese Rev 0 → `GEN-01/RED/SOURCE/JP-JA/REV-0/...`
- Japanese Rev A → `GEN-01/RED/SOURCE/JP-JA/REV-A/...`
- USA/Europe English Rev 0 → `GEN-01/RED/SOURCE/US-EU-EN/REV-0/...`
- German Rev 0 → `GEN-01/RED/SOURCE/EU-DE/REV-0/...`
- French Rev 0 → `GEN-01/RED/SOURCE/EU-FR/REV-0/...`
- Italian Rev 0 → `GEN-01/RED/SOURCE/EU-IT/REV-0/...`
- Spanish Rev 0 → `GEN-01/RED/SOURCE/EU-ES/REV-0/...`

The duplicate English ROM is one source identity and must be recorded as a duplicate/provenance observation, never as a separate structural release.

## Repository-wide infrastructure

The repository root may contain `.github`, `README.md`, `STRUCTURE.md`, `MIGRATION.md`, and `META/` in addition to canonical `GEN-XX` roots.

`META/` is reserved for repository-wide catalogs, migration indexes, schemas, and validation metadata. Project artifacts still belong under `GEN-XX`.

## Migration rule

Roman generation roots and the old five-level tree are legacy paths. During migration they may remain temporarily, but no new work should be added there. Current content must be moved to the narrowest truthful `SOURCE`, `TARGET`, `COMPARE`, or `SHARED` owner. Git history preserves old paths; do not keep duplicate live copies only for compatibility.
