# Pokémon Green JP — Bank 15 deep audit (Rev 0 vs Rev A)

- Role: Maps 11, Battle Engine 9, Diploma, Trainer Sight.
- Raw differences: **313**; live: **302**; `Garbage 21`: **11**.
- **295 live bytes** are HOME relocation effects.
- **5 bytes** are bank-0F target relocations.
- **2 bytes** form one bank-01 pointer relocation (`5912 → 58B7`, crossing a page boundary).
- Direct bank-15 revision edit: **none found**.

**Verdict:** 302/302 live differences are external relocation effects. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
