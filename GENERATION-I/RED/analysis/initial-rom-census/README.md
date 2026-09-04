# Pokémon Red ROM census — initial inventory

Date: 2026-09-05 (Asia/Seoul)

## Scope

This inventory covers the eight project ROM files currently mounted for the Red family: Japanese Rev 0 / Rev A plus English, German, French, Italian, and Spanish localized builds. ROM binaries are intentionally excluded from GitHub. Only metadata, hashes, checksums, and aggregate comparison results are stored here.

## Inputs

| File | Size | Banks | Header title | Version | Cartridge | SGB | SHA-1 |
|---|---:|---:|---|---:|---|---:|---|
| Pocket Monsters - Aka (Japan) (SGB Enhanced).gb | 524,288 B | 32 | `POKEMON RED` | 0 | `0x03 MBC1+RAM+BATTERY` | `0x03` | `0623ad12f48c259447980d68bd85ddbf8204b2cd` |
| Pocket Monsters - Aka (Japan) (Rev A) (SGB Enhanced).gb | 524,288 B | 32 | `POKEMON RED` | 1 | `0x03 MBC1+RAM+BATTERY` | `0x03` | `ef74c79cded14204ac79e77f4964d9cb25003120` |
| Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb | 1,048,576 B | 64 | `POKEMON RED` | 0 | `0x13 MBC3+RAM+BATTERY` | `0x03` | `ea9bcae617fdf159b045185467ae58b2e4a48b9a` |
| Pokemon - Red Version (USA, Europe) (SGB Enhanced) - 복사본.gb | 1,048,576 B | 64 | `POKEMON RED` | 0 | `0x13 MBC3+RAM+BATTERY` | `0x03` | `ea9bcae617fdf159b045185467ae58b2e4a48b9a` |
| Pokemon - Rote Edition (Germany) (SGB Enhanced).gb | 1,048,576 B | 64 | `POKEMON RED` | 0 | `0x1B MBC5+RAM+BATTERY` | `0x03` | `87d523fe1a0c548db7c5477b451ddec1eb083c06` |
| Pokemon - Version Rouge (France) (SGB Enhanced).gb | 1,048,576 B | 64 | `POKEMON RED` | 0 | `0x1B MBC5+RAM+BATTERY` | `0x03` | `47a7622fa30e6402a3891fe65b3a930bf9bd7aec` |
| Pokemon - Versione Rossa (Italy) (SGB Enhanced).gb | 1,048,576 B | 64 | `POKEMON RED` | 0 | `0x1B MBC5+RAM+BATTERY` | `0x03` | `65b97cf8f2f1cff711a6d08c6c894c8ce65ce522` |
| Pokemon - Edicion Roja (Spain) (SGB Enhanced).gb | 1,048,576 B | 64 | `POKEMON RED` | 0 | `0x1B MBC5+RAM+BATTERY` | `0x03` | `fc17c5b904d551b1b908054ccd1c493f755f832a` |

All eight files have valid Game Boy header checksums and valid global checksums. Declared ROM size matches physical file size in every case. All report 32 KiB cartridge RAM and SGB support.

## Deduplication

The two English files are byte-for-byte identical. The eight filenames therefore represent **seven unique ROM byte images**.

## Japanese Rev 0 ↔ Rev A

- Total differing bytes: **46,167 / 524,288 (8.805656%)**
- Only bank `0x1B` is completely identical between the two Japanese revisions.
- The delta is distributed across almost the whole image; it is not a header-only revision.

| Bank | Different bytes | Difference |
|---:|---:|---:|
| 00 | 13,108 | 80.0049% |
| 01 | 11,804 | 72.0459% |
| 02 | 18 | 0.1099% |
| 03 | 366 | 2.2339% |
| 04 | 233 | 1.4221% |
| 05 | 83 | 0.5066% |
| 06 | 348 | 2.1240% |
| 07 | 560 | 3.4180% |
| 08 | 60 | 0.3662% |
| 09 | 519 | 3.1677% |
| 0A | 14 | 0.0854% |
| 0B | 13 | 0.0793% |
| 0C | 32 | 0.1953% |
| 0D | 65 | 0.3967% |
| 0E | 79 | 0.4822% |
| 0F | 15,402 | 94.0063% |
| 10 | 135 | 0.8240% |
| 11 | 307 | 1.8738% |
| 12 | 406 | 2.4780% |
| 13 | 36 | 0.2197% |
| 14 | 379 | 2.3132% |
| 15 | 313 | 1.9104% |
| 16 | 330 | 2.0142% |
| 17 | 397 | 2.4231% |
| 18 | 359 | 2.1912% |
| 19 | 32 | 0.1953% |
| 1A | 2 | 0.0122% |
| 1B | 0 | 0.0000% |
| 1C | 203 | 1.2390% |
| 1D | 425 | 2.5940% |
| 1E | 132 | 0.8057% |
| 1F | 7 | 0.0427% |

## Cross-language structural anchors

- Bank `0x1B` is byte-identical across Japanese Rev 0, Japanese Rev A, EN, DE, FR, IT, and ES. This is a strong cross-build anchor for later ownership mapping.
- The localized 1 MiB builds have banks `0x2D`–`0x3F` completely filled with `0x00`: **19 banks / 311,296 bytes**. This is recorded as trailing zero-fill only; it must not be treated as confirmed reusable free space until references and bank-switch behavior are mapped.
- English uses MBC3 while DE/FR/IT/ES use MBC5, so localization comparison must account for banking implementation differences rather than assuming identical executable layouts.

## Initial conclusions

1. Japanese Rev A is a broad internal revision, not a tiny patch.
2. Western localization expanded the ROM from 512 KiB to 1 MiB and changed mapper strategy.
3. The five Western builds share a large trailing zero-filled region, but actual safe free-space certification requires a reference census.
4. The common `0x1B` bank gives a reliable fixed point for cross-language alignment.
5. The duplicated English copy should be excluded from future expensive comparisons while retained in the manifest as an uploaded input.

## Next census layers

1. Bank ownership map: code, text, maps, graphics, audio, tables, padding/unused candidates.
2. Pointer/reference census, including banked references.
3. Character tables, fonts, text engine, name-entry and UI string storage.
4. Cross-language executable/data relocation map.
5. Map/event/NPC/trainer/wild/item/battle/system data census.
6. Semantic Rev 0 ↔ Rev A diff after ownership mapping.

## Reproducibility

`tools/rom_census.py` reproduces the ROM-safe inventory from locally supplied `.gb` files. It does not contain or emit ROM payload bytes.
