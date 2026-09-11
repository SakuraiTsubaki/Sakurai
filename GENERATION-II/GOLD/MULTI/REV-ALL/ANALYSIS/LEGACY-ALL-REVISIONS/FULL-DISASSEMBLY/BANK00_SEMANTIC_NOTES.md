# Bank $00 semantic notes — first pass

All addresses are CPU ROM0 addresses and were checked directly against the eight uploaded ROMs.

## Shared core

- `$0000`: `di ; jp $0100` in all eight ROMs.
- `$0010`: shared bank-switch helper pattern `ldh [$FF9F], a ; ld [$2000], a ; ret`.
- `$0028`: shared indexed 16-bit jump-table helper ending in `jp hl`.
- `$0040`: VBlank vector `jp $0150` in all eight.
- `$0048`: LCD vector `jp $041B` in all eight.
- `$0050`: timer vector is `reti` in all eight.
- `$0150`: Home prologue begins identically in all eight.

## Region-sensitive vectors

- Japanese Rev 0 and Rev A are effectively the same in the vector/header entry area; their Bank $00 full-bank images differ by one byte elsewhere.
- English/German/French/Italian/Spanish share the same vector design, with localization-dependent RST08 and later Bank $00 targets shifted.
- Korean differs structurally at RST18/RST20/RST38. Instead of the `$FF` trap/filler pattern used by Japanese/western ROMs, Korean contains executable wait/delay-style routines. Serial/Joypad and header-entry targets also shift.

## Entry targets

- English/western baseline header entry uses `jp $05C6` (German/French/Italian/Spanish use the same entry target in the sampled header bytes).
- Japanese uses `jp $05C5`.
- Korean uses `jp $05CA`.
- Serial vector target: western `$06AA`, Japanese `$06A9`, Korean `$0698`.
- Joypad vector target: western `$08DF`, Japanese `$08DE`, Korean `$08D2`.

These differences make Bank $00 the first semantic anchor for cross-region symbol mapping.
