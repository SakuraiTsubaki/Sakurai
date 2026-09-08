# Pokémon Silver ROM census (8 target ROMs)

Generated from the user-supplied ROMs. **No ROM binary is included.**

## Header / identity summary

| Language/region | Revision | Size | Banks | CGB flag | Cart type | Header ROM size | Header rev | Full-zero banks | SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| JP | REV-0 | 1024 KiB | 64 | `0x80` | `0x10` | `0x05` | 0 | 0 (0 KiB) | `0a532063a3ff5750a464582aa7bbee2b6d42e1a92a136d9f4590e373487b615c` |
| JP | REV-A | 1024 KiB | 64 | `0x80` | `0x10` | `0x05` | 1 | 0 (0 KiB) | `99e5267fbf5a7748d4f3b75ba1990cb5d91348339468607a04bfbc6081c62d71` |
| USA-EUROPE | REV-0 | 2048 KiB | 128 | `0x80` | `0x10` | `0x06` | 0 | 28 (448 KiB) | `72b190859a59623cbef6c49d601f8de52c1d2331b4f08a8d2acc17274fc19a8c` |
| DE | REV-0 | 2048 KiB | 128 | `0x80` | `0x10` | `0x06` | 0 | 26 (416 KiB) | `c3d1fd0dec1d5fa9aa7f85275e79c52aa9175d191c63cbed7b406c306d946348` |
| FR | REV-0 | 2048 KiB | 128 | `0x80` | `0x10` | `0x06` | 0 | 26 (416 KiB) | `e120c4ddb0dc3e25b95c9c71b3ffd59ff57ce689cf4d79d04913ba59140c18c2` |
| IT | REV-0 | 2048 KiB | 128 | `0x80` | `0x10` | `0x06` | 0 | 26 (416 KiB) | `04c442246d1ae0ed6bf5e072bb7e3d06376e584b953d6b14047b39e45fbb0cb4` |
| ES | REV-0 | 2048 KiB | 128 | `0x80` | `0x10` | `0x06` | 0 | 26 (416 KiB) | `6797010c052e8f9373ea2b9e855ec078b34fda12e5ccf742eb19bb5e8f6947c2` |
| KR | REV-0 | 2048 KiB | 128 | `0xC0` | `0x10` | `0x06` | 0 | 24 (384 KiB) | `ebbac63c0c4309c82dbb6723e7163369784f962b4fd3e2f486075307c3008a22` |

All eight ROMs have valid Nintendo header checksum and global checksum.

## Fully empty 16 KiB banks (all bytes `00`)

- **JP REV-0:** none
- **JP REV-A:** none
- **USA-EUROPE REV-0:** 13 22 27 28 29 2C 2D 2F 34 35 58 63 67 6F 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E
- **DE REV-0:** 13 22 28 29 2C 2D 2F 34 35 63 67 6F 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E
- **FR REV-0:** 13 22 28 29 2C 2D 2F 34 35 63 67 6F 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E
- **IT REV-0:** 13 22 28 29 2C 2D 2F 34 35 63 67 6F 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E
- **ES REV-0:** 13 22 28 29 2C 2D 2F 34 35 63 67 6F 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E
- **KR REV-0:** 13 22 27 28 29 2C 2D 2F 34 35 58 63 67 6A 6B 6F 73 74 75 76 77 7C 7D 7E

## Cross-version free-bank observations

- Western EN/DE/FR/IT/ES common fully-empty banks: **26 banks = 416 KiB**: 13 22 28 29 2C 2D 2F 34 35 63 67 6F 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E
- EN/DE/FR/IT/ES/KR common fully-empty banks: **20 banks = 320 KiB**: 13 22 28 29 2C 2D 2F 34 35 63 67 6F 73 74 75 76 77 7C 7D 7E
- JP Rev0/RevA are 1 MiB images (64 banks), so they can in principle be padded to 2 MiB while staying inside MBC3’s 128-bank ROM addressing limit; this requires careful bank-reference and build validation.
- International/Korean images are already 2 MiB, the conventional MBC3 ROM-addressing ceiling. Further physical ROM growth cannot use stock MBC3 banking unchanged.
- Empty-bank counts are a coarse first-pass capacity metric only. Every candidate bank must still be proven unreferenced before reuse.

## JP Rev0 vs RevA byte-level diff

- Differing bytes: **19,150**
- First differing offset: `0x00014C`
- Last differing offset: `0x0FFFE3`
- Differing bytes by 16 KiB bank: `00`=179, `01`=103, `03`=5, `04`=60, `05`=2, `09`=82, `0A`=1, `0B`=7, `0F`=160, `14`=2, `21`=2, `23`=10787, `24`=1, `25`=60, `3E`=79, `3F`=7620

## Immediate engineering implication

For a large species/form expansion, the first practical strategy should be to reclaim and formally verify currently empty banks, then redesign ID widths/tables/pointers/save structures as needed. A mapper change is not a drop-in solution because Silver depends on MBC3 RTC functionality.

## Reproducibility

- Analysis bank size: 16 KiB (`0x4000`).
- `full-zero bank` means all 16,384 bytes in that physical ROM bank are `0x00`.
- Source ROMs were read only; no ROM was modified or redistributed.