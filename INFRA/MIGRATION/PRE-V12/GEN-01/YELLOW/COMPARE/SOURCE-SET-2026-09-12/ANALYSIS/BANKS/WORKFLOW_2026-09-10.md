# Pokémon Yellow/Pikachu — Bank-integrated survey + disassembly workflow

## Fixed completion rule

A bank is **not complete** merely because its role has been identified. A bank is complete only when all of the following are satisfied in the same pass:

1. 16 KiB bank byte inventory and hashes are recorded.
2. JP revisions and international variants are compared.
3. Code / pointer / text / graphics / audio / map / padding boundaries are classified.
4. Confirmed executable regions are promoted to symbolic LR35902/RGBDS-style assembly.
5. Unresolved or non-code regions remain byte-exact (`db`/raw) rather than being falsely decoded as instructions.
6. Recombining the bank reproduces the original bank bytes; ROM-level SHA-1 validation remains the final gate.

This means **survey and disassembly advance together bank-by-bank**.

## Current state

- All 9 unique ROMs × 64 banks already have Stage-0 byte-exact disassembly scaffolds.
- Stage-0 ROM reconstruction validation: **9/9 SHA-1 PASS**.
- Bank 00: semantic/symbolic pass underway; startup, interrupt vectors and bank-switch core are identified.
- Bank 01: semantic pass started in this cycle; module structure agrees at a high level between canonical EN and JP disassemblies, but actual byte layout differs heavily across regions.
- Remaining banks remain Stage-0 exact until their semantic pass begins.

## Pass order

The working order prioritizes executable cores first so their labels can resolve cross-bank calls in later data/map/text banks:

`00 → 01 → 03 → 0E → 0F → 10 → 1C → 3D → 3E → 3F → P1 banks → P2 banks`

No later bank is considered "survey-complete" without its simultaneous disassembly status being updated.
