# `sprite.c` cross-version code map

`sprite.c` begins immediately after the localized `text.c` object. Despite the very different Japanese/international text-engine sizes before it, the sprite engine itself is one shared implementation across all eight FireRed baselines.

| Baseline | Start | End exclusive | Size |
|---|---:|---:|---:|
| JP Rev 0 | `0x0800668C` | `0x08008870` | 8676 |
| JP Rev 1 | `0x080065F8` | `0x080087DC` | 8676 |
| US Rev 0 | `0x08006B10` | `0x08008CF4` | 8676 |
| US Rev 1 | `0x08006B24` | `0x08008D08` | 8676 |
| FR | `0x08006A7C` | `0x08008C60` | 8676 |
| DE | `0x08006A90` | `0x08008C74` | 8676 |
| IT | `0x08006A90` | `0x08008C74` | 8676 |
| ES | `0x08006A7C` | `0x08008C60` | 8676 |

A complete byte audit against US Rev 0 classifies every differing byte as either a relocated 32-bit address literal or an ARMv4T Thumb `BL` displacement. No ordinary instruction difference remains. The object is therefore modeled as one shared logical source across all regions/revisions.

The historical US FireRed map divides this one object into conceptual sprite-management subregions (base object management, animation, affine/rotscale, tile allocation, palette allocation). The current linker places all of those routines in `src/sprite.o`, and the independently verified complete object boundary extends through the subsprite routines to `0x08008CF4` in US Rev 0.

The next source object is `string_util.c`; because the string implementation itself is localization-sensitive, its Japanese entry bytes do not match the international signature even though the `sprite.c` boundary remains fixed by its verified size.

Raw measurements are in `analysis/sprite/object_audit.csv`.
