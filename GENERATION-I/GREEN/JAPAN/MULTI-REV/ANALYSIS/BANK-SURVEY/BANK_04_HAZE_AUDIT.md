# Bank 04 deep audit — Haze revision behavior

Bank 04 includes move names, font/player graphics, start-menu material, NPC sprites and Battle Engine 1.

## Direct semantic revision edit

In `HazeEffect_`, both revisions clear the target's nonvolatile status first. They then inspect the old status to decide whether to invalidate the selected move for the current turn.

- Rev 0: masks only `SLP_MASK`.
- Rev A: masks `(1 << FRZ) | SLP_MASK`.

Therefore Rev A adds Freeze to the “cannot execute the already-selected move after Haze clears the status” condition. In Rev 0, a frozen target cured by Haze is not caught by this post-clear move-invalidation mask; Rev A is.

The core Haze labels remain at the same addresses (`HazeEffect_` at `$7F1D`, `.cureStatuses` at `$7F4C`, `.cureVolatileStatuses` at `$7F56`), so this is a compact true logic edit rather than a function relocation.

## Raw-diff interpretation

Bank 04 has 233 differing bytes, but only a small subset are the direct Haze logic edit. The rest is primarily changed absolute operands caused by relocated ROM0/bank1 targets plus residual data differences.
