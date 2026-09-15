# Generation IV → Generation III battle sprite master — Batch 001 (#001 BULBASAUR)

This is the first deterministic batch under the project-wide Generation III insertion contract.

## Source

Five supplied Generation IV ROM observations are read directly and never modified: Diamond USA Rev.05, Pearl USA Rev.05, Platinum Korea Rev.00, HeartGold Korea Rev.00, SoulSilver Korea Rev.00. The active base battle archives are read through NitroFS and species 001 uses the `species * 6` member block.

Diamond/Pearl scanned NCGR payloads use the DP back-to-front LCRNG-XOR decode direction. Platinum/HGSS use the front-to-back direction. The decoded source canvas is 160x80 containing two 80x80 frames. Palette index 0 is treated as transparent.

## Conversion

- complete 80x80 source frame -> complete 64x64 target canvas; no opaque-bbox normalization
- preservation-v2 exact area-overlap voting
- source palette indices only; no RGB interpolation or new colors
- rare-index exponent: 0.08
- silhouette protection: transparency cannot win when opaque overlap is >= 0.78125 (50% of the 1.5625 target footprint)
- no generative image tools / antialiasing / bilinear / bicubic
- Generation III graphics: 64x64, 4bpp, 2048-byte tile-order graphics, index 0 transparent
- Generation III palette: source 16-entry 15-bit palette retained as 32 bytes
- compressed graphics: deterministic GBA/Nintendo type-0x10 LZ77 stream

## Batch result

- logical source roles: 80
- canonical raw NCGR members: 5
- canonical raw NCLR members: 2
- canonical 80x80 rendered source images: 15
- canonical 64x64 index/graphics assets: 8
- canonical target palettes: 2
- canonical rendered 64x64 assets after rendered-pixel SHA-256 dedup: 15
- validation: PASS

All five game identities, both logical gender slots, front/back, both source frames, and normal/shiny palette roles remain present in `logical_manifest.*` even when bytes are deduplicated.
