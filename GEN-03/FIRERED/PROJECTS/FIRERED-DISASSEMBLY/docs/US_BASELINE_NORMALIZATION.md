# English FireRed Baseline Normalization

Audit date: 2026-09-13

The two user-supplied English FireRed images had valid GBA headers but did not initially match the canonical public SHA-1 values. Byte-level inspection showed that each image differs from the canonical target only in the final two bytes of the 16 MiB ROM image.

## Rev 0 / BPRE revision 0

- Original local tail at `0x00FFFFFE-0x00FFFFFF`: `00 19`
- Canonical padding tail: `FF FF`
- No other byte change is required.
- Normalized CRC32: `dd88761c`
- Normalized MD5: `e26ee0d44e809351c8ce2d73c7400cdd`
- Normalized SHA-1: `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`
- Normalized SHA-256: `3d0c79f1627022e18765766f6cb5ea067f6b5bf7dca115552189ad65a5c3a8ac`

## Rev 1 / BPRE revision 1

- Original local tail at `0x00FFFFFE-0x00FFFFFF`: `00 18`
- Canonical padding tail: `FF FF`
- No other byte change is required.
- Normalized CRC32: `84ee4776`
- Normalized MD5: `51901a6e40661b3914aa333c802e24e8`
- Normalized SHA-1: `dd5945db9b930750cb39d00c84da8571feebf417`
- Normalized SHA-256: `729041b940afe031302d630fdbe57c0c145f3f7b6d9b8eca5e98678d0ca4d059`

## Handling policy

The originally supplied files remain read-only and unchanged. Normalized images are derived work copies only and are never committed to GitHub. The repository stores the transformation rule, verification hashes, and tooling required to reproduce the normalization.

This establishes canonical English Rev 0 and Rev 1 reconstruction targets without treating the altered local files themselves as canonical baselines.
