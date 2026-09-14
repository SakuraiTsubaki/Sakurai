# blit module

## Scope

`blit` follows `window` and ends at the `window_8bpp` empty stub (`nullsub_9`). Direct ROM comparison confirms this entire module is byte-identical across all seven supported LeafGreen targets.

## Module ranges

| Target | Start | End exclusive | Size |
|---|---:|---:|---:|
| Japan | `0x004A2C` | `0x005000` | `0x5D4` |
| USA | `0x004A60` | `0x005034` | `0x5D4` |
| Europe Rev 1 | `0x004A74` | `0x005048` | `0x5D4` |
| Germany | `0x0049E0` | `0x004FB4` | `0x5D4` |
| France | `0x0049CC` | `0x004FA0` | `0x5D4` |
| Italy | `0x0049E0` | `0x004FB4` | `0x5D4` |
| Spain | `0x0049CC` | `0x004FA0` | `0x5D4` |

All seven slices have the same SHA-1:

`b0e3ce14860e1a52194c96fedf44e7c5b5ef0101`

This is stronger than structural equality: the object bytes themselves are identical after placement.

## Function order and relative offsets

| Offset | Symbol |
|---:|---|
| `0x000` | `BlitBitmapRect4BitWithoutColorKey` |
| `0x044` | `BlitBitmapRect4Bit` |
| `0x224` | `FillBitmapRect4Bit` |
| `0x2E0` | `BlitBitmapRect4BitTo8Bit` |
| `0x530` | `FillBitmapRect8Bit` |

Absolute target addresses are recorded in `symbols/blit.csv`.

## Boundary verification

Immediately after the final `FillBitmapRect8Bit` return, every target contains the same sequence beginning with `nullsub_9` (`bx lr`) followed by the `AddWindow8Bit` Thumb prologue. This fixes the end of `blit` and the beginning of `window_8bpp` independently of the linker script.

## Reconstruction decision

Use one common source/object implementation for all seven targets. No language- or revision-specific source split is needed for this module.
