# Pocket Monsters Midori JP Rev A — Korean title prototype

Target title display: **포켓몬스터 / 그린**

## Target

- Source ROM: `Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb`
- Source SHA-256: `3f0dc460ca8d06be1c9ac96307c939c0ea7baa366b40c2f1f4ad63242b6c4816`
- Source SHA-1: `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`

## Title asset mapping

- Large title-logo block: `0x10400`–`0x109FF`
- Length: `0x600` bytes / 1536 bytes
- Format: Game Boy 2bpp
- Layout: 16×6 tiles, row-major
- Tile count: 96

The block boundary was identified by tile-level inspection: the Japanese title-logo rows occupy the 0x10400–0x109FF range and the data at 0x10A00 changes to a different graphics/font region.

## Prototype output

The replacement asset renders `포켓몬스터` with a compact `그린` version label inside the same 128×48-pixel / 96-tile allocation, so this first prototype does not require relocating the title block.

The IPS patch contains only the replacement `0x600`-byte title block. The source ROM remains untouched and is not stored in GitHub.

## Verification

- IPS re-application reproduced the locally patched working copy byte-for-byte.
- Changed byte range remained inside the intended title block (`0x10400`–`0x109FF`).
- 1146 bytes differ from the original inside that block; the remaining bytes are naturally identical because of blank/background pixels.
- Runtime emulator verification is still pending in the current environment.

Reusable implementation assets are stored in the parallel Tsubaki path:
`GENERATION-I/POCKET-MONSTERS-RGBY/JAPAN-TO-KOREAN/MIDORI-REV-A/TITLE/`.
