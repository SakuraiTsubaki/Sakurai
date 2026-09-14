# `sprite.c` affine-frame and public animation API map

This pass continues immediately after `DecrementAffineAnimDelayCounter` and maps 17 consecutive `sprite.c` functions across all nine Sapphire reference ROMs. The scope covers affine-frame application, image/affine animation control APIs, affine-state reset/allocation, and OAM matrix rotation/scaling.

## Covered functions

`ApplyAffineAnimFrameRelativeAndUpdateMatrix → ConvertScaleParam → GetAffineAnimFrame → ApplyAffineAnimFrame → StartSpriteAnim → StartSpriteAnimIfDifferent → SeekSpriteAnim → StartSpriteAffineAnim → StartSpriteAffineAnimIfDifferent → ChangeSpriteAffineAnim → ChangeSpriteAffineAnimIfDifferent → SetSpriteSheetFrameTileNum → ResetAffineAnimData → AllocOamMatrix → FreeOamMatrix → InitSpriteAffineAnim → SetOamMatrixRotationScaling`.

Exact per-family addresses and sizes live in `config/sprite_affine_api.yml`.

## Historical symbol cross-check

The AXPE boundaries were cross-checked against historical `pret/pokeruby` assembly at commit `4af578c1865e4b620f4c64401e0a16ccbd9efc8d`.

| Current name | Historical label | AXPE address |
| --- | --- | ---: |
| `ApplyAffineAnimFrameRelativeAndUpdateMatrix` | `rotscale_frame_apply_relative_and_sync` | `0x08001DFC` |
| `ConvertScaleParam` | `divide_0x10000_by` | `0x08001E94` |
| `GetAffineAnimFrame` | `rotscale_load_frame` | `0x08001EAC` |
| `ApplyAffineAnimFrame` | `sub_8001F18` | `0x08001F18` |
| `StartSpriteAnim` | `StartObjectImageAnim` | `0x08001F58` |
| `StartSpriteAnimIfDifferent` | `StartObjectImageAnimIfDifferent` | `0x08001F70` |
| `SeekSpriteAnim` | `SeekObjectImageAnim` | `0x08001F8C` |
| `StartSpriteAffineAnim` | `StartObjectRotScalAnim` | `0x08002008` |
| `StartSpriteAffineAnimIfDifferent` | `StartObjectRotScalAnimIfDifferent` | `0x08002034` |
| `ChangeSpriteAffineAnim` | `sub_8002068` | `0x08002068` |
| `ChangeSpriteAffineAnimIfDifferent` | `sub_80020A0` | `0x080020A0` |
| `SetSpriteSheetFrameTileNum` | `sub_80020D4` | `0x080020D4` |
| `ResetAffineAnimData` | `rotscale_reset_all` | `0x0800212C` |
| `AllocOamMatrix` | `rotscale_alloc_entry` | `0x08002160` |
| `FreeOamMatrix` | `rotscale_free_entry` | `0x08002198` |
| `InitSpriteAffineAnim` | `obj_alloc_rotscale_entry` | `0x080021D8` |
| `SetOamMatrixRotationScaling` | `sub_8002228` | `0x08002228` |

Retail ROM bytes remain authoritative for the multi-region map and fingerprints.

## Family layout

All 17 functions retain the same sizes in JP and the international builds for this pass. The established layout offsets therefore remain constant through the full block:

- JP = AXPE `-0xE4`
- DE/FR/IT = AXPE `+0x134`

The next source-level function is `LoadSpriteSheet`:

- JP: `0x080021C4`
- AXPE: `0x080022A8`
- DE/FR/IT: `0x080023DC`

## Byte-level findings

The following 10 functions are raw-byte identical across all nine ROMs:

`GetAffineAnimFrame`, `ApplyAffineAnimFrame`, `StartSpriteAnim`, `StartSpriteAnimIfDifferent`, `SeekSpriteAnim`, `StartSpriteAffineAnim`, `StartSpriteAffineAnimIfDifferent`, `ChangeSpriteAffineAnim`, `ChangeSpriteAffineAnimIfDifferent`, and `SetSpriteSheetFrameTileNum`.

Across the eight non-Japanese ROMs, 14 of 17 functions are raw-byte identical. `ResetAffineAnimData`, `AllocOamMatrix`, `FreeOamMatrix`, and `InitSpriteAffineAnim` are identical across all international builds but differ in JP because their linked RAM/function addresses differ.

The main build-specific code in this block is concentrated in `ApplyAffineAnimFrameRelativeAndUpdateMatrix`, `ConvertScaleParam`, and `SetOamMatrixRotationScaling`, where linked helper addresses and/or code placement vary.

The following revision pairs are byte-identical for all 17 functions:

- `EUR-AXPE-v1` = `USA-EUR-AXPE-v2`
- `FRA-AXPF-v0` = `FRA-AXPF-v1`
- `ITA-AXPI-v0` = `ITA-AXPI-v1`

## Verification

`tools/analyze_sprite_affine_api.py` fingerprints this block from a local read-only Sapphire ROM. Per-target expected fingerprints are stored under `verification/sprite_affine_api/`.

## Next boundary

Continue with `LoadSpriteSheet` and the sprite-sheet/tile-range management functions while preserving the independent JP address map.
