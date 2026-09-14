# Japanese Bank 00 — sprite decompression engine

This range begins immediately after `PickUpItemText` and ends immediately before `ResetPlayerSpriteData`.

## ROM-verified ranges

| Build | Range | Size | SHA-1 | Next routine |
|---|---:|---:|---|---|
| V1.0 | `$0FCE-$136A` | 925 bytes | `a127c4dc6a33d2d7468a4397af87685ba26c1010` | `ResetPlayerSpriteData` at `$136B` |
| V1.1 | `$0FBC-$1358` | 925 bytes | `81226620765494ee6a124ab609821a55b5b77489` | `ResetPlayerSpriteData` at `$1359` |

The two blocks have identical logical structure and identical length. An aligned byte comparison finds 44 differing bytes. Every difference is an address operand produced by the `$12` ROM0 relocation in V1.1 or by another ROM0 target that is itself `$12` earlier (for example `FillMemoryAddr`). No algorithm/data-table change was found.

## Recovered engine

`home/jp_uncompress.asm` reconstructs:

- `UncompressSpriteData` bank/RAM setup wrapper
- `_UncompressSpriteData` state initialization
- bit-stream reader and input pointer maintenance
- run-length decoding of zero pairs
- 1bpp chunk output and buffer cursor movement
- differential decode for both sprite chunks
- normal and horizontally flipped nybble decode tables
- XOR chunk merge modes
- nybble bit-reversal table
- mode-2 decode path
- sprite buffer pointer setup helpers

The SRAM work buffers are `$A188-$A30F` and `$A310-$A497`, each `$188` bytes. The Bank 00 state block used by this engine is `$D07E-$D091`.

## Graphics-asset policy

This range contains sprite processing code and small decode lookup tables only. It does **not** contain compressed Pokémon/trainer sprite artwork, so no PNG asset is emitted for this Bank 00 step. When the later sprite-data banks are reconstructed, both the source tile/compressed data and directly viewable PNGs must be committed.

## Cross-check

The recovered routine order and semantics were cross-checked against the public Japanese Red/Green disassembly (`Narishma-gb/pokegreen`), while offsets, hashes, revision differences, SRAM addresses, WRAM addresses, and byte boundaries above were independently verified against the two supplied Japanese Red ROMs.
