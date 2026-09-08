# Pokémon Gold reproducibility corpus snapshot

Current local/exported corpus contains **138 distributable work files** and no ROM binaries.

- ZIP SHA-256: `d4cac9a6af649f35034b32d50807273d857630299bbc4785f9a574cd1a77c18d`
- Coverage: KR REV-0, JP REV-0, JP REV-A, USA-EUROPE REV-0, DE REV-0, FR REV-0, IT REV-0, ES REV-0
- Determinism check: complete corpus regenerated twice from the same eight ROM inputs with identical path sets and **0 file SHA-256 mismatches**.
- Generated source scaffolds: 8 `.asm`, 8 `.inc`, 8 `.sym`, 8 layout maps.
- Original `.gbc`, generated `.bin`, and byte-for-byte ROM-derived binary payloads are excluded from GitHub.

Use `tools/build_gold_repro_corpus.py` with the ROMs identified in `manifests/rom_inventory.csv` to regenerate the full working corpus.
