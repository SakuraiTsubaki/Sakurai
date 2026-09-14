# `sprite.c` sprite-sheet and tile-range map

This pass continues at `LoadSpriteSheet` and maps 14 consecutive sprite-sheet/tile-range functions across all nine Sapphire reference ROMs, ending at `LoadSpriteSheetDeferred`.

## Covered functions

`LoadSpriteSheet → LoadSpriteSheets → AllocTilesForSpriteSheet → AllocTilesForSpriteSheets → LoadTilesForSpriteSheet → LoadTilesForSpriteSheets → FreeSpriteTilesByTag → FreeSpriteTileRanges → GetSpriteTileStartByTag → IndexOfSpriteTileTag → GetSpriteTileTagByTileStart → AllocSpriteTileRange → RequestSpriteSheetCopy → LoadSpriteSheetDeferred`.

Exact addresses and sizes live in `config/sprite_sheet_tiles.yml`.

## Historical AXPE boundaries

The retail AXPE boundaries were cross-checked against historical `pret/pokeruby` assembly at commit `4af578c1865e4b620f4c64401e0a16ccbd9efc8d`:

| Current name | Historical label | AXPE address |
| --- | --- | ---: |
| `LoadSpriteSheet` | `LoadObjectPic` | `0x080022A8` |
| `LoadSpriteSheets` | `LoadObjectPics` | `0x080022EC` |
| `AllocTilesForSpriteSheet` | `sub_8002318` | `0x08002318` |
| `AllocTilesForSpriteSheets` | `sub_8002344` | `0x08002344` |
| `LoadTilesForSpriteSheet` | `sub_8002370` | `0x08002370` |
| `LoadTilesForSpriteSheets` | `sub_800239C` | `0x0800239C` |
| `FreeSpriteTilesByTag` | `FreeObjectTilesByTag` | `0x080023C8` |
| `FreeSpriteTileRanges` | `FreeAllObjectTiles` | `0x08002440` |
| `GetSpriteTileStartByTag` | `GetObjectTileRangeStartByTag` | `0x08002480` |
| `IndexOfSpriteTileTag` | `IndexOfObjectTilesTag` | `0x080024AC` |
| `GetSpriteTileTagByTileStart` | `GetTagByObjectTileRangeStart` | `0x080024D8` |
| `AllocSpriteTileRange` | `AddObjectTileRange` | `0x08002524` |
| `RequestSpriteSheetCopy` | `sub_800256C` | `0x0800256C` |
| `LoadSpriteSheetDeferred` | `sub_8002594` | `0x08002594` |

## Family layout

All 14 functions have the same sizes in JP and international builds. The established displacement therefore remains constant:

- JP = AXPE `-0xE4`
- DE/FR/IT = AXPE `+0x134`

The next function is `FreeAllSpritePalettes`:

- JP: `0x080024E4`
- AXPE: `0x080025C8`
- DE/FR/IT: `0x080026FC`

## Byte-level findings

`LoadSpriteSheets` is raw-byte identical across all nine ROMs.

Across the eight international ROMs, 12 of the 14 functions are raw-byte identical. The two build-dependent functions are `LoadSpriteSheet` and `LoadTilesForSpriteSheet`, which embed build-specific call or data addresses.

The JP build differs in additional tile-range helpers because RAM/data placement differs, but preserves the same function sizes and control-flow ordering.

The following revision pairs are byte-identical for all 14 functions:

- `EUR-AXPE-v1` = `USA-EUR-AXPE-v2`
- `FRA-AXPF-v0` = `FRA-AXPF-v1`
- `ITA-AXPI-v0` = `ITA-AXPI-v1`

## Verification

`tools/analyze_sprite_sheet_tiles.py` fingerprints this block. Per-target expected SHA-256 fingerprints live under `verification/sprite_sheet_tiles/`.

## Next boundary

Continue at `FreeAllSpritePalettes` into sprite palette allocation/loading and palette tag management.
