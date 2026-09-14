# Main bootstrap function map

This report maps the LeafGreen main/bootstrap module across the seven verified retail targets. ROM offsets are relative to the start of the 16 MiB image; add `0x08000000` for GBA ROM virtual addresses.

## Verified module boundaries

All targets enter `AgbMain` at ROM offset `0x0003A4`. The end of the module is the start of the next source module immediately after `ClearPokemonCrySongs`.

| Target | `AgbMain` start | `UpdateLinkAndCallCallbacks` | module end | `AgbMain` size | post-`AgbMain` delta vs USA |
|---|---:|---:|---:|---:|---:|
| Japan | `0x0003A4` | `0x0004B0` | `0x000968` | `0x10C` | `+0x00` |
| USA | `0x0003A4` | `0x0004B0` | `0x000968` | `0x10C` | `+0x00` |
| Europe Rev 1 | `0x0003A4` | `0x0004C4` | `0x00097C` | `0x120` | `+0x14` |
| Germany | `0x0003A4` | `0x0004C0` | `0x000978` | `0x11C` | `+0x10` |
| France | `0x0003A4` | `0x0004AC` | `0x000964` | `0x108` | `-0x04` |
| Italy | `0x0003A4` | `0x0004C0` | `0x000978` | `0x11C` | `+0x10` |
| Spain | `0x0003A4` | `0x0004AC` | `0x000964` | `0x108` | `-0x04` |

The important structural result is that `AgbMain` itself varies in size, but every mapped function after it through `ClearPokemonCrySongs` retains the same size and ordering. Each target therefore has one stable post-`AgbMain` address delta for this complete module.

## Confirmed functions

The module contains 28 named functions in this order:

1. `AgbMain`
2. `UpdateLinkAndCallCallbacks`
3. `InitMainCallbacks`
4. `CallCallbacks`
5. `SetMainCallback2`
6. `StartTimer1`
7. `SeedRngAndSetTrainerId`
8. `GetGeneratedTrainerIdLower`
9. `EnableVCountIntrAtLine150`
10. `InitKeys`
11. `ReadKeys`
12. `InitIntrHandlers`
13. `SetVBlankCallback`
14. `SetHBlankCallback`
15. `SetVCountCallback`
16. `SetSerialCallback`
17. `VBlankIntr`
18. `InitFlashTimer`
19. `HBlankIntr`
20. `VCountIntr`
21. `SerialIntr`
22. `RestoreSerialTimer3IntrHandlers`
23. `IntrDummy`
24. `WaitForVBlank`
25. `SetVBlankCounter1Ptr`
26. `DisableVBlankCounter1`
27. `DoSoftReset`
28. `ClearPokemonCrySongs`

The exact per-target addresses are recorded in `main_bootstrap_matrix.csv` and `symbols/main_bootstrap.csv`.

## Behavioral landmarks verified from disassembly

- `AgbMain` performs RAM reset and display initialization, initializes GPU/key/IRQ/audio/RFU/flash state, establishes main callbacks, and enters the frame loop.
- `ReadKeys` contains the original L=A key-repeat behavior noted by later decompilation work.
- `InitIntrHandlers` copies the interrupt dispatch template and installs the RAM interrupt vector.
- The interrupt callbacks occur in the expected order: VBlank, HBlank, VCount, Serial.
- `DoSoftReset` disables IME, shuts down sound/scanline/DMA state, then invokes BIOS soft reset.
- `ClearPokemonCrySongs` is the final function in this module; the following function at the recorded module end belongs to the next source module.

## Address-family grouping

For the functions after `AgbMain`, the seven builds collapse into four address families:

- `+0x00`: Japan, USA
- `+0x14`: Europe Rev 1
- `+0x10`: Germany, Italy
- `-0x04`: France, Spain

This grouping is an address-layout result only. It must not be treated as proof that the underlying code/data bytes are identical; literal pools and external call targets can still differ between targets.

## Verification method

The function map was established directly against the seven read-only ROMs. Stable byte signatures were used to locate `InitMainCallbacks` and downstream functions, and neighboring function boundaries were checked by Thumb disassembly and return/literal-pool structure. The USA layout was used as the naming baseline; each target was then independently checked at the derived address.

A reproducible scanner is provided at `tools/scan_main_bootstrap.py`.
