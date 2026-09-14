# Early `main.c` function map

This note continues reconstruction immediately after `AgbMain` and maps the next 21 Thumb functions through `ClearPokemonCrySongs` across all nine reference ROMs.

## Confirmed boundaries

| Function | JP | AXPE | DE/FR/IT | Size (JP / intl.) |
| --- | ---: | ---: | ---: | ---: |
| `UpdateLinkAndCallCallbacks` | `08000348` | `08000340` | `08000474` | `48 / 48` |
| `InitMainCallbacks` | `08000390` | `08000388` | `080004BC` | `20 / 20` |
| `CallCallbacks` | `080003B0` | `080003A8` | `080004DC` | `24 / 24` |
| `SetMainCallback2` | `080003D4` | `080003CC` | `08000500` | `14 / 18` |
| `SeedRngWithRtc` | `080003E8` | `080003E4` | `08000518` | `1C / 1C` |
| `InitKeys` | `08000404` | `08000400` | `08000534` | `28 / 28` |
| `ReadKeys` | `0800042C` | `08000428` | `0800055C` | `9C / 9C` |
| `InitIntrHandlers` | `080004C8` | `080004C4` | `080005F8` | `7C / 7C` |
| callback setters (4) | `08000544` | `08000540` | `08000674` | `0C each` |
| `VBlankIntr` | `08000574` | `08000570` | `080006A4` | `7C / 7C` |
| `InitFlashTimer` | `080005F0` | `080005EC` | `08000720` | `14 / 14` |
| `HBlankIntr` | `08000604` | `08000600` | `08000734` | `30 / 30` |
| `VCountIntr` | `08000634` | `08000630` | `08000764` | `30 / 30` |
| `SerialIntr` | `08000664` | `08000660` | `08000794` | `30 / 30` |
| `IntrDummy` | `08000694` | `08000690` | `080007C4` | `04 / 04` |
| `WaitForVBlank` | `08000698` | `08000694` | `080007C8` | `20 / 20` |
| `DoSoftReset` | `080006B8` | `080006B4` | `080007E8` | `70 / 70` |
| `ClearPokemonCrySongs` | `08000728` | `08000724` | `08000858` | `24 / 24` |

`config/early_main.yml` contains the full machine-readable table, including every callback setter separately.

## Structural findings

The Japanese build is four bytes shorter in `SetMainCallback2`, which explains why the earlier +8-byte displacement relative to AXPE becomes +4 bytes from `SeedRngWithRtc` onward. The DE/FR/IT family keeps the same international function sizes and is displaced by `0x134` because of the extended localization metadata before `Init`.

The following function bodies are byte-identical across every non-Japanese target examined, despite their different language builds: `SetMainCallback2`, `InitKeys`, `ReadKeys`, all four callback setters, and `IntrDummy`. Other functions retain the same control-flow structure but encode different ROM/RAM addresses or external branch targets.

## Revision findings

- `EUR-AXPE-v1` and `USA-EUR-AXPE-v2` are byte-identical throughout this mapped `main.c` block.
- `USA-AXPE-v0` has the same function boundaries and logic shape, but differs in selected literal/call targets from the later AXPE builds.
- French Rev 0 and Rev 1 are byte-identical throughout this block.
- Italian Rev 0 and Rev 1 are byte-identical throughout this block.
- German Rev 1, French, and Italian share the same boundaries but differ in linked addresses/call targets because each localization build has a different overall ROM layout.

Per-function SHA-256 fingerprints for all nine targets are stored in `verification/early_main_function_hashes.csv`.

## Source cross-check

The function ordering and semantics agree with the public `pret/pokeruby` `src/main.c`: callback dispatch, input handling, interrupt initialization, VBlank/HBlank/VCount/Serial handlers, soft reset, and cry-song clearing occur in the same order. The boundaries and hashes in this repository are derived from the nine locally verified retail Sapphire ROMs rather than copied from that source.

## Next boundary

The next function begins immediately after `ClearPokemonCrySongs` (`0x0800074C` JP, `0x08000748` AXPE, `0x0800087C` DE/FR/IT). Reconstruction should continue from there into the next linked source unit while keeping the same per-target boundary and fingerprint checks.
