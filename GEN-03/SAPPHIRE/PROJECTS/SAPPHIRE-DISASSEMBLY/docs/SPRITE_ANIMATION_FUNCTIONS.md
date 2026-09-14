# `sprite.c` animation-loop reconstruction map

This pass continues immediately after `DestroySpriteAndFreeResources` and maps the next sprite-animation block across all nine Pokémon Sapphire reference ROMs.

## Covered sequence

International builds contain:

`DrawPartyMenuMonText → AnimateSprite → BeginAnim → ContinueAnim → AnimCmd_frame → AnimCmd_end → AnimCmd_jump → AnimCmd_loop → BeginAnimLoop → ContinueAnimLoop → JumpToTopOfAnimLoop`.

The Japanese retail build transitions directly from `DestroySpriteAndFreeResources` to `AnimateSprite`; there is no `DrawPartyMenuMonText` body in this sequential `sprite.c` region. Exact addresses and sizes are stored in `config/sprite_animation.yml`.

## Structural split: Japanese vs. international

At the end of the previous pass the JP/AXPE start delta is `-0x14`:

- JP next byte: `0x08001418`
- AXPE next byte: `0x0800142C`

AXPE then contains `DrawPartyMenuMonText` from `0x0800142C` through `0x080014FB` (`0xD0` bytes), while the JP build starts `AnimateSprite` immediately at `0x08001418`.

Therefore, from `AnimateSprite` through `JumpToTopOfAnimLoop`, the JP layout is AXPE `-0xE4`. The animation functions in this pass retain the same sizes between JP and AXPE; the larger displacement comes from the earlier `ResetAllSprites` size difference (`-0x4`) plus the omitted international-only `DrawPartyMenuMonText` block (`-0xD0`) on top of the pre-existing `-0x10` layout difference.

DE/FR/IT continue to preserve AXPE sizes at a constant `+0x134` displacement.

## Function boundaries

| Function | JP | AXPE | DE/FR/IT | Size |
| --- | ---: | ---: | ---: | ---: |
| `DrawPartyMenuMonText` | — | `0x0800142C` | `0x08001560` | `0xD0` |
| `AnimateSprite` | `0x08001418` | `0x080014FC` | `0x08001630` | `0x48` |
| `BeginAnim` | `0x08001460` | `0x08001544` | `0x08001678` | `0xF0` |
| `ContinueAnim` | `0x08001550` | `0x08001634` | `0x08001768` | `0xA0` |
| `AnimCmd_frame` | `0x080015F0` | `0x080016D4` | `0x08001808` | `0xAC` |
| `AnimCmd_end` | `0x0800169C` | `0x08001780` | `0x080018B4` | `0x18` |
| `AnimCmd_jump` | `0x080016B4` | `0x08001798` | `0x080018CC` | `0xC8` |
| `AnimCmd_loop` | `0x0800177C` | `0x08001860` | `0x08001994` | `0x20` |
| `BeginAnimLoop` | `0x0800179C` | `0x08001880` | `0x080019B4` | `0x38` |
| `ContinueAnimLoop` | `0x080017D4` | `0x080018B8` | `0x080019EC` | `0x20` |
| `JumpToTopOfAnimLoop` | `0x080017F4` | `0x080018D8` | `0x08001A0C` | `0x74` |

## Byte-level findings

All nine ROM identities were rechecked before fingerprint generation. The following revision pairs are byte-identical for every function present in their shared sequence:

- `EUR-AXPE-v1` = `USA-EUR-AXPE-v2` (`11/11`)
- `FRA-AXPF-v0` = `FRA-AXPF-v1` (`11/11`)
- `ITA-AXPI-v0` = `ITA-AXPI-v1` (`11/11`)

Across all eight non-Japanese builds, eight of the eleven international function bodies are raw-byte identical: `BeginAnim`, `AnimCmd_frame`, `AnimCmd_end`, `AnimCmd_jump`, `AnimCmd_loop`, `BeginAnimLoop`, `ContinueAnimLoop`, and `JumpToTopOfAnimLoop`.

Five helpers are raw-byte identical across all nine ROMs: `AnimCmd_end`, `AnimCmd_loop`, `BeginAnimLoop`, `ContinueAnimLoop`, and `JumpToTopOfAnimLoop`.

The remaining differences are retained as target-specific fingerprints because they contain build-dependent addresses, call targets, or source-layout differences.

## Verification

`tools/analyze_sprite_animation.py` fingerprints this block directly from a local read-only Sapphire ROM. Per-target expected fingerprints are stored under `verification/sprite_animation/`.

The ROM bytes are authoritative for all boundaries and hashes. Current `pret/pokeruby/src/sprite.c` is used only to attach source-level names and semantics to the independently measured retail sequence.

## Next boundary

The next function is `BeginAffineAnim`:

- JP: `0x08001868`
- AXPE: `0x0800194C`
- DE/FR/IT: `0x08001A80`

The next pass should continue through the affine-animation command/state helpers while preserving the independent JP layout map.
