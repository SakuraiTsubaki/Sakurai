# Pokémon Green JP — Bank 08 deep audit (Rev 0 vs Rev A)

## Layout
Bank 08 contains `Bill's PC`, `Audio Engine 2`, `Music 2`, low-health audio, `Sound Effects 2`, and the corresponding SFX headers. The exact map fills the bank through `7FFF`; there is no garbage tail section.

## Delta census
- Raw differences: **60 bytes**
- Live-region differences: **60 bytes**
- Residual/garbage differences: **0 bytes**

Every difference is an address relocation to a HOME symbol moved by the Rev-A `-0x12` HOME shrink:
- 56 low-byte changes: `-18`
- 4 high-byte borrow changes: `-1`
- other byte deltas: **0**

## Verdict
No direct bank-08 revision edit found. 60/60 differing bytes are HOME relocation effects; audio/PC semantics and section sizes are unchanged. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
