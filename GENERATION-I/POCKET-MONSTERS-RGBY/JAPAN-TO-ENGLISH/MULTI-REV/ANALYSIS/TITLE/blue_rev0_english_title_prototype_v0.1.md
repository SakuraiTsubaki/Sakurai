# Pocket Monsters Blue (Japan) → English title prototype v0.1

## Base ROM

The **Japanese Pocket Monsters Blue ROM** is the working/base ROM.

- Source SHA-1: `0da501e3e5c51ab8fef55b092dcdd7e6b050e424`
- Source SHA-256: `71a70e5f77c109177d21c998310ffe01a68e8cd2f41e72e7129093b890c7d3d1`

The English Pokémon Blue ROM is used only as an English implementation reference.

## Title logo

- Japanese Blue title-logo block: `0x11799`
- English Blue verified Pokémon logo block: `0x11380`
- Size: `0x700` bytes = 112 Game Boy 2bpp tiles = 16×7 tiles

The English Pokémon logo is transplanted into the Japanese Blue title-logo slot.
Japanese Blue's own version-specific title data is otherwise preserved.

## Output verification

- ROM size unchanged: 524288 bytes
- Output SHA-256: `c9ff9e8cbb09d489fb1fc65853e143df1a42a64ec9128c7434c8cd2f1f045352`
- IPS SHA-256: `aed2353a4f4cb9b9028978eacff3c531f7b8a1ed956c933c1fe82b8eb2268929`
- Header checksum: `0xE5`
- Global checksum: `0x897D`
- IPS reapplied to the clean Japanese Blue ROM and reproduced the output byte-for-byte.

No original ROM binary is stored in GitHub.
