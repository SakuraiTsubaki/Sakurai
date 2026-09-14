# Japanese Bank 00 — `$0B3C-$0BA6`

This range contains the DMG palette loading/fade routines and eight packed palette triplets used by Japanese Red V1.0/V1.1.

Recovered structured source in `home/jp_fade.asm` includes:

- `LoadGBPal`
- `GBFadeInFromBlack`
- `GBFadeOutToWhite`
- `GBFadeIncCommon`
- `GBFadeOutToBlack`
- `GBFadeInFromWhite`
- `GBFadeDecCommon`
- `FadePal1` through `FadePal8`

## ROM verification

The complete range is 107 bytes (`$0B3C-$0BA6` inclusive).

- V1.0 SHA-1: `47c726b87c4a965e5a90cfa6800baf242be34251`
- V1.1 SHA-1: `b50ead680f9e38ffe83d5904f46ff300a93f1bf8`
- differing bytes: 2

Both differences are the low byte of the two `DelayFrames` call operands:

- V1.0: `DelayFrames = $3781`
- V1.1: `DelayFrames = $376F`

The palette data itself is byte-identical between revisions. `wMapPalOffset = $D2DC` is decoded directly from the machine code and recorded in `constants/memory.asm`.
