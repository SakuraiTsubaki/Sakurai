# Korean Gold — New Game spawn analysis

## Scope
Direct binary analysis of `Pocket Monsters Geum (Korea).gbc` for the GEN2 Kanto Start implementation.

## Base identity
- Size: `0x200000` bytes
- SHA-1: `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65`

## New Game routine location
A structural opcode scan for the New Game sequence (`xor a`, write debug flags, four calls, load spawn constant, write `wDefaultSpawnpoint`, set map-entry method, jump to continue loop) returned exactly one match in the ROM.

- Routine sequence begins: `0x005C4B`
- Spawn immediate byte: `0x005C5C`
- Original value: `0x00` = `SPAWN_HOME`
- Korean Gold disassembly spawn constants define `SPAWN_PALLET = 0x02`.

## First implementation step
For the bootstrap smoke test, patch `0x005C5C` from `00` to `02` and recompute the global checksum. This makes New Game enter the existing Generation II Pallet Town spawn point while leaving the original ROM untouched.

## Important limitation
This is only the first routing hook. A complete Kanto-start game still requires Kanto-specific initial flags, early progression, starter flow, blackout/respawn behavior, map/event integration, and expanded RGBYGSC content. Those should be layered on top of this verified New Game hook rather than replacing it with destructive edits.
