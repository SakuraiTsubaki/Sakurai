# Pokémon Green JP — Bank 0D deep audit (Rev 0 vs Rev A)

- Role: `Pics 5` + slot-machine systems
- Raw/live differences: **65 / 65**; no garbage-tail section.
- **63 bytes** are HOME `-0x12` relocation effects.
- The remaining **2 bytes** form one bank-01 pointer relocation: `DisplayTextIDInit` `724C→71F1` (`-0x5B`), crossing a page boundary.
- Direct bank-0D revision edit: **none found**.

**Verdict:** 65/65 differences are external relocation effects. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
