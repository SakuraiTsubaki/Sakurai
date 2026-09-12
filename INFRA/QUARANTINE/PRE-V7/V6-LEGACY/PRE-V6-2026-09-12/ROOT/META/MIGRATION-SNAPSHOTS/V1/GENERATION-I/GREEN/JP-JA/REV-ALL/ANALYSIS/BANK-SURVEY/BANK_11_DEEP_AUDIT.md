# Pokémon Green JP — Bank 11 deep audit (Rev 0 vs Rev A)

- Role: Maps 5–6, Pokédex Rating, Hidden Events Core.
- Raw differences: **307**; live: **259**; `Garbage 17`: **48**.
- All **259 live bytes** are HOME `-0x12` relocation effects (254 low-byte changes + 5 high-byte borrows).
- Direct bank-11 revision edit: **none found**.

**Verdict:** **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
