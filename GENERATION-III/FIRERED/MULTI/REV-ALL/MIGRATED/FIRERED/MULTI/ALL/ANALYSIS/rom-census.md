# Pokémon FireRed ROM Census

Date: 2026-09-09

This manifest records identification metadata only. Original ROM binaries are not stored in this repository.

## Uploaded set

| Language / Region | Revision | File | Size | Game code | Internal title | Maker | Header version | Header checksum | CRC32 | SHA-1 | SHA-256 |
|---|---:|---|---:|---|---|---|---:|---|---|---|---|
| Japan | Rev 0 | `Pocket Monsters - Fire Red (Japan).gba` | 16,777,216 | BPRJ | POKEMON FIRE | 01 | 0 | 0x63 valid | 3B2056E9 | 04139887b6cd8f53269aca098295b006ddba6cfe | 1e4af44b0c75cc8649bfb8649dc4ae5850bf5358bd6b9cd0bf779c99f9db1486 |
| Japan | Rev 1 | `Pocket Monsters - Fire Red (Japan) (Rev 1).gba` | 16,777,216 | BPRJ | POKEMON FIRE | 01 | 1 | 0x62 valid | BB640DF7 | 7c7107b87c3ccf6e3dbceb9cf80ceeffb25a1857 | cec5fc4dbe38cd8026bd6664a1a041d9dc91e8d4249bab04e7bde70c3cdf4e06 |
| English (USA) | Rev 0 | `Pokemon - Fire Red Version (USA).gba` | 16,777,216 | BPRE | POKEMON FIRE | 01 | 0 | 0x68 valid | 07C5CC23 | d3b806453369b4b086c792eb3c05a02f00057f50 | b59a65bb439b7dfdf2ffbbe5102be03de2501a71f5e081eec1c76f9d2ef3ba00 |
| English (USA/Europe) | Rev 1 | `Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba` | 16,777,216 | BPRE | POKEMON FIRE | 01 | 1 | 0x67 valid | 29A4CDDF | c4d0119d9bcb36687f41a8f7ca72ab7af60558e4 | 6d306e01ba04907efaa0611a32fee3b440a1e8ac8b4e0acdd223dc9281afa170 |
| Germany | Rev 0 | `Pokemon - Feuerrote Edition (Germany).gba` | 16,777,216 | BPRD | POKEMON FIRE | 01 | 0 | 0x69 valid | 1A81EEDF | 18a3758ceeef2c77b315144be2c3910d6f1f69fe | eed4fb0242bcbb6e0b0b80b197b47e3aec99ef4c5562cc45bae50ae86b970507 |
| France | Rev 0 | `Pokemon - Version Rouge Feu (France).gba` | 16,777,216 | BPRF | POKEMON FIRE | 01 | 0 | 0x67 valid | 5DC668F6 | fc663907256f06a3a09e2d6b967bc9af4919f111 | 245866842349cedbe2a034c6d20438d26d18b627b3d0909d7cb795fc87d7675a |
| Italy | Rev 0 | `Pokemon - Versione Rosso Fuoco (Italy).gba` | 16,777,216 | BPRI | POKEMON FIRE | 01 | 0 | 0x64 valid | 73A72167 | 66a9d415205321376b4318534c0dce5f69d28362 | ad52b593ef0c7439e1409d3f0a1ec3ff865a494ca46c2184fe65573759838f3a |
| Spain | Rev 0 | `Pokemon - Edicion Rojo Fuego (Spain).gba` | 16,777,216 | BPRS | POKEMON FIRE | 01 | 0 | 0x5A valid | 9F08064E | ab8f6bfe0ccdaf41188cd015c8c74c314d02296a | ab696c065639e4d73c3c3ed9d4fbf9c7fed593761f3b6746256ff82465596554 |

## Header conclusions

- All eight images are exactly 16 MiB (0x01000000 bytes).
- All eight use internal title `POKEMON FIRE` and maker code `01`.
- Region/language is distinguished by game code: BPRJ (Japan), BPRE (English), BPRD (German), BPRF (French), BPRI (Italian), BPRS (Spanish).
- The GBA header revision byte at 0xBC confirms Rev 0 versus Rev 1 for the Japanese and English pairs.
- The header complement/checksum at 0xBD validates for every uploaded image.

## Raw Rev 0 ↔ Rev 1 comparison

A byte-for-byte comparison was also made as a first-pass locator only:

- Japan Rev 0 ↔ Rev 1: 7,016,197 differing bytes, spread across 475 separate 16 KiB analysis chunks; first difference at 0x000000BC, last at 0x00FDFFFE.
- English Rev 0 ↔ Rev 1: 6,367,135 differing bytes, spread across 456 separate 16 KiB analysis chunks; first difference at 0x000000BC, last at 0x00FFFFFF.

These counts must **not** be interpreted as the number of bug fixes or semantic edits. Large compiled-ROM differences can result from relocation, rebuilt data, pointer changes, compression, padding, and layout changes. Semantic revision analysis requires disassembly/data-structure-aware comparison.

## Next analysis stage

Use these eight hashes as immutable source identities, then perform a full ROM map and disassembly-oriented census by region/revision. For GBA, 16 KiB or other fixed-size chunks are useful analysis units, but they are not hardware ROM banks in the Game Boy / Game Boy Color sense.
