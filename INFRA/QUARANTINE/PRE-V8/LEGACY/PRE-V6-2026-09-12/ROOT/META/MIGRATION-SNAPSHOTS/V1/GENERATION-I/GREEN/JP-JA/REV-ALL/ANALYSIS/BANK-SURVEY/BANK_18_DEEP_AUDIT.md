# Pokémon Green JP — Bank 18 deep audit (Rev 0 vs Rev A)

- Role: Maps 16–17, Cinnabar Lab fossils, Hidden Events 4.
- Raw differences: **359**; live: **315**; `Garbage 24`: **44 differing bytes**.
- All **315 live bytes** are HOME `-0x12` relocation effects (302 low-byte changes + 13 high-byte borrows).
- Direct bank-18 revision edit: **none found**.

**Verdict:** **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
