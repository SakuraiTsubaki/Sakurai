# `sprite.c` affine-animation core reconstruction map

This pass continues at `BeginAffineAnim` and maps the first 19 affine-animation helper functions through `DecrementAffineAnimDelayCounter` across all nine Pokémon Sapphire reference ROMs.

## Layout

The animation-layout split established in the previous pass remains stable through this whole block:

- JP starts at `BeginAffineAnim @ 0x08001868` and remains AXPE `-0xE4`.
- AXPE starts at `0x0800194C`.
- DE/FR/IT start at `0x08001A80` and remain AXPE `+0x134`.

All 19 mapped functions have the same sizes in JP and international builds. Exact addresses and sizes are stored in `config/sprite_affine_core.yml`.

## Byte-level findings

The following revision pairs are byte-identical for all 19 functions:

- `EUR-AXPE-v1` = `USA-EUR-AXPE-v2`
- `FRA-AXPF-v0` = `FRA-AXPF-v1`
- `ITA-AXPI-v0` = `ITA-AXPI-v1`

Eighteen of the nineteen functions are raw-byte identical across all eight non-Japanese builds; only `ContinueAffineAnim` differs because of build-dependent linked call targets.

Seventeen of the nineteen functions are raw-byte identical across **all nine ROMs**. The only functions that retain target-dependent raw bytes are:

- `ContinueAffineAnim`
- `CopyOamMatrix` (JP differs from the international builds because its literal/address encoding reflects the independent JP layout)

This makes the affine command/state core one of the most structurally stable regions measured so far.

## Covered functions

`BeginAffineAnim → ContinueAffineAnim → AffineAnimDelay → AffineAnimCmd_loop → BeginAffineAnimLoop → ContinueAffineAnimLoop → JumpToTopOfAffineAnimLoop → AffineAnimCmd_jump → AffineAnimCmd_end → AffineAnimCmd_frame → CopyOamMatrix → GetSpriteMatrixNum → SetSpriteOamFlipBits → AffineAnimStateRestartAnim → AffineAnimStateStartAnim → AffineAnimStateReset → ApplyAffineAnimFrameAbsolute → DecrementAnimDelayCounter → DecrementAffineAnimDelayCounter`.

## Verification

`tools/analyze_sprite_affine_core.py` fingerprints the block directly from a local read-only Sapphire ROM. Per-target expected fingerprints live under `verification/sprite_affine_core/`.

Retail ROM bytes are authoritative for boundaries and hashes. Current `pret/pokeruby/src/sprite.c` is used to attach source-level names and semantics.

## Next boundary

The next function is `ApplyAffineAnimFrameRelativeAndUpdateMatrix`:

- JP: `0x08001D18`
- AXPE: `0x08001DFC`
- DE/FR/IT: `0x08001F30`
