# Generation I migration map

Status: **game roots moved**.

| Legacy root | Current upstream namespace |
| --- | --- |
| `GEN-01/RED/` | `projects/disassembly/PocketMonsters-Aka-Disassembly/` |
| `GEN-01/GREEN/` | `projects/disassembly/PocketMonsters-Midori-Disassembly/` |
| `GEN-01/BLUE/` | `projects/disassembly/PocketMonsters-Ao-Disassembly/` |
| `GEN-01/YELLOW/` | `projects/disassembly/PocketMonsters-Pikachu-Disassembly/` |

The move reused the existing Git tree objects, preserving the underlying file contents while replacing the legacy generation/game owner paths with exact upstream repository identity.

`GEN-01/PROJECTS/` remains temporarily because it may contain genuinely derived or cross-repository work and must be classified separately before moving to `derived/` or another truthful owner.
