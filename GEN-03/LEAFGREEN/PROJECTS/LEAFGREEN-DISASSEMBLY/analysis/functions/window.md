# window module

## Scope

`window` follows `text_printer` and ends exactly where `blit` begins. Direct Thumb disassembly of all seven retail LeafGreen ROMs confirms one common relative function layout.

## Module ranges

| Target | Start | End exclusive | Size | SHA-1 |
|---|---:|---:|---:|---|
| Japan | `0x003AEC` | `0x004A2C` | `0xF40` | `c70680076bfda9f00fc7583b9e39105d5f4d4565` |
| USA | `0x003B20` | `0x004A60` | `0xF40` | `8a580872ae7130dfd0098b38654b8a51c879cba2` |
| Europe Rev 1 | `0x003B34` | `0x004A74` | `0xF40` | `23fe4027546a34aaf438f3bf95a842dbc8963e83` |
| Germany | `0x003AA0` | `0x0049E0` | `0xF40` | `d3963f22519d9cb218dd6cdd94468befadaa9643` |
| France | `0x003A8C` | `0x0049CC` | `0xF40` | `de429009ce2276e16182b4dbc0ce6c1bb4403d24` |
| Italy | `0x003AA0` | `0x0049E0` | `0xF40` | `dd1ae352e3af63df6633cddbaadb9b6035606cf5` |
| Spain | `0x003A8C` | `0x0049CC` | `0xF40` | `239333a3133f5a1a92a2c6b721c9f54bf9af46d5` |

Raw hashes differ because absolute ROM/RAM references are relocated between targets. The module size and all 21 verified function offsets are identical.

## Function order and relative offsets

| Offset | Symbol |
|---:|---|
| `0x000` | `nullsub_8` |
| `0x004` | `InitWindows` |
| `0x1C4` | `AddWindow` |
| `0x31C` | `RemoveWindow` |
| `0x3AC` | `FreeAllWindowBuffers` |
| `0x400` | `CopyWindowToVram` |
| `0x480` | `PutWindowTilemap` |
| `0x4E0` | `PutWindowRectTilemapOverridePalette` |
| `0x598` | `ClearWindowTilemap` |
| `0x5E8` | `PutWindowRectTilemap` |
| `0x698` | `BlitBitmapToWindow` |
| `0x6D0` | `BlitBitmapRectToWindow` |
| `0x790` | `BlitBitmapRectToWindowWithColorKey` |
| `0x858` | `FillWindowPixelRect` |
| `0x8E4` | `CopyToWindowPixelBuffer` |
| `0x93C` | `FillWindowPixelBuffer` |
| `0x988` | `ScrollWindow` |
| `0xD4C` | `CallWindowFunction` |
| `0xD9C` | `SetWindowAttribute` |
| `0xE30` | `GetWindowAttribute` |
| `0xF14` | `GetNumActiveWindowsOnBg` |

Per-target absolute addresses are recorded in `symbols/window.csv`.

## Boundary verification

The first `blit` routine, `BlitBitmapRect4BitWithoutColorKey`, has the same Thumb entry signature in all seven targets and begins immediately after the `0xF40`-byte `window` object:

- Japan: `0x08004A2C`
- USA: `0x08004A60`
- Europe Rev 1: `0x08004A74`
- Germany / Italy: `0x080049E0`
- France / Spain: `0x080049CC`

This independently fixes the `window` end boundary.

## Reconstruction decision

Use one semantic `window` source implementation across all seven targets. Target-specific linker placement and relocated references account for the differing raw hashes; there is no evidence here for a separate localized source layout.

The next object is `blit`.
