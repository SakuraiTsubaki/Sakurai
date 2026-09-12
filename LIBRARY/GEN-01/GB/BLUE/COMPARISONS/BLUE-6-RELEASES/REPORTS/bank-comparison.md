# Pokémon Blue six-release comparison

Generated directly from the six supplied project ROM images. No ROM binaries are committed.

- `JP-JA-HV0`: 512 KiB, 32 × 16 KiB banks.
- `US-EU-EN-HV0`, `EU-DE-HV0`, `EU-FR-HV0`, `EU-IT-HV0`, `EU-ES-HV0`: 1 MiB, 64 × 16 KiB banks.
- All six images share exactly one byte-identical bank within the common 0x00–0x1F range: bank `1B`.
- The five western images share 20 byte-identical banks: `1B`, `2D`–`3F`.
- Per-release header and dump hashes are stored under each canonical release/dump manifest.
