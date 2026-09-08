# Pokémon Gold — KR — REV-0 ROM Identification

Source ROM is read-only and is **not stored in this corpus/repository**.

| Field | Value |
|---|---|
| Source filename | `Pocket Monsters Geum (Korea).gbc` |
| File size | 2,097,152 bytes |
| MD5 | `82bd1d9171e60f147d9eeea13ef07a12` |
| SHA-1 | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` |
| SHA-256 | `9c273e86e6120c6a038160ccb0153b8b20425b84fc08a496281c1d1bcac492f6` |
| CRC32 | `249a7a66` |
| Header title | `POKEMON_GLDAAUK` |
| CGB flag | `0xC0` |
| Cartridge type | `0x10` (MBC3+TIMER+RAM+BATTERY) |
| ROM size code | `0x06` (2,097,152 bytes declared) |
| RAM size code | `0x03` (32,768 bytes declared) |
| Destination code | `0x01` |
| Version byte | `0x00` |
| 16 KiB banks | 128 |
| Header checksum | stored `0x08`, calculated `0x08` — PASS |
| Global checksum | stored `0x778A`, calculated `0x778A` — PASS |
| Fully zero 16 KiB banks | 0x13, 0x22, 0x27, 0x28, 0x29, 0x2C, 0x2D, 0x2F, 0x34, 0x35, 0x58, 0x63, 0x67, 0x6A, 0x6B, 0x6F, 0x73, 0x74, 0x75, 0x76, 0x77, 0x7C, 0x7D, 0x7E |

## Reproducibility

Run `python tools/build_gold_repro_corpus.py --rom-dir <directory> --out <output>` from the MULTI corpus.
The generator recomputes every hash, header field, bank statistic, 4 KiB chunk hash, and comparison table from the local ROMs.
