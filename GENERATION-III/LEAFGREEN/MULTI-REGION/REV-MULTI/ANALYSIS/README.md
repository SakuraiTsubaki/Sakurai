# Pokémon LeafGreen — full-ROM reproducibility analysis

This directory contains **metadata and reproducible analysis outputs only**. The seven original `.gba` files are input material and are intentionally not committed.

## Contents

- `ROM_SET.json` — canonical machine-readable identity for all seven source ROMs.
- `HEADERS.csv` — GBA header fields, checksums, revision bytes, and cryptographic hashes.
- `BLOCKS_1M.csv` — 1 MiB full-ROM block hashes plus entropy / padding statistics.
- Per-ROM 64 KiB fingerprints are generated deterministically by the matching Tsubaki tooling; precomputed copies are included in the downloadable reproducibility export.
- `PAIRWISE_DIFF.csv` — pairwise full-ROM difference totals.
- `PAIRWISE_BLOCK_DIFF_1M.csv` — pairwise difference density by 1 MiB region.
- `POINTER_DENSITY_1M.csv` — aligned 32-bit GBA ROM-pointer density by region.
- `REPRODUCIBILITY_SCOPE.md` — what “complete reproducible work material” means in this project.

The matching extractor / verifier / split / rebuild tooling lives in the Tsubaki repository at the same hierarchy under `TOOLING`.
