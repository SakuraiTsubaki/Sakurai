# RBY ENGLISH → Japanese RGBY Title Status

## Base-ROM rule

All working ROMs are Japanese originals. English Red/Blue/Yellow are implementation references only. Original ROM binaries are not stored in GitHub.

## Current valid title work

- Red Rev 0 — corrected v0.2
- Red Rev A — corrected v0.2
- Green Rev 0 — corrected v0.2
- Green Rev A — corrected v0.2
- Blue Rev 0 — prototype v0.1
- Pikachu Rev 0A — English Yellow title prototype v0.1
- Pikachu Rev B — English Yellow title prototype v0.1
- Pikachu Rev C — English Yellow title prototype v0.1
- Pikachu Rev D — English Yellow title prototype v0.1

All current IPS files are stored in the matching Tsubaki `PATCHES/TITLE` directory.

## Invalid legacy work

The original Red v0.1 and Green v0.1 title prototypes are invalid because they assumed the English Pokémon logo was stored at the Japanese ROM file offset `0x10419`. The verified English source offset is `0x11380` (ROM address `04:5380`).

Do not use the old v0.1 Red/Green patch files. Use the corrected v0.2 patches instead.

## Validation status

- IPS reapply / byte-for-byte reconstruction: passed for current patches
- ROM size preservation: passed
- checksum recalculation: completed
- emulator/runtime title-screen validation: still required before final release status
