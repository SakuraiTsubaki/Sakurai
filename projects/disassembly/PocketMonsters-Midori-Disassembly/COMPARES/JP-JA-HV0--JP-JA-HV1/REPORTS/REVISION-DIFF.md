# Pocket Monsters Midori revision comparison

Canonical releases:

- `JP-JA-HV0` — `DUMP-SHA256-6576B4E0979E93D4`
- `JP-JA-HV1` — `DUMP-SHA256-3F0DC460CA8D06BE`

Both observed images are 524,288-byte (512 KiB) Japanese Game Boy ROMs titled `POKEMON GREEN`, with SGB support and valid header/global checksums. The header version is 0 for HV0 and 1 for HV1.

Direct byte comparison found 46,168 changed bytes (8.80584717% of the image) across 5,436 contiguous changed ranges. The first changed byte is at `0x000051`; the last is at `0x07FFFF`. Bank `1B` is byte-identical between revisions. The three largest per-bank changes are bank `0F` (15,403 bytes), bank `00` (13,109), and bank `01` (11,803).

ROM binaries and lossless whole-ROM bank/chunk decompositions are not committed. This repository stores identity, hashes, analyses, tables, reports, and reproducibility metadata.
