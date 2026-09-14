# Generation II migration map

Status: **game roots moved**.

| Legacy root | Current upstream namespace |
| --- | --- |
| `GEN-02/GOLD/` | `projects/disassembly/PocketMonsters-Kin-Disassembly/` |
| `GEN-02/SILVER/` | `projects/disassembly/PocketMonsters-Gin-Disassembly/` |
| `GEN-02/CRYSTAL/` | `projects/disassembly/PocketMonsters-Crystal-Disassembly/` |

The move reused the existing Git tree objects, preserving the underlying file contents while replacing legacy generation/game owner paths with exact upstream repository identity.

`GEN-02/COMPARES/` remains temporarily because its ownership is cross-repository by nature and should be classified into `derived/` or another truthful aggregate namespace after inspection.
