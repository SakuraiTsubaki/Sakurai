# FireRed integrated bank census + disassembly — Pass 3

- Analysis bank size: `0x4000` (16 KiB); **not** a hardware bank-switching unit.
- Coverage: 8 ROMs × 1,024 banks = **8,192 bank instances**.
- Machine code is disassembled only where independent binary evidence identifies candidate `.text` / `lib_text` ranges; data/script/asset banks remain classified as data to avoid fake instruction listings.
- CPU decode: ARM7TDMI / ARMv4T via LLVM (`armv4t-none-eabi`, `thumbv4t-none-eabi`).

## Detected code regions

| ROM | main text banks | later lib text banks | candidate entries | strong heuristic |
|---|---:|---:|---:|---:|
| JP_R0 | `000–058` | `06F–072` | 13,255 | 11,300 |
| JP_R1 | `000–058` | `06F–072` | 13,204 | 11,273 |
| EN_R0 | `000–057` | `076–079` | 13,025 | 11,209 |
| EN_R1 | `000–057` | `076–079` | 13,025 | 11,210 |
| DE_R0 | `000–057` | `077–07A` | 13,031 | 11,190 |
| FR_R0 | `000–057` | `076–079` | 12,882 | 11,194 |
| IT_R0 | `000–057` | `076–078` | 12,813 | 11,195 |
| ES_R0 | `000–057` | `076–079` | 13,012 | 11,196 |

## Bank 000 mixed-mode proof

The first ARM instruction at file offset `0x000000` / bus `0x08000000` branches to `0x08000204`. Offsets `0x000004..0x000203` are GBA header/logo/metadata. ARM startup/IRQ-support code begins at `0x08000204`; at `0x08000230` it executes `bx r1`, with the literal value `0x080003A5`, switching into Thumb state at file offset `0x3A4` / bus `0x080003A4`.

Each candidate code bank has a corresponding generated `.asm` file locally under `banks/<ROM>/`. The entry counts are **heuristic candidates, not a proved function total**: BL-shaped halfwords and embedded literal/data bytes can create false positives. `confirmed_function_candidates.csv` records the evidence for each candidate so later symbol/control-flow passes can promote or reject it.

## Generated files

- `bank_master_integrated.csv`: pass-2 semantic census joined to pass-3 disassembly metadata for all 8,192 bank instances.
- `bank_disassembly_summary.csv`: one row for every ROM×bank.
- `confirmed_function_candidates.csv`: Thumb call/function-pointer-derived entry candidates.
- `code_regions.csv`: detected main and library code bank ranges.
- `banks/<ROM>/bank_XXX.asm`: LLVM raw disassembly for candidate machine-code banks.
- `scan_and_disassemble.py`: reproducible scanner/generator.

The full generated package is not a ROM image and contains no ELF-wrapped ROM copies. Local archive SHA-256: `54173851f34cc45a7f2b8f2b47fb68c39a1b6893b22cba4b20e75c145c60c142`.
