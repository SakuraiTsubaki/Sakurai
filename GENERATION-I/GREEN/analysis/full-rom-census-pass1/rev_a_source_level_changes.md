# Pokémon Green Rev 0 → Rev A — confirmed source-level change census

This note separates **confirmed revision-conditional source changes** from raw binary relocation/garbage differences. Reference source is the exact-hash `Narishma-gb/pokegreen` disassembly, where Green Rev 0 is built with `_GREEN + _REV0` and Green Rev A with `_GREEN + _REV1`.

## Why 46,168 raw differing bytes are misleading

The two images differ at 46,168 same-offset bytes, but several source changes add/remove/move code or garbage, causing all later bytes in a bank to shift. Sequence alignment remains above 0.90 even in banks 00, 01 and 0F, the three enormous raw-delta banks. The semantic revision must therefore be read from revision conditionals and symbol ownership, not a naive byte-for-byte patch list.

## Confirmed revision-conditional areas

### 1. Serial/link core — `home/serial.asm`

Rev 0 contains an extra `Serial_ExchangeBytes` special case: while link state is reset and the local Game Boy is using the internal clock, the receive destination is redirected to `wNameBuffer`. Rev A removes that block.

The unchanged `home/serial2.asm` routines are also **placed at a different point** in `home/serial.asm`: Rev 0 includes them before `Serial_ExchangeByte`; Rev A includes them after the serial-counter helper routines. This relocation is a major reason bank 00 shows huge same-offset differences even though much code remains equivalent.

### 2. Rev-0-only serial routine removed — `engine/battle/print_type.asm`

Rev 0 contains `UnusedSerialFunction`, which manipulates serial counters and can fall through into `PrintMonType` (the disassembly itself marks the fallthrough as a bug). Rev A removes the routine entirely. Because following code shifts, this contributes to large binary deltas beyond the routine's own byte length.

### 3. Haze/freeze handling — `engine/battle/move_effects/haze.asm`

When Haze clears the target's non-volatile status, both revisions suppress the target's selected move if the previous status included sleep. Rev A extends that test to **freeze as well as sleep**. This prevents a Pokémon that was frozen immediately before Haze from proceeding with a selected move merely because Haze cleared the freeze status.

This is a confirmed gameplay bug-fix-level semantic change, not padding noise.

### 4. Battle-core control flow — `engine/battle/core.asm`

Confirmed Rev A conditionals include:

- Player `THRASHING_ABOUT` / `CHARGING_UP` checks are consolidated into one mask test rather than two Rev-0 tests. This is largely equivalent logic but changes code size/layout.
- If the enemy is using a trapping multi-turn move, Rev A explicitly writes `CANNOT_MOVE` to `wPlayerSelectedMove` before continuing. Rev 0 only jumps to enemy move selection at that point.
- Move-menu setup is reordered/shortened in Rev A (`wMoveMenuType` cleared using the already-zero accumulator, then animation ID formed by incrementing it); behavior is intended to be equivalent but binary size/order changes.
- Link battle handling in Rev A explicitly recognizes `LINKBATTLE_NO_ACTION` before interpreting the received action as a switch index; Rev 0 uses a different post-subtraction check.
- Rev A additionally clears `wMenuItemToSwap` when returning from the battle item menu, preventing stale menu-swap state from carrying forward.

These changes make bank 0F a high-priority semantic regression-test area even though much of its 15,403-byte raw delta is relocation.

### 5. Cable Club / data exchange — `engine/link/cable_club.asm`

Rev 0 uses `wUnknown_CCE0` in several link-initialization/synchronization paths. Rev A removes those uses and directly sends zero during the two sync-byte writes where Rev 0 reads the variable (which had been cleared earlier).

Rev 0 also contains an additional post-transfer trainer-name corruption check and associated error text/endless-loop path; Rev A removes that block. Its removal shifts subsequent code/text in the containing bank and contributes substantially to same-offset differences.

### 6. Cable Club NPC — `engine/link/cable_club_npc.asm`

Rev 0 writes `$10` to `wUnknown_CCE0` after receiving Pokédex/link state in a revision-specific path. That write is absent in Rev A, consistent with removal of the variable's functional use elsewhere.

### 7. WRAM declaration — `ram/wram.asm`

Rev 0 names one byte `wUnknown_CCE0` and reserves one additional byte. Rev A reserves the same total two bytes anonymously (`ds 2`). Therefore this particular declaration does **not** shift all later WRAM addresses; it reflects removal of the variable's named/useful role rather than a memory-size change.

### 8. Garbage/padding ownership — `garbage.asm`

Many `Garbage N` regions are revision-dependent and contain different retained bytes or placement. They are linker-owned, so even long `00`/`FF` runs are not automatically free space. Rev 0 has one genuinely linker-unallocated ROM byte at bank 1A `$7FFF`; Rev A allocates it as one-byte `Garbage 26`.

## Revision testing implications

Rev A should not simply be called “the same game with header revision 1.” Confirmed semantic differences touch **serial/link behavior, Cable Club data exchange, battle control flow, Haze/freeze handling, menu state, and removed unused/buggy serial code**, while extensive layout/garbage changes amplify their raw byte footprint.

For the RBY ENGLISH → G project, Rev 0 and Rev A should therefore remain separate baselines until every revision-conditional behavior is classified as one of:

1. actual gameplay/link bug fix to preserve,
2. code-size/optimization-only change,
3. removed unused/debug/buggy routine,
4. garbage/padding/layout-only difference,
5. data/text change with player-visible effect.
