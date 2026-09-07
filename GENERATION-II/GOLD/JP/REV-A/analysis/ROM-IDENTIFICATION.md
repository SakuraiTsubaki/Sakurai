# Pokémon Gold — Japan — REV-A ROM Identification

Source ROM is treated as read-only and is **not stored in this repository**.

| Field | Value |
|---|---|
| Source filename | `Pocket Monsters Kin (Japan) (Rev A).gbc` |
| File size | 1,048,576 bytes (1 MiB) |
| SHA-1 | `a222402235d484ee8e39f3f31bae57cf13daf585` |
| MD5 | `79aece8a042e4fa57aba9455c4d21a97` |
| Header title bytes | `POKEMON_GLDAAUJ` (+ CGB flag byte) |
| CGB flag | `0x80` |
| Cartridge type | `0x10` (MBC3 + TIMER + RAM + BATTERY) |
| ROM size code | `0x05` (1 MiB) |
| RAM size code | `0x03` |
| Destination code | `0x00` |
| ROM version byte | `0x01` |
| Canonical revision path | `REV-A` |
| Header checksum | stored `0x47`, calculated `0x47` — PASS |
| Global checksum | stored `0x8460`, calculated `0x8460` — PASS |

## Verification status

- Version byte `0x01` confirms this is distinct from Japanese REV-0 and is filed as `REV-A`.
- File size matches the Game Boy header ROM-size declaration.
- Header checksum matches.
- Global checksum matches.
- ROM identification metadata only; no copyrighted ROM binary is committed.
