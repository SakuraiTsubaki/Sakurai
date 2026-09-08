# Pokémon Gold Complete Reproducibility Workset

This tree combines every reproducible work product generated for the eight verified Pokémon Gold ROMs in this project. The source ROM images are external, read-only inputs and are not included.

## Layers

- **Phase 0 — physical corpus:** ROM identity, checksums, bank maps, 4 KiB chunk hashes, byte frequencies, blank-bank inventory, exact whole-bank RGBDS `INCBIN` scaffolds, cross-version comparisons, and generators/verifiers.
- **Phase 1 — structural survey:** fixed Bank 00 CFG, stable/ROM-local symbols, entropy, long fill runs, pointer/address candidates, and cross-version Bank 00 comparisons.
- **Phase 2 — fixed-bank alignment:** normalized basic-block families and Korean ↔ international structural equivalence evidence.
- **Phase 3 — full-ROM atlas:** every byte in all 896 banks covered by an explicit segment contract, every-bank features, pointer/far-pointer windows, 256-byte page hashes, cross-version bank correspondence evidence, and segmented RGBDS rebuild scaffolds.

Each phase ships its generator and verifier. `tools/build_complete_workset.py` orchestrates all four layers when runtime permits.
