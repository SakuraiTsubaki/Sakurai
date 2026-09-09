# Pokémon Green JP — Bank 1D deep audit (Rev 0 vs Rev A)

- Role: Maps 18–20, Itemfinder, vending machine, League PC, hidden items.
- Raw differences: **425**; live: **363**; `Garbage 29`: **62**.
- All **363 live bytes** are HOME `-0x12` relocation effects (347 low-byte changes + 16 high-byte borrows).
- All 62 bytes of `Garbage 29` differ.
- Direct bank-1D revision edit: **none found**.

**Verdict:** **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
