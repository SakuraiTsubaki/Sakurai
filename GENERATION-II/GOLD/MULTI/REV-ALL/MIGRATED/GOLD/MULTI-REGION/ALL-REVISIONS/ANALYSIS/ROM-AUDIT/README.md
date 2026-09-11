# Pokémon Gold uploaded-ROM audit

Generated from the eight uploaded `.gbc` ROMs. Original ROM binaries are **not** included.

## Key findings

- 8 ROM images detected; all header and global checksums validate.
- Japanese Rev 0 / Rev A are 1 MiB (64 × 16 KiB banks).
- Korean / USA-Europe / German / French / Italian / Spanish ROMs are 2 MiB (128 × 16 KiB banks).
- Korean Gold reports CGB flag `0xC0` (CGB-only) and SGB flag `0x00`; the other seven report CGB flag `0x80`, and the Japanese/Western ROMs report SGB flag `0x03`.
- Japanese Rev 0 vs Rev A differ in 10,841 bytes across banks $00, $04, $05, $09, $0A, $0F, $14, $21, $23, $24.

## Files

- `audit_gold_roms.py` — reproducible scanner
- `rom_manifest.csv` — ROM-level header/checksum/hash manifest
- `bank_manifest.csv` — per-bank hashes/entropy/empty-bank flags
- `pairwise_bank_identity.csv` — same-index exact-bank comparison
- `japan_rev0_vs_reva_diff_runs.csv` — contiguous Rev 0 ↔ Rev A difference ranges
- `summary.json` — machine-readable summary

## Safety / provenance

The script reads `.gbc` files from the input directory and never modifies them. No copyrighted ROM binary is written to this analysis package.
