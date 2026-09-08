# Pokémon Gold — JP — REV-0 ROM Identification

Source ROM is read-only and is **not stored in this corpus/repository**.

| Field | Value |
|---|---|
| Source filename | `Pocket Monsters Kin (Japan).gbc` |
| File size | 1,048,576 bytes |
| MD5 | `85be569fe89f58c40f60480313314c67` |
| SHA-1 | `8814f1039450a5d3684b1389f588ccd7ee7c3436` |
| SHA-256 | `7cfeceae00737a1f0713c9ab0b3a9e6eb8d05ff6002eb81308072a6f85e385e7` |
| CRC32 | `524478d4` |
| Header title | `POKEMON_GLDAAUJ` |
| CGB flag | `0x80` |
| Cartridge type | `0x10` (MBC3+TIMER+RAM+BATTERY) |
| ROM size code | `0x05` (1,048,576 bytes declared) |
| RAM size code | `0x03` (32,768 bytes declared) |
| Destination code | `0x00` |
| Version byte | `0x00` |
| 16 KiB banks | 64 |
| Header checksum | stored `0x48`, calculated `0x48` — PASS |
| Global checksum | stored `0x8A70`, calculated `0x8A70` — PASS |
| Fully zero 16 KiB banks | none |

## Reproducibility

Run `python tools/build_gold_repro_corpus.py --rom-dir <directory> --out <output>` from the MULTI corpus.
The generator recomputes every hash, header field, bank statistic, 4 KiB chunk hash, and comparison table from the local ROMs.
