# Pokémon Green JP — Bank 1C deep audit (Rev 0 vs Rev A)

- Role: credits, splash, Hall of Fame, healing machine, player animations, ghost Marowak animation, battle transitions, Town Map, icons, trades, palettes, save.
- Raw differences: **203**; live: **195**; `Garbage 28`: **8**.
- **193 live bytes** are HOME relocation effects.
- **2 live bytes** are one bank-01 pointer relocation: `PrintSaveScreenText` `5C42 → 5BE7` (`-0x5B`), with both low and high bytes changing.
- Direct bank-1C revision edit: **none found**.

**Verdict:** 195/195 live differences are external relocation effects. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
