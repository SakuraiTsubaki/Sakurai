# Pokémon Red supplied source baseline — 2026-09-13

Eight local read-only inputs were inspected. They represent seven unique byte streams because the second English file is an exact duplicate of the first English file by SHA-1 and SHA-256.

| Release | Version | Size | Banks | Cartridge | SHA-1 |
|---|---:|---:|---:|---:|---|
| Japan / Japanese | Rev 0 | 524,288 | 32 | `0x03` | `0623ad12f48c259447980d68bd85ddbf8204b2cd` |
| Japan / Japanese | Rev 1 | 524,288 | 32 | `0x03` | `ef74c79cded14204ac79e77f4964d9cb25003120` |
| USA-Europe / English | Rev 0 | 1,048,576 | 64 | `0x13` | `ea9bcae617fdf159b045185467ae58b2e4a48b9a` |
| Germany / German | Rev 0 | 1,048,576 | 64 | `0x1B` | `87d523fe1a0c548db7c5477b451ddec1eb083c06` |
| Italy / Italian | Rev 0 | 1,048,576 | 64 | `0x1B` | `65b97cf8f2f1cff711a6d08c6c894c8ce65ce522` |
| Spain / Spanish | Rev 0 | 1,048,576 | 64 | `0x1B` | `fc17c5b904d551b1b908054ccd1c493f755f832a` |
| France / French | Rev 0 | 1,048,576 | 64 | `0x1B` | `47a7622fa30e6402a3891fe65b3a930bf9bd7aec` |

All eight inputs have valid Nintendo header checksums and valid global checksums. Every input declares and contains an integral number of 16 KiB ROM banks. SGB support is enabled (`0x03`) in every header.

## Repository split

`Sakurai` receives this baseline, the complete inventory, the comparison CSV, and the v11 routing manifest. `Tsubaki`, as the complete non-ROM superset, receives all of those at the same paths plus the reproducible inspector and implementation-side extraction metadata.

No `.gb` image, renamed ROM, reconstructed ROM, or duplicate ROM is committed. The inventory contains only metadata and cryptographic hashes.
