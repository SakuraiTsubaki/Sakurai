# `window.c` cross-version code map

`window.c` follows the text-printer object. Unlike `text_printer.c`, the window manager remains one shared implementation across all eight audited FireRed baselines.

| Baseline | Start | End exclusive | Size |
|---|---:|---:|---:|
| JP Rev 0 | `0x08003AEC` | `0x08004A2C` | 3904 |
| JP Rev 1 | `0x08003A58` | `0x08004998` | 3904 |
| US Rev 0 | `0x08003B20` | `0x08004A60` | 3904 |
| US Rev 1 | `0x08003B34` | `0x08004A74` | 3904 |
| FR | `0x08003A8C` | `0x080049CC` | 3904 |
| DE | `0x08003AA0` | `0x080049E0` | 3904 |
| IT | `0x08003AA0` | `0x080049E0` | 3904 |
| ES | `0x08003A8C` | `0x080049CC` | 3904 |

US Rev 0 symbol landmarks include `InitWindows` at `0x08003B24`, `AddWindow` at `0x08003CE4`, `RemoveWindow` at `0x08003E3C`, `FreeAllWindowBuffers` at `0x08003ECC`, `CopyWindowToVram` at `0x08003F20`, `ScrollWindow` at `0x080044A8`, `GetWindowAttribute` at `0x08004950`, and `GetNumActiveWindowsOnBg` at `0x08004A34`.

Every cross-version differing byte in the complete object is either a relocation-sensitive 32-bit address literal or a Thumb `BL` displacement. No ordinary instruction byte differs. Therefore `window.c` is modeled as one shared source object across Japanese and international builds.

`blit.c` begins immediately at each end-exclusive address above. Raw measurements are in `analysis/window/object_audit.csv`.
