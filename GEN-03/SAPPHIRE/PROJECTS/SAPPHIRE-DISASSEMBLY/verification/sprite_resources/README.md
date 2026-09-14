# Sprite resource block verification

This directory records SHA-256 fingerprints for the 13-function `src/sprite.c` block from `AllocSpriteTiles` through `DestroySpriteAndFreeResources`.

`manifest.csv` contains 117 rows: 9 verified Sapphire ROM releases × 13 mapped functions. ROM binaries are not stored in the repository.

Generate a per-ROM record with:

```sh
python3 tools/analyze_sprite_resources.py /path/to/sapphire.gba --format csv
```

Addresses are release-family aware. In particular, the Japanese `ResetAllSprites` function is four bytes shorter than the international build, so later JP addresses in this block are not derived from one constant offset.
