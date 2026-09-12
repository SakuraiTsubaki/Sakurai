# Pokémon Red multi-region full-bank disassembly scaffold

Generated from the seven unique uploaded ROM images; the duplicate English copy is omitted.

## Completed
- 384 total 16 KiB banks covered (JP 32+32; EN/DE/FR/IT/ES 64 each).
- Every byte represented locally in RGBDS-compatible `db` source under `<rom>/banks/`.
- Linear LR35902 decode comments attached to instruction-sized chunks.
- `$0104-$014F` Game Boy header forced to data so Bank 00 decoding resumes at `$0150`.
- Every generated source tree reconstructed from its `db` directives and matched its original ROM byte-for-byte.
- Bank hashes/statistics, pairwise similarity, international commonality and direct CALL/JP candidate tables generated.

## Semantics
This is a lossless whole-ROM disassembly scaffold. Linear decoding cannot distinguish mixed code/data by itself, so `db` bytes are authoritative and comments are hints. Semantic conversion should replace these blocks with real instructions, labels, pointer tables, scripts, text, maps, graphics and audio while retaining hash verification.

Exact semantic split-disassembly baselines are known for JP Rev0/RevA, EN, DE, FR and ES. Italian is the uploaded build for which no exact complete public split-disassembly baseline was located in this pass.

## Suggested bank conversion order
1. Bank 00 — vectors/header/home/interrupts.
2. Banks 01-1F — engine/audio/maps/graphics.
3. International 20-2C — text/Pokedex/move names.
4. 2D-3F — prove free-space status and cross-reference safety.
5. Italian — structural label transfer from EN/DE/FR/ES followed by Italian-only resolution.
6. Hash verification after every converted bank.

## GitHub publication boundary
The generated `banks/*.asm`, `listings/*.csv`, and full archives are intentionally kept out of the repository because the byte-exact scaffold is sufficient to reconstruct the copyrighted ROM images. GitHub receives only hashes, derived statistics, methodology and semantic annotations that do not reproduce the ROM payload.
