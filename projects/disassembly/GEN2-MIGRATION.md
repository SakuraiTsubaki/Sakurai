# Generation II migration map

Status: **provisional placement — granular re-audit required**.

The legacy game roots were previously moved as whole Git tree objects. That preserved bytes, but it did **not** prove that every nested file belongs to the corresponding upstream repository.

| Provisional namespace | Legacy source root | Audit status |
| --- | --- | --- |
| `projects/disassembly/PocketMonsters-Kin-Disassembly/` | former `GEN-02/GOLD/` | Re-audit required |
| `projects/disassembly/PocketMonsters-Gin-Disassembly/` | former `GEN-02/SILVER/` | Re-audit required |
| `projects/disassembly/PocketMonsters-Crystal-Disassembly/` | former `GEN-02/CRYSTAL/` | Re-audit required |

Each nested file or coherent subdirectory must now be classified using [`../../docs/MIGRATION_AUDIT.md`](../../docs/MIGRATION_AUDIT.md).

Direct upstream material may remain under the exact Disassembly repository namespace. Cross-version comparisons, consolidated inventories, shared analyses, or multi-source reports may belong under `derived/` or `shared/` instead.

`GEN-02/COMPARES/` remains migration input until its real ownership is established.

No Generation II namespace is considered fully canonical until the re-audit is complete.
