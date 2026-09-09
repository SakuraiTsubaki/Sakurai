# LeafGreen Bank Survey + Disassembly Policy

Each 64 KiB analysis bank (`0x10000` bytes) is surveyed and disassembled in the same pass.

For every ROM and every bank `00`–`FF`, record:

1. Bank hashes / entropy / fill ranges.
2. Confirmed and candidate ROM pointers.
3. Candidate Thumb entry points from pointers with bit 0 set.
4. ARM entry points and mode-switch stubs where identified.
5. Recursive control-flow targets (BL/B/BX) as they are confirmed.
6. Literal pools and pointer tables separated from executable code.
7. Event scripts, text, compressed graphics/data, audio and other non-code regions separated from executable code.
8. Cross-version relocation/equivalence mapping so identical code/data are not independently misclassified.
9. Confidence per region (`confirmed`, `probable`, `candidate`, `data`, `fill`).
10. No ROM binaries are committed.

## Address convention

File offset `0x000000` corresponds to GBA ROM address `0x08000000`.
Analysis bank N covers file offsets `N*0x10000 .. N*0x10000+0xFFFF`, or ROM addresses `0x08000000 + N*0x10000 .. +0xFFFF`.

## Important

A linear disassembly of all bytes is not treated as valid disassembly. ARM/Thumb decoding is emitted only for regions reached from known/candidate entry points or independently validated as executable; literal pools and embedded data are carved out as the map improves.
