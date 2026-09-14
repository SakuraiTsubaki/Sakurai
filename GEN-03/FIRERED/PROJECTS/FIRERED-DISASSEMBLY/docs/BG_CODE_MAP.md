# `bg.c` cross-version code map

The background/GPU interface object follows `dma3_manager.c` in every audited FireRed baseline.

| Baseline | Start | End exclusive | Size |
|---|---:|---:|---:|
| JP Rev 0 | `0x08001028` | `0x0800292C` | `0x1904` (6404) |
| JP Rev 1 | `0x08001024` | `0x08002928` | `0x1904` (6404) |
| US Rev 0 | `0x08001028` | `0x0800292C` | `0x1904` (6404) |
| US Rev 1 | `0x0800103C` | `0x08002940` | `0x1904` (6404) |
| FR | `0x08001024` | `0x08002928` | `0x1904` (6404) |
| DE | `0x08001038` | `0x0800293C` | `0x1904` (6404) |
| IT | `0x08001038` | `0x0800293C` | `0x1904` (6404) |
| ES | `0x08001024` | `0x08002928` | `0x1904` (6404) |

The object is the same size in all eight ROMs. A byte-level comparison against US Rev 0 shows small regional differences, but every differing byte belongs to either:

1. a 32-bit ROM/RAM address literal, or
2. an ARMv4T Thumb `BL` call pair whose displacement changes because linked targets move.

No differing byte remains in ordinary arithmetic, data-processing, conditional-branch, load/store, or return instructions after those relocation-sensitive categories are removed. Therefore this repository treats `bg.c` as one shared logical source object for all eight builds.

`analysis/bg/object_audit.csv` records the direct ROM comparison. The US Rev 0 object boundary is independently consistent with the historical FireRed code map (`0x08001028..0x0800292B`) and with the current `pret/pokefirered` linker ordering (`bg.o` followed by `malloc.o`).
