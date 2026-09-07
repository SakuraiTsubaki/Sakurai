# GEN2 Kanto Start — GOLD KR Phase 08
## Pallet cluster RGBY → Gen II collision conversion

Status: **PASS / no ROM patch in this phase**

## Scope
- Pallet Town exterior
- Red’s House 1F
- Red’s House 2F
- Blue/Green’s House
- Oak’s Lab
- RGBY and Gold border blocks for all five maps

## Conversion rule
Gen I movement collision samples the lower-left 8×8 tile of each 2×2 movement quadrant. For a 4×4 block the four sampled tile indices are `4, 6, 12, 14` (TL, TR, BL, BR). Imported RGBY blocks are converted from those original passability samples, then special semantics are restored using verified Gold same-coordinate behavior and warp locations. Existing Gold blocks retain their original collision table unchanged.

## Special semantics retained
- Pallet Town: `DOOR`, `WATER`, `TALL_GRASS`
- Red’s House 1F/2F: `WINDOW`, `STAIRCASE`, `TV`, `PC`, `BOOKSHELF`, `WARP_CARPET_DOWN`
- Blue/Green’s House: `WINDOW`, `RADIO`, `TOWN_MAP`, `TV`, `BOOKSHELF`, `WARP_CARPET_DOWN`
- Oak’s Lab: `WINDOW`, `BOOKSHELF`, `WARP_CARPET_DOWN`

## Results
| Map | RGBY source blocks converted (border included) | explicit special overrides | unresolved |
|---|---:|---:|---:|
| PalletTown | 28 | 18 | 0 |
| RedsHouse1F | 9 | 8 | 0 |
| RedsHouse2F | 9 | 6 | 0 |
| BluesHouse | 13 | 8 | 0 |
| OaksLab | 12 | 6 | 0 |

Total imported source blocks analysed: **71**.
Unresolved special-collision candidates: **0**.

## Border preservation
- RGBY: Pallet `$0B`; Red house 1F/2F `$0A`; Blue/Green house `$0A`; Oak Lab `$03`.
- Gold: Pallet `$0F`; all four interiors `$00`.
- Border blocks are kept in the capacity/allocation set even when absent from the map `.blk` payload.

## Warp validation
- Pallet Town three RGBY building entrances resolve to Gen II `DOOR`.
- Red’s House and Blue/Green’s House bottom exits resolve to `WARP_CARPET_DOWN`.
- Red’s House inter-floor stair warps retain `FLOOR + warp_event`, matching Gold behavior at the same coordinates.
- Oak’s Lab two bottom exits resolve to `WARP_CARPET_DOWN`.

## Preservation rule
No RGBY or Gold collision/content is removed. Imported RGBY blocks receive converted collision data; original Gold metatiles keep their original collision entries. If a visually identical block requires different collision semantics, it must remain a separate metatile entry.

## Next
Allocate the actual merged metatile IDs and static tile IDs for all five Pallet-cluster maps while preserving Gold IDs where safe. Animated/reserved tile IDs are excluded from RGBY-only allocation. Then emit final Gen II metatile, collision, map-remap and 2bpp assets.
