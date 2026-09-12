# Bug / glitch / error audit workstream

This checklist is intentionally version-aware. Do not assume an issue exists in all eight ROMs.

## Priority P0 — corruption/crash/execution
- English Coin Case text terminator / arbitrary-code path.
- Save initialization and Hall of Fame edge cases.
- Box/storage bounds and migration when species/item IDs become 16-bit.
- Text-engine pointer/bank bounds after relocation.
- Mapper/RTC bank-register correctness.

## Priority P1 — battle correctness
- Fast Ball / Love Ball / Moon Ball calculations.
- Dragon Fang vs Dragon Scale held-effect mismatch.
- Present damage behavior.
- Belly Drum HP precondition.
- Beat Up link desynchronization.
- Pursuit revival interactions.
- stat overflow/rollover and boosted stat bounds.
- Transform/Sketch edge cases.
- Counter/Mirror Coat edge cases.
- EXP Share/experience arithmetic and under/overflow.

## Priority P1 — world/save/time
- Day Care experience loss.
- RTC/day rollover and daylight-saving/event timers.
- cloning/reset-window behavior: decide whether to preserve as historical exploit or harden saves.
- S.S. Aqua and Cerulean Gym anomalies.
- Time Capsule validation and new-format incompatibilities.

## Priority P2 — localization-specific
- JP Bug-Catching Contest behavior.
- EN Coin Case.
- KR Dude tutorial graphics misalignment path.
- Re-test every localized text interpreter because text lengths/terminators differ.

## Required test metadata
issue_id, affected_language, affected_revision, original_rom_sha1, bank, address, reproduction_steps, expected, actual, fix_status, compatibility_notes, regression_test
