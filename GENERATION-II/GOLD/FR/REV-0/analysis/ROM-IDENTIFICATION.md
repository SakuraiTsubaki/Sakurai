# Pokémon Gold — FR — REV-0 ROM Identification

Source ROM is read-only and is **not stored in this corpus/repository**.

| Field | Value |
|---|---|
| Source filename | `Pokemon - Version Or (France).gbc` |
| File size | 2,097,152 bytes |
| MD5 | `9af19423c5fa3dbe4fdcc78d2bc7d1c0` |
| SHA-1 | `c147c0d8c2b71b7628a7233436f5c052b5b17081` |
| SHA-256 | `6103cadf2ae505f4b489a8a414c8db27a2307d797ddf8a3a848659b591dd4023` |
| CRC32 | `37a70702` |
| Header title | `POKEMON_GLDAAUF` |
| CGB flag | `0x80` |
| Cartridge type | `0x10` (MBC3+TIMER+RAM+BATTERY) |
| ROM size code | `0x06` (2,097,152 bytes declared) |
| RAM size code | `0x03` (32,768 bytes declared) |
| Destination code | `0x01` |
| Version byte | `0x00` |
| 16 KiB banks | 128 |
| Header checksum | stored `0x4A`, calculated `0x4A` — PASS |
| Global checksum | stored `0x6FC6`, calculated `0x6FC6` — PASS |
| Fully zero 16 KiB banks | 0x13, 0x22, 0x28, 0x29, 0x2C, 0x2D, 0x2F, 0x34, 0x35, 0x63, 0x67, 0x6F, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E |

## Reproducibility

Run `python tools/build_gold_repro_corpus.py --rom-dir <directory> --out <output>` from the MULTI corpus.
The generator recomputes every hash, header field, bank statistic, 4 KiB chunk hash, and comparison table from the local ROMs.
