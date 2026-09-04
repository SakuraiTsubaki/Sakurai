# Pokémon Crystal hardware/header audit

All seven project ROMs are 2 MiB / 128 × 16 KiB banks, CGB-only, cartridge type `0x10` (MBC3 + timer + RAM + battery), ROM-size code `0x06`, and pass both header and global checksum validation.

## SRAM header split
- JP: RAM-size code `0x05` = 64 KiB SRAM (8 banks).
- EN/DE/FR/IT/ES: RAM-size code `0x03` = 32 KiB SRAM (4 banks).
- This hardware-header difference aligns with the Japanese build carrying mobile-era SRAM requirements and must be preserved when comparing save/mobile structures.

## Destination/version
- JP destination code: `0x00`; ROM version: 0.
- International destination code: `0x01`.
- EN RevA ROM version: 1; EN Rev0 and DE/FR/IT/ES: 0.

## Safety implication
- Save/SRAM structures cannot be assumed interchangeable between JP and international images merely because the ROMs share the same 2 MiB size.
