# Pokémon Emerald — 64 KiB Bank Census + Disassembly

This workstream couples the existing 64 KiB ROM-bank census with executable-code discovery and disassembly. The analytical banks are 0x10000-byte blocks, not hardware bank-switching units.

## Rules

- Every bank is classified before code decoding: CODE, MIXED_CODE_DATA, SCRIPT/RODATA, GRAPHICS, PADDING/FREE, or UNKNOWN.
- Arbitrary data bytes are never treated as valid disassembly simply because they decode as ARM/Thumb instructions.
- Function candidates are gathered from whole-ROM evidence: Thumb pointers, Thumb BL targets, PUSH {...,LR} prologues, and selected ARM pointers.
- Cross-bank calls and pointers are credited to the target bank.
- JP, EN, FR, DE, IT, and ES are tracked independently because code/library placement differs by build.

## Verified executable boundaries

All six builds enter Thumb main code at ROM offset `0x0003A4` (`0x080003A4`, `AgbMain`). The ARM startup/IRQ bootstrap occupies `0x000204–0x0003A3`.

| Build | Thumb main end (exclusive) | library start | library end (exclusive) |
|---|---:|---:|---:|
| JP | `0x1DABA4` | `0x28D2F8` | `0x29BDA0` |
| EN | `0x1DB674` | `0x2DED70` | `0x2E952E` |
| FR | `0x1DB2D0` | `0x2E7D44` | `0x2F2502` |
| DE | `0x1DB1CC` | `0x2F4AB0` | `0x2FF26E` |
| IT | `0x1DB1BC` | `0x2DFCFC` | `0x2EA4BA` |
| ES | `0x1DB2D4` | `0x2E64FC` | `0x2F0CBA` |

The library-start anchor is the byte-identical `GameCubeMultiBoot_Hash` block. Western last-main and `strcpy` anchors are also verified by unique cross-ROM signatures. JP uses its own later libc tail.

## Current bank pass

BANK 00 has been decoded in two architecture-correct regions for all six builds:

- ARM: `0x08000204–0x080003A3`
- Thumb: `0x080003A4–0x0800FFFF`

Raw decoder output is still only an intermediate representation: literal pools, embedded tables, and exact function/object boundaries are promoted to semantic completion only after symbol/control-flow verification.

## Files

- `emerald_bank_disasm.py` — whole-ROM candidate scan + per-bank inventory + architecture-correct raw decoding.
- `derive_disasm_boundaries.py` — reproducible boundary/anchor verifier.
- `boundary_evidence.json` — cross-language executable boundaries and signature hashes.
- `bank-00-report.md` — first combined census/disassembly work unit.

ROM binaries are never stored in this repository.