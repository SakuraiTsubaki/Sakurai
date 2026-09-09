# Pokémon Green JP — Bank 16 deep audit (Rev 0 vs Rev A)

- Role: Maps 12–13, Battle Engines 10–11.
- Raw differences: **330**; live: **307**; `Garbage 22`: **23 differing bytes**.
- **305 live bytes** are HOME relocation effects.
- The remaining **2 live bytes** are two references to bank-0F `LoadEnemyMonData` `6DF1 → 6DF7`.
- Direct bank-16 revision edit: **none found**.

**Verdict:** 307/307 live differences are external relocation effects. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
