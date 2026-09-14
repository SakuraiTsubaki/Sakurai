# Early `sprite.c` reconstruction map

This stage begins immediately after `ClearPokemonCrySongs` and confirms that the next linked source unit is `src/sprite.c`. The first 21 functions, from `ResetSpriteData` through `CalcCenterToCornerVec`, have been mapped across all nine Sapphire reference ROMs.

## Source-unit boundary

The linker order in public `pret/pokeruby` is `src/crt0.o → src/main.o → src/sprite.o`, matching the retail transition observed here. The first sprite function is:

- JP: `ResetSpriteData @ 0x0800074C`
- AXPE: `ResetSpriteData @ 0x08000748`
- DE/FR/IT: `ResetSpriteData @ 0x0800087C`

Its retail call sequence matches the reconstructed source semantics: `ResetOamRange(0, 128)`, `ResetAllSprites`, `ClearSpriteCopyRequests`, `ResetAffineAnimData`, `FreeSpriteTileRanges`, then sprite/OAM state initialization.

## First 21 functions

The mapped block is:

`ResetSpriteData → AnimateSprites → BuildOamBuffer → UpdateOamCoords → BuildSpritePriorities → SortSprites → CopyMatricesToOamBuffer → AddSpritesToOamBuffer → CreateSprite → CreateSpriteAtEnd → CreateInvisibleSprite → CreateSpriteAt → CreateSpriteAndAnimate → DestroySprite → ResetOamRange → LoadOam → ClearSpriteCopyRequests → ResetOamMatrices → SetOamMatrix → ResetSprite → CalcCenterToCornerVec`.

Exact addresses and sizes for each region family are stored in `config/early_sprite.yml`.

## Japanese compiler/layout differences

The Japanese build is not a simple fixed-offset copy of the international code. The first six functions keep the same sizes as AXPE, but two OAM-building functions diverge:

| Function | JP size | International size |
| --- | ---: | ---: |
| `CopyMatricesToOamBuffer` | `0x4C` | `0x54` |
| `AddSpritesToOamBuffer` | `0x8C` | `0x98` |

After these differences, subsequent JP function addresses are `0x10` earlier than the equivalent AXPE addresses through the end of this mapped block. Therefore Japanese function boundaries are tracked independently rather than inferred by a constant delta.

## International and revision findings

DE/FR/IT preserve the international function sizes in this block and are located at AXPE offsets plus `0x134`, inherited from the extended pre-`Init` localization metadata.

The following revision pairs are byte-identical for all 21 mapped sprite functions:

- `EUR-AXPE-v1` = `USA-EUR-AXPE-v2`
- `FRA-AXPF-v0` = `FRA-AXPF-v1`
- `ITA-AXPI-v0` = `ITA-AXPI-v1`

Thirteen function bodies are byte-identical across every analyzed non-Japanese target despite language-specific ROM layouts: `ResetSpriteData`, `BuildOamBuffer`, `UpdateOamCoords`, `BuildSpritePriorities`, `SortSprites`, `CopyMatricesToOamBuffer`, `CreateSprite`, `CreateSpriteAtEnd`, `CreateSpriteAt`, `DestroySprite`, `ClearSpriteCopyRequests`, `ResetOamMatrices`, and `SetOamMatrix`. Functions that embed linked addresses or language-build-specific targets differ while preserving the same boundaries and source semantics.

## Verification

`tools/analyze_early_sprite.py` fingerprints these 21 boundaries directly from a local read-only retail ROM. Per-target SHA-256 records are kept under `verification/early_sprite/` so future reconstruction changes can be checked independently for every supported release.

## Continuation

The next function is `AllocSpriteTiles`:

- JP: `0x08001074`
- AXPE: `0x08001084`
- DE/FR/IT: `0x080011B8`

That continuation is now mapped through `DestroySpriteAndFreeResources`. See `docs/SPRITE_RESOURCE_FUNCTIONS.md`, `config/sprite_resources.yml`, and `verification/sprite_resources/` for the next 13 functions and their 117 per-target fingerprints.
