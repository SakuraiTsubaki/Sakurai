# Generation I migration map

The former generation-level game roots are being moved into exact Disassembly upstream namespaces:

| Legacy root | Upstream namespace |
| --- | --- |
| `GEN-01/RED/` | `projects/disassembly/PocketMonsters-Aka-Disassembly/` |
| `GEN-01/GREEN/` | `projects/disassembly/PocketMonsters-Midori-Disassembly/` |
| `GEN-01/BLUE/` | `projects/disassembly/PocketMonsters-Ao-Disassembly/` |
| `GEN-01/YELLOW/` | `projects/disassembly/PocketMonsters-Pikachu-Disassembly/` |

The move preserves Git tree objects and therefore the underlying file contents while replacing the legacy generation/game owner path with exact upstream repository identity.

`GEN-01/PROJECTS/` is not part of this 1:1 move because it may contain genuinely derived or cross-repository work and must be classified separately.
