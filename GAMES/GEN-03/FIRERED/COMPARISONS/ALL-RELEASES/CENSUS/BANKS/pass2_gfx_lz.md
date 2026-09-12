# Pokémon FireRed — analytical-bank census pass 2: graphics/LZ structure

Date: 2026-09-10

## Scope

This pass refines the 16 KiB (`0x4000`) analytical-bank map from pass 1 using validated GBA LZ77 (`0x10`) stream detection, direct binary comparison, and the current `pret/pokefirered` linker scripts.

## Confirmed English graphics boundary

The current `pret/pokefirered` linker script explicitly places:

```ld
    gfx_data 0x08D00000 :
    ALIGN(4)
    {
        src/graphics.o(.rodata);
    } > ROM =0

    extra :
```

The Rev 1 linker script uses the same fixed `0x08D00000` graphics address. Since a GBA ROM is mapped at `0x08000000`, this corresponds to file offset `0x00D00000`, analytical bank `0x340`.

This matches the uploaded EN/European ROMs, whose high non-FF region begins at file offset `0xD00000`. Therefore the high-address data beginning there is not generic padding: it contains the deliberately placed graphics section and subsequent extra data.

Reference: https://github.com/pret/pokefirered/blob/master/ld_script.ld and `ld_script_rev10.ld`.

## Japanese shifted graphics-region inference

The uploaded Japanese ROMs begin their corresponding high non-FF region at file offset `0xC00000` (analytical bank `0x300`), one MiB before the English/European `0xD00000` boundary.

Binary evidence:

- JP file offset `0xC00000` and EN file offset `0xD00000` begin with the same 80-byte prefix.
- Comparing 16 KiB banks under a `+0x100000` EN shift, 79 of the first 104 shifted banks are byte-identical.
- Exact shifted-identical runs include relative banks `001–003`, `005–020`, and `022–051`.

This is strong evidence that the Japanese build places a corresponding graphics blob at `0xC00000`; however, this remains an inference until corroborated by a Japanese linker/map source.

## Validated LZ77 (`0x10`) stream scan

A structural LZ77 validator was run over the main payload region below `0x71C000`. Candidate streams were accepted only when the compressed control/data sequence parsed consistently for the declared decompressed length.

Validated stream counts:

| ROM | Streams |
|---|---:|
| JP Rev0 | 585 |
| JP Rev1 | 585 |
| EN Rev0 | 511 |
| EN Rev1 | 511 |
| German | 497 |
| French | 497 |
| Italian | 498 |
| Spanish | 497 |

### Highest-density JP Rev0 analytical banks

| Bank | Offset | Validated LZ streams |
|---|---:|---:|
| `082` | `0x208000` | 38 |
| `0E6` | `0x398000` | 28 |
| `109` | `0x424000` | 26 |
| `0E5` | `0x394000` | 23 |
| `10C` | `0x430000` | 22 |
| `081` | `0x204000` | 20 |
| `101` | `0x404000` | 20 |
| `0F2` | `0x3C8000` | 19 |
| `0ED` | `0x3B4000` | 18 |
| `10E` | `0x438000` | 17 |

### Highest-density EN Rev0 analytical banks

| Bank | Offset | Validated LZ streams |
|---|---:|---:|
| `093` | `0x24C000` | 31 |
| `092` | `0x248000` | 27 |
| `0F4` | `0x3D0000` | 26 |
| `110` | `0x440000` | 26 |
| `0F3` | `0x3CC000` | 24 |
| `118` | `0x460000` | 22 |
| `0FC` | `0x3F0000` | 20 |
| `119` | `0x464000` | 20 |
| `11B` | `0x46C000` | 17 |
| `11A` | `0x468000` | 14 |

These banks are priority candidates for graphics/tile/palette/compressed-resource semantic labeling. A validated LZ stream alone does not identify the asset type.

## Main-payload composition from decompilation linker order

The public FireRed linker script confirms that the pre-gap payload is heterogeneous rather than a single executable block. It contains, in order and interleaved by linker sections, executable `.text`, event/battle/field script data, library code, `.rodata` including maps and text/data tables, song/sound data, and multiboot-related data before the separately fixed graphics section.

Accordingly, pass 3 must tag banks from symbols/section ranges rather than assigning one semantic type to large offset spans.

## Pointer-heuristic warning

Raw aligned 32-bit values numerically falling inside `0x08000000–0x08FFFFFF` were collected only as a coarse heuristic. They are **not accepted as proven pointers**. Random/compressed data can produce such values, and apparent targets were observed even in known all-FF or revision-absent areas. These counts must not be used alone to call a bank 'referenced'. Future pointer analysis must require source-context validation and/or symbol/decompilation cross-reference.

## Next pass

Pass 3 will cross-reference every non-FF analytical bank against linker/symbol ranges and classify content into at least:

- ARM/Thumb executable code
- event/battle/field scripts
- text/string tables and localized strings
- maps/metatiles/map events
- Pokémon/item/move/trainer/system tables
- music/SFX/sample data
- compressed graphics/resources
- fixed high graphics section / extra data
- confirmed free/padding space
- unresolved/residual data

The pass-1 1024-bank index remains the coarse coordinate system for all later semantic maps.
