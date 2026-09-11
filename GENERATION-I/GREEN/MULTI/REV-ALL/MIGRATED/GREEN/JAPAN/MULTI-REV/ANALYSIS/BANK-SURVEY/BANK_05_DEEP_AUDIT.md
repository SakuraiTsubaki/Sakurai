# Pokémon Green JP — Bank 05 deep audit (Rev 0 vs Rev A)

## Layout
- `NPC Sprites 2`: starts `4000`
- `Battle Engine 2` follows
- live region ends `7FD5`
- `Garbage 5`: `7FD6–7FFF` (`0x2A` bytes)
- Rev 0 / Rev A boundaries are identical.

## Delta census
- Raw differences: **83 bytes**
- Live-region differences: **42 bytes**
- Garbage-region differences: **41 bytes**

All 42 live bytes are relocation effects:
- **39 bytes**: references to HOME symbols moved by the bank-00 `-0x12` shrink (`36` low-byte `-18` changes + `3` high-byte borrow changes).
- `7DC6`: bank-0F `PlayCurrentMoveAnimation` `7FDB → 7FE0` (`+5`).
- `7DDB`: bank-0F `DrawHUDsAndHPBars` `4EB8 → 4EB2` (`-6`).
- `7EC1`: bank-01 `PlayerPC` `7BF9 → 7B99` (`-0x60`).

The remaining 41 differences are inside `Garbage 5` (41/42 garbage bytes differ).

## Verdict
No direct bank-05 revision logic/data edit found. All live deltas are external-symbol relocation effects. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
