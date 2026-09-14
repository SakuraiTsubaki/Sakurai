# Sprite engine reconstruction — Phase 2, Part 2

Part 2 begins at the `AnimCmd_frame` boundary immediately after the Part-1 `ContinueAnim` region and maps the complete normal animation-command core, affine animation-command core, animation state helpers, and OAM matrix allocation/initialization through `InitSpriteAffineAnim`.

## Coverage

- 42 functions per target.
- 13 verified Ruby ROM targets.
- 546 target/function records.
- Exactly `0xB54` / 2,900 bytes in every target.
- Next boundary: `SetOamMatrixRotationScaling`.

The common relative layout is stored in `symbols/sprite_part2_layout.csv`; target bases/end offsets and region hashes are in `symbols/sprite_part2_targets.csv`. `tools/analyze_sprite_part2.py` verifies the whole source ROM and the complete Part-2 region before generating per-function addresses and SHA-1 fingerprints.

## Important convergence

Part 1 required three layout families because of Japanese compiler/layout differences and German debug-only overflow handling. At `AnimCmd_frame`, those earlier shifts stop changing the internal layout: **all 13 targets share the same 42-function size/offset sequence for this entire Part-2 block**.

The targets still begin this common block at different file offsets:

| Target family | Part-2 start | Part-2 end |
|---|---:|---:|
| Japan Rev 0 | `0x15F0` | `0x2144` |
| English Rev 0/1/2 | `0x16D4` | `0x2228` |
| DE/FR/IT/ES retail | `0x1808` | `0x235C` |
| German Debug | `0x1820` | `0x2374` |

## Function groups

The mapped block contains:

- normal animation command handlers: `AnimCmd_frame`, `AnimCmd_end`, `AnimCmd_jump`, `AnimCmd_loop`, loop helpers;
- affine animation dispatch/loop handlers: `BeginAffineAnim`, `ContinueAffineAnim`, `AffineAnimDelay`, `AffineAnimCmd_*`, loop helpers;
- matrix/state helpers: `CopyOamMatrix`, `GetSpriteMatrixNum`, `SetSpriteOamFlipBits`, `AffineAnimState*`, affine-frame application and scale conversion;
- public animation controls: `StartSpriteAnim`, `StartSpriteAnimIfDifferent`, `SeekSpriteAnim`, `StartSpriteAffineAnim`, `ChangeSpriteAffineAnim`, and variants;
- affine/OAM setup: `ResetAffineAnimData`, `AllocOamMatrix`, `FreeOamMatrix`, `InitSpriteAffineAnim`.

## Region fingerprints

| Target/group | SHA-1 |
|---|---|
| Japan Rev 0 | `6f968d34ec3381eab3a0c6bfc4b448111ef5fcc2` |
| English Rev 0 | `60043948dee2e897522325fe48cd0ef8cf8bb691` |
| English Rev 1/2 | `89026f42648d79ce5fcf1821cef7040cd9fc9db8` |
| German Rev 0/1 | `2af90c823640dfda1fc7c4f25d9febb872624f74` |
| German Debug | `7a5f5b08db2925ac0c675bb18f78784dd3bbb5d6` |
| French Rev 0/1 | `c95c1d7bec07b0dcc7775c3ebe17e67dce5d24bb` |
| Italian Rev 0/1 | `12f5f88bf2776f950ad755a23dbf37ce69d9935d` |
| Spanish Rev 0/1 | `df6e199fabcf560d9ee49c10370c9c6f01836c71` |

## Cumulative sprite-engine coverage

After Parts 1 and 2, the mapped contiguous `sprite.o` prefix reaches:

| Target family | `sprite.o` start | Current mapped end | Bytes mapped |
|---|---:|---:|---:|
| Japan Rev 0 | `0x74C` | `0x2144` | `0x19F8` |
| English retail | `0x748` | `0x2228` | `0x1AE0` |
| DE/FR/IT/ES retail | `0x87C` | `0x235C` | `0x1AE0` |
| German Debug | `0x87C` | `0x2374` | `0x1AF8` |

Retail/debug targets now have 80 mapped sprite-engine functions; Japan has 79 because the Part-1 linked sequence does not contain the international `DrawPartyMenuMonText` block at that position.

## Next pass

Continue at `SetOamMatrixRotationScaling`, then map sprite sheet/tile allocation, palette management, subsprites/OAM construction, and the remaining sprite engine until the `sprite.o -> text.o` object boundary is identified.
