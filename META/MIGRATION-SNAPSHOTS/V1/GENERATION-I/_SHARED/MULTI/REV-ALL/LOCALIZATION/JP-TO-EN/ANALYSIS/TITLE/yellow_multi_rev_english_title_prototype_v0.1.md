# Pocket Monsters Pikachu (Japan) → English Yellow title prototype v0.1

## Base rule

All four outputs are built from the supplied **Japanese Pocket Monsters Pikachu ROMs**.
The supplied English Pokémon Yellow ROM is used only as the implementation reference.

## Why Yellow needs a real port

Japanese Pikachu and English Yellow do not use the same title-logo layout.

Japanese:
- logo graphics: 0x600 bytes
- logo tilemap: 14 × 4
- separate `POCKET MONSTERS` row
- speech bubble: 7 × 3

English:
- main title graphics: 0x730 bytes
- corner graphics: 0x30 bytes
- logo tilemap: 16 × 7
- `Yellow Version` is integrated into that international title composition
- speech bubble: 7 × 4

Therefore a same-offset graphics overwrite would be invalid.

## Implementation

The original Japanese title routines remain in bank $29 but their three entry points are redirected to replacement routines stored in the bank-$29 tail.

Allocation:
- loader: file 0xA4E60 / CPU $4E60
- logo placement: file 0xA4EA0 / CPU $4EA0
- bubble placement: file 0xA4EB0 / CPU $4EB0
- 16×7 logo tilemap: 0xA4F00
- 7×4 bubble tilemap: 0xA4F70
- main English Yellow logo graphics: 0xA4F90
- three corner tiles: 0xA56C0

For Japanese revisions 0A/B/C, the disassembly documents 0xA4E60–0xA7FFF as the 12,704-byte `garbage_41.bin` tail.
The supplied Rev D ROM is zero-filled from 0xA4E60 through the end of bank $29.

The original Japanese Pikachu BG graphics, OBJ graphics, and Pikachu tilemap are retained. They are byte-for-byte identical to the supplied English Yellow equivalents.

## Validation

- All four source ROMs remain untouched.
- ROM size is unchanged.
- Header checksum is not altered.
- Global checksum is recalculated per output.
- Every IPS was reapplied to its clean Japanese source and reproduced the output ROM byte-for-byte.
- Runtime emulator validation is still required before calling the title implementation final.

No original ROM binary is stored in GitHub.
