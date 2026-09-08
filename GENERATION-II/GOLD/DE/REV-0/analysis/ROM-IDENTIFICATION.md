# Pokémon Gold — DE — REV-0 ROM Identification

Source ROM is read-only and is **not stored in this corpus/repository**.

| Field | Value |
|---|---|
| Source filename | `Pokemon - Goldene Edition (Germany).gbc` |
| File size | 2,097,152 bytes |
| MD5 | `7542ec9b695d4fe38adfdaaa57364d83` |
| SHA-1 | `9254195d461ea942eaaa08cc4b83de3cf82aea0d` |
| SHA-256 | `542f275f8632ef5265e5cde80a8ba1f0ec11ce714ef9d773088a92680bd17d73` |
| CRC32 | `4889dfaa` |
| Header title | `POKEMON_GLDAAUD` |
| CGB flag | `0x80` |
| Cartridge type | `0x10` (MBC3+TIMER+RAM+BATTERY) |
| ROM size code | `0x06` (2,097,152 bytes declared) |
| RAM size code | `0x03` (32,768 bytes declared) |
| Destination code | `0x01` |
| Version byte | `0x00` |
| 16 KiB banks | 128 |
| Header checksum | stored `0x4C`, calculated `0x4C` — PASS |
| Global checksum | stored `0xDC97`, calculated `0xDC97` — PASS |
| Fully zero 16 KiB banks | 0x13, 0x22, 0x28, 0x29, 0x2C, 0x2D, 0x2F, 0x34, 0x35, 0x63, 0x67, 0x6F, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E |

## Reproducibility

Run `python tools/build_gold_repro_corpus.py --rom-dir <directory> --out <output>` from the MULTI corpus.
The generator recomputes every hash, header field, bank statistic, 4 KiB chunk hash, and comparison table from the local ROMs.
