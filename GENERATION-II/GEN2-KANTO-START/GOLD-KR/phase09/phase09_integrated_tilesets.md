# GEN2 Kanto Start — GOLD KR Phase 09
## Pallet cluster integrated tileset allocation

Status: **PASS / generated assets; ROM pointers not changed in this phase**

## Allocation policy
- Preserve Gold tile IDs and used/border metatile IDs whenever safe.
- Reserve tile `$03` and `$14` conservatively; KANTO uses them for flower/water animation.
- Import RGBY-only tile graphics into otherwise unused slots.
- Deduplicate an RGBY block with a Gold block only when both graphics **and collision semantics** match.
- Keep RGBY and Gold border blocks in the allocation set.

## Capacity
| Map | static tiles | limit | metatile IDs used | limit | imported RGBY blocks newly allocated | exact block reuse |
|---|---:|---:|---:|---:|---:|---:|
| PalletTown | 95 | 96 | 57 | 128 | 28 | 0 |
| RedsHouse1F | 80 | 96 | 19 | 128 | 8 | 1 |
| RedsHouse2F | 96 | 96 | 17 | 128 | 8 | 1 |
| BluesHouse | 75 | 96 | 26 | 128 | 13 | 0 |
| OaksLab | 42 | 96 | 16 | 128 | 4 | 8 |

## Pixel round-trip validation
- PalletTown: RGBY `PASS` / Gold `PASS` (320×288 px)
- RedsHouse1F: RGBY `PASS` / Gold `PASS` (128×128 px)
- RedsHouse2F: RGBY `PASS` / Gold `PASS` (128×128 px)
- BluesHouse: RGBY `PASS` / Gold `PASS` (128×128 px)
- OaksLab: RGBY `PASS` / Gold `PASS` (160×192 px)

Result: **10/10 source renders reproduced byte-for-byte at the pixel-buffer level.**

## 2bpp validation
The PNG→Game Boy 2bpp encoder was cross-checked against the uploaded Red ROM using the Gen I DOJO/GYM tileset. The complete 1,536-byte graphics payload reproduced the ROM bytes exactly.

## Generated per-map assets
Each integrated tileset directory contains:
- `tiles.png` — 96-slot merged grayscale tilesheet
- `tiles.2bpp` — 1,536-byte Game Boy 2bpp payload
- `metatiles.bin` — 128×16-byte Gen II metatile table
- `collision.asm` and `collision.bin` — 128×4 collision table
- `rgby_remapped.blk` — RGBY layout rewritten to merged block IDs
- `gold_passthrough.blk` — original Gold block IDs, intentionally unchanged
- `manifest.json` — source→merged tile/block IDs and hashes

## Important
These are **new dedicated Pallet-cluster tilesets**. The original global Gold `KANTO`, `PLAYERS_HOUSE`, `HOUSE`, and `LAB` tilesets are not overwritten or deleted; other maps remain free to use the originals.

## Next
Wire the five dedicated tilesets into Gold map headers / tileset tables, place their data in verified free ROM space, update bank/pointers, then switch each Pallet-cluster map to the matching integrated asset while keeping the Phase 03–05 events intact.
