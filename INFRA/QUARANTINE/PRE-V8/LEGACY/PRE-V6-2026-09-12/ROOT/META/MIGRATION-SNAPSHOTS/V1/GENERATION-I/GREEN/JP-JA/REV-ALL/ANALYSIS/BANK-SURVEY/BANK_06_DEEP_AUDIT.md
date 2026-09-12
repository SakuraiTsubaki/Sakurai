# Pokémon Green JP — Bank 06 deep audit (Rev 0 vs Rev A)

## Layout
Bank 06 contains `Maps 1`, `Maps 2`, `Play Time`, and `Doors and Ledges`. The live region ends at `7FCF`; `Garbage 6` is `7FD0–7FFF` (`0x30` bytes). Rev 0 / Rev A section boundaries are identical.

## Delta census
- Raw differences: **348 bytes**
- Live-region differences: **308 bytes**
- Garbage-region differences: **40 bytes**

All **308 live bytes** are exactly the byte-level consequences of references to HOME symbols moved by `-0x12` in Rev A:
- 296 low-byte changes: `-18`
- 12 high-byte borrow changes: `-1`
- other live-byte deltas: **0**

## Verdict
No direct bank-06 revision edit found. 308/308 live differences are HOME relocation operands/pointers; 40 differences are revision-specific `Garbage 6`. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
