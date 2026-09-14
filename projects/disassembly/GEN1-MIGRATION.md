# Generation I migration map

Status: **provisional placement — granular re-audit required**.

The legacy game roots were previously moved as whole Git tree objects. That preserved bytes, but it did **not** prove that every nested file belongs to the corresponding upstream repository.

| Provisional namespace | Legacy source root | Audit status |
| --- | --- | --- |
| `projects/disassembly/PocketMonsters-Aka-Disassembly/` | former `GEN-01/RED/` | Re-audit required |
| `projects/disassembly/PocketMonsters-Midori-Disassembly/` | former `GEN-01/GREEN/` | Re-audit required |
| `projects/disassembly/PocketMonsters-Ao-Disassembly/` | former `GEN-01/BLUE/` | Re-audit required |
| `projects/disassembly/PocketMonsters-Pikachu-Disassembly/` | former `GEN-01/YELLOW/` | Re-audit required |

Each nested file or coherent subdirectory must now be classified using [`../../docs/MIGRATION_AUDIT.md`](../../docs/MIGRATION_AUDIT.md).

Direct upstream material may remain under the exact Disassembly repository namespace. Comparisons, supplied/uploaded source-set audits, cross-version inventories, consolidated reports, and other multi-source products may belong under `derived/` or `shared/` instead.

`GEN-01/PROJECTS/` remains migration input until its real ownership is established.

No Generation I namespace is considered fully canonical until the re-audit is complete.
