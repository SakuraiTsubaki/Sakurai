# Pokémon Gold — multi-region analysis

This directory contains reproducible analysis artifacts for the uploaded Pokémon Gold ROM set.

## Source set (ROM files are not stored here)

- Pocket Monsters Kin (Japan), Rev 0
- Pocket Monsters Kin (Japan), Rev A
- Pokémon Gold Version (USA/Europe)
- Pokémon Goldene Edition (Germany)
- Pokémon Version Or (France)
- Pokémon Versione Oro (Italy)
- Pokémon Edición Oro (Spain)
- Pocket Monsters Geum (Korea)

## Repository policy

- **Never commit original ROM images.**
- Commit analysis reports, inventories, hashes, tools/scripts, provenance ledgers, patches, and other non-ROM outputs.
- Every derived result must be reproducible from the local source ROMs and the tools in this directory.
- Hashes identify source images without redistributing copyrighted ROM data.

## Current baseline

The 2026-09-05 census validates all eight ROM header/global checksums, records cryptographic hashes and cartridge metadata, fingerprints 16 KiB banks, and localizes the Japanese Rev 0 → Rev A binary delta.
