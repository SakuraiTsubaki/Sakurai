# Bank 0F deep audit — Battle Core

## Revision structure

- Rev 0: Battle Core `$4000-$7FFA` = `$3FFB` bytes, followed by 5 residual bytes.
- Rev A: Battle Core `$4000-$7FFF` = full `$4000` bytes.
- Net semantic growth: **+5 bytes**.

Despite this tiny net growth, raw comparison reports 15,403 differing bytes because changes occur near the front of a densely packed bank and alter later addresses/pointers.

## Confirmed direct revision edits

### 1. CHARGING_UP / THRASHING_ABOUT check

Rev 0 uses separate bit tests/branches. Rev A loads the flags byte once and masks the two bits together. This saves 3 bytes.

### 2. Enemy trapping-move handling

Rev 0 jumps directly to enemy-move selection when `USING_TRAPPING_MOVE` is set. Rev A explicitly distinguishes the not-trapped path and, on the trapped path, writes `CANNOT_MOVE` to `wPlayerSelectedMove` before continuing. This adds 7 bytes relative to Rev 0 and makes the no-action state explicit.

### 3. Move-menu state initialization

Rev A reuses the zero already in A, stores `wMoveMenuType`, increments A, then stores `wAnimationID`. This saves 2 bytes versus Rev 0.

### 4. Link-battle action decoder

Rev A explicitly recognizes `LINKBATTLE_NO_ACTION` before the `sub 4` transformation. Rev 0 instead performs a different post-subtraction `LINKBATTLE_STRUGGLE` check. Footprint is effectively unchanged, but semantics differ.

### 5. Bag swap/menu-state clearing

Rev A additionally clears `wMenuItemToSwap` when resetting relevant bag/menu state. This adds 3 bytes and is consistent with preventing stale swap-selection state from persisting into battle item handling.

### Exact size reconciliation

`-3 + 7 - 2 + 0 + 3 = +5 bytes`, exactly matching the Battle Core growth from `$3FFB` to `$4000`.

## Shared link-battle desync candidate

The source also has a revision-independent warning: when recovering a trapping move after an opponent switch, a `MIRROR MOVE` check is missing alongside the `METRONOME` check and the comment says this might cause a link-battle desync.

Record this as a **source-annotated candidate**, not yet a proven runtime bug. Reproduce in deterministic two-instance link testing before fixing it.
