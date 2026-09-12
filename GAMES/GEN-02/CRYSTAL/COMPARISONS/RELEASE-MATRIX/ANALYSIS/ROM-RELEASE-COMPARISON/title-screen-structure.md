# Pokémon Crystal title-screen structure survey

Date: 2026-09-09
Scope: seven uploaded Pokémon Crystal retail ROMs (JP, EN v1.0, EN Rev A, DE, FR, ES, IT)
Original ROMs were read-only; no ROM binary is included in this report.

## 1. High-level structure

The Crystal title screen is assembled at runtime rather than stored as one flat bitmap.
It combines:

1. BG tile graphics for the Pokémon/version/copyright logo
2. BG attribute maps for per-line palette selection and the logo gradient
3. VRAM bank 1 graphics for the four-frame running Suicune animation
4. OBJ/OAM graphics for the descending crystal foreground
5. 16 CGB palettes (8 BG + 8 OBJ)
6. Per-scanline SCX overrides for the left/right title entrance effect
7. A title-state machine (entrance -> timer -> main -> end)

The English disassembly in pret/pokecrystal confirms the same conceptual structure seen in the uploaded ROM bytes.

## 2. Common title initializer

All inspected ROMs enter the main title initializer at:

- ROM bank: $43
- CPU address: $6D67
- File offset: $10ED67

This routine clears palettes/sprites/tilemaps, disables the LCD, loads title graphics into VRAM, builds BG tile and attribute maps, copies palettes, initializes SCX/SCY/WX/WY, configures 8x16 OBJ mode, initializes Suicune/crystal animation, then plays the title entrance SFX.

## 3. Asset locations

### Western layout (EN/DE/FR/ES/IT)

These five language families use the same physical title layout and the same asset addresses.
EN v1.0 and EN Rev A are byte-identical in bank $43.

| Asset | Bank:CPU | File offset | Compressed bytes | Decompressed bytes | Tiles |
|---|---:|---:|---:|---:|---:|
| Running Suicune | 43:6F46 | 10EF46 | 981 | 4096 | 256 |
| Title logo | 43:7326 | 10F326 | 2503 | 2496 | 156 |
| Crystal foreground | 43:7CEE | 10FCEE | 489 | 960 | 60 |
| Title palettes | 43:7EDE | 10FEDE | 128 | 128 | 16 palettes |

The logo expands to 156 2bpp tiles. The original source layout corresponds to 20 x 8 tiles with four blank trailing tiles trimmed from storage.

Western logo placement:

- Pokémon logo + localized version label: x=0, y=3, 20 x 7 tiles, first tile ID $80
- Copyright line: x=3, y=0, 13 x 1 tiles, first tile ID $0C
- Version-label palette override: x=5, y=9, width 11, BG palette 1

Localized title labels observed from the ROM graphics:

- EN: `CRYSTAL VERSION`
- DE: `KRISTALL-EDITION`
- FR: `VERSION CRISTAL`
- ES: `EDICIÓN CRISTAL`
- IT: `VERSIONE CRISTALLO`

DE/FR/ES/IT share one title palette set. EN differs only in BG palette 1 color #2:

- EN: RGB15 (15,16,31)
- DE/FR/ES/IT: RGB15 (2,3,30)

### Japanese layout

The Japanese title uses a different logo layout and therefore different offsets after the common Suicune block.

| Asset | Bank:CPU | File offset | Compressed bytes | Decompressed bytes | Tiles |
|---|---:|---:|---:|---:|---:|
| Running Suicune | 43:6F4B | 10EF4B | 981 | 4096 | 256 |
| Title logo | 43:732B | 10F32B | 1566 | 2304 | 144 |
| Crystal foreground | 43:794B | 10F94B | 489 | 960 | 60 |
| Title palettes | 43:7B3B | 10FB3B | 128 | 128 | 16 palettes |

Japanese logo placement is split into three blocks instead of one continuous western block:

- x=3, y=3, 14 x 1 tiles, first tile ID $81: small `POCKET MONSTERS`
- x=2, y=4, 16 x 5 tiles, first tile ID $90: large Japanese title logo
- x=5, y=9, 10 x 2 tiles, first tile ID $E3: `クリスタルバージョン`
- copyright: x=3, y=0, 13 x 1 tiles, first tile ID $00

The Japanese BG palette gradient is also structurally different from the western gradient.

## 4. Shared animated assets

The decompressed Running Suicune data is identical across all seven ROMs:

- SHA-1: `4120d9269ab0...`
- 4096 bytes = 256 tiles
- Four animation frames are selected every 8 frames using base tile IDs `$80`, `$88`, `$00`, `$08`.
- Each displayed Suicune frame is an 8 x 6 tile region.

The crystal foreground is also identical across all seven ROMs:

- SHA-1: `d104b7cf8cf5...`
- 960 bytes = 60 tiles
- 30 OAM objects in 8x16 mode (5 rows x 6 objects) consume 60 tiles.
- The title animation moves all 30 objects downward by two pixels per update until the crystal reaches its final position.

## 5. BG/OBJ and animation behavior

The western initializer assigns logo gradient palettes by scanline rows:

- rows 3-4 -> BG palette 2
- row 5 -> BG palette 3
- row 6 -> BG palette 4
- row 7 -> BG palette 5
- rows 8-9 -> BG palette 6
- localized version label area -> BG palette 1
- copyright -> BG palette 7

The lower six title rows use VRAM bank 1 for the Suicune tiles.

The entrance effect uses the `wLYOverrides` buffer and LCD STAT-driven `SCX` writes. Alternating scanlines begin offset by +112 / -112 pixels and converge toward the normal position, creating the split left/right logo entrance.

The title timer is initialized to `73 * 60 + 36` frames (4416 frames, about 73.6 seconds at 60 Hz) before the title loop times out and advances.

## 6. Revision / localization conclusions

- EN v1.0 and EN Rev A: title bank is identical; Rev A did not alter the title screen.
- DE/FR/ES/IT: same western engine layout and same asset offsets as EN; only localized logo pixels and one shared palette variant differ.
- JP: same core title engine concept, but the logo renderer/layout and palette gradient are genuinely different; the Japanese logo is 144 tiles instead of 156.
- Suicune and foreground crystal graphics are common across every inspected region.

## 7. Implication for a new Korean title

A Korean Crystal title does not need to be constrained to a single text string replacement. There are two viable native patterns already present in retail ROMs:

1. Western pattern: one 20-tile-wide composite Pokémon logo + Korean version subtitle.
2. Japanese pattern: multiple independently positioned logo/subtitle blocks, which gives more freedom for Korean typography.

For a Korean title that visually follows the official Korean Gold/Silver style, the safest implementation path is to preserve the existing Crystal animation engine (Suicune, crystal OBJ, palettes/SCX effects) and replace only the title-logo tile payload, tile placement table/code, and affected palette rows.

## 8. External technical cross-check

Cross-checked against pret/pokecrystal:

- `engine/movie/title.asm`
- `engine/menus/intro_menu.asm`
- `gfx/title/title.pal`
- `gfx/lz.mk`
- project Makefile title-GFX rules

No external ROM binary was used.
