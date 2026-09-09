# Gold multi-region full-ROM disassembly scaffold

Eight uploaded Pokémon Gold ROMs were surveyed bank-by-bank. Original ROM binaries and byte-exact ROM-reconstructing bank ASM are not stored in this public repository.

## Current state

- 8 ROMs / 896 total 16 KiB banks surveyed.
- A private working scaffold represents every ROM byte in per-bank RGBDS ASM and reconstructs all eight inputs byte-for-byte.
- Public repository material is limited to reproducible tooling, hashes, structural notes, and non-reconstructing analysis.
- English uploaded Gold exactly matches the documented `pret/pokegold` Gold build SHA-1.
- Japanese Rev 0 / Rev A exactly match `Narishma-gb/pokesilver` documented build targets.
- Korean Gold exactly matches `Narishma-gb/pokegold-kr` documented build target.
- German/French/Italian/Spanish are being mapped from the English semantic source plus binary localization deltas.

## Semantic order

1. Bank $00 vectors/header/home.
2. Code-heavy banks and battle engine.
3. Pointer tables / compressed graphics.
4. Maps/events and scripts.
5. Text, Pokédex, names, descriptions.
6. Audio.
7. Korean-specific expansion banks and unresolved localization banks.
