# Pokémon Yellow / Pocket Monsters Pikachu — canonical routing

This game uses Repository Structure v4.1 routing. The 14 supplied filenames represent 9 unique byte images and 9 release identities. Filename extensions and preservation-style display names are observations, not directory identity.

## Sakurai ownership

`LIBRARY/GEN-01/GB/YELLOW/RELEASES/<RELEASE-ID>/` owns official-build identity, header facts, release manifests, exact supplied dump observations, reverse engineering, and release-specific research.

`LIBRARY/GEN-01/GB/YELLOW/COMPARISONS/SOURCE-SET-2026-09-12/` owns facts that require two or more Yellow releases: filename deduplication, bank identity matrices, cross-release semantic passes, cross-release disassembly transfer, and verification.

`LIBRARY/GEN-01/GB/YELLOW/SHARED/` owns only release-independent parsers, schemas, and terminology. It must not be used as a substitute for an unknown release owner.

`PROJECTS/YELLOW-MODERNIZATION/` owns project research/design that transforms the source releases. It references release IDs; it does not copy ROM binaries.

## Tsubaki ownership

Production output is project-owned: `PROJECTS/YELLOW-MODERNIZATION/IMPLEMENTATION/<TARGET-ID>/...`. Tsubaki source-lock manifests reference the Sakurai release IDs and hashes. Tsubaki does not create a fake `KR-KO` official Yellow release for a project localization.

## Fixed source IDs

- `JP-JA-HV0` — Japan header version 0 / preservation label Rev 0A
- `JP-JA-HV1` — Japan header version 1 / Rev B
- `JP-JA-HV2` — Japan header version 2 / Rev C
- `JP-JA-HV3` — Japan header version 3 / Rev D
- `US-EU-EN-HV0` — English USA/Europe header version 0
- `EU-DE-HV0` — German header version 0
- `EU-FR-HV0` — French header version 0
- `EU-IT-HV0` — Italian header version 0
- `EU-ES-HV0` — Spanish header version 0

## Forbidden ownership shortcuts

Do not create new canonical paths containing `MULTI`, `REV-ALL`, `ALL-RELEASES`, or `MULTI-REGION`. Do not split identical `.gb`/`.gbc` filename aliases into separate releases. CGB/SGB flags, mapper type, filename, and file extension are manifest fields rather than path dimensions.

Original ROM binaries remain local/read-only and are never committed.
