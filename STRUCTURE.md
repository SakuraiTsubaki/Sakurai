# Repository Structure v2 — Source-ROM Ownership Model

## Why v2 exists

The old fixed path `GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE` mixed three different ownership concepts: official source ROM builds, derived/target localizations, and cross-build research. That could make a target locale look like an official source release and forced shared English binaries into artificial regional buckets.

V2 separates provenance before the work-type layer.

## Canonical generation root

Use zero-padded numeric generation folders:

`GEN-01`, `GEN-02`, ... `GEN-10`, `GEN-11`.

Roman-numeral roots such as `GENERATION-I` are legacy. Numeric roots sort correctly and remain future-proof beyond Generation IX.

## Canonical game root

`GEN-XX/<GAME>/`

GAME is a stable uppercase slug such as `RED`, `GREEN`, `BLUE`, `YELLOW`, `GOLD`, `SILVER`, `CRYSTAL`, `FIRERED`, `LEAFGREEN`, or `LEGENDS-Z-A`.

`_SHARED` is allowed only for material genuinely owned by multiple games within one generation.

## Four ownership branches

### SOURCE

Official source builds only:

`GEN-XX/<GAME>/SOURCE/<RELEASE-ID>/<REV>/<WORK-TYPE>/...`

`RELEASE-ID` describes the actual release/build identity, not a desired target language. Examples include `JP-JA`, `KR-KO`, `US-EU-EN`, `EU-DE`, `EU-FR`, `EU-IT`, and `EU-ES`.

Revision labels preserve the verified release label. Valid examples include `REV-0`, `REV-A`, `REV-0A`, `REV-B`, `REV-C`, `REV-D`, numeric revisions, and `REV-ALL` where an aggregate is intentional. When the Game Boy header revision byte differs from the human release label, record both in the manifest.

Original ROM binaries are never uploaded. Store identity, hashes, header data, bank maps, provenance, decoded data, disassembly, tests, and tools only.

### TARGET

Derived outputs, modernization targets, translations, rebuilds, and ports:

`GEN-XX/<GAME>/TARGET/<TARGET-ID>/<BASE-ID>/<WORK-TYPE>/...`

`TARGET-ID` identifies the produced target, such as `KR-KO`.

`BASE-ID` identifies the actual source lineage and revision, for example:

- `JP-JA-REV-0`
- `JP-JA-REV-A`
- `US-EU-EN-REV-0`
- `US-EU-EN-REV-A`

A Korean Crystal output therefore belongs under `TARGET/KR-KO/<BASE-ID>/...`; it must not create `SOURCE/KR-KO` unless an actual Korean Crystal source ROM exists.

Additional technical/reference ROMs that are not the owning base ROM belong in provenance manifests. For this project, Korean Gold/Silver can be implementation references for Hangul while a Japanese or English ROM remains the owning base source.

### COMPARE

Artifacts whose subject is inherently multi-source or multi-revision:

`GEN-XX/<GAME>/COMPARE/<SCOPE>/<WORK-TYPE>/...`

Examples:

- `COMPARE/ALL-SOURCES/ANALYSIS/...`
- `COMPARE/JP-JA-REVISIONS/DIFFS/...`
- `COMPARE/LOCALIZATION-FAMILIES/DATA/...`

This replaces ambiguous `MULTI/REV-ALL` ownership where the artifact is truly comparative.

### SHARED

Game-wide material that is not owned by one source release or target:

`GEN-XX/<GAME>/SHARED/<SCOPE>/<WORK-TYPE>/...`

Use this for common schemas, generic tools, engine-wide symbol conventions, reusable tests, and other release-independent material.

## Sakurai work types

`ANALYSIS`, `CENSUS`, `STRUCTURE`, `TEXT`, `DATA`, `DIFFS`, `TOOLS`, `TESTS`, `VERIFICATION`, `REPORTS`, `LOCALIZATION`, `DISASSEMBLY`, `MANIFESTS`, `MAPS`, `SYMBOLS`.

## Verified Gen I / Gen II source set

The 23 supplied ROMs are mapped one-by-one in `META/SOURCE-ROM-CATALOG.md`.

Important routing facts established by that catalog:

- Shared USA/Europe English binaries use `US-EU-EN` as one source identity.
- Actual Korean source ROMs in the supplied set are Gold and Silver only.
- There is no Korean Crystal source ROM in the supplied set.
- Japanese Yellow has four supplied source revisions: `REV-0A`, `REV-B`, `REV-C`, and `REV-D`.
- Gold/Silver Japanese revisions and English Crystal revisions are kept distinct rather than collapsed into a generic revision bucket.

## Repository-wide infrastructure

The repository root may contain `.github`, `README.md`, `STRUCTURE.md`, `MIGRATION.md`, and `META/` in addition to canonical `GEN-XX` roots.

`META/` is reserved for repository-wide catalogs, migration indexes, schemas, and validation metadata. Project artifacts still belong under `GEN-XX`.

## Migration rule

Roman generation roots and the old five-level tree are legacy paths. During migration they may remain temporarily, but no new work should be added there. Current content must be moved to the narrowest truthful `SOURCE`, `TARGET`, `COMPARE`, or `SHARED` owner. Git history preserves old paths; do not keep duplicate live copies only for compatibility.
