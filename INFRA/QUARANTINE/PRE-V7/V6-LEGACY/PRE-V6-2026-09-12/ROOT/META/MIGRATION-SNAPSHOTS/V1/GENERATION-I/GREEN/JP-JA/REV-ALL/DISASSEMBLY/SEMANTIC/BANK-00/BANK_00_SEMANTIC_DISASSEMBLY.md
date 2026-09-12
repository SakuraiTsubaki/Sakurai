# Pokémon Green JP — Bank 00 semantic disassembly + total survey

## Scope
This is the first combined **bank survey + semantic disassembly** pass. It does not treat a linear opcode decode as semantic code. The raw ROM is cross-checked against the exact-matching `Narishma-gb/pokegreen` source/symbol layout and the Rev 0 / Rev A ROM bytes.

## Bank layout
| Region | Rev 0 | Rev A | Meaning |
|---|---:|---:|---|
| Reset/interrupt vectors | $0000-$0067 | same | executable vector stubs + unused vector padding |
| Garbage Header | $0068-$00FF | same section | non-semantic residual/header-area data |
| Cartridge Header | $0100-$014F | same | entry + Nintendo/cart header |
| Home | $0150-$3FD5 | $0150-$3FC3 | common routines/data always visible in ROM0 |
| Garbage 0 | $3FD6-$3FFF | $3FC4-$3FFF | revision-specific residual bytes |

Rev A Home is exactly **$12 (18) bytes shorter**.

## Source decomposition
`home.asm` maps Bank 00 into **67 ordered source units**. The full ordered manifest is in `BANK_00_MODULE_MANIFEST.csv`. Code, tables, text, pointer data, and residual regions are kept distinct rather than decoding all data as opcodes.

## Instruction-level verified core
The current pass has byte/symbol/source verification for **18 core entries/sections**: vectors/header, startup, input, LCD, initialization, VBlank, serial/link, timer, and bank switching. See `BANK_00_VERIFIED_ROUTINES.csv`.

### Boot and interrupt chain
- `$0100 Start` is the normal cartridge entry and jumps to `$0150 _Start`.
- `_Start` jumps to `Init` at `$09DA` in both revisions.
- VBlank vector `$0040` jumps to `VBlank` `$0AAC`.
- Timer vector `$0050` jumps to `$0D9A` (Rev 0) / `$0D88` (Rev A), where `Timer` is only `reti`.
- Serial vector `$0058` jumps to `Serial` `$0BA7` in both revisions.
- LCD vector `$0048` and unused RST vectors route to the documented unused RST38 path; RST38 jumps to echo RAM `$F080`. This is catalogued as an intentional/unreachable anomaly until reachability proves otherwise.

## Revision delta — direct semantic change
The Bank 00 **direct** revision edit is localized to the serial subsystem:

1. `Serial_ExchangeBytes.storeReceivedByte` in Rev 0 contains an 18-byte conditional block.
2. It tests `wLinkState == LINK_STATE_RESET` and internal-clock state and can redirect receive destination `de` to `wNameBuffer`.
3. Rev A removes that block.
4. `home/serial2.asm` is included **before** `Serial_ExchangeByte` in Rev 0 and **after** `SetUnknownCounterToFFFF` in Rev A.
5. The removal/reordering shifts later Home symbols by `$12`; most later Bank 00 differences are therefore relocated call/jump immediates rather than rewritten logic.

Examples:
- `Serial_ExchangeByte`: `$0CAA → $0C1C`
- `Timer`: `$0D9A → $0D88`
- `BankswitchHome`: `$3606 → $35F4`
- `Bankswitch`: `$3620 → $360E`

## Code/data classification rules now fixed for every bank
1. **Executable code** — only ranges supported by source/symbol/control-flow evidence.
2. **Structured data** — tables, text, graphics, map data, pointers, headers; never promoted to code just because bytes decode as legal LR35902 opcodes.
3. **Residual/garbage** — preserved and hashed, but excluded from semantic control-flow.
4. **Xrefs** — calls/jumps/pointers recorded against symbols, with revision relocation distinguished from semantic edits.
5. **Revision deltas** — classified as direct logic, relocation, data/pointer change, or residual.
6. **Bug/glitch review** — source comments are candidates until reachability/reproduction confirms them.

## Bank 00 status
- Raw byte coverage: **100%**
- Lossless reversible baseline: **100%** (local only; not public GitHub)
- Section/source decomposition: **100% mapped**
- Core instruction-level verification: **started and verified for critical boot/interrupt/link/bankswitch paths**
- Revision-delta survey: **100% complete**
- Full symbol-by-symbol Xref/reachability annotation: **continuing inside this same bank before Bank 01 semantic closeout**

This establishes the format to be used for Banks 01–1F: **Bank → Section → Source unit → Symbol → code/data → Xref → reachability → revision delta → bug status**.
