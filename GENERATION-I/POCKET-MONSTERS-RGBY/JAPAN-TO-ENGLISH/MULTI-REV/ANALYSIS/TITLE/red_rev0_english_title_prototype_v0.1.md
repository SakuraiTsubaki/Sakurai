# Pocket Monsters Aka — English Title Prototype v0.1

- Base: `Pocket Monsters - Aka (Japan) (SGB Enhanced).gb`
- Base SHA-256: `392ce450d708c8d127aaed7afc20001a48625bd83a5fa5325be82f5c0972ccfa`
- Output SHA-256: `ab99ff626af1e8428fe6780b56be3980b3475214e1ef252eefc52f8607c6c32e`
- IPS SHA-256: `cbeeee43dba6ea44ee61ef156c9154bdcdc6a6c0913e0bab2f81fac88d97167e`

## Changes

- `0x010419–0x010B18` (`0x700` bytes): Japanese title-logo tiles replaced by the English Pokémon logo tiles taken from the supplied English Red ROM at `0x011380–0x011A7F`.
- `0x00014E–0x00014F`: global checksum recalculated (`A2C1` → `5008`).
- Header checksum remains `0x32`.
- ROM size remains 512 KiB.
- The Japanese and English `Red Version` graphic blocks were byte-identical, so no version-label data was replaced.

## Validation

- IPS patch reapplied to the untouched Japanese Red ROM and reproduced the output ROM byte-for-byte.
- No bytes outside the title-logo block and global checksum were changed.
- Title loader in Japanese Red copies exactly `0x700` bytes for the Pokémon logo, matching the English Red logo allocation (16 × 7 Game Boy 2bpp tiles).
- Runtime boot/screenshot verification is still pending because this execution environment has no Game Boy emulator executable installed.
