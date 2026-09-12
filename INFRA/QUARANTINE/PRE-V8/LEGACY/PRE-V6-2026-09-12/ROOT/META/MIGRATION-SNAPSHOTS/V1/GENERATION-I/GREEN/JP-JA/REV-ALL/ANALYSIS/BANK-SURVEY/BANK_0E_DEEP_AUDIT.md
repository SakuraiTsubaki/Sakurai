# Pokémon Green JP — Bank 0E deep audit (Rev 0 vs Rev A)

- Role: `Battle Engine 7`; base stats, Pokémon names/cries, move data, trainer AI, evolution/moves and related battle helpers.
- Raw differences: **79**; live: **78**; garbage: **1** (`Garbage 14`).
- **67 live bytes** are HOME `-0x12` relocation effects.
- The remaining **11 live bytes** are bank-0F symbol relocations caused by the already-confirmed Battle Core revision edits:
  - `AIGetTypeEffectiveness` `672B→6732`
  - `_LoadTrainerPic` `733E→7343`
  - `EnemySendOut` `49F8→49F9`
  - `StatModifierUpEffect` `7762→7767`
  - `PlayCurrentMoveAnimation` `7FDB→7FE0` (3 references)
  - `DrawHUDsAndHPBars` `4EB8→4EB2`
  - `PrintButItFailedText_` `7F4E→7F53` (3 references)
- Direct bank-0E revision edit: **none found**.

**Verdict:** 78/78 live differences are external relocation effects; the sole residual difference is `Garbage 14`. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
