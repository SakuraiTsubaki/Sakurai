# Pokémon Crystal multilingual ROM baseline

> Generated from the seven project ROMs on 2026-09-05. No ROM bytes are stored in this repository.

## Scope

JP, EN Rev 0, EN Rev A, DE, FR, IT, ES.

## Header / hash inventory

| ID | Size | Banks | Ver | RAM code | Dest | SHA-1 | Header | Global |
|---|---:|---:|---:|---|---|---|---|---|
| JP | 2097152 | 128 | 0 | 0x05 | 0x00 | `95127b901bbce2407daf43cce9f45d4c27ef635d` | OK | OK |
| EN-RevA | 2097152 | 128 | 1 | 0x03 | 0x01 | `f2f52230b536214ef7c9924f483392993e226cfb` | OK | OK |
| EN-Rev0 | 2097152 | 128 | 0 | 0x03 | 0x01 | `f4cd194bdee0d04ca4eac29e09b8e4e9d818c133` | OK | OK |
| ES | 2097152 | 128 | 0 | 0x03 | 0x01 | `889a06fc0bb863666865aa69def0adf97945ac2a` | OK | OK |
| DE | 2097152 | 128 | 0 | 0x03 | 0x01 | `accb584293ba056152f1fd908439b019017ff2fe` | OK | OK |
| FR | 2097152 | 128 | 0 | 0x03 | 0x01 | `c055992b16b7399c687647725cdd1f4f13a2f75c` | OK | OK |
| IT | 2097152 | 128 | 0 | 0x03 | 0x01 | `6cee05e5b95beeae74b8365ad18ec4a07a8c4af8` | OK | OK |

## Immediate findings

- All seven files are exactly 2,097,152 bytes (2 MiB), i.e. 128 × 16 KiB banks.
- All seven pass both Game Boy header-checksum and global-checksum validation.
- All seven identify as `PM_CRYSTAL`, CGB-only (`0xC0`), cartridge type `0x10`, ROM-size code `0x06`.
- JP has destination code `0x00`, ROM version `0`, and RAM-size code `0x05`.
- All non-JP builds have destination code `0x01` and RAM-size code `0x03`.
- EN Rev A is header version `1`; EN Rev 0 and the other localized builds are header version `0`.
- EN Rev 0 vs EN Rev A differs at only **584 bytes (0.0278%)**.
- EN revision differences occur only in banks: `00` (4 bytes), `10` (9 bytes), `11` (2 bytes), `3E` (8 bytes), `47` (1 bytes), `5C` (546 bytes), `7E` (2 bytes), `7F` (12 bytes).
- Banks identical byte-for-byte across all seven ROMs: `30`, `31`, `37`, `3B`, `3C`, `3D`, `4B`, `4C`, `7A`.

## Next analysis layers

1. Bank-by-bank entropy/fill/free-space census.
2. Cross-language structural alignment and pointer/table census.
3. Text/font/charset detection per language.
4. EN Rev 0 ↔ Rev A exact patch-range classification.
5. JP ↔ international structural delta, especially RAM/mobile-related systems.
6. Map/event/trainer/Pokédex/UI/system-text data inventories.

## Repository policy

- ROM originals are not committed.
- Only hashes, metadata, reports, tools, patches, and other non-ROM outputs belong in GitHub.
