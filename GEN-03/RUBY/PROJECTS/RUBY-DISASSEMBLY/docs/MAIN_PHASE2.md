# Main / interrupt core symbolization — Phase 2 continuation

This pass continues directly from the previously identified `AgbMain` entry point and maps the complete `main.c` startup/interrupt core through `ClearPokemonCrySongs`.

## Result

The following 22 functions are now boundary-mapped for every one of the 13 verified Ruby ROM targets (286 target/function records):

`AgbMain`, `UpdateLinkAndCallCallbacks`, `InitMainCallbacks`, `CallCallbacks`, `SetMainCallback2`, `SeedRngWithRtc`, `InitKeys`, `ReadKeys`, `InitIntrHandlers`, `SetVBlankCallback`, `SetHBlankCallback`, `SetVCountCallback`, `SetSerialCallback`, `VBlankIntr`, `InitFlashTimer`, `HBlankIntr`, `VCountIntr`, `SerialIntr`, `IntrDummy`, `WaitForVBlank`, `DoSoftReset`, and `ClearPokemonCrySongs`.

The checked-in representation deliberately avoids duplicating the same address data hundreds of times:

- `symbols/main_layouts.csv` — function-relative offsets and sizes for the Japanese and international compiler-layout families.
- `symbols/main_targets.csv` — each target's `AgbMain` base, mapped-region end, size, and region SHA-1.
- `manifests/main_phase2.json` — both layouts plus all 286 per-function SHA-1 fingerprints. A target's exact ROM address is `0x08000000 + agbmain_offset + relative_offset`; its Thumb pointer address is that address plus one.
- `tools/analyze_main.py` — regenerates all three artifacts after exact whole-ROM SHA-1 verification against `manifests/source_roms.json`.

No ROM bytes are committed.

## Two layout families

### International / debug family

English Rev 0/1/2, German Rev 0/1, German Debug, French Rev 0/1, Italian Rev 0/1, and Spanish Rev 0/1 all share one function-boundary layout relative to `AgbMain`.

The mapped region is `0x4FC` bytes long.

| Function | Relative offset |
|---|---:|
| `AgbMain` | `+0x000` |
| `UpdateLinkAndCallCallbacks` | `+0x0F4` |
| `InitMainCallbacks` | `+0x13C` |
| `CallCallbacks` | `+0x15C` |
| `SetMainCallback2` | `+0x180` |
| `SeedRngWithRtc` | `+0x198` |
| `InitKeys` | `+0x1B4` |
| `ReadKeys` | `+0x1DC` |
| `InitIntrHandlers` | `+0x278` |
| `VBlankIntr` | `+0x324` |
| `DoSoftReset` | `+0x468` |
| `ClearPokemonCrySongs` | `+0x4D8` |
| next object | `+0x4FC` |

The boundaries are stable even though literal-pool values and `BL` destinations differ between languages because downstream code/data are relocated.

### Japanese family

Japan Rev 0 has the same semantic function sequence but a slightly different compiler layout.

Its mapped region is `0x500` bytes long. `AgbMain` itself is 8 bytes larger than the international layout, while `SetMainCallback2` is 4 bytes smaller, leaving most later functions shifted by `+0x4`.

| Function | Relative offset |
|---|---:|
| `AgbMain` | `+0x000` |
| `UpdateLinkAndCallCallbacks` | `+0x0FC` |
| `InitMainCallbacks` | `+0x144` |
| `CallCallbacks` | `+0x164` |
| `SetMainCallback2` | `+0x188` |
| `SeedRngWithRtc` | `+0x19C` |
| `InitKeys` | `+0x1B8` |
| `ReadKeys` | `+0x1E0` |
| `InitIntrHandlers` | `+0x27C` |
| `VBlankIntr` | `+0x328` |
| `DoSoftReset` | `+0x46C` |
| `ClearPokemonCrySongs` | `+0x4DC` |
| next object | `+0x500` |

## Region fingerprints

| Target | Size | SHA-1 |
|---|---:|---|
| Japan Rev 0 | `0x500` | `7e3b70650013f2e17cf52f53702c4708d42038fc` |
| English Rev 0 | `0x4FC` | `4c8f97962d241089136471922e2fba28933c55fe` |
| English Rev 1/2 | `0x4FC` | `e55482f58a22da864200cb2bef2224042ff03c32` |
| German Rev 0/1 | `0x4FC` | `5f4200e14bd5432ca077e30a59e72a4040570d3f` |
| German Debug | `0x4FC` | `45b2504cb9eafe2ca8876150e11c4357330fc66e` |
| French Rev 0/1 | `0x4FC` | `966d6030a3df7957e7490941da358c6aafb25519` |
| Italian Rev 0/1 | `0x4FC` | `78ee774f1fa88f98f963d0d01e52f3abf792d447` |
| Spanish Rev 0/1 | `0x4FC` | `22a81d81daf33d711871cb1b5b98bb794b97e002` |

This confirms that each non-English retail Rev 0/Rev 1 pair is byte-identical in this early `main.c` region, and English Rev 1/Rev 2 are byte-identical here. The known revision differences occur later.

## Semantic cross-check and object boundary

Function order and behavior were cross-checked against the public `pret/pokeruby` implementation; addresses, sizes, and hashes here are derived directly from the verified local ROM set.

The byte immediately after `ClearPokemonCrySongs` starts `sprite.o` / `ResetSpriteData` at:

- Japan: file offset `0x74C` / ROM address `0x0800074C`
- English: file offset `0x748` / ROM address `0x08000748`
- DE/FR/IT/ES + German Debug: file offset `0x87C` / ROM address `0x0800087C`

The next pass continues through the `sprite.c` engine before `text`, `string_util`, `link`, and `rtc`.
