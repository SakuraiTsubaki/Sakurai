# GEN2 Kanto Start — GOLD KR Phase 10
## Pallet cluster integrated tileset substrate

Status: **ROM substrate patch built and byte-verified**

Base ROM SHA-1: `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65`
Phase 05 SHA-1: `0abf0c0ad98cd6439e37cd515ebd772f622333f3`
Phase 10 SHA-1: `ab47690884c4f65e1df305a6ef11e61a4404522d`

## Goal

Phase 08/09 produced RGBY+GOLD-compatible tile/metatile/collision containers for Pallet Town, Red's House 1F/2F, Blue/Green's House and Oak's Lab. Phase 10 embeds those five containers in the Korean Gold ROM without overwriting the global KANTO/HOUSE/PLAYERS_HOUSE/LAB tilesets.

The active GOLD block maps are deliberately left unchanged in this phase. Only the five Pallet-cluster map records are switched to new tileset IDs, so current GOLD rendering and collision can be regression-tested before RGBY layout/event activation.

## Tileset compression verification

The Korean Gold ROM stores tileset graphics as GSC lz3 streams. Existing pointers were recovered directly from the ROM:

- KANTO GFX `70:4407`
- HOUSE GFX `37:6133`
- PLAYERS_HOUSE GFX `07:5E4C`
- LAB GFX `08:4AB2`

All four decompress to exactly 96 tiles / 1536 bytes. Their decompressed bytes match the public Korean disassembly PNG graphics after applying the PNG palette-index reversal `(3,2,1,0)`.

For the Phase 10 patcher, the new 1536-byte graphics are encoded using valid literal-only lz3 commands. Each stream is 1585 bytes and round-trips exactly through the lz3 decompressor.

## Tilesets table

The live `Tilesets` table was uniquely identified at `05:56BE` / file `0x0156BE`. Each entry is 15 bytes.

`LoadMapTileset` contains the unique signature beginning at file `0x002E59`:

`21 BE 56 01 0F 00 FA 3F D1 ... 3E 05 ...`

The `05` bank is separately hard-coded, so the expanded table must remain in Bank 05. Bank 05 has a trailing 2120-byte all-zero region. The 34-entry table (510 bytes) is relocated to `05:7800`, and only the `ld hl, Tilesets` immediate is changed from `56BE` to `7800`.

## Free-bank selection

Bank 73 and Bank 74 are both exactly 16 KiB of zero bytes in the clean Korean Gold ROM and in the cumulative Phase 05 build. `layout.link` assigns no `ROMX $73` or `ROMX $74` section. These two banks are therefore used as dedicated Pallet integration asset banks.

## New runtime tileset IDs

| ID | Container | GFX | Metatiles | Collision | Reused behavior/palette basis |
| --- | --- | --- | --- | --- | --- |
| `1D` | Pallet Town | `73:4000` | `73:4700` | `73:4F00` | KANTO |
| `1E` | Red House 1F | `73:5100` | `73:5800` | `73:6000` | PLAYERS_HOUSE |
| `1F` | Red House 2F | `73:6200` | `73:6900` | `73:7100` | PLAYERS_HOUSE |
| `20` | Blue/Green House | `74:4000` | `74:4700` | `74:4F00` | HOUSE |
| `21` | Oak Lab | `74:5100` | `74:5800` | `74:6000` | LAB |

No runtime `NUM_TILESETS` bounds check exists; the compile-time constant is only used by the constants/table assertion. IDs `1D–21` therefore work once the table is extended.

## Pallet map records

`MapGroup_Pallet` was recovered at file `0x094895`. Its six records are Route 1, Pallet Town, Red House 1F, Red House 2F, Blue/Green House and Oak Lab, each 9 bytes.

Phase 10 changes only the tileset byte of records 1–5:

- Pallet Town `0x09489F`: `03 -> 1D`
- Red House 1F `0x0948A8`: `05 -> 1E`
- Red House 2F `0x0948B1`: `05 -> 1F`
- Blue/Green House `0x0948BA`: `04 -> 20`
- Oak Lab `0x0948C3`: `09 -> 21`

Route 1 remains on original KANTO.

## Direct GOLD compatibility proof

The live block pointers were recovered through each map's attribute record and compared against the Phase 09 `gold_passthrough.blk` files:

- Pallet Town `2A:5497` — identical
- Red House 1F `37:4B96` — identical
- Red House 2F `37:4BA6` — identical
- Blue/Green House `2A:6867` — identical
- Oak Lab `37:4BB6` — identical

For every block currently used by those five GOLD maps, including each border block:

- integrated metatile definition equals the original GOLD definition — **5/5 PASS**
- integrated collision quadruplet equals the original GOLD definition — **5/5 PASS**
- every referenced 8x8 tile has byte-identical 2bpp graphics — **5/5 PASS**

Therefore switching the tileset IDs does not alter the current GOLD layout's visible pixels or movement collision.

## Output validation

- lz3 new-GFX round-trip: **5/5 PASS**
- Phase09 metatile equality: **5/5 PASS**
- Phase09 collision equality: **5/5 PASS**
- clean original -> cumulative Phase10 patcher: **PASS**
- clean original + Phase10 IPS: **PASS**
- output SHA-1: `ab47690884c4f65e1df305a6ef11e61a4404522d`
- output SHA-256: `fe675e50ed3006c8866306b25c1aacc43b2fafe31713b9ed275f27b05eb8feab`
- header checksum: `08`
- global checksum: `90F6`

## Not activated in Phase 10

- RGBY remapped map layouts are not yet selected as active layouts.
- Dedicated GSC CGB vs RGBY Classic palette profiles are not yet activated.
- No map size changes are made.
- No original global tileset is overwritten.
- No original event is removed.

This phase is the safe runtime substrate for the next Pallet integration pass: final map composition, RGB/Yellow opening-event restoration and palette-profile integration.
