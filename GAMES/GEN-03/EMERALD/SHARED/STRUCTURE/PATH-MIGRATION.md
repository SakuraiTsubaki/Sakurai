# Emerald v3 path migration

## Verified source set

The supplied Emerald ROM set contains seven filenames but six unique byte identities. Canonical release IDs are:

- `GBA-JP-JA-BPEJ-REV-0`
- `GBA-US-EU-EN-BPEE-REV-0`
- `GBA-EU-DE-BPED-REV-0`
- `GBA-EU-FR-BPEF-REV-0`
- `GBA-EU-IT-BPEI-REV-0`
- `GBA-EU-ES-BPES-REV-0`

The two supplied English filenames are exact duplicates and share one release tree.

## Canonical release roots

`GAMES/GEN-03/EMERALD/RELEASES/<RELEASE-ID>/...`

Each release has `MANIFESTS/release.json` containing header identity, size, hashes, and supplied filename provenance. Original ROM binaries remain outside GitHub.

## Cross-release research

Legacy:

`GENERATION-III/EMERALD/MULTI/REV-ALL/...`

Canonical:

`GAMES/GEN-03/EMERALD/COMPARISONS/GBA-REV-0-LOCALIZATION-SET/...`

The comparison manifest explicitly lists the six member release IDs. `MULTI` and `REV-ALL` are no longer semantic owners.

## Work-type routing

- Bank-census summaries -> `ANALYSIS/BANK-CENSUS/`
- Bank-census scripts -> `TOOLS/BANK-CENSUS/`
- Disassembly reports/evidence -> `DISASSEMBLY/BANK-CENSUS/`
- Disassembly scripts -> `TOOLS/DISASSEMBLY/`

## Derived production rule

Patches, modernization, localization, and rebuild outputs belong under:

`GAMES/GEN-03/EMERALD/PROJECTS/<PROJECT-ID>/COMMON/...`
`GAMES/GEN-03/EMERALD/PROJECTS/<PROJECT-ID>/TARGETS/<TARGET-ID>/...`

They must not be placed under `RELEASES`, even when the output language matches its source ROM. The project/target manifest records the exact base release ID(s).
