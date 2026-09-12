# Pokémon Ruby — Bank-by-Bank Survey + Disassembly Pass

## Scope
- 13 uploaded Ruby GBA ROMs.
- Analysis bank size: 0x10000 bytes (64 KiB). This is an analysis partition, not a GBA hardware bank-switching unit.
- Total ROM×bank records: 3,200.
- Existing physical survey retained: hashes, entropy, fill runs, ROM-pointer density, ASCII/LZ candidates, semantic coarse region.
- Added in this pass: ARM/THUMB opcode-family sweep, startup-mode transition extraction, THUMB function-pointer seeds, conservative recursive THUMB control-flow traversal, and raw dual-mode Bank 00 disassembly.

## Important correctness rule
A GBA ROM mixes executable code and data in the same address space. A raw linear disassembly will inevitably decode literal pools, tables, scripts, graphics, text, and compressed data as fake instructions. Therefore this project keeps two layers separate:

1. **RAW DISASSEMBLY** — ARM and THUMB views produced mechanically. Useful for inspection but not semantic proof.
2. **CANDIDATE CFG DISASSEMBLY** — seeded from the real startup transition plus aligned odd ROM pointers whose target begins with `PUSH {..., LR}`, then follows direct THUMB `BL`, conditional/unconditional branches, returns, and indirect transfer stops. This is more selective, but still heuristic until matched to symbols/source.

Do not treat `candidate_recursive_*` columns as verified code size.

## Startup structure established from the uploaded ROMs
Two startup layouts were observed.

### Layout A — Japanese / English builds
- ROM word 0: `EA000032` -> ARM branch to file offset `0x000000D0` (`0x080000D0`).
- `BX r1` at `0x000000FC`.
- literal at `0x00000244` is odd ROM pointer `0x0800024D`.
- THUMB execution begins at file offset `0x0000024C` (`0x0800024C`).

Observed in AXVJ v0 Japanese and AXVE v0/v1/v2 English builds.

### Layout B — Spanish / French / Italian / German builds
- ROM word 0: `EA00007F` -> ARM branch to file offset `0x00000204` (`0x08000204`).
- extended data block occupies the space before `Init`.
- `BX r1` at `0x00000230`.
- literal at `0x00000378` is odd ROM pointer `0x08000381`.
- THUMB execution begins at file offset `0x00000380` (`0x08000380`).

Observed in all uploaded ES/FR/IT/DE retail revisions and the German Debug ROM.

The pret/pokeruby `crt0.s` source independently describes the German extended pre-Init block, followed by ARM `Init`, then `ldr r1, =AgbMain` / `bx r1`. The uploaded ES/FR/IT binaries show the same extended-layout geometry even though pret/pokeruby directly supports the German localized configuration.

## Exact public source reference matches
| Uploaded key | pret/pokeruby target | SHA-1 status |
|---|---|---|
| AXVE_v0_USA | pokeruby.gba | exact |
| AXVE_v1_EUR | pokeruby_rev1.gba | exact |
| AXVE_v2_USA_EUR | pokeruby_rev2.gba | exact |
| AXVD_v0_DEU | pokeruby_de.gba | exact |
| AXVD_v1_DEU | pokeruby_de_rev1.gba | exact |
| AXVD_v0_DEU_DEBUG | pokeruby_de_debug.gba | exact |

Seven other language/version ROMs currently have no exact pret/pokeruby build target in the checked repository and must be mapped by binary comparison rather than assumed symbol identity.

## Generated inventories
- `ruby_bank_disasm_inventory.csv` — 3,200 rows; bank survey plus ARM/THUMB instruction-family counts and candidate recursive-code coverage.
- `ruby_bootstrap_entries.csv` — startup ARM entry, `BX r1`, AgbMain pointer literal, and THUMB entry for all 13 ROMs.
- `ruby_disasm_reference_matches.csv` — local SHA-1 to exact pret/pokeruby build mapping.
- `ruby_thumb_pointer_targets.csv` — aligned odd ROM pointer targets, xref counts and strong `PUSH {...,LR}` flags.
- `ruby_thumb_function_entries.csv` — 142,953 ROM-specific candidate entries: 13 bootstrap entries, 71,201 strong pointer/prologue seeds, 71,739 direct-BL targets.
- `ruby_thumb_cfg_summary.csv` — ROM-level candidate CFG statistics.
- `ruby_usa_v0_thumb_cfg_edges.csv` — USA v0 candidate direct control-flow inventory: 167,197 edges (90,029 Bcc; 50,144 B; 27,024 BL).
- `ruby_bank00_disassembly_bundle.zip` — local raw ARM and THUMB linear views for Bank 00 of all 13 ROMs plus bootstrap JSON.
- `ruby_disasm_pipeline.py` — reproducible local analysis pipeline.

## Bank 00 first semantic labels
### Common
- `0x08000000`: `Start` (ARM branch)
- GBA header / Nintendo logo / title / game code / maker / checksum fields follow.
- GPIO header area begins around `0x080000C4` in the pokeruby reference source.

### Layout A
- `0x080000D0`: `Init` (ARM)
- `0x0800010C`: `IntrMain` (ARM)
- `0x0800024C`: `AgbMain` entry (THUMB)

### Layout B
- `0x080000D0..0x08000203`: extended localized metadata/data block
- `0x08000204`: `Init` (ARM)
- `0x08000240`: `IntrMain` (ARM)
- `0x08000380`: `AgbMain` entry (THUMB)

## Confidence states
- `RAW_ONLY`: mechanical ARM/THUMB decoding only.
- `CFG_CANDIDATE`: reached from conservative THUMB seeds/branches.
- `SOURCE_MATCH_EXACT`: address/content confirmed against an exact pret/pokeruby build.
- `CROSS_VERSION_MAPPED`: transferred by verified binary correspondence from an exact source-matched build.
- `SEMANTIC_VERIFIED`: function/data identity checked against symbols/source and ROM bytes.

Raw instruction text never promotes a region to executable code by itself.
