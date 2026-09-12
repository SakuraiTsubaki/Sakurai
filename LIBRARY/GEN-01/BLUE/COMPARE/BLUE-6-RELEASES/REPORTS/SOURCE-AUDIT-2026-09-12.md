# Pokémon Blue six-ROM source audit

Generated from the six supplied ROM images. No ROM bytes are included in this report.

## Release set

- JP-JA-HV0: 524,288 bytes / 32 banks.
- Five western releases: 1,048,576 bytes / 64 banks each.
- Header and global checksums validate for all six images.

## Cross-release identity

- Same-index banks byte-identical across all six releases: 1B.
- Same-index banks byte-identical across all five western releases: 1B, 2D, 2E, 2F, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 3A, 3B, 3C, 3D, 3E, 3F.
- Western zero-filled banks: 2D, 2E, 2F, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 3A, 3B, 3C, 3D, 3E, 3F.

The bank fingerprint CSV records SHA-1/SHA-256, entropy and fill ratios for every bank. Pairwise similarity is measured only over the common byte length of each pair, so JP-vs-western comparisons cover the 512 KiB range shared by both files.

## Repository routing

- Release/dump identity and source-derived facts -> Sakurai `LIBRARY/GEN-01/GB/BLUE/RELEASES/...`.
- Six-release comparisons, bank fingerprints and disassembly tracking -> Sakurai `LIBRARY/GEN-01/GB/BLUE/COMPARISONS/BLUE-6-RELEASES/...`.
- Production assets made for Korean localization/modernization -> Tsubaki `PROJECTS/BLUE-KR-KO-MODERN/...`.
- Raw ROM binaries are never committed. Dump nodes contain metadata only.
