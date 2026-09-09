# Pokémon Green JP — Bank 0D deep audit (Rev 0 vs Rev A)

- Role: `Pics 5` + slot-machine systems
- Raw/live differences: **65 / 65**; no garbage-tail section.
- **64 bytes** are HOME `-0x12` relocation effects.
- The remaining byte relocates bank-01 `DisplayTextIDInit` `724C→71F1` (`-0x5B`).
- Direct bank-0D revision edit: **none found**.

**Verdict:** 65/65 differences are external relocation effects. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
