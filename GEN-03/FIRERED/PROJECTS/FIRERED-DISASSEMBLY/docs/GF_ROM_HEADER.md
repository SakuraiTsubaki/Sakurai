# Game Freak ROM Header (`0x100..0x203`)

All eight FireRed baselines contain a **0x104-byte Game Freak compatibility header** immediately after the standard GBA header area.

- ROM offset: `0x000100`
- End exclusive: `0x000204`
- The ARM entry branch at ROM offset `0x000000` targets `0x08000204`, so startup code begins immediately after this structure.

The layout matches the structure independently documented by the public `pret/pokefirered` decompilation (`src/rom_header_gf.c`). This project also validates every field directly against its own eight ROM baselines.

## Version and language IDs

| Baseline | GF version | GF language |
|---|---:|---:|
| Japanese Rev 0 | 4 | 1 |
| Japanese Rev 1 | 4 | 1 |
| USA Rev 0 | 4 | 2 |
| USA Rev 1 | 4 | 2 |
| French | 4 | 3 |
| Italian | 4 | 4 |
| German | 4 | 5 |
| Spanish | 4 | 7 |

All variants use the internal ASCII game name `pokemon red version`.

## Important localization-dependent fields

The Japanese builds are structurally different from the international builds in multiple compatibility-header constants.

| Field | Japanese | International |
|---|---:|---:|
| `field_075` | 5 | 10 |
| `pokemon_name_length_2` | 5 | 10 |
| `field_078` | 7 | 12 |
| `field_079` | 8 | 12 |
| `field_07B` | 7 | 12 |
| `field_07C` | 4 | 6 |
| `field_07D` | 10 | 16 |
| `field_07F` | 10 | 12 |
| `field_080` | 10 | 15 |
| `field_081` | 5 | 11 |
| `field_083` | 3 | 8 |
| `field_084` | 7 | 12 |
| `save_block_1_size` | `0x3D40` | `0x3D68` |

This confirms that a byte-exact Japanese build cannot be implemented by swapping only encoded strings. Save structures and text/name constraints must be configurable at compile/link time.

## Pointer fields

The header contains direct ROM pointers to major tables including:

- Pokémon front/back sprite tables
- normal/shiny palette tables
- icon tables and icon palettes
- species-name table
- move-name table
- decoration table
- species info
- ability names/descriptions
- item table
- battle-move table
- Poké Ball graphics/palettes

These pointers vary substantially by language and revision because preceding data sizes and link placement vary. `analysis/gf_rom_header/headers.csv` and `analysis/gf_rom_header/headers.json` are the authoritative extracted comparison tables.

## Source reconstruction

`include/gf_rom_header.h` defines the exact `0x104`-byte structure and `src/gf_rom_header.c` emits it from symbolic table references plus language-dependent constants.

A local ARM compile/link test was run separately for all eight canonical baselines. For each build, the appropriate language constant and the independently extracted symbol addresses were supplied to the linker. The generated `0x000100..0x000203` bytes matched the corresponding ROM **byte-for-byte in all eight cases**.

This means the compatibility header no longer needs to be retained as an opaque ROM slice. As the referenced graphics/data tables are reconstructed, their linker symbols can directly populate the pointer fields.

## Status

**Reconstruction status: VERIFIED / SOURCE-REGENERATABLE**

Together with `src/rom_header.s` and `src/crt0.s`, this completes a source representation of the ROM-start region through `0x0003A3`.
