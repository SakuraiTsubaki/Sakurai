# Pokémon Green JP — Bank 03 deep audit (Rev 0 vs Rev A)

## Scope
- ROM bank: `03` (`0x00C000–0x00FFFF` file range; CPU `4000–7FFF` when mapped)
- Raw differing bytes: **366 / 16384**

## Semantic layout
Both revisions have the same map boundary:
- semantic section `bank3`: `4000–7FE0` (`0x3FE1` bytes)
- `Garbage 3`: `7FE1–7FFF` (`0x1F` bytes)

The bank contains joypad/input, toggleable-object data, field-move messages, inventory, map song/header-bank data, overworld/player state, poison, tilesets, daycare EXP, wild encounters, item effects, map update/Cut, object toggling/push boulder, add-mon/flags/healing/BCD, initial player data, bag quantity, pathfinding, HP bar and several hidden-event handlers/texts.

Repository-wide revision-conditional search shows no `_REV0`/`_REV1` conditional in the bank-03 source set. Direct conditionals are instead concentrated in bank 00 serial code, bank 01 link code, bank 04 Haze, bank 09 unused serial helper, bank 0F battle core, WRAM, and garbage selection.

## Exhaustive delta census
- Active/semantic region differences: **336 bytes**
- `Garbage 3` differences: **30 bytes** (31-byte garbage region; one byte happens to match)

### Active-region classification
Of the 336 active differing bytes:

1. **332 bytes** are the byte-level consequences of 16-bit references to HOME symbols that moved by `-0x12` in Rev A.
   - 310 changed low bytes have delta `-18`.
   - 22 additional changed high bytes have delta `-1` because subtracting `0x12` crossed a `xx00` page boundary.
   - These are address relocation effects, not bank-03 code changes.

2. The remaining **4 bytes** are bank-0F target-address relocations caused by the confirmed Rev-A Battle Core edits:

| Bank-03 operand location | Rev 0 target | Rev A target | Symbol | Delta |
|---|---:|---:|---|---:|
| `5738` | `0F:59A0` | `0F:59A8` | `IsGhostBattle` | `+0x08` |
| `58FF` | `0F:6DF1` | `0F:6DF7` | `LoadEnemyMonData` | `+0x06` |
| `6244` | `0F:7762` | `0F:7767` | `StatModifierUpEffect` | `+0x05` |
| `64DC` | `0F:5377` | `0F:5372` | `MoveSelectionMenu` | `-0x05` |

These four are also relocation-only effects; the surrounding bank-03 instruction sequences retain their structure.

## Garbage region
`Garbage 3` is `7FE1–7FFF`. **30/31 bytes differ** between revisions. This is classified as revision-specific residual/filler and excluded from executable/data semantic-change counts.

## Verdict
- Direct bank-03 revision edit: **none found**.
- 336/336 active differing bytes: **explained by relocated external symbols**.
- 30 residual differing bytes: **Garbage 3**.
- Section size and bank-03 semantic layout: **identical**.
- Status: **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
