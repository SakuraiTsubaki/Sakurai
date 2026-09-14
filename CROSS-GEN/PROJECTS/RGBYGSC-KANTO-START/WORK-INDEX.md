# RGBY カントー地方 -> GSC — work index

This is the **single starting point** for finding Sakurai-side work for this project.

Canonical project home:

`CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/`

## Actual Kanto work — start here

The concrete Kanto-start phase work is inside this project root at:

`GEN2-KANTO-START/GOLD-KR/`

Key carried-forward work includes:

- `GEN2-KANTO-START/GOLD-KR/analysis/` — bootstrap, Oak's Lab RGB starters, Pallet RGBY fidelity analysis
- `GEN2-KANTO-START/GOLD-KR/phase04/` — Pallet starter gate
- `GEN2-KANTO-START/GOLD-KR/phase05/` — Oak early-game branch
- `GEN2-KANTO-START/GOLD-KR/phase06/` — Pallet full-survey baseline and block diff
- `GEN2-KANTO-START/GOLD-KR/phase07/` — internal tileset capacity
- `GEN2-KANTO-START/GOLD-KR/phase08/` — RGBY → Gen II collision conversion
- `GEN2-KANTO-START/GOLD-KR/phase09/` — integrated tileset allocation
- `GEN2-KANTO-START/GOLD-KR/phase10/` — integrated tileset substrate
- `GEN2-KANTO-START/GOLD-KR/phase11/` — RGBY Pallet intro activation
- `GEN2-KANTO-START/GOLD-KR/phase12/` — RGBY Pallet fidelity
- later phase directories in the same `GOLD-KR/` tree, including palette/profile and regression work

The current Tsubaki production/runtime workspace is at the matching project coordinate, with Korean Silver work exposed at:

`SakuraiTsubaki/Tsubaki:CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/IMPLEMENTATION/SILVER-KR/`

`GSC-KANTO-TO-RGBY/` is the **opposite-direction project** and is not the owner of this work.

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

All production/data-plane work belongs at the exact same project coordinate in Tsubaki:

`SakuraiTsubaki/Tsubaki:CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/`

Tsubaki contains the generated ROM catalogs, runtime-anchor tables, implementation assets, build metadata and production verification.

## Finding rule

A project-owned artifact must not exist **only** under `INFRA/MIGRATION/`, a retired `TARGET` path, a reverse-direction project, or a release coordinate. Source release identity may remain under `GEN-XX/<GAME>/RELEASES/...`; project-specific work derived from those inputs must be discoverable from this project root.
