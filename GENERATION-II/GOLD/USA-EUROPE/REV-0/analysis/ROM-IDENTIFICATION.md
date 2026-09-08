# Pokémon Gold — USA-EUROPE — REV-0 ROM Identification

Source ROM is read-only and is **not stored in this corpus/repository**.

| Field | Value |
|---|---|
| Source filename | `Pokemon - Gold Version (USA, Europe).gbc` |
| File size | 2,097,152 bytes |
| MD5 | `a6924ce1f9ad2228e1c6580779b23878` |
| SHA-1 | `d8b8a3600a465308c9953dfa04f0081c05bdcb94` |
| SHA-256 | `fb0016d27b1e5374e1ec9fcad60e6628d8646103b5313ca683417f52b97e7e4e` |
| CRC32 | `6bde3c3e` |
| Header title | `POKEMON_GLDAAUE` |
| CGB flag | `0x80` |
| Cartridge type | `0x10` (MBC3+TIMER+RAM+BATTERY) |
| ROM size code | `0x06` (2,097,152 bytes declared) |
| RAM size code | `0x03` (32,768 bytes declared) |
| Destination code | `0x01` |
| Version byte | `0x00` |
| 16 KiB banks | 128 |
| Header checksum | stored `0x4B`, calculated `0x4B` — PASS |
| Global checksum | stored `0x682D`, calculated `0x682D` — PASS |
| Fully zero 16 KiB banks | 0x13, 0x22, 0x27, 0x28, 0x29, 0x2C, 0x2D, 0x2F, 0x34, 0x35, 0x58, 0x63, 0x67, 0x6F, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E |

## Reproducibility

Run `python tools/build_gold_repro_corpus.py --rom-dir <directory> --out <output>` from the MULTI corpus.
The generator recomputes every hash, header field, bank statistic, 4 KiB chunk hash, and comparison table from the local ROMs.
