# window_8bpp module

## Scope

`window_8bpp` follows `blit`. Direct Thumb disassembly confirms one common seven-function relative layout across all supported LeafGreen targets.

## Module ranges

| Target | Start | End exclusive | Size | SHA-1 |
|---|---:|---:|---:|---|
| Japan | `0x005000` | `0x005348` | `0x348` | `af175d6fa260d8ecabb268567fb81a05b5110423` |
| USA | `0x005034` | `0x00537C` | `0x348` | `6c0d338f788e3ea8a09283f467ba4b07533c1147` |
| Europe Rev 1 | `0x005048` | `0x005390` | `0x348` | `6ff859b62dd2b9422b180d888f3459186effa7f1` |
| Germany | `0x004FB4` | `0x0052FC` | `0x348` | `ae8b8cd94b0c9199e0069690f76238155a3c37d7` |
| France | `0x004FA0` | `0x0052E8` | `0x348` | `3c68b220ea8cda5b350e3aac77fef441b13198db` |
| Italy | `0x004FB4` | `0x0052FC` | `0x348` | `ae8b8cd94b0c9199e0069690f76238155a3c37d7` |
| Spain | `0x004FA0` | `0x0052E8` | `0x348` | `3c68b220ea8cda5b350e3aac77fef441b13198db` |

Germany and Italy are byte-identical for this object; France and Spain are also byte-identical. Other targets preserve the same code layout with relocated references.

## Function order and relative offsets

| Offset | Symbol |
|---:|---|
| `0x000` | `nullsub_9` |
| `0x004` | `AddWindow8Bit` |
| `0x10C` | `FillWindowPixelBuffer8Bit` |
| `0x14C` | `FillWindowPixelRect8Bit` |
| `0x1D8` | `BlitBitmapRectToWindow4BitTo8Bit` |
| `0x2A4` | `CopyWindowToVram8Bit` |
| `0x31C` | `GetNumActiveWindowsOnBg8Bit` |

Absolute target addresses are recorded in `symbols/window_8bpp.csv`.

## Boundary verification

The module begins with the `nullsub_9` empty Thumb function immediately after `blit`. The function at relative offset `0x31C` is the active-window counter; it returns before the next `text` object begins. The bytes at each target's end are identical at the next function entry, independently confirming the boundary.

## Reconstruction decision

Use one semantic `window_8bpp` source implementation. Keep target-specific placement/relocations in linker configuration rather than duplicating source.

The next object is `text`.
