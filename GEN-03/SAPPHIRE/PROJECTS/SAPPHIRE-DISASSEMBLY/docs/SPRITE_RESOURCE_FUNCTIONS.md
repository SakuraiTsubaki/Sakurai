# `sprite.c` resource-management reconstruction map

This pass continues immediately after `CalcCenterToCornerVec` and maps the next 13 `sprite.c` functions across all nine Sapphire reference ROMs. The covered retail block begins with sprite tile allocation and ends after destruction/freeing of tile, palette, and OAM-matrix resources.

## Covered functions

`AllocSpriteTiles → SpriteTileAllocBitmapOp → SpriteCallbackDummy → ProcessSpriteCopyRequests → RequestSpriteFrameImageCopy → RequestSpriteCopy → CopyFromSprites → CopyToSprites → ResetAllSprites → FreeSpriteTiles → FreeSpritePalette → FreeSpriteOamMatrix → DestroySpriteAndFreeResources`.

Exact per-family addresses and sizes are stored in `config/sprite_resources.yml`.

## Boundary provenance

The AXPE retail boundaries were cross-checked against the historical pre-decomp `pret/pokeruby` assembly at commit `4af578c1865e4b620f4c64401e0a16ccbd9efc8d`, where the block appears under older object-oriented names such as `AllocObjectTiles`, `Unused_ObjectTileAllocationBitArrayOp`, `ProcessObjectCopyRequests`, and `RemoveObjectAndFreeResources`. Current `pret/pokeruby/src/sprite.c` supplies the modern source-level names used by this repository.

The retail ROM bytes remain the authority for addresses, sizes, and hashes.

## Family layout

The block starts at:

- JP: `AllocSpriteTiles @ 0x08001074`
- AXPE: `AllocSpriteTiles @ 0x08001084`
- DE/FR/IT: `AllocSpriteTiles @ 0x080011B8`

DE/FR/IT preserve AXPE function sizes and remain at AXPE `+0x134` throughout this block.

Japanese layout requires an independent boundary map. It initially remains AXPE `-0x10`, but `ResetAllSprites` is `0x3C` bytes in JP versus `0x40` bytes in the international builds. Consequently the following JP functions begin AXPE `-0x14` through the end of this pass:

| Function | JP | AXPE | JP size | AXPE size |
| --- | ---: | ---: | ---: | ---: |
| `ResetAllSprites` | `0x08001364` | `0x08001374` | `0x3C` | `0x40` |
| `FreeSpriteTiles` | `0x080013A0` | `0x080013B4` | `0x1C` | `0x1C` |
| `FreeSpritePalette` | `0x080013BC` | `0x080013D0` | `0x10` | `0x10` |
| `FreeSpriteOamMatrix` | `0x080013CC` | `0x080013E0` | `0x2C` | `0x2C` |
| `DestroySpriteAndFreeResources` | `0x080013F8` | `0x0800140C` | `0x20` | `0x20` |

## Byte-level findings

All nine reference ROM identities were rechecked against `config/versions.yml` before generating fingerprints.

The following revision pairs are byte-identical for all 13 functions in this block:

- `EUR-AXPE-v1` = `USA-EUR-AXPE-v2`
- `FRA-AXPF-v0` = `FRA-AXPF-v1`
- `ITA-AXPI-v0` = `ITA-AXPI-v1`

For non-Japanese builds, 11 of 13 function bodies collapse to one raw SHA-256 value across every language/revision in this block. The two exceptions are `ProcessSpriteCopyRequests` and `ResetAllSprites`, whose linked addresses/call targets vary by build while their mapped boundaries remain stable.

`SpriteCallbackDummy`, `CopyFromSprites`, and `CopyToSprites` are raw-byte identical across all nine analyzed ROMs. Other JP differences are expected from linked addresses and compiler/layout variation and are retained as separate fingerprints rather than normalized away.

## Verification

`tools/analyze_sprite_resources.py` fingerprints this block directly from a local read-only Sapphire ROM. The aggregate output for 9 ROMs × 13 functions is stored under `verification/sprite_resources/`.

## Next boundary

The next source-level function is `DrawPartyMenuMonText` (historical assembly label `sub_800142C` for AXPE):

- JP next boundary: `0x08001418`
- AXPE next boundary: `0x0800142C`
- DE/FR/IT next boundary: `0x08001560`

The Japanese body diverges structurally at this point, so the next pass must continue with independent function-boundary confirmation rather than applying the AXPE delta mechanically.
