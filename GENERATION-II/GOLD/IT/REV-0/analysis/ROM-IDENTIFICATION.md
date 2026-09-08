# Pokémon Gold — IT — REV-0 ROM Identification

Source ROM is read-only and is **not stored in this corpus/repository**.

| Field | Value |
|---|---|
| Source filename | `Pokemon - Versione Oro (Italy).gbc` |
| File size | 2,097,152 bytes |
| MD5 | `89bb59dc49b59b0cd30b7384d9860bb8` |
| SHA-1 | `032608fe8947b627584a4a0eccc7bf9ad3588426` |
| SHA-256 | `367e606f82b9e2e16d0cc8011c5ba2df1862da574e57ffd66e786a82af5b6e22` |
| CRC32 | `4c184ce3` |
| Header title | `POKEMON_GLDAAUI` |
| CGB flag | `0x80` |
| Cartridge type | `0x10` (MBC3+TIMER+RAM+BATTERY) |
| ROM size code | `0x06` (2,097,152 bytes declared) |
| RAM size code | `0x03` (32,768 bytes declared) |
| Destination code | `0x01` |
| Version byte | `0x00` |
| 16 KiB banks | 128 |
| Header checksum | stored `0x47`, calculated `0x47` — PASS |
| Global checksum | stored `0xCE0C`, calculated `0xCE0C` — PASS |
| Fully zero 16 KiB banks | 0x13, 0x22, 0x28, 0x29, 0x2C, 0x2D, 0x2F, 0x34, 0x35, 0x63, 0x67, 0x6F, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E |

## Reproducibility

Run `python tools/build_gold_repro_corpus.py --rom-dir <directory> --out <output>` from the MULTI corpus.
The generator recomputes every hash, header field, bank statistic, 4 KiB chunk hash, and comparison table from the local ROMs.
