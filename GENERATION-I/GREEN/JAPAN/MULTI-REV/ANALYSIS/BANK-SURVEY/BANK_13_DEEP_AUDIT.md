# Pokémon Green JP — Bank 13 deep audit (Rev 0 vs Rev A)

- Role: trainer pictures, Maps 9, Predefs.
- Raw differences: **36**; live: **34**; `Garbage 19`: **2**.
- The live differences split exactly into **13 ordinary HOME relocation bytes** plus **21 changed bytes in the 99-entry `PredefPointers` table**.
- `PredefPointers` entries are three bytes (`bank + 16-bit address`). Nineteen entries change address while their bank byte remains fixed. Those changes point to already-relocated routines in HOME, bank 01, bank 09, or bank 0F.
- Notable entries include `DrawPlayerHUDAndHPBar`, `AnimateSendingOutMon`, `LearnMove`, `CableClub_Run`, `PrintMonType`, `AskName`, and `PrintMoveType`.
- The source also deliberately encodes `JumpMoveEffect` with bank `$03` (`; wrong bank`) and similarly documents other forced-bank predefs; the revision changes only the address field, not that bank byte.
- Direct bank-13 revision edit: **none found**.

**Verdict:** all 34 live differences are external-symbol relocation effects. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
