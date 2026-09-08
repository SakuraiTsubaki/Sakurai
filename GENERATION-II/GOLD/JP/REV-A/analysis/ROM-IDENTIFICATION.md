# Pokémon Gold — JP — REV-A ROM Identification

Source ROM is read-only and is **not stored in this corpus/repository**.

| Field | Value |
|---|---|
| Source filename | `Pocket Monsters Kin (Japan) (Rev A).gbc` |
| File size | 1,048,576 bytes |
| MD5 | `79aece8a042e4fa57aba9455c4d21a97` |
| SHA-1 | `a222402235d484ee8e39f3f31bae57cf13daf585` |
| SHA-256 | `27a07a1d3faf9c6a0b1b60d5e88ee3a4159a751a47b4c46ab09f1202d52bac3e` |
| CRC32 | `4ef7f2a5` |
| Header title | `POKEMON_GLDAAUJ` |
| CGB flag | `0x80` |
| Cartridge type | `0x10` (MBC3+TIMER+RAM+BATTERY) |
| ROM size code | `0x05` (1,048,576 bytes declared) |
| RAM size code | `0x03` (32,768 bytes declared) |
| Destination code | `0x00` |
| Version byte | `0x01` |
| 16 KiB banks | 64 |
| Header checksum | stored `0x47`, calculated `0x47` — PASS |
| Global checksum | stored `0x8460`, calculated `0x8460` — PASS |
| Fully zero 16 KiB banks | none |

## Reproducibility

Run `python tools/build_gold_repro_corpus.py --rom-dir <directory> --out <output>` from the MULTI corpus.
The generator recomputes every hash, header field, bank statistic, 4 KiB chunk hash, and comparison table from the local ROMs.
