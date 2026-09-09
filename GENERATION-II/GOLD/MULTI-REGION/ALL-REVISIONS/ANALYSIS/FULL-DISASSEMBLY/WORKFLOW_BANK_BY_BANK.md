# Bank-by-bank survey + disassembly workflow

This project does not separate "bank survey" from "disassembly". Every bank is processed as a single unit.

1. Fingerprint the 16 KiB physical bank for every regional/revision ROM.
2. Classify the bank by actual domain: LR35902 CPU code, script bytecode, audio bytecode, text, graphics/compression, map/event structures, pointer/table data, or empty/reserved space.
3. Run only the correct decoder(s). Mixed banks may require multiple decoders and explicit boundaries.
4. Discover entry points from hardware vectors, direct calls/jumps, Gen II farcall/callfar signatures, bank-switch helpers, and known/verified section boundaries.
5. Recursively decode reachable LR35902 code. Unreached bytes remain data until independent evidence says otherwise.
6. Resolve indirect dispatch such as Gen II `rst $28` jump tables when the table base is proven by reachable code.
7. Map symbols across releases by binary evidence; never assume the same bank/address means the same function across JP/KR/EN/EU layouts.
8. Record regional relocation/overflow and revision deltas.
9. Reassemble or otherwise byte-verify the bank/ROM after semantic replacement.
10. Mark the bank complete only when every byte is accounted for by code or a known data domain and verification passes.

## Completion states

- `empty-confirmed`
- `cpu-disassembly-candidate-partial`
- `cpu-disassembly-validated-partial`
- `needs-script-bytecode-disassembly`
- `needs-audio-bytecode-disassembly`
- `needs-structured-data-decoder`
- `needs-code-seeding-or-structure-analysis`
- future: `semantically-accounted-byte-perfect`

A raw linear CPU dump is explicitly **not** considered a full disassembly.
