# Repository Migration — V1 → Source-ROM Path V2

## Why V1 is being replaced

V1 used:

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

That model mixed three different concepts in one axis: actual source ROM release, target/output locale, and cross-source work. It also forced shared USA/Europe English binaries into artificial `US-EN` versus `EU-EN` choices.

## V2 ownership model

Generation roots use zero-padded numeric IDs: `GEN-01`, `GEN-02`, ...

Each game has four ownership branches:

- `SOURCE/<RELEASE-ID>/<REV>/<WORK-TYPE>`
- `TARGET/<TARGET-ID>/<BASE-ID>/<WORK-TYPE>`
- `COMPARE/<SCOPE>/<WORK-TYPE>`
- `SHARED/<SCOPE>/<WORK-TYPE>`

Examples:

- `GEN-01/RED/SOURCE/JP-JA/REV-A/MANIFESTS/...`
- `GEN-01/RED/SOURCE/US-EU-EN/REV-0/TEXT/...`
- `GEN-01/RED/TARGET/KR-KO/JP-JA-REV-0/LOCALIZATION/...`
- `GEN-02/CRYSTAL/TARGET/KR-KO/US-EU-EN-REV-A/TEXT/...`

## Source identity rules

1. `SOURCE` means an actual official source build exists.
2. `TARGET` means a derived build/output; target locale is not proof of an official source ROM.
3. `US-EU-EN` is a single release ID for the supplied shared USA/Europe English ROMs.
4. The supplied Korean source ROMs are Gold and Silver only; Korean Crystal must therefore be routed under `TARGET/KR-KO`, not `SOURCE/KR-KO`.
5. Japanese Yellow keeps exact source labels `REV-0A`, `REV-B`, `REV-C`, `REV-D`; the header revision byte is metadata, not the directory name.
6. `BASE-ID` must identify the source lineage, for example `JP-JA-REV-0`, `JP-JA-REV-A`, or `US-EU-EN-REV-0`.
7. Cross-release/revision artifacts belong in `COMPARE`; release-independent game-wide infrastructure belongs in `SHARED`.
8. Extra technical references, such as Korean Gold/Silver being used to implement Hangul in another game's target, belong in provenance manifests rather than pretending to be that game's source ROM.

## Migration policy

Roman `GENERATION-*` roots are legacy and may remain temporarily while files are moved. New work must use V2. Existing artifacts are moved to the narrowest truthful V2 owner; duplicate live copies are not kept solely for old paths. Git history preserves historical locations.

The verified 23-ROM mapping is recorded in `META/SOURCE-ROM-CATALOG.md`.

ROM binaries are never committed.
