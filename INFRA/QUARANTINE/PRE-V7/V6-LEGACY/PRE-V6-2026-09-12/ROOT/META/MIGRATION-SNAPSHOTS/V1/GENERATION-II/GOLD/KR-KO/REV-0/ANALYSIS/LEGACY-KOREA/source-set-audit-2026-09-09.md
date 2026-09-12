# Uploaded ROM source-set audit (2026-09-09)

Context: GS Korean → Pocket Monsters Korean localization/retranslation project. Original ROM binaries remain local/read-only and are not uploaded.

## Validation

- 23 ROMs inspected (Gen I: 12, Gen II: 11).
- All 23 pass Nintendo logo, declared ROM size, header checksum, and global checksum validation.
- Full local audit includes MD5/SHA-1/SHA-256/CRC32, header fields, revision byte, CGB/SGB flags, mapper, bank counts, revision diffs, version-pair similarity, and candidate padding runs.

## Source-set SHA-1

- `ef74c79cded14204ac79e77f4964d9cb25003120` — Pocket Monsters - Aka (Japan) (Rev A) (SGB Enhanced).gb
- `0623ad12f48c259447980d68bd85ddbf8204b2cd` — Pocket Monsters - Aka (Japan) (SGB Enhanced).gb
- `0da501e3e5c51ab8fef55b092dcdd7e6b050e424` — Pocket Monsters - Ao (Japan) (SGB Enhanced).gb
- `95127b901bbce2407daf43cce9f45d4c27ef635d` — Pocket Monsters - Crystal Version (Japan).gbc
- `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` — Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb
- `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` — Pocket Monsters - Midori (Japan) (SGB Enhanced).gb
- `1fb6c264e950d97ce3fd99b347e485b2150df4ff` — Pocket Monsters - Pikachu (Japan) (Rev 0A) (SGB Enhanced).gb
- `28e4b8531ea4ea1de5a396fccb0cfba51b06b149` — Pocket Monsters - Pikachu (Japan) (Rev B) (SGB Enhanced).gb
- `91864ecdf26d1c593bde4d9ed615520eb57d5e41` — Pocket Monsters - Pikachu (Japan) (Rev C) (SGB Enhanced).gb
- `a40298a8123613ee60cd7aab204d788b8425976e` — Pocket Monsters - Pikachu (Japan) (Rev D) (SGB Enhanced).gb
- `cb22d7e03a74dc3a563fde6be8626626b2b392e7` — Pocket Monsters Eun (Korea).gbc
- `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` — Pocket Monsters Geum (Korea).gbc
- `a11d5ddc26eb826086593f82370b15d16404d33e` — Pocket Monsters Gin (Japan) (Rev A).gbc
- `fa8c51059c1642faa570db56ef089f54d1d2011f` — Pocket Monsters Gin (Japan).gbc
- `a222402235d484ee8e39f3f31bae57cf13daf585` — Pocket Monsters Kin (Japan) (Rev A).gbc
- `8814f1039450a5d3684b1389f588ccd7ee7c3436` — Pocket Monsters Kin (Japan).gbc
- `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2` — Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb
- `f2f52230b536214ef7c9924f483392993e226cfb` — Pokemon - Crystal Version (USA, Europe) (Rev A).gbc
- `f4cd194bdee0d04ca4eac29e09b8e4e9d818c133` — Pokemon - Crystal Version (USA, Europe).gbc
- `d8b8a3600a465308c9953dfa04f0081c05bdcb94` — Pokemon - Gold Version (USA, Europe).gbc
- `ea9bcae617fdf159b045185467ae58b2e4a48b9a` — Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb
- `49b163f7e57702bc939d642a18f591de55d92dae` — Pokemon - Silver Version (USA, Europe).gbc
- `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1` — Pokemon - Yellow Version (USA, Europe).gbc

## Key implementation findings

- JP Red/Green/Blue: 512 KiB, MBC1. EN Red/Blue: 1 MiB, MBC3.
- JP Yellow: 1 MiB, MBC3. EN Yellow: 1 MiB, MBC5.
- JP Gold/Silver: 1 MiB (64 banks), CGB-supported + SGB.
- KR Gold/Silver: 2 MiB (128 banks), CGB-only + no SGB.
- EN Gold/Silver: 2 MiB (128 banks), CGB-supported + SGB.
- JP/EN Crystal: 2 MiB, CGB-only, no SGB.
- KR Gold vs Silver share 92 exact-identical 16 KiB banks, making them strong paired references for shared Hangul engine/font/UI data.
- Long 0x00/0xFF runs are only candidate padding; none are declared safe free space until pointer/reference analysis.

## Revision byte-diff summary

- JP Red v0→v1: 46,167 changed bytes across 31 banks; first 0x51, last 0x7FFFF.
- JP Green v0→v1: 46,168 changed bytes across 31 banks; first 0x51, last 0x7FFFF.
- JP Yellow v0→v1: 307,668 changed bytes across 61 banks; first 0x38, last 0xFFFFF.
- JP Yellow v1→v2: 39,485 changed bytes across 60 banks; first 0x69, last 0xFFFFE.
- JP Yellow v2→v3: 245,538 changed bytes across 61 banks; first 0x68, last 0xFFFFF.
- JP Gold v0→v1: 10,841 changed bytes across 10 banks; first 0x14C, last 0x92023.
- JP Silver v0→v1: 19,150 changed bytes across 16 banks; first 0x14C, last 0xFFFE3.
- EN Crystal v0→v1: 584 changed bytes across 8 banks; first 0x14C, last 0x1FFFFF.

## Next decomposition

1. Build per-ROM 16 KiB bank hash maps and cross-region exact/near-identical-bank links.
2. Isolate GS Korean Hangul font, character code tables, text decoder, text-box/UI, naming/SRAM handling, pointer tables and bank-switching behavior.
3. Build JP and EN text/pointer maps independently; do not assume shared mapper/layout.
4. Keep each revision as a separate translation/implementation source.
5. Verify allocatable free space only after code/data/reference scans.
