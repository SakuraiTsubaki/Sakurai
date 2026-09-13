# Crystal localization source-set comparison

Seven uploaded source images were inspected byte-for-byte. Each image is 2 MiB (128 × 16 KiB banks), CGB-only, and declares cartridge type `0x10` (MBC3 + timer + RAM + battery).

The Japanese BXTJ-HV0 image declares 64 KiB RAM (`0x05`); the international images declare 32 KiB (`0x03`). BYTE-HV1 reports header version 1; all other images in this set report version 0.

See `TABLES/BANK-DIFF-MATRIX.csv` for pairwise identical/different bank counts.
