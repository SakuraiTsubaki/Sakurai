# Pokémon Yellow / Pocket Monsters Pikachu — v5 canonical routing

The supplied set contains 14 filenames representing 9 unique byte images and 9 release identities. Filename extensions and preservation display names are observations, not release owners.

## Source ownership

Japanese Pikachu releases have CGB flag `0x00` and use the GB execution profile:

`LIBRARY/GEN-01/YELLOW/SOURCE/GB/CART/<RELEASE-ID>/`

International Yellow releases have CGB flag `0x80` and use the dual-mode GBC execution profile:

`LIBRARY/GEN-01/YELLOW/SOURCE/GBC/CART/<RELEASE-ID>/`

Each exact supplied image is a dump observation below its release:

`.../DUMPS/USER-UPLOAD-<SHA1-8>/`

The `.gb`/`.gbc` filename pairs for EN/DE/ES/FR/IT are byte-identical aliases and do not create extra releases or dumps.

## Cross-release ownership

`LIBRARY/GEN-01/YELLOW/COMPARE/SOURCE-SET-2026-09-12/` owns multi-release evidence: ROM inventory, filename alias deduplication, header matrix, bank identity matrices, semantic bank passes, cross-release disassembly, symbol transfer, and verification.

`LIBRARY/GEN-01/YELLOW/SHARED/` is only for release-independent parsers and reusable format tooling.

Derived modernization/localization work belongs under `PROJECTS/YELLOW-MODERNIZATION/`.

## Fixed release / dump identities

- JP-JA-HV0 -> USER-UPLOAD-1fb6c264 (GB)
- JP-JA-HV1 -> USER-UPLOAD-28e4b853 (GB)
- JP-JA-HV2 -> USER-UPLOAD-91864ecd (GB)
- JP-JA-HV3 -> USER-UPLOAD-a40298a8 (GB)
- US-EU-EN-HV0 -> USER-UPLOAD-cc7d0326 (GBC)
- EU-DE-HV0 -> USER-UPLOAD-42f3714e (GBC)
- EU-ES-HV0 -> USER-UPLOAD-1dc24203 (GBC)
- EU-FR-HV0 -> USER-UPLOAD-0aceec0e (GBC)
- EU-IT-HV0 -> USER-UPLOAD-05bb8e99 (GBC)

New canonical paths must not use `MULTI`, `REV-ALL`, `ALL`, `MULTI-REGION`, `_SHARED`, `MISC`, `OTHER`, `GENERAL`, or `REV-UNKNOWN`.

Original ROM binaries remain local/read-only and are never committed.
