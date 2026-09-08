# Pokémon Gold — Korea REV-0 — ROM bank audit

Source ROM is treated as read-only. No ROM binary is stored in this report or repository.

## Identification

- Source: `Pocket Monsters Geum (Korea).gbc`
- Size: 2,097,152 bytes (2 MiB)
- ROM banks: 128 × 16 KiB
- Cartridge type: `0x10` — MBC3 + TIMER + RAM + BATTERY
- ROM size code: `0x06` — 2 MiB
- RAM size code: `0x03`
- CGB flag: `0xC0`
- Revision byte: `0x00`
- SHA-1: `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65`
- SHA-256: `9c273e86e6120c6a038160ccb0153b8b20425b84fc08a496281c1d1bcac492f6`
- Header checksum: stored `0x08`, calculated `0x08` — PASS
- Global checksum: stored `0x778A`, calculated `0x778A` — PASS

## Fully blank 16 KiB ROM banks

The following banks are entirely `0x00` and are the strongest initial candidates for repacking/relocation work:

`13 22 27 28 29 2C 2D 2F 34 35 58 63 67 6A 6B 6F 73 74 75 76 77 7C 7D 7E`

- Count: **24 banks**
- Gross capacity: **393,216 bytes (384 KiB)**

Important: long zero-filled spans inside nonblank banks are **not** classified as safe free space until pointer, table, and control-flow references are audited.

## Bank-switching observation

The ROM contains the standard bank-switch helper sequence in bank 0:

- `LDH [hROMBank], A`
- `LD [$2000], A`
- `RET`

At ROM offset `0x000012`, the bank number in `A` is written directly to the MBC ROM-bank register without an explicit `AND 0x7F` in this helper. This is relevant to evaluating an MBC30-style 4 MiB extension, but all callers and emulator/hardware mapper behavior still require validation before treating banks `0x80-0xFF` as usable.

## Expansion constraints discovered so far

1. **Storage mapper wall:** Standard MBC3 exposes at most 2 MiB / 128 ROM banks. The Korean ROM is already at this declared size.
2. **Internal slack:** 24 completely zeroed banks provide 384 KiB of high-confidence candidate capacity before changing mapper behavior.
3. **Species-ID wall:** Gen II party/base-data structures use a one-byte species field, so a National Dex beyond 255 IDs requires a structural 16-bit species-ID migration across RAM, save data, party/box structs, battle state, scripts, encounter tables, evolution data, UI, and lookup routines. This is a deeper engine change than merely adding ROM banks.
4. **4 MiB path:** MBC30 is the RTC-preserving mapper-family extension to investigate first. The existing bank-switch helper is compatible in shape with an 8-bit bank value, but this alone does not prove the full engine is 4 MiB-safe.

## Next audit targets

- Enumerate every write/call path that changes ROM banks and test for masks/range assumptions.
- Map all one-byte species fields in WRAM/SRAM/party/box/battle/script structures.
- Measure current per-species data and compressed sprite footprint to estimate 1025/1579-slot storage needs.
- Build a 4 MiB experimental ROM copy (never modifying the original) and test MBC30 banking + RTC behavior in compatible emulators.
