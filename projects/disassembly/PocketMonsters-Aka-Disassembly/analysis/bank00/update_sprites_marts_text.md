# Japanese Bank 00 — `UpdateSprites`, marts, and overworld text

This range continues immediately after the Bank 00 audio dispatcher and ends immediately before `UncompressSpriteData`.

## ROM-verified ranges

| Build | Range | Size | SHA-1 | Next routine |
|---|---:|---:|---|---|
| V1.0 | `$0EBD-$0FCD` | 273 bytes | `37b02753579c1a722df7279698851b4c0f5aee3b` | `UncompressSpriteData` at `$0FCE` |
| V1.1 | `$0EAB-$0FBB` | 273 bytes | `3a4ee1ffbcfd876b6673668d90e0f228b330c741` | `UncompressSpriteData` at `$0FBC` |

Aligned by relative offset, only three bytes differ between revisions. They are all address operands caused by the `$12` relocation of the Bank 00 block or by the revision-specific `Predef` address.

## Subranges

### `UpdateSprites`

- V1.0 `$0EBD-$0ED5`
- V1.1 `$0EAB-$0EC3`
- 25 bytes
- shared SHA-1 `6f1d866957939a078153f34a7be865d1c52fc9eb`

This is a Bank 00 trampoline that checks `wUpdateSpritesEnabled`, temporarily switches to bank 1, calls `_UpdateSprites` at `01:4A1C`, then restores the previous bank. It is sprite-processing code only; it contains no sprite image pixels.

### Mart inventory scripts

- V1.0 `$0ED6-$0F68`
- V1.1 `$0EC4-$0F56`
- 147 bytes
- shared SHA-1 `bef836f194fcc8376c5745b5487fe7b722b4e3b3`

The complete Bank 00 mart inventory block is byte-identical in both revisions, including the unreferenced Bike Shop and unused mart lists. Source is `data/items/jp_marts.asm`.

### Common overworld text

- V1.0 `$0F69-$0FCD`
- V1.1 `$0F57-$0FBB`
- 101 bytes
- V1.0 SHA-1 `468135746ddc6fb5023ca3d25c8ea3caf1f252e9`
- V1.1 SHA-1 `f1dff9eca636e77b3890d2e8b52be2cf33e9aaaf`

Recovered labels include `TextScriptEnd`, `ExclamationText`, `GroundRoseText`, `BoulderText`, `MartSignText`, `PokeCenterSignText`, and `PickUpItemText`. The only aligned byte differences are the relocated `TextScriptEndingText` pointer, the revision-specific `Predef` call operand, and the relocated `TextScriptEnd` jump operand.

Source files:

- `home/jp_update_sprites.asm`
- `data/items/jp_marts.asm`
- `home/jp_overworld_text.asm`

The following Bank 00 routine is the sprite compression/decompression engine. Actual sprite artwork is not stored in this range; when sprite graphics data banks are reached, reconstructed PNGs and their tile-source/build metadata must be committed alongside the source.
