# Generation IV → Pocket Monsters ROM census tools

`rom_content_census.py` reproduces the native metadata census used by this project without modifying or committing ROM binaries.

Input is a local JSON array whose records contain `path`, `platform`, `release_id`, and optionally `dump_id`. The ROM files remain outside Git.

For NDS/NTR inputs it walks FNT/FAT, records every named NitroFS file with offsets, size and SHA-1, detects NARC containers, and records their member counts. For GBA inputs it validates the header checksum, records long `00`/`FF` runs together with aligned ROM-pointer reference counts, and scans 4-byte-aligned structurally valid `0x10` LZ77 streams.

The GBA outputs are **candidate observations**. A padding run is not certified free space, and an LZ77 candidate is not a semantically identified game asset. Promotion into `DOMAINS`, Tsubaki `ASSETS`, or an allocation map requires pointer/code/data/compression/runtime verification.

Example:

```text
python rom_content_census.py local-roms.json --out census-output
```

Generated raw tables are reproducible working data. Canonical conclusions are promoted to the corresponding `LIBRARY/.../NATIVE`, `DOMAINS`, comparison, or project verification paths only after validation.
