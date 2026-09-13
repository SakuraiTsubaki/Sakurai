# GS Korean → Pocket Monsters source ROM audit

Generated directly from the 23 supplied GB/GBC ROM images. Original ROM binaries are not included.

## Repository routing

- **Sakurai**: source identity, hashes, cartridge/header metadata, bank maps, cross-ROM comparisons, extraction/verification tooling.
- **Tsubaki**: reusable production assets derived from supplied ROMs, with provenance back to Sakurai release/dump IDs.

## Current source set

- ROMs audited: **23**
- Header checksum valid: **23/23**
- Global checksum valid: **23/23**
- Bank hashes emitted locally: **1760**

## Korean Gold/Silver structural result

The Korean Gold and Silver ROMs are both 2 MiB / 128 banks. Bank-by-bank comparison shows 92 identical banks and 36 differing banks.

Important Korean-language implementation regions confirmed directly from the supplied ROMs:

- `0x6C`: byte-identical between Korean Gold and Silver.
- `0x78–0x7A`: byte-identical between Korean Gold and Silver; rendered as an 8×16 1bpp font atlas in Tsubaki.
- `0x68–0x69`: differ between Gold and Silver and must remain version-owned research data.

This package intentionally records structure and provenance without committing full original ROM images.
