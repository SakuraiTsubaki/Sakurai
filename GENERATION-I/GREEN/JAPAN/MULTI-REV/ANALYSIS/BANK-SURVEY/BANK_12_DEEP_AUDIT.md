# Pokémon Green JP — Bank 12 deep audit (Rev 0 vs Rev A)

- Role: Maps 7–8, Screen Effects.
- Raw differences: **406**; live: **321**; `Garbage 18`: **85**.
- All **321 live bytes** are HOME `-0x12` relocation effects (314 low-byte changes + 7 high-byte borrows).
- All 85 bytes of `Garbage 18` differ.
- Direct bank-12 revision edit: **none found**.

**Verdict:** **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
