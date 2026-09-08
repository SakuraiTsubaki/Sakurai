# Pokémon Gold — ES — REV-0 ROM Identification

Source ROM is read-only and is **not stored in this corpus/repository**.

| Field | Value |
|---|---|
| Source filename | `Pokemon - Edicion Oro (Spain).gbc` |
| File size | 2,097,152 bytes |
| MD5 | `9462bc81907e38c59acccd739690e6f9` |
| SHA-1 | `162ea54c6a3cff374642e6dd842f9bffac847e7b` |
| SHA-256 | `7b78e33a348a0729e38ee0fd778cf49b3e07c35d2175ebc74d8f9be41f41455b` |
| CRC32 | `3434a92b` |
| Header title | `POKEMON_GLDAAUS` |
| CGB flag | `0x80` |
| Cartridge type | `0x10` (MBC3+TIMER+RAM+BATTERY) |
| ROM size code | `0x06` (2,097,152 bytes declared) |
| RAM size code | `0x03` (32,768 bytes declared) |
| Destination code | `0x01` |
| Version byte | `0x00` |
| 16 KiB banks | 128 |
| Header checksum | stored `0x3D`, calculated `0x3D` — PASS |
| Global checksum | stored `0x9353`, calculated `0x9353` — PASS |
| Fully zero 16 KiB banks | 0x13, 0x22, 0x28, 0x29, 0x2C, 0x2D, 0x2F, 0x34, 0x35, 0x63, 0x67, 0x6F, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E |

## Reproducibility

Run `python tools/build_gold_repro_corpus.py --rom-dir <directory> --out <output>` from the MULTI corpus.
The generator recomputes every hash, header field, bank statistic, 4 KiB chunk hash, and comparison table from the local ROMs.
