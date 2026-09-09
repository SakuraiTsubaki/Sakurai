# Pokémon Green JP — Bank 10 deep audit (Rev 0 vs Rev A)

- Role: Pokédex, trade movie, intro, trade2.
- Raw differences: **135**; live: **121**; `Garbage 16`: **14**.
- All **121 live bytes** are HOME `-0x12` relocation effects (108 low-byte changes + 13 page-borrow high-byte changes).
- Direct bank-10 revision edit: **none found**.

**Verdict:** **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
