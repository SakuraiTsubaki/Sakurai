# Bank 00 layout — recovered ranges

This document records ranges independently verified against the seven unique uploaded Red-family ROMs.

## Common vectors and entry header

All seven builds use `nop; jp $0150` at `$0100`. The reset slots at `$0000-$0037`, VBlank/LCD/Timer/Serial/Joypad vectors, and their build-specific handler targets are represented in `home/header.asm`.

The Japanese builds differ from the western builds at RST `$38`:

- Japanese V1.0/V1.1: `jp $F080` at `$0038`.
- Western builds: `rst $38` at `$0038`.

## Japanese `$0068-$00FF`

Japanese Red does not place the western `High Home` helpers after the Joypad vector. `$0061-$0067` is zero-filled and `$0068-$00FF` contains revision-specific residual bytes. They are preserved in `home/garbage_header.asm`.

- V1.0 SHA-1 for `$0068-$00FF`: `e825cf552841abf607fea09748fcae672cbe2b79`
- V1.1 SHA-1 for `$0068-$00FF`: `ab8bed6a4b09d119f383ca1f8b5c6050c0a83ee9`

## Western `$0061-$00FF`

English, German, Italian, Spanish, and French Red are byte-identical from `$0061-$00FF`. `$0061-$00BD` contains `DisableLCD`, `EnableLCD`, `ClearSprites`, `HideSprites`, `FarCopyData`, and `CopyData`; `$00BE-$00FF` is zero-filled. The reconstructed source is in `home/high_home.asm`.

SHA-1 for `$0061-$00FF` across all five western builds: `62518b31ffe74d9a3d075cb813d0a2f62f6e07df`.

## `_Start` at `$0150`

- Japanese V1.0/V1.1: `jp Init` with `Init = $09DA`.
- Western builds: CGB boot-register check, store to build-specific `wOnCGB`, then jump to build-specific `Init`.

The initial instructions are reconstructed in `home/start.asm`.

## Japanese `$0153-$01C3`

Japanese Red V1.0 and V1.1 are byte-identical throughout this range. It contains `Joypad`, LCD helpers, sprite clear/hide helpers, `FarCopyData`, and `CopyData`.

Range SHA-1: `90200ac376116d0ab6092465801788eac3f872fb`.

The machine code confirms the Japanese `wBuffer = $CEE4`; western Red uses `$CEE9`.

## Japanese `$01C4-$028B` — collision tables

V1.0 and V1.1 are byte-identical. This 200-byte block contains the per-tileset collision tile lists from `Underground_Coll` through `Plateau_Coll`, including one empty/unused `$FF`-only table.

- size: 200 bytes
- SHA-1: `af69e30d0ddd85bf0f2be3fe6182073a5acc8099`
- source: `data/tilesets/jp_collision_tile_ids.asm`

The structured `db` tables were regenerated from the supplied ROM bytes and reproduce the complete `$01C4-$028B` byte range exactly.

## Japanese `$028C-$0358` — copy/video helpers

V1.0 and V1.1 are byte-identical throughout this range. Recovered routines:

- `FarCopyData2`
- `FarCopyData3`
- `FarCopyDataDouble`
- `CopyVideoData`
- `CopyVideoDataDouble`

Range SHA-1: `aa2ddaaf5882261093d2bdf010cdf44f4f03c97a`.

The code directly verifies HRAM locations used by the VBlank copy subsystem, including `hROMBankTemp = $FF8B`, `hAutoBGTransferEnabled = $FFBA`, and the copy control block at `$FFC1-$FFCF`.

## Japanese `$0359-$03D1` — input interruption and screen helpers

Recovered routines:

- `CheckForUserInterruption`
- `ClearScreenArea`
- `CopyScreenTileBufferToVRAM`
- `ClearScreen`

Most bytes are shared between V1.0 and V1.1. Two revision-dependent call targets are preserved explicitly:

| Target | V1.0 | V1.1 |
|---|---:|---:|
| `JoypadLowSensitivity` | `$3879` | `$3867` |
| `Delay3` | `$3E07` | `$3DF5` |

`DelayFrame = $0B31` and `GetRowColAddressBgMap = $0774` are common to both revisions in this recovered range.

Range hashes:

- `$0359-$0373` V1.0: `b611b36637cc37f345d977ef8fa201ff8f6df06c`
- `$0359-$0373` V1.1: `32e403bf684e79d2c5d988562e0f37ddc104f8c7`
- `$0374-$03D1` V1.0: `3aaf68f68b7b7fc95145cd0fdc870f8a506bab1e`
- `$0374-$03D1` V1.1: `3a37fb78af1f17288e463c623e7ce4d474416743`

The source for `$028C-$03D1` is in `home/jp_copy2.asm`.

## Japanese `$03D2-$04C8` — text rendering core

This block contains `TextBoxBorder`, `PlaceString`, `PlaceNextChar`, the control-character dictionary, Japanese dakuten/handakuten conversion, and `NextChar`.

The two Japanese revisions differ by only one byte in this complete 247-byte range: the high byte of the `PrintLetterDelay` call target at `$04C2-$04C4`.

| Target | V1.0 | V1.1 |
|---|---:|---:|
| `PrintLetterDelay` | `$391D` | `$390B` |

Range SHA-1 values:

- V1.0: `96d926650aef3da4237aabeed5b46a5be58f0412`
- V1.1: `a6eac2faadef25b113867f1203637861b4b3e916`

The recovered code exposes the original Japanese text encoding behavior directly: `$E4/$E5` are handakuten/dakuten marks, values below `$60` are converted into base kana plus a diacritic tile, and the text-control codes occupy the `$4B-$5E` range. Source is in `home/jp_text_core.asm`.

## External cross-checks

Semantic labels were cross-checked against the public `pret/pokered` disassembly and the public `Narishma-gb/pokegreen` Japanese Red/Green disassembly. Byte values, offsets, ROM hashes, revision differences, and localization differences recorded here are independently verified from the supplied ROM files.
