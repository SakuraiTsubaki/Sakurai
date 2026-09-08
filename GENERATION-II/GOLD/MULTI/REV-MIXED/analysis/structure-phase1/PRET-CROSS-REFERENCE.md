# pret/pokegold semantic cross-reference

Reference repository: `pret/pokegold` (public disassembly), used only as a semantic cross-check.

Confirmed vector semantics used by this corpus:

- `$0008`: `FarCall`
- `$0010`: `Bankswitch`
- `$0028`: `JumpTable`
- `$0040`: VBlank interrupt vector
- `$0048`: LCD interrupt vector
- `$0058`: Serial interrupt vector
- `$0060`: Joypad interrupt vector
- `$0100`: cartridge entry point (`Start`), which reaches `_Start`

Addresses beyond these stable vector semantics are **not** copied from the upstream English disassembly into the Korean map without ROM-local evidence.
