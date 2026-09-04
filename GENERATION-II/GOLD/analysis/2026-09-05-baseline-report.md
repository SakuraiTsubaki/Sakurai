# Pokémon Gold multi-region ROM baseline census — 2026-09-05

This report records metadata only. No ROM image or ROM byte payload is included.

## Scope

- ROMs inspected: **8**
- Total source bytes inspected locally: **14,680,064**
- Variants: JP Rev 0, JP Rev A, EN, DE, FR, IT, ES, KR
- All 8 images pass both Nintendo header checksum and global checksum validation.

## Header census

| Variant | Size | Banks | Manufacturer | CGB mode | SGB | ROM ver. | SHA-1 |
|---|---:|---:|---|---|---|---:|---|
| Pocket Monsters Geum (Korea).gbc | 2 MiB | 128 | AAUK | CGB-only (0xC0) | 0x00 | 0 | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` |
| Pocket Monsters Kin (Japan) (Rev A).gbc | 1 MiB | 64 | AAUJ | CGB-compatible (0x80) | 0x03 | 1 | `a222402235d484ee8e39f3f31bae57cf13daf585` |
| Pocket Monsters Kin (Japan).gbc | 1 MiB | 64 | AAUJ | CGB-compatible (0x80) | 0x03 | 0 | `8814f1039450a5d3684b1389f588ccd7ee7c3436` |
| Pokemon - Edicion Oro (Spain).gbc | 2 MiB | 128 | AAUS | CGB-compatible (0x80) | 0x03 | 0 | `162ea54c6a3cff374642e6dd842f9bffac847e7b` |
| Pokemon - Gold Version (USA, Europe).gbc | 2 MiB | 128 | AAUE | CGB-compatible (0x80) | 0x03 | 0 | `d8b8a3600a465308c9953dfa04f0081c05bdcb94` |
| Pokemon - Goldene Edition (Germany).gbc | 2 MiB | 128 | AAUD | CGB-compatible (0x80) | 0x03 | 0 | `9254195d461ea942eaaa08cc4b83de3cf82aea0d` |
| Pokemon - Version Or (France).gbc | 2 MiB | 128 | AAUF | CGB-compatible (0x80) | 0x03 | 0 | `c147c0d8c2b71b7628a7233436f5c052b5b17081` |
| Pokemon - Versione Oro (Italy).gbc | 2 MiB | 128 | AAUI | CGB-compatible (0x80) | 0x03 | 0 | `032608fe8947b627584a4a0eccc7bf9ad3588426` |

## Immediate structural findings

- The two Japanese images are **1 MiB / 64 × 16 KiB banks**; all six localized images are **2 MiB / 128 banks**.
- The Korean image is uniquely marked **CGB-only (0xC0)** and **SGB unsupported (0x00)**. The other seven are **CGB-compatible (0x80)**; JP and the European/US localizations report SGB support (0x03).
- Cartridge type is uniformly **0x10: MBC3 + TIMER + RAM + BATTERY**; declared SRAM is uniformly **32 KiB**.
- Header manufacturer suffixes encode the market/language family in this set: `AAUJ`, `AAUE`, `AAUD`, `AAUF`, `AAUI`, `AAUS`, `AAUK`.

## Japanese Rev 0 → Rev A binary delta

- Different bytes: **10,841**
- Contiguous changed ranges: **426**
- Changed banks: **10 / 64**
- Bank `0x23` alone contains **10,821** changed bytes (**99.82%** of all differing bytes).
- Outside bank `0x23`, only 20 byte positions differ in this raw census; four are header/version/global-checksum bytes at `0x014C–0x014F`.
- This is only a byte-level localization of the revision delta; semantic attribution requires disassembly/data-structure mapping.

### Changed-bank counts

| Bank | Differing bytes |
|---:|---:|
| `0x00` | 5 |
| `0x04` | 5 |
| `0x05` | 1 |
| `0x09` | 1 |
| `0x0A` | 1 |
| `0x0F` | 2 |
| `0x14` | 2 |
| `0x21` | 2 |
| `0x23` | 10,821 |
| `0x24` | 1 |

## Same-index identical bank fingerprints

Exact 16 KiB bank equality is a conservative signal: equal means byte-for-byte identical; non-equal does not imply wholly different semantics.

- `Pocket Monsters Geum (Korea).gbc` ↔ `Pokemon - Gold Version (USA, Europe).gbc`: **29/128** banks identical at the same index.
- `Pocket Monsters Kin (Japan) (Rev A).gbc` ↔ `Pokemon - Gold Version (USA, Europe).gbc`: **8/64** banks identical at the same index.
- `Pokemon - Gold Version (USA, Europe).gbc` ↔ `Pokemon - Goldene Edition (Germany).gbc`: **47/128** banks identical at the same index.
- `Pokemon - Gold Version (USA, Europe).gbc` ↔ `Pokemon - Version Or (France).gbc`: **47/128** banks identical at the same index.
- `Pokemon - Gold Version (USA, Europe).gbc` ↔ `Pokemon - Versione Oro (Italy).gbc`: **47/128** banks identical at the same index.

## Next analysis layers

1. Per-bank entropy/fill/free-space census and executable/data partitioning.
2. Cross-version pointer and bank-call topology; identify stable shared code banks versus localized text/data banks.
3. Character tables, fonts, text engines, string pointer tables, UI/name-entry differences — with Korean as a first-class target.
4. Semantic disassembly of JP Rev 0 → Rev A changes, especially bank `0x23`.
5. Maintain a provenance ledger for every extracted structure and every later patch; ROM originals remain excluded from GitHub.
