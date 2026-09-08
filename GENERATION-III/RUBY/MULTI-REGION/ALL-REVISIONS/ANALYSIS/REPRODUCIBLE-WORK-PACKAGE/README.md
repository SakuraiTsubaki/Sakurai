# Pokémon Ruby — Reproducible ROM Work Package

This package is a **binary-free reproducible analysis kit** for the 13 supplied Pokémon Ruby GBA ROMs.
It deliberately does not contain ROM bytes or extracted copyrighted assets. Given the original `.gba` files, it regenerates the manifests, whole-ROM page fingerprints, revision-difference maps, validated GBA LZ77 candidate index, verification results, and lossless split/rebuild checks.

## Repository path policy

`GENERATION-III / RUBY / LANGUAGE-REGION / REV / WORK-TYPE`

Analysis/research material belongs in **Sakurai**. Reusable implementation assets and user-authored patches belong in **Tsubaki**. Original ROM binaries are never committed.

## One-command reproduction

```bash
./run_analysis.sh /path/to/ruby-roms
```

The package uses Python 3 standard library only.

## Generated coverage

- ROM identity: size, MD5, SHA-1, SHA-256, GBA header fields and checksum verification.
- Full address-space coverage: one fingerprint row for every 64 KiB page of every ROM.
- Revision comparison: every contiguous changed byte range is mapped by offsets, lengths and before/after hashes without embedding ROM bytes.
- GBA LZ77 scan: every structurally valid `0x10` stream candidate is indexed with offset, decompressed length, compressed span and content hash.
- Pointer tooling: `scan_pointers.py` can generate a complete aligned or unaligned ROM-pointer candidate index from any supplied ROM.
- Lossless split/rebuild: `split_rebuild.py` splits a ROM into deterministic chunks and verifies byte-identical reconstruction.
- Regression test: all catalogued ROMs are rebuilt in-memory and checked against SHA-256.

## Important limitation

This is a reproducibility framework, not a full source-code disassembly. Machine-code/data semantic labeling, script command decoding, map/event tables, text codecs, graphics/palette extraction and symbol recovery are later layers that can be added while keeping the same manifests and address identities.
