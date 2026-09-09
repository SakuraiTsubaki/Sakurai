# Pokémon Green JP — Bank 07 deep audit (Rev 0 vs Rev A)

## Layout
Bank 07 contains `Maps 3`, `Maps 4`, `Clear Save`, and `Hidden Events 1`. The live region ends at `7FB8`; `Garbage 7` is `7FB9–7FFF` (`0x47` bytes). Rev 0 / Rev A boundaries are identical.

## Delta census
- Raw differences: **560 bytes**
- Live-region differences: **493 bytes**
- Garbage-region differences: **67 bytes**

Live-region classification:
- **492 bytes** are HOME relocation effects (`467` low-byte `-18` changes + `25` high-byte borrow changes).
- **1 byte** at `62DE` is a bank-01 target relocation: `DisplayNameRaterScreen` `01:64FB → 01:64A0` (`-0x5B`). This reflects the bank-01 link-code removals before that symbol, not a bank-07 edit.

67/71 bytes of `Garbage 7` differ.

## Verdict
No direct bank-07 revision edit found. 493/493 live differing bytes are external relocation effects. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
