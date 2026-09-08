# Pokémon Blue/Ao full-ROM reproducibility corpus

This corpus covers the six exact user-supplied Blue/Ao ROMs: Japanese, English USA/Europe, German, French, Italian, and Spanish.

The ROM binaries are never committed. `generate_blue_reproducibility.py` matches local inputs by SHA-256 and regenerates the physical-bank corpus under the required hierarchy:

`GENERATION-I → BLUE → LANGUAGE/REGION → REV-0 → ANALYSIS → reproducibility`

Generated material includes ROM/header identities, per-bank SHA-256/CRC32/entropy/fill statistics, 0x00/0xFF fill-run candidates, byte-exact RGBDS INCBIN bank scaffolds, pairwise per-bank byte differences, identical-bank groups, long shared-byte runs, and free-space summaries.

The baseline round-trip test splits each ROM into 16 KiB banks, rejoins them in bank order, and requires exact SHA-256 equality. All six source ROMs passed byte-for-byte round-trip verification in the working package.

Important: partial 0x00/0xFF runs are candidates, not automatically safe free space. Entire blank banks are high-confidence physical free-space candidates, but semantic reference analysis remains required before repurposing any region.
