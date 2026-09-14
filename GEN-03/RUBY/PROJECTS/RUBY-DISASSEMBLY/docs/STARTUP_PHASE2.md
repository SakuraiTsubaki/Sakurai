# Startup / CRT Reconstruction — Phase 2

Phase 2 begins the symbolized reconstruction at the first byte of each ROM.

## Confirmed CRT families

The ARM initialization signature was located directly in all 13 verified ROMs. The `AgbMain` literal was then used to determine the exact end of the ARM CRT and the first Thumb main-code address.

| Family | `Init` | `AgbMain` | CRT body size |
|---|---:|---:|---:|
| Japan Rev 0 | `0x080000D0` | `0x0800024D` (Thumb) | `0x17C` |
| English Rev 0/1/2 | `0x080000D0` | `0x0800024D` (Thumb) | `0x17C` |
| DE/FR/IT/ES retail | `0x08000204` | `0x08000381` (Thumb) | `0x17C` |
| German debug | `0x08000204` | `0x08000381` (Thumb) | `0x17C` |

The executable CRT body itself is the same size in every family. The later European-language entry point is caused by an additional `0x134`-byte metadata block inserted at file offset `0xD0` before `Init`.

## CRT-body identity groups

SHA-1 over `Init..AgbMain` gives three retail/debug body groups:

- English retail: `93e796ed6f3677ea4208fccfb36335bcb86e849c`
- DE/FR/IT/ES retail: `d1efd64016887149ba602c83c5ddbb7225c8b887`
- Japan Rev 0: `9c33a92cf3d6067dfcdf688ae0985379ba2c50f0`
- German debug: `bcbd54eb2fb51a7c7d1b7bfe982d03aad8a3a9be`

The actual ARM instruction stream is effectively shared. English and Japanese differ in the CRT body by one byte, solely from the relocated `gIntrTable` RAM literal (`0x03001BC0` vs `0x03001B30`). German debug differs from European retail by two bytes, again solely from the `gIntrTable` literal (`0x03001C40` vs `0x03001BC0`). This means one semantic CRT source can serve all targets once RAM symbols are resolved per build.

## European extended metadata block

DE/FR/IT/ES images contain a structured block at file offsets `0xD0–0x203`:

- `0xD0–0xFF`: twelve `0xFFFFFFFF` words
- `0x100`: game-version value (`2` for Ruby)
- `0x104`: language ID
- `0x108`: ASCII signature `pokemon ruby version`
- `0x11C–0x127`: zero padding
- `0x128–0x14F`: ten ROM pointers
- `0x150–0x1B7`: fixed metadata/constants
- `0x1B8–0x1FF`: zero-filled reserved words
- `0x200`: `0xFFFFFFFF`

Confirmed language IDs in the supplied ROM set:

| Language | ID |
|---|---:|
| French | 3 |
| Italian | 4 |
| German | 5 |
| Spanish | 7 |

The ten pointer fields at `0x128–0x14C` resolve to:

1. Pokémon front-picture table
2. Pokémon back-picture table
3. normal palette table
4. shiny palette table
5. Pokémon icon table
6. icon palette-index table
7. icon palette table
8. species-name table
9. move-name table
10. decoration table

The exact per-language addresses are recorded in `manifests/startup_phase2.json`. Rev 0 and Rev 1 of each language use the same values; the German debug build has its own shifted pointer set.

## Initial symbols

`symbols/startup_symbols.csv` records `Start`, `Init`, `IntrMain`, and `AgbMain` for every verified target. These are the first ROM-derived symbols in the repository and form the anchor for subsequent function/data mapping.

## Reconstruction strategy

The CRT should be represented as one shared semantic ARM source with build-time differences for:

- optional European extended metadata block;
- language ID and asset-table pointers;
- `gIntrTable` RAM symbol;
- version/header fields handled by the build/header-fix stage.

No source ROM should be required once those fields and the standard GBA header construction are represented by repository source/build tools.

## Next target

Continue from `AgbMain` in Thumb mode, identify the `main` object/function boundaries, then expand symbols forward into `sprite`, `text`, `string_util`, `link`, and `rtc`. The already identified RTC revision patch will be attached to the symbolized `ConvertDateToDayCount` routine during that pass.
