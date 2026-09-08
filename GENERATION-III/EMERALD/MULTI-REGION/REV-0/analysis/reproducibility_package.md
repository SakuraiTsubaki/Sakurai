# Pokémon Emerald ROM reproducibility package

This package records the uploaded Generation III Emerald ROM set without redistributing ROM bytes.

## Coverage
- 7 source filenames recorded, 6 unique ROM images.
- All files are 16 MiB, software version 0, and pass the GBA header checksum.
- `EN-US-EU` and `EN-US-EU-ALIAS` are byte-identical.
- Every byte of every source image is represented by a deterministic 16384-byte chunk boundary and checksum in `analysis/chunks_16k.csv`.

## Reproducible outputs
- ROM identity: MD5, SHA-1, SHA-256, CRC32, size.
- GBA header fields and checksum validation.
- 16 KiB full-ROM chunk hashes, entropy, zero/FF density, distinct-byte count.
- 1 MiB navigation-region hashes.
- Per-byte-value frequency tables.
- Recognizable aligned GBA pointer-class counts.
- Pairwise whole-ROM byte similarity.
- Per-16-KiB difference density against the canonical English ROM.

## Reproduction
Place the original ROMs in `/mnt/data` using the recorded filenames and run:

```bash
python tools/audit_emerald.py
python tools/verify_roms.py /mnt/data
```

The ROMs themselves are intentionally excluded. The analysis tables are derivable metadata and the scripts make them reproducible from the local originals.

## Next structural layer
This byte-complete forensic layer is the foundation for conservative classification into ARM/Thumb code, pointer tables, text, graphics/palettes, maps/scripts, audio, and free/unused space. Those semantic classifications should keep offsets and evidence so they remain traceable to this package.
