# FireRed National Dex Expansion

Generation III / Pokémon FireRed engine expansion project.

## Current targets

- National Dex Species: **1025** currently, with **1–4095 reserved** for future base species.
- Pokémon varieties reference set: **1351** current PokéAPI Pokémon records.
- Pokémon Form records reference set: **1579** current form-layer records.
- Base Species ID rule: `SPECIES_* == National Dex number` for IDs 1–4095.
- Gameplay-variety range: `0x1000–0x1FFF` (4096–8191).
- `SPECIES_EGG = 0xFFFE`, `SPECIES_INVALID = 0xFFFF`.
- Form IDs are independent `u16` IDs.

## Stock FireRed findings

Stock FRLG stores species IDs as `u16` in Pokémon, battle Pokémon and trainer party records, so the stock 412-species count is not the fundamental identifier-width limit.

The major stock engine bottlenecks found so far are:

1. Ability IDs are `u8`, and stored Pokémon only choose between two ability slots.
2. Base EXP yield is `u8`.
3. Evolution data is fixed at five evolution records per species.
4. Packed level-up learnsets allocate only 9 bits to move IDs (max 511), with a stock constant of 20 level-up moves.
5. Pokédex Seen/Owned flags are sized for the stock species count.
6. Forms are special-cased rather than represented by a general form/variety system.

## Save strategy

The stock `SaveBlock2` contains a 0x400-byte unused filler region. A 4095-entry Pokédex requires 512 bytes each for Seen and Owned. Retaining the stock 52-byte arrays and storing only the extensions needs 460 × 2 = **920 bytes**, leaving **104 bytes** of that filler unused. This allows a 4095-entry Seen/Caught cap without enlarging `SaveBlock2`.

## ROM policy

No copyrighted ROM binaries are committed. The repository contains analysis, hashes/manifests, source, generated tables and patch/build material only.

See:

- `analysis/original-engine-limits.md`
- `data/architecture.json`
- `data/rom_manifest.json`
