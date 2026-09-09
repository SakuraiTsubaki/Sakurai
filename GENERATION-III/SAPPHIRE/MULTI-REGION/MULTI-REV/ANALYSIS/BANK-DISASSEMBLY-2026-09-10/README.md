# Pokémon Sapphire — 64 KiB bank census + static ARM/Thumb disassembly

This package combines the bank-by-bank ROM census with control-flow-aware disassembly for all **9 supplied Sapphire ROMs**. Original ROM binaries are not redistributed.

## Analysis model
- “Bank” = fixed `0x10000` (64 KiB) logical analysis unit. GBA ROM itself is flat-mapped.
- ARM reset/startup is separated from Thumb code.
- Thumb starts only after the detected ARM `BX` handoff; the GBA header is never decoded as Thumb.
- Initial function seeds: real startup handoff + ROM pointers whose targets begin with Thumb `PUSH`-style function prologues.
- Leaf/non-prologue functions are then discovered by actual `BL`/branch control flow.
- The per-ROM `gScriptCmdTable`-equivalent is found by the normalized function-pointer signature of AXPE Rev0. This is the end of the **contiguous main code region**, not a global executable ceiling.
- Calls beyond that boundary are followed, exposing later library/BIOS-wrapper code islands.
- Verified LZ77 ranges and obvious 00/FF padding are excluded from executable traversal.
- Scripts, text, graphics, sound and other data are retained as data instead of being linearly mis-decoded as instructions.

## Final ROM summary

| ROM | Thumb entry | Main code end | Function seeds | Basic blocks | Accepted code | Later code banks |
|---|---:|---:|---:|---:|---:|---|
| AXPJ_rev0 | `0x24C` | `0x145190` | 9,494 | 31,758 | 839,456 B | `1A,1B` |
| AXPD_rev1 | `0x380` | `0x14B208` | 9,685 | 32,211 | 857,104 B | `1E` |
| AXPE_rev0 | `0x24C` | `0x14AE30` | 9,674 | 32,144 | 856,072 B | `1D,1E` |
| AXPE_rev1 | `0x24C` | `0x14AE50` | 9,668 | 32,132 | 855,716 B | `1D,1E` |
| AXPE_rev2 | `0x24C` | `0x14AE50` | 9,668 | 32,132 | 855,716 B | `1D,1E` |
| AXPF_rev0 | `0x380` | `0x14B2EC` | 9,688 | 32,231 | 857,444 B | `1E` |
| AXPF_rev1 | `0x380` | `0x14B2EC` | 9,688 | 32,231 | 857,444 B | `1E` |
| AXPI_rev0 | `0x380` | `0x14B250` | 9,692 | 32,234 | 857,494 B | `1D,1E` |
| AXPI_rev1 | `0x380` | `0x14B250` | 9,692 | 32,234 | 857,494 B | `1D,1E` |

## Files
- `bank_disassembly_summary.csv` — **2,176 rows**, one for every logical bank image.
- `rom_disassembly_summary.csv` — ROM-level boundaries and CFG counts.
- `revision_instruction_diffs.csv` — known revision changes decoded into actual Thumb instruction changes.
- `CODE_ISLANDS.md` — executable islands after the main code/data boundary.
- Local full package additionally contains ARM startup listings, function seeds, basic blocks, CFG edges, and all 2,176 per-bank ASM listings.
- `bank_static_disassembler.py` — reproducible scanner/disassembler source.

## Next semantic-disassembly phase
AXPE Rev0 is used as the symbol-labeling base. `pret/pokeruby` names/sections can be attached to exact addresses, then propagated across revisions and languages using byte signatures and CFG signatures. That turns the present static disassembly into a source-level bank map without sacrificing the regional/revision differences.
