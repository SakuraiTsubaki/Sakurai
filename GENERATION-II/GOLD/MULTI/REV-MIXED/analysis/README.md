# Pokémon Gold multi-ROM reproducibility corpus

This corpus covers the eight supplied Pokémon Gold ROM variants: KR, JP REV-0, JP REV-A, USA/EUROPE, DE, FR, IT, and ES.

It deliberately **does not contain ROM bytes**. Instead it contains enough deterministic metadata and tooling to identify the exact local source ROMs, regenerate bank/chunk maps, compare revisions/localizations, locate blank banks, and verify that future analysis is being performed against the same inputs.

## Included

- ROM inventory with MD5/SHA-1/SHA-256/CRC32
- Game Boy cartridge/header metadata and checksum verification
- 16 KiB bank maps with hashes, entropy, fill statistics, and longest 00/FF runs
- 4 KiB chunk SHA-256 maps for fine-grained change localization
- Full byte-frequency tables
- Blank-bank reports
- Pairwise ROM similarity tables
- Cross-ROM bank hash matrix and identical-bank groups
- Exact JP REV-0 vs REV-A contiguous diff ranges
- Deterministic generator and verifier scripts
- Per-ROM byte-exact RGBDS rebuild scaffolds (`.asm`, `.inc`, `.sym`, layout map) using local `source.gbc` via `INCBIN`
- Local-only bank splitter (generated `.bin` files are ignored and must never be committed)
- Corpus-wide SHA-256 manifest for generated work files

## Repository rule

Original ROMs and byte-for-byte ROM-derived binary assets are excluded. To reproduce the corpus, provide the exact local ROMs whose hashes appear in `manifests/rom_inventory.csv`.
