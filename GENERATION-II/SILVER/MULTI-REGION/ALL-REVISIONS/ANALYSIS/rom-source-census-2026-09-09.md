# Pokémon Silver uploaded ROM source census — 2026-09-09

Direct binary audit of the eight project ROMs. Original ROM binaries are **not** stored in this repository.

## Source set

|ID|Region / revision|Size|Banks|Header title|CGB|SGB|ROM ver|SHA-1|Checksums|
|---|---|---:|---:|---|---|---|---:|---|---|
|JP-0|JAPAN REV-0|1 MiB|64|`POKEMON_SLVAAXJ`|`0x80`|`0x03`|0|`fa8c51059c1642faa570db56ef089f54d1d2011f`|header/global OK|
|JP-A|JAPAN REV-A|1 MiB|64|`POKEMON_SLVAAXJ`|`0x80`|`0x03`|1|`a11d5ddc26eb826086593f82370b15d16404d33e`|header/global OK|
|EN|USA-EUROPE REV-0|2 MiB|128|`POKEMON_SLVAAXE`|`0x80`|`0x03`|0|`49b163f7e57702bc939d642a18f591de55d92dae`|header/global OK|
|DE|GERMANY REV-0|2 MiB|128|`POKEMON_SLVAAXD`|`0x80`|`0x03`|0|`8ecc58d621faaedf2a934bd2583d527220df7bb9`|header/global OK|
|FR|FRANCE REV-0|2 MiB|128|`POKEMON_SLVAAXF`|`0x80`|`0x03`|0|`a4a7e8079b7a53e4d9ef43382bbb1090b9d45d1a`|header/global OK|
|IT|ITALY REV-0|2 MiB|128|`POKEMON_SLVAAXI`|`0x80`|`0x03`|0|`c9eca9d0a837beb9137bb7d779e469c54e9f8d77`|header/global OK|
|ES|SPAIN REV-0|2 MiB|128|`POKEMON_SLVAAXS`|`0x80`|`0x03`|0|`05bd978ab2cb104b0aff3f696896e30885203a18`|header/global OK|
|KR|KOREA REV-0|2 MiB|128|`POKEMON_SLVAAXK`|`0xC0`|`0x00`|0|`cb22d7e03a74dc3a563fde6be8626626b2b392e7`|header/global OK|

## High-level findings

- JP Rev0 and JP Rev A are 1 MiB / 64-bank builds. All other uploaded regional builds are 2 MiB / 128-bank builds.
- Every ROM declares MBC3 + timer + RAM + battery (`0x10`) and 32 KiB external RAM (`0x03`).
- All eight ROMs pass both the Game Boy header checksum and global checksum.
- Korean Silver is structurally distinct at the cartridge header level: CGB flag `0xC0` and SGB flag `0x00`; the other seven use CGB `0x80` and SGB `0x03`.
- Header title suffixes identify region: `...XJ` JP, `...XE` EN, `...XD` DE, `...XF` FR, `...XI` IT, `...XS` ES, `...XK` KR.
- Banks byte-identical at the same index across all eight ROMs (within JP's 0x00–0x3F range): 0x0C, 0x2A, 0x30, 0x37, 0x3B, 0x3C, 0x3D (7 banks).
- Western EN/DE/FR/IT/ES builds have 47/128 banks byte-identical at the same index.
- Korean and English builds have 29/128 banks byte-identical at the same index.
- Upper-bank allocation is materially different in Korean: banks `0x78–0x7A` are populated in KR while those banks are all-zero in the five Western builds.

## Japanese revision delta

JP Rev A differs from JP Rev0 in 16 of 64 banks: 0x00, 0x01, 0x03, 0x04, 0x05, 0x09, 0x0A, 0x0B, 0x0F, 0x14, 0x21, 0x23, 0x24, 0x25, 0x3E, 0x3F.
Overall JP Rev0 ↔ Rev A byte equality: 98.1737%; exact same-index banks: 48/64.
The largest revision deltas are concentrated in banks `0x23` and `0x3F`; these should be disassembled/diffed first when identifying bug fixes or data revisions.

## Selected pairwise similarity

|Pair|Byte equality over overlap|Exact same-index banks|
|---|---:|---:|
|JP-0 ↔ JP-A|98.1737%|48/64|
|KR ↔ EN|57.9274%|29/128|
|ES ↔ IT|74.7975%|48/128|
|ES ↔ FR|72.9507%|47/128|
|EN ↔ DE|69.4211%|47/128|

## Generated audit data

- `rom-source-manifest-2026-09-09.csv`: one row per ROM with hashes, header fields, checksums, and zero-bank map.
- `rom-source-manifest-2026-09-09.json`: machine-readable equivalent.
- `bank-fingerprint-matrix-2026-09-09.csv`: per-bank SHA-1 fingerprints and equality flags across all regions.
- `jp-rev0-vs-reva-diff-banks-2026-09-09.csv`: bank-level Rev0/Rev A change map.

## Next analysis axis

Proceed bank-by-bank from `0x00` upward, classifying code/data/text/graphics/pointers, locating regional relocations, and recording exact cross-version equivalence and revision-only changes. No ROM binary needs to be committed.
