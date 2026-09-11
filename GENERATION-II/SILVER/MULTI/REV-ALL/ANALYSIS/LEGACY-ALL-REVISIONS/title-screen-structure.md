# Pokémon Silver multi-region title screen structure

This analysis was derived directly from the eight project ROMs: JP Rev0, JP Rev A, EN, DE, FR, IT, ES, and KR. Original ROM binaries are not stored here.

## High-level construction

The Silver title screen is assembled at runtime rather than stored as one complete bitmap.

1. Clear palettes/tilemap/sprites and VRAM.
2. Decompress static title graphics into VRAM.
3. Copy the 4-tile Lugia trail region (the original Silver code copies 8 tiles; the extra 4 tiles overlap the first 64 compressed Lugia bytes but are not displayed).
4. Build/load a 32x18 title BG tilemap (576 bytes after decoding).
5. Build CGB attribute/palette layout.
6. Enable LCD.
7. Initialize the animated Lugia OBJ.
8. Initialize title scene state/timer and scanline SCX overrides.
9. Load SGB/CGB title palette layout and start title music.
10. The title loop scrolls the background/cloud region, advances title-scene state, animates Lugia, and handles title input/menu transition.

## ROM entry points and static-data references

| ROM | TitleScreen start | VRAM-load point | Static logo GFX | Secondary/top GFX | Lugia GFX | Trail | Tilemap |
|---|---:|---:|---|---|---|---|---|
| JP Rev0 | 0x00643A | 0x006459 | 39:4410 -> 9000 | none | 39:41E0 -> 8000 | 39:41A0 -> 8F80 | 39:497C, compressed |
| JP Rev A | 0x00643A | 0x006459 | 39:4410 -> 9000 | none | 39:41E0 -> 8000 | 39:41A0 -> 8F80 | 39:497C, compressed |
| EN | 0x006292 | 0x0062B1 | 26:4000 -> 9000 | 26:4498 -> 8800 | 39:4220 -> 8000 | 39:41E0 -> 8F80 | 26:462A, raw |
| DE | 0x0062CA | 0x0062E9 | 26:4000 -> 9000 | 26:4706 -> 8800 | 39:4220 -> 8000 | 39:41E0 -> 8F80 | 26:4898, raw |
| FR | 0x0062C7 | 0x0062E6 | 26:4000 -> 9000 | 26:4706 -> 8800 | 39:4220 -> 8000 | 39:41E0 -> 8F80 | 26:4898, raw |
| IT | 0x0062C4 | 0x0062E3 | 26:4000 -> 9000 | 26:4706 -> 8800 | 39:4220 -> 8000 | 39:41E0 -> 8F80 | 26:4898, raw |
| ES | 0x0062DC | 0x0062FB | 26:4000 -> 9000 | 26:4706 -> 8800 | 39:4220 -> 8000 | 39:41E0 -> 8F80 | 26:4898, raw |
| KR | 0x006326 | 0x006345 | 26:4000 -> 9000 | none | 39:4220 -> 8000 | 39:41E0 -> 8F80 | 26:47C6, compressed |

Bank:address is CPU-visible banked ROM addressing. File offsets can be calculated as `bank*0x4000 + (address-0x4000)` for ROMX addresses.

## GFX decompression sizes

| Group | Compressed bytes consumed | Decompressed bytes | Tiles |
|---|---:|---:|---:|
| JP title static GFX | 0x56B | 0x760 | 118 |
| KR title static GFX | 0x7C5 | 0x7F0 | 127 |
| EN lower/localized GFX | 0x497 | 0x700 | 112 |
| DE/FR/IT/ES lower/localized GFX | 0x705 | 0x700 | 112 |
| EN/DE/FR/IT/ES shared top Pokémon logo | 0x191 | 0x3C0 | 60 |
| Lugia OBJ GFX (all 8 ROMs) | 0x222 | 0x800 | 128 |

The decompressed Lugia GFX SHA-1 is identical across all eight ROMs (`2763f08020e5...`). The 0x80-byte trail-copy result is also identical across all eight ROMs (`f708f327e7c1...`). The western 60-tile top Pokémon logo is identical across EN/DE/FR/IT/ES (`c9eed6594f4b...`).

## Tilemap format split

All title tilemaps decode to a full 32x18 BG map = 576 bytes.

- EN/DE/FR/IT/ES: raw 576-byte tilemap followed by FF.
- JP/KR: compact command stream.
  - command bit7 = 0: repeat the following tile value `count` times.
  - command bit7 = 1: emit an incrementing tile sequence beginning at the following tile value for `count` tiles.
  - FF terminates the stream.

Western five ROMs decode to the exact same tilemap. JP and KR each have a distinct decoded tilemap.

## CGB title attribute layout

The palette/attribute layout also differs by title family.

- Western (EN/DE/FR/IT/ES): palette 1 covers rows 0-6 across the 20 visible columns; palette 3 overrides row 6 columns 5-14; palette 4 covers rows 12-16.
- JP: palette 1 covers rows 1-4 columns 1-14; palette 3 covers rows 1-4 columns 15-18; palette 2 covers row 5 columns 2-16; palette 4 covers rows 12-16.
- KR: palette 1 covers rows 0-4 columns 1-16; palette 3 covers rows 2-4 columns 16-18; palette 2 covers row 5 columns 1-15; palette 4 covers rows 12-16.

JP and KR use the same 5 title BG palettes, which differ from the western Silver title BG palettes. The 2 OBJ palettes used by the title are shared.

## Localization structure

- JP: one static title GFX stream contains the Japanese title composition.
- KR: one static title GFX stream contains the Korean title composition.
- EN/DE/FR/IT/ES: split structure.
  - shared 60-tile `POKéMON` top logo.
  - language/version-specific 112-tile lower/static set containing subtitle/copyright-related title graphics and shared lower-screen imagery.
- Western tilemap is shared; the per-language visual change is mainly in the lower/localized tile data.

Visible copyright years in the reconstructed backgrounds: JP 1999, EN 2000, DE/FR/IT/ES 2001, KR 2002.

## Revision result

Within the identified title initialization, palette/tilemap loader, and title GFX regions, JP Rev0 and JP Rev A are byte-identical. No title-specific revision difference was found in these blocks.

## Editing implication

For a multi-language rebuild, do not force every regional Silver ROM onto one existing title-data layout. A safer plan is to preserve each ROM family's loader architecture first, then optionally normalize it later to a unified expanded title-resource format after all references and animation behavior are mapped.