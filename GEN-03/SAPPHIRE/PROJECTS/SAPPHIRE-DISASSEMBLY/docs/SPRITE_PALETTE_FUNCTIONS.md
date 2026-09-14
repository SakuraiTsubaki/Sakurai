# `sprite.c` sprite-palette allocation and tag map

This pass continues at `FreeAllSpritePalettes` and maps eight consecutive palette-management functions across all nine Sapphire reference ROMs, ending at `FreeSpritePaletteByTag`.

## Covered functions

`FreeAllSpritePalettes → LoadSpritePalette → LoadSpritePalettes → DoLoadSpritePalette → AllocSpritePalette → IndexOfSpritePaletteTag → GetSpritePaletteTagByPaletteNum → FreeSpritePaletteByTag`.

Exact addresses and sizes live in `config/sprite_palette.yml`.

## Historical AXPE boundaries

The AXPE boundaries were cross-checked against historical `pret/pokeruby` assembly at commit `4af578c1865e4b620f4c64401e0a16ccbd9efc8d`:

| Current name | Historical label | AXPE address |
| --- | --- | ---: |
| `FreeAllSpritePalettes` | `ResetObjectPaletteAllocator` | `0x080025C8` |
| `LoadSpritePalette` | `LoadTaggedObjectPalette` | `0x08002600` |
| `LoadSpritePalettes` | `LoadTaggedObjectPalettes` | `0x0800264C` |
| `DoLoadSpritePalette` | `LoadObjectPalette` | `0x08002678` |
| `AllocSpritePalette` | `AllocObjectPalette` | `0x08002690` |
| `IndexOfSpritePaletteTag` | `IndexOfObjectPaletteTag` | `0x080026C0` |
| `GetSpritePaletteTagByPaletteNum` | `gpu_pal_tag_by_index` | `0x080026F8` |
| `FreeSpritePaletteByTag` | `FreeObjectPaletteByTag` | `0x08002708` |

## Family layout

All eight functions keep identical sizes in JP and international builds, preserving the established displacement:

- JP = AXPE `-0xE4`
- DE/FR/IT = AXPE `+0x134`

The next function is `SetSubspriteTables`:

- JP: `0x0800264C`
- AXPE: `0x08002730`
- DE/FR/IT: `0x08002864`

## Byte-level findings

Seven of the eight functions are raw-byte identical across all eight international ROMs. The sole exception is `DoLoadSpritePalette`, whose external `LoadPalette` call encoding changes with the linked build layout.

The JP build has separate raw fingerprints for all eight functions because its RAM/data placement and linked addresses differ, while function sizes and ordering remain the same.

The following revision pairs are byte-identical for all eight functions:

- `EUR-AXPE-v1` = `USA-EUR-AXPE-v2`
- `FRA-AXPF-v0` = `FRA-AXPF-v1`
- `ITA-AXPI-v0` = `ITA-AXPI-v1`

## Verification

`tools/analyze_sprite_palette.py` fingerprints this block. Expected per-target SHA-256 fingerprints live under `verification/sprite_palette/`.

## Next boundary

Continue at `SetSubspriteTables` into sprite/subsprite OAM-buffer construction.
