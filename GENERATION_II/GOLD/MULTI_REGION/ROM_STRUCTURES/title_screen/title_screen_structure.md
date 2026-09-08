# Pokémon Gold — Title Screen Structure Survey

## Scope

ROM-level comparison of the title-screen implementation across the uploaded Pokémon Gold regional ROMs. Original ROM binaries remain read-only and are not uploaded.

## Core structure

The Gold title screen is composed of separate runtime/data components rather than one monolithic graphic:

- title-screen loader/runtime code
- logo GFX
- title tilemap
- Ho-Oh title trail
- Ho-Oh sprite GFX
- CGB/SGB/DMG palette handling
- title animation/timer state

The pret `pokegold` disassembly confirms the western Gold implementation loads `TitleScreenGFX1`, `TitleScreenGFX2`, `TitleScreenGFX4`, and `TitleScreenGFX3` into distinct VRAM regions, then loads palettes and the title tilemap.

## Regional ROM mapping

| Version | Title loader | Main logo GFX | Additional GFX | Tilemap | Ho-Oh trail | Ho-Oh GFX |
|---|---:|---:|---:|---:|---:|---:|
| JP v1.0 | 0x6469 | 0xE45C8 | — | 0xE4AFC | 0xE41A0 | 0xE4220 |
| JP Rev A | 0x6469 | 0xE45C8 | — | 0xE4AFC | 0xE41A0 | 0xE4220 |
| USA/Europe | 0x62C0 | 0x98000 | 0x98476 | 0x98616 | 0xE41E0 | 0xE4260 |
| Germany | 0x62F7 | 0x98000 | 0x98706 | 0x988A6 | 0xE41E0 | 0xE4260 |
| France | 0x62F5 | 0x98000 | 0x98706 | 0x988A6 | 0xE41E0 | 0xE4260 |
| Italy | 0x62F2 | 0x98000 | 0x98706 | 0x988A6 | 0xE41E0 | 0xE4260 |
| Spain | 0x6308 | 0x98000 | 0x98706 | 0x988A6 | 0xE41E0 | 0xE4260 |
| Korea | 0x6355 | 0x98000 | — | 0x987C2 | 0xE41E0 | 0xE4260 |

## Japan

Japanese Gold uses one large compressed title-logo graphic rather than the western split-logo scheme.

- logo stream: file offset `0xE45C8`
- decompressed size: 1,824 bytes = 114 2bpp tiles
- tilemap stream: file offset `0xE4AFC`
- decompressed tilemap: 576 bytes = 32×18 BG map

JP v1.0 and Rev A use the same title-screen code/data mapping identified above.

## Korea

Korean Gold also uses a single title-logo graphic. Its title routine does not load the western `TitleScreenGFX2` split-logo component.

- logo stream: file offset `0x98000`
- decompressed size: 2,032 bytes = 127 2bpp tiles
- tilemap stream: file offset `0x987C2`
- decompressed tilemap: 576 bytes = 32×18 BG map

The Korean title tilemap uses the compact title-map encoding family seen in the Japanese version, rather than the 577-byte western raw tilemap representation.

## Western releases

USA/Europe Gold uses the split-logo arrangement represented by pret/pokegold:

- `GFX1` at `0x98000`: 1,792 bytes = 112 tiles
- `GFX2` at `0x98476`: 960 bytes = 60 tiles
- tilemap at `0x98616`: 577 bytes (576-byte 32×18 map plus terminator)

German/French/Italian/Spanish builds share the additional-logo/tilemap placement shown in the table while localizing the version/logo content in the primary GFX block.

## Ho-Oh layer

The Ho-Oh display is separable from the title logo:

- Ho-Oh trail: 128 bytes = 8 tiles
- Ho-Oh sprite after decompression: 1,408 bytes = 88 tiles

This makes title-logo replacement possible without replacing the Ho-Oh animation assets.

## Palette structure

The CGB title layout uses five BG palettes and two OBJ palettes in the canonical Gold disassembly.

## Practical model

- JP: `single logo GFX → compressed 32×18 tilemap → Ho-Oh trail → Ho-Oh`
- KR: `single logo GFX → compressed 32×18 tilemap → Ho-Oh trail → Ho-Oh`
- EN/DE/FR/IT/ES: `primary/version GFX → upper Pokémon-logo GFX → raw tilemap → Ho-Oh trail → Ho-Oh`

## Source-reference notes

Canonical implementation reference: pret/pokegold (`engine/movie/title.asm`, `gfx/misc.asm`, `engine/gfx/color.asm`, `engine/gfx/cgb_layouts.asm`). ROM offsets and regional differences above were derived from the uploaded ROM set and cross-checked against the canonical western disassembly.
