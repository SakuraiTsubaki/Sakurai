# Pokémon Green JP — Bank 0C deep audit (Rev 0 vs Rev A)

- Role: `Pics 4` + `Battle Engine 6`
- Raw differences: **32**; live: **5**; garbage: **27** (`Garbage 12`).
- Live classification: **3 HOME relocation bytes** + bank-0F `PlayCurrentMoveAnimation` `7FDB→7FE0` + bank-0F `PrintButItFailedText_` `7F4E→7F53`.
- Direct bank-0C revision edit: **none found**.

**Verdict:** 5/5 live differences are external relocation effects. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
