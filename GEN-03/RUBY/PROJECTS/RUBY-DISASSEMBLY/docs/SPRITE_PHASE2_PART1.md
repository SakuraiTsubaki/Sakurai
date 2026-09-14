# Sprite engine reconstruction — Phase 2, Part 1

This pass continues at the byte immediately following `ClearPokemonCrySongs` and confirms that the next linked object is `sprite.o`, matching the public `pokeruby` linker order `main.o -> sprite.o -> text.o -> string_util.o -> link.o -> rtc.o`.

The mapped scope is the sprite engine from `ResetSpriteData` through `ContinueAnim`. The next confirmed boundary is `AnimCmd_frame`.

## Coverage

Three compiler/layout families are required for the verified 13-ROM set:

| Family | Targets | Functions mapped | Region size |
|---|---:|---:|---:|
| `retail_intl` | 11 retail international targets | 38 | `0xF8C` |
| `japan` | Japan Rev 0 | 37 | `0xEA4` |
| `german_debug` | German Debug | 38 | `0xFA4` |

That is 493 verified target/function records in this first sprite-engine pass.

The exact relative function boundaries and sizes are stored in `symbols/sprite_part1_layouts.csv`. Per-target base/end offsets and mapped-region SHA-1 fingerprints are in `symbols/sprite_part1_targets.csv`. `tools/analyze_sprite_part1.py` verifies the whole ROM first, verifies the mapped region, then regenerates per-function addresses and SHA-1 fingerprints.

## Family differences

### Retail international

English Rev 0/1/2, German Rev 0/1, French Rev 0/1, Italian Rev 0/1, and Spanish Rev 0/1 share the same Part-1 function-boundary layout. Literal pools and called addresses still vary by target, so each target retains its own fingerprints.

### Japanese

The Japanese build shares the same early sprite-engine semantics but differs in several compiled function sizes. In particular, `CopyMatricesToOamBuffer`, `AddSpritesToOamBuffer`, and `ResetAllSprites` are smaller than the international layout.

The international `DrawPartyMenuMonText` block is not present between `DestroySpriteAndFreeResources` and `AnimateSprite` in this Japanese linked sequence: `AnimateSprite` begins directly at relative `+0xCCC`. This pass records the observed ROM layout only; any Japanese-specific replacement/call path will be resolved when the related party-menu/text objects are mapped.

### German debug

The German debug build follows the retail international layout until the sprite-copy request functions. Its debug-only overflow handling contains `Crash(sDmaOverErrorMsg)` branches in `RequestSpriteFrameImageCopy` and `RequestSpriteCopy`. Those two functions are each 12 bytes larger than retail, shifting all following Part-1 code by `+0x18` overall.

## Target region fingerprints

| Target/group | Start | End | Size | SHA-1 |
|---|---:|---:|---:|---|
| Japan Rev 0 | `0x74C` | `0x15F0` | `0xEA4` | `217fff7e0511bac82c99eb6f97f603eea884c560` |
| English Rev 0 | `0x748` | `0x16D4` | `0xF8C` | `02aa36aa39c95e3e0692f6b217fc8ef57bec6e0d` |
| English Rev 1/2 | `0x748` | `0x16D4` | `0xF8C` | `2e06fa9b2be3fd683a1ce34a075d08d366219930` |
| German Rev 0/1 | `0x87C` | `0x1808` | `0xF8C` | `93129324a367ba2cc6143109ebe3b295b8a2d034` |
| German Debug | `0x87C` | `0x1820` | `0xFA4` | `76172c5ca607f1b6197a2fdd88b52dcf43121e7c` |
| French Rev 0/1 | `0x87C` | `0x1808` | `0xF8C` | `870a5c9ddba29b2f7b86ec1ad6264b0bc6c27a28` |
| Italian Rev 0/1 | `0x87C` | `0x1808` | `0xF8C` | `f2b58f94b198040989f673f4ced88bf96bcb5863` |
| Spanish Rev 0/1 | `0x87C` | `0x1808` | `0xF8C` | `a6492ac1652989a5dda09dc1921e4f0ece171334` |

## Engine code vs. graphical sprite assets

This pass maps `sprite.c` engine code only. It does **not** extract Pokémon/trainer/overworld graphic tiles yet, so there are no visual sprite images to add in this specific pass. When graphical sprite extraction begins, the repository will include the rebuildable tile/palette/source data **and human-viewable PNG images** together.

## Next pass

Continue at `AnimCmd_frame`, finish the normal animation command loop, then map the affine-animation command/state machinery and the remaining `sprite.c` functions. After the complete `sprite.o` boundary is identified, proceed to `text.o`.
