# Pokémon Silver full-ROM reproducibility layer

This directory is the canonical ROM-free reproducibility entry point for the eight Silver targets: JP Rev0, JP RevA, USA/Europe, DE, FR, IT, ES, and KR.

`generate_silver_reproducibility.py` identifies source ROMs by SHA-256 rather than filename and deterministically generates per-target material under `GENERATION-II/SILVER/<LANGUAGE-REGION>/<REV>/reproducibility/`.

Generated material includes `manifest.json`, `header.json`, `expected.sha256`, whole-ROM `banks.csv`, `fill_runs_ge64.csv`, an RGBDS physical-bank `layout.asm`, `verify_rom.py`, `reproduce.py`, `Makefile`, `.gitignore`, and README files. Cross-version output includes the eight-ROM manifest, pairwise byte/bank comparison, bank-equivalence groups, Japanese revision diff ranges, and common full-zero-bank candidates.

The source ROMs, split bank binaries, and rebuilt ROMs are never committed. Every target was tested by SHA verification, 16 KiB bank split, deterministic rejoin, and SHA verification of the rejoined image; all eight passed byte-exactly.
