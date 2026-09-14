# Block 00 Survey — `0x000000-0x00FFFF`

This is the first semantic pass over the 64 KiB block map. The reference set contains six unique ROM payloads: JPN, ENG, FRA, DEU, ITA and ESP. `ENG_U` is byte-identical to `ENG_USA_EUR` and is treated as an alias.

## Confirmed layout anchors

- ROM offset `0x000000` contains the same ARM branch instruction in all six unique releases: `EA00007F`.
- The branch target is ROM offset `0x000204` (`0x08000204` in the GBA ROM address space).
- The standard GBA cartridge header occupies the beginning of the ROM.
- ROM offsets `0x000100-0x000203` contain the Game Freak cross-title metadata structure used as a directory of important Emerald data tables.
- Executable startup code begins at `0x000204`.
- No structurally valid GBA LZ10 stream was found inside Block 00, so this block is primarily startup code / metadata rather than compressed asset payload.

The English reference SHA-1 (`f3ae088181bf583e55daf962a92bb46f4f1d07b7`) matches the byte-exact target documented by the public `pret/pokeemerald` decompilation. Its linker order places `rom_header`, the Game Freak ROM header, and `crt0` at the beginning of ROM, which agrees with the offsets confirmed directly from the supplied ROM.

## Cross-release similarity

Only 5,040 of 65,536 byte positions (7.690430%) are identical across all six unique releases at the same offsets. This low six-way value is dominated by the Japanese build having a substantially different layout from the five western-language builds.

The western releases are highly similar inside Block 00:

| Pair | Same bytes |
| --- | ---: |
| ENG / FRA | 98.591614% |
| ENG / DEU | 98.252869% |
| ENG / ITA | 98.757935% |
| ENG / ESP | 98.318481% |
| ITA / ESP | 98.861694% |

The detailed pairwise matrix is stored in `block_00_pairwise_similarity.csv`.

## Pointer behavior

Aligned 32-bit values that point into `0x08000000-0x08FFFFFF` are common throughout this block:

- JPN: 638 ROM-pointer words
- ENG/FRA/DEU/ITA/ESP: 644 ROM-pointer words each

Comparing each western localization with ENG, 152 differing aligned words are ROM pointers in both builds and there are no one-sided ROM-pointer differences at those positions. This strongly indicates shared executable structure with relocated language-dependent data.

Dominant pointer deltas relative to ENG include:

- FRA: `+0x8FD4` at 94 positions, `+0x3F34` at 22 positions
- DEU: `+0x15D40` at 94 positions, `+0x110A4` at 22 positions
- ITA: `+0xF8C` at 94 positions, `-0x39AC` at 22 positions
- ESP: `+0x778C` at 94 positions, `+0x2534` at 22 positions

The complete delta census is stored in `block_00_pointer_deltas.csv`.

## Game Freak ROM header

`0x000100-0x000203` has now been parsed for every unique release. The structure directly exposes high-value semantic roots including:

- Pokémon front sprite table
- Pokémon back sprite table
- normal and shiny palette tables
- Pokémon icon table and icon palettes
- Pokémon species-name table
- move-name table
- decoration table
- species parameter table
- ability names and descriptions
- item table
- battle-move table
- Poké Ball graphics and palettes
- save-block sizes and important save-data offsets / flags

Machine-readable values are in `gf_rom_headers.json` and `gf_rom_headers.csv`. `tools/extract_gf_rom_header.py` regenerates them from verified local reference ROMs.

Selected ROM offsets:

| Root | JPN | ENG | FRA | DEU | ITA | ESP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pokémon names | `0x2EA31C` | `0x3185C8` | `0x3200F8` | `0x32CF38` | `0x317F8C` | `0x31E82C` |
| Move names | `0x2EACC4` | `0x31977C` | `0x3212AC` | `0x32E0EC` | `0x319140` | `0x31F9E0` |
| Species data | `0x2F0D54` | `0x3203CC` | `0x327F3C` | `0x334D8C` | `0x31FDCC` | `0x326688` |
| Ability names | `0x2EBDC4` | `0x31B6DB` | `0x32324E` | `0x33009E` | `0x31B0DB` | `0x321999` |
| Item table | `0x55CEE8` | `0x5839A0` | `0x587D6C` | `0x5946DC` | `0x58000C` | `0x58639C` |
| Battle moves | `0x2ED220` | `0x31C898` | `0x324408` | `0x331258` | `0x31C298` | `0x322B54` |
| Front sprite table | `0x2DDA1C` | `0x30A18C` | `0x311CBC` | `0x31EAFC` | `0x309B50` | `0x3103F0` |
| Back sprite table | `0x2D6148` | `0x3028B8` | `0x30A3E8` | `0x317228` | `0x30227C` | `0x308B1C` |

## Block 00 status

The block is no longer an unclassified 64 KiB region. Its first `0x204` bytes have stable semantic anchors, and the embedded metadata header provides direct pointers into the major content tables needed by later extraction passes.

Next work from these roots:

1. determine exact record counts / strides / termination rules for the name and gameplay-data tables
2. extract Pokémon names, move names, species data, abilities, items and moves into structured source
3. follow sprite table entries to compressed graphics and palettes, exporting viewable PNG alongside source metadata
4. continue executable lifting from startup into the remaining Block 00 code while preserving per-release relocation differences
5. verify each extracted table against all six unique reference releases
