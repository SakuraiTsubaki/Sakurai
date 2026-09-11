# Pokémon Green JP — Bank 0B deep audit (Rev 0 vs Rev A)

- Role: `Pics 3` + `Battle Engine 5`
- Raw differences: **13**; live: **12**; garbage: **1** (`Garbage 11`).
- All **12 live bytes** are HOME `-0x12` relocation effects (10 low-byte changes + 2 high-byte borrows).
- Direct bank-0B revision edit: **none found**.

**Verdict:** **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
