# Pokémon Green JP — Bank 0A deep audit (Rev 0 vs Rev A)

- Role: `Pics 2` + `Battle Engine 4`
- Raw differences: **14**; live: **7**; garbage: **7** (`Garbage 10`).
- Live classification: **5 HOME relocation bytes** plus two bank-0F target relocations: `MoveHitTest` `684D→6854` and `PlayCurrentMoveAnimation` `7FDB→7FE0`.
- Direct bank-0A revision edit: **none found**.

**Verdict:** 7/7 live differences are external relocation effects. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
