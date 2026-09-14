# RGBY カントー地方 -> GSC — work index

This is the **single starting point** for finding Sakurai-side work for this project.

Canonical project home:

`CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/`

## Current v12 control/research work

- Project identity and rules: `PROJECT.json`
- Current source set: `MANIFESTS/source-set-v12.json`
- Korean localization policy: `SPEC/LOCALIZATION-KR.md`
- Current repository routing: `SPEC/repository-routing-v12.md`
- Public disassembly pins: `REFERENCES/disassembly-pins.json`
- Current ROM deconstruction report: `REPORTS/ROM-DECONSTRUCTION/source-audit-2026-09-13.md`
- Current ROM inventory table: `TABLES/ROM-DECONSTRUCTION/rom_inventory.csv`
- Current audit tool: `TOOLS/audit_gb_gbc_source.py`
- Version migration record: `MIGRATION.md`

## Carried forward from v9

These files previously survived only in the old `CROSS-GEN/TARGET/...` history. They are now inside the canonical project root:

- `MANIFESTS/source-set-v09.json`
- `REPORTS/ROM-DECONSTRUCTION/bank-fingerprint-summary-v09.json`
- `REPORTS/ROM-DECONSTRUCTION/source-audit-summary-v09.md`
- `TABLES/ROM-DECONSTRUCTION/rom-inventory-v09.csv`
- `SPEC/repository-routing-v09.md`
- `TOOLS/audit_gb_gbc_sources-v09.py`
- `HISTORY/V09/README.md`

The former live v10 metadata is explicitly snapshotted under `HISTORY/V10/`. The original `SPEC/repository-routing-v10.md` remains alongside the v12 routing specification for comparison.

## Production counterpart

All production/data-plane work is at the exact same relative coordinate in Tsubaki:

`SakuraiTsubaki/Tsubaki:CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/`

Tsubaki contains the generated ROM catalogs and runtime-anchor tables and is the home for future semantic assets, conversions, implementation, patches, builds and production verification.

## Finding rule

A project-owned artifact must not exist **only** under `INFRA/MIGRATION/`, a retired `TARGET` path, or a release coordinate. Source release identity may remain under `GEN-XX/<GAME>/RELEASES/...`; project-specific work derived from those inputs must be discoverable from this project root.
