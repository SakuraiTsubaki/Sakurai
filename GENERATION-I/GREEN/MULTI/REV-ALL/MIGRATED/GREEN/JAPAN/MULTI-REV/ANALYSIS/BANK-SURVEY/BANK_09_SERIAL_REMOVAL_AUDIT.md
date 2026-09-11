# Bank 09 deep audit — Rev-0-only unused serial routine

Bank 09 is mostly Pokémon picture data followed by Battle Engine 3.

## Direct revision change

Rev 0 begins Battle Engine 3 with `UnusedSerialFunction`. The source labels it unused and contains an explicit `; bug: fallthrough` comment on one path. Rev A removes this routine entirely.

- Rev 0: Battle Engine 3 `$7DCE-$7FCD` = `$0200` bytes; `UnusedSerialFunction` at `$7DCE`, `PrintMonType` at `$7DF4`.
- Rev A: Battle Engine 3 `$7DCE-$7FA7` = `$01DA` bytes; `PrintMonType` moves to `$7DCE`.
- Difference = `$26` = 38 bytes exactly.

The removed routine's 38 bytes become extra tail residual space, explaining the large local shifted region after `$7DCE`.

## Audit interpretation

Raw comparison reports 519 differing bytes in bank 09. The direct semantic deletion is 38 bytes; most remaining differences arise because the following Battle Engine 3 code shifts upward by 38 bytes and references elsewhere change accordingly.
