# GEN2 Kanto Start — Gold KR Phase 12

## Scope
Phase 12 closes two fidelity gaps left explicit by Phase 11: the two imported RGBY Pallet NPCs no longer reuse GSC dialogue, and the Yellow Pikachu scripted capture scene no longer uses the stock Gen II Dude battle backpic.

## RGBY NPC text
- The RGBY girl keeps her original meaning: she is raising Pokémon, and when they become strong they can protect her.
- The RGBY technology NPC keeps the original PC-storage explanation: technology allows items and Pokémon to be stored/retrieved as data through a PC.
- These are independent scripts/text blocks; the original GSC Teacher and Fisher scripts remain intact.

## Yellow Professor Oak backpic
- Yellow's special Pallet Pikachu event uses Professor Oak as the simulated catcher.
- Gold's tutorial battle normally loads `DudeBackpic`. Phase 12 hooks the backpic selection path and selects a dedicated Yellow Professor Oak backpic only for the project's Pikachu tutorial condition.
- Route 29's original Rattata capture tutorial remains on Dude.
- Yellow's 32x32 Oak back image is padded into the Gen II tutorial backpic canvas without altering its source pixels, then stored as LZ3 data in verified free space at the end of Bank 0F.

## Validation
- Phase 11 -> Phase 12 delta IPS: PASS
- Clean Korean Gold -> Phase 12 cumulative IPS: PASS
- Output SHA-1: `ca7ae66029e3fb1ad41ede040cd4ff761b829804`
- Output SHA-256: `edf7e58f7716adea0e9c5196f0678d3b5243f80c6776f78098eec367fd6dc9ea`
- Header checksum: `08`
- Global checksum: `631C`
- Emulator playtest: NOT RUN

## Remaining Pallet fidelity work
1. Preserve distinct RGB and Yellow Classic Pallet palette profiles alongside GSC CGB time-of-day colors.
2. Provide an in-game profile-selection mechanism without deleting original interactions.
3. Perform an emulator playthrough when a compatible runtime is available.
