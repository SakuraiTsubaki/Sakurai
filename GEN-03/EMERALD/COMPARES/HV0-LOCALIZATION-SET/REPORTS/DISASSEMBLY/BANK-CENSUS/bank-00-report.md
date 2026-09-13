# Emerald BANK 00 — census + disassembly pass

- Analytical bank: ROM `0x000000–0x00FFFF` / GBA `0x08000000–0x0800FFFF`.
- GBA header / bootstrap / IRQ code is mixed ARM, then normal game code enters Thumb at `0x080003A4`.
- `AgbMain` at `0x080003A4` is independently present in both pret US and JP function maps.

## Confirmed layout

| ROM offset | GBA address | Classification |
|---|---|---|
| `000000–0000BF` | `08000000–080000BF` | GBA cartridge header |
| `0000C0–000203` | `080000C0–08000203` | header-adjacent/reserved bootstrap padding/data |
| `000204–0003A3` | `08000204–080003A3` | ARM startup / interrupt bootstrap |
| `0003A4–00FFFF` | `080003A4–0800FFFF` | Thumb main code + literal pools / local data |

## Cross-language code evidence

| Build | all candidates | strong | PUSH LR | Thumb BL sites | BX LR | POP PC patterns |
|---|---:|---:|---:|---:|---:|---:|
| JP | 1446 | 512 | 514 | 1159 | 80 | 18 |
| EN | 1378 | 506 | 508 | 1174 | 78 | 0 |
| FR | 1371 | 504 | 508 | 1174 | 78 | 0 |
| DE | 1367 | 504 | 508 | 1174 | 78 | 0 |
| IT | 1386 | 504 | 519 | 1174 | 78 | 0 |
| ES | 1374 | 504 | 508 | 1174 | 78 | 0 |

## Verified first symbols

| Address | US symbol | JP symbol |
|---|---|---|
| `080003A4` | `AgbMain` | `AgbMain` |
| `080004C4` | `UpdateLinkAndCallCallbacks` | same |
| `080004D8` | `InitMainCallbacks` | same |
| `0800051C` | `CallCallbacks` | same |
| `08000540` | `SetMainCallback2` | same |
| `08000560` | `SeedRngAndSetTrainerId` | same |

The early symbol addresses remain aligned, but JP/Western code sizes begin diverging within BANK 00 (for example around allocator routines), so symbols must be tracked per build rather than copied by offset.

## Emitted raw decode

For each of JP/EN/FR/DE/IT/ES:
- `bank_00_ARM_startup.asm.txt`: confirmed ARM region only.
- `bank_00_Thumb_main.asm.txt`: Thumb decode from `0x080003A4` to bank end.
- `function_candidates.csv`: whole-ROM pointer/BL/prologue evidence assigned to target banks.

Raw decode is not treated as semantic completion: literal pools and embedded data still require object/symbol boundary classification.
