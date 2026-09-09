# Pokémon Green JP — Bank 1E deep audit (Rev 0 vs Rev A)

- Role: status ailments, battle animations, Cut2, dust/smoke, fishing, move animations, evolution, elevator, TM prices.
- Raw differences: **132**; live: **113**; `Garbage 30`: **19 differing bytes**.
- All **113 live bytes** are HOME `-0x12` relocation effects (94 low-byte changes + 19 high-byte borrows).
- Direct bank-1E revision edit: **none found**.

**Verdict:** **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
