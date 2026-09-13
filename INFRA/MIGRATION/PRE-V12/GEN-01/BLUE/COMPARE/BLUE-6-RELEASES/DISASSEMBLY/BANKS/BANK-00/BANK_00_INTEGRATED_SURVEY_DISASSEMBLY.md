# BLUE 6-ROM Bank $00 — Integrated Survey + Disassembly Pass 1

This pass applies the new rule: a bank is surveyed and disassembled in the same work unit. The uploaded ROM bytes are the authority; public disassemblies are semantic cross-checks only.

## Completion gate for every bank

A bank is not marked complete until: (1) raw metrics and regional diffs are recorded, (2) executable code and data boundaries are classified, (3) symbols/pointers are mapped, (4) unresolved ranges are explicitly tracked, and (5) the reconstructed bank/ROM passes byte-for-byte hash verification.

## Bank $00 facts from the uploaded ROMs

- Size: 16,384 bytes per ROM.
- Six-way identical positions: 248 / 16,384 (1.514%).
- Western five-way identical positions: 4,842 / 16,384 (29.553%).

### Bank SHA-1

- JP: `3f3c27f7b8960211fc903af906610c34d98e7a84`
- EN: `cf785a689639826f7a9ae2eda88e8d6cdeebc54e`
- FR: `351387bf9ad2c98f0545109c032d7a93f675f306`
- DE: `bf5661ca44cdee2e1827016ef556aa36e17108cc`
- IT: `35646dd4fa4ca99c3e4f0ea567fcbe4d19d7390a`
- ES: `3fd427297d15e9f0b13a2e83fb233d8946623bf4`

## Vectors / cartridge header

| Region | $0038 | VBlank $0040 | LCD $0048 | Timer $0050 | Serial $0058 | Joypad $0060 | Cart | ROM size |
|---|---|---|---|---|---|---|---:|---:|
| JP | JP $F080 | JP $200A | RST $38 | JP $22E6 | JP $2105 | RETI | `03` | `04` |
| EN | RST $38 | JP $2024 | RST $38 | JP $2306 | JP $2125 | RETI | `13` | `05` |
| FR | RST $38 | JP $2020 | RST $38 | JP $2302 | JP $2121 | RETI | `1B` | `05` |
| DE | RST $38 | JP $2024 | RST $38 | JP $2306 | JP $2125 | RETI | `1B` | `05` |
| IT | RST $38 | JP $2024 | RST $38 | JP $2306 | JP $2125 | RETI | `1B` | `05` |
| ES | RST $38 | JP $2023 | RST $38 | JP $2305 | JP $2124 | RETI | `1B` | `05` |

All six use `NOP; JP $0150` at the cartridge entry point. The Nintendo logo/header block occupies the standard $0100–$014F region; semantic code resumes at $0150.

## Recursive SM83 code discovery — pass 1

Seeds: RST/interrupt vectors, cartridge entry `$0100`, and main start `$0150`. Direct `JP`, `JR`, `CALL`, and `RST` targets inside ROM0 are followed recursively. Indirect/banked dispatch is intentionally not guessed in this pass, so the coverage below is a conservative lower bound, not a final code-size measurement.

| Region | Instructions discovered | Reachable bytes | Bank coverage | Branch targets |
|---|---:|---:|---:|---:|
| JP | 847 | 1377 | 8.405% | 81 |
| EN | 895 | 1459 | 8.905% | 84 |
| FR | 895 | 1459 | 8.905% | 84 |
| DE | 895 | 1459 | 8.905% | 84 |
| IT | 895 | 1459 | 8.905% | 84 |
| ES | 895 | 1459 | 8.905% | 84 |

Key result: EN/FR/DE/IT/ES each produce the same pass-1 instruction/byte counts, but not the same instruction addresses. FR/ES in particular contain relocations, so semantic matching must use routine signatures and references rather than blindly copying English offsets.

## Semantic anchors for Bank $00

The English reference disassembly confirms the canonical ROM0 structure: interrupt vectors at `$0040/$0048/$0050/$0058/$0060`, home code beginning immediately after the vectors, cartridge entry at `$0100`, and `Start` at `$0150`. It also identifies early home routines such as `DisableLCD`, `FarCopyData`, `CopyData`, `ReadJoypad`, and `Joypad`. These names are imported only after the uploaded bytes are matched to the corresponding routine body.

## Status

- Survey: **done for pass 1** (hashes, header/vector map, regional diff runs, common-byte counts).
- Disassembly: **started in the same pass** (recursive reachable-code listings and code-range maps generated for all 6 ROMs).
- Semantic labeling: **in progress**; Bank $00 is not yet “complete” because indirect dispatch targets, data tables, all code/data boundaries, and per-region label mapping still need confirmation.
- Next operation within the same Bank $00: map the English semantic anchors onto EN bytes, derive relocation/signature matches for FR/DE/IT/ES, then independently map JP where the home layout differs. Only after all unresolved ranges are classified do we advance to Bank $01.
