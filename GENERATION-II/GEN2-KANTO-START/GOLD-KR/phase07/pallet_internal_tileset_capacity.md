# GEN2 Kanto Start — GOLD KR Phase 07
## Pallet Town internal RGBY+GOLD tileset capacity

Status: ANALYSIS / NO ROM PATCH IN THIS PHASE
Base implementation ROM: `Pocket Monsters Geum (Korea).gbc`

## Scope

This phase covers the four Pallet Town interior maps:

- Red's House 1F
- Red's House 2F
- Blue/Green's House
- Professor Oak's Lab

The goal is to prove whether RGBY and Korean Gold visual structures can coexist in the Generation II renderer without discarding either generation's tiles.

## Critical source correction

Generation I `OaksLab` does **not** use the Gen I `LAB` tileset. Its map header uses `DOJO`, and `DOJO`/`GYM` share `gym.2bpp` + `gym.bst` in pokered.

The correct conversion pair is therefore:

`RGBY DOJO/GYM -> GOLD LAB`

Using Gen I `lab.bst` for Oak's Lab is incorrect.

## ROM-grounded byte verification

The public disassembly data was searched directly in the uploaded source ROMs. Each listed source byte sequence occurred exactly once.

| Asset | ROM file offset | Bank | CPU address | Bytes verified |
|---|---:|---:|---:|---:|
| Gen I RedsHouse blockset | `0x65270` | 25 | `0x5270` | 304 |
| Gen I House blockset | `0x65980` | 25 | `0x5980` | 560 |
| Gen I Dojo/Gym blockset | `0x6867F` | 26 | `0x467F` | 1856 |
| Gen II PlayersHouse metatiles | `0x1E22C` | 7 | `0x622C` | 1024 |
| Gen II House metatiles | `0xDE5D3` | 55 | `0x65D3` | 1021-byte verified prefix |
| Gen II Lab metatiles | `0x20E82` | 8 | `0x4E82` | 1024 |

No source ROM binary is stored in this repository.

## Capacity result

Generation II static BG tileset budget used here: 96 8x8 tiles. Metatile budget: 128 4x4 blocks.

| Final merged interior | Gen I used tiles | Gen II used tiles | Conservative tile upper bound | Exact pixel union | Conservative metatile upper bound | Result |
|---|---:|---:|---:|---:|---:|---|
| Red's House 1F | 40 | 42 | 82 | **79** | 18 | FIT |
| Red's House 2F | 49 | 49 | 98 | **93** | 16 | FIT |
| Blue/Green's House | 37 | 51 | **88** | not required | 24 | FIT |
| Oak's Lab | 30 | 38 | **68** | not required | 22 | FIT |

### Red's House split is required

If both Red's House floors are forced to share one merged tileset, the exact cross-generation pixel union is 125 unique tiles, exceeding the 96-tile static budget.

Therefore the merged implementation must split the floors:

- `REDS_HOUSE_1F_MERGED` — 79 used unique pixel tiles
- `REDS_HOUSE_2F_MERGED` — 93 used unique pixel tiles

This preserves RGBY and Gold visuals without expanding the Generation II VRAM model.

### Blue/Green's House and Oak's Lab

Both fit even if Gen I and Gen II tile IDs are pessimistically treated as completely unrelated:

- Blue/Green's House: `88 / 96`
- Oak's Lab: `68 / 96`

Pixel deduplication is therefore optional rather than required for capacity.

## Pallet cluster tileset architecture

The Pallet Town cluster should use five integration tileset domains:

1. `PALLET_MERGED` — exterior; prior result 89 used unique tiles
2. `REDS_HOUSE_1F_MERGED`
3. `REDS_HOUSE_2F_MERGED`
4. `BLUES_HOUSE_MERGED`
5. `OAKS_LAB_MERGED`

The two Red's House floors must not be forced back into one merged static tileset.

## Collision conversion rule for the next phase

Do not copy Generation I passability bytes directly into Generation II `tilecoll` data.

Next phase must:

1. preserve existing Gold collision definitions for Gold-origin blocks;
2. derive Gen I quadrant behavior from the exact Gen I 4x4 block tile layout and collision lists;
3. translate doors, stairs, warps and other special movement semantics explicitly rather than flattening all passable cells to generic floor;
4. validate every resulting quadrant in-game.

## Result

**Phase 07 graphics capacity: PASS.**

All Pallet Town exterior/interior RGBY + Korean Gold visual content can be retained within normal Generation II static tileset limits by using map-specific merged tilesets. No VRAM-engine expansion is required for the Pallet cluster at this stage.

Next: merged metatile/collision mapping, then NPC/event/script integration.