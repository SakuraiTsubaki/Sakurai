# RGBY カントー地方 -> GSC — project migration record

Status: **v12 migration repaired — 2026-09-14**.

## Version history

| Version | Canonical project coordinate | Result |
|---|---|---|
| v9 | `CROSS-GEN/TARGET/RGBYGSC-KANTO-START/` | Initial ROM audit / project routing. |
| v10 | `CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/` | New project coordinate created, but several unique v9 files were removed from the live tree instead of being carried forward. |
| v11 | `CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/` | Coordinate retained; no complete per-project carry-forward audit was recorded. |
| v12 | `CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/` | Repository architecture standardized, but the earlier v9→v10 omission was not repaired until this record. |

## Recovered v9 Sakurai work

- `MANIFESTS/source-set.json` → `MANIFESTS/source-set-v09.json`
- `REPORTS/SOURCE-ROM-AUDIT/bank_fingerprint_summary.json` → `REPORTS/ROM-DECONSTRUCTION/bank-fingerprint-summary-v09.json`
- `REPORTS/SOURCE-ROM-AUDIT/rom_inventory.csv` → `TABLES/ROM-DECONSTRUCTION/rom-inventory-v09.csv`
- `REPORTS/SOURCE-ROM-AUDIT/summary.md` → `REPORTS/ROM-DECONSTRUCTION/source-audit-summary-v09.md`
- `SPEC/repository-routing.md` → `SPEC/repository-routing-v09.md`
- `TOOLS/audit_gb_gbc_sources.py` → `TOOLS/audit_gb_gbc_sources-v09.py`
- v9 project README → `HISTORY/V09/README.md`

Source commit: `2e38d672452429ab7c209f208a2a46fabe82f434`.

The v10 live `PROJECT.json` and `README.md` are preserved under `HISTORY/V10/` before the live metadata is advanced to v12.

## Current v12 repair

- Live project metadata now reports layout v12.
- `WORK-INDEX.md` is the human-facing project entry point.
- `MANIFESTS/source-set-v12.json` carries the current content-addressed dump IDs.
- `SPEC/repository-routing-v12.md` defines the no-orphan rule for future migrations.
- `SPEC/LOCALIZATION-KR.md` carries forward the Korean localization rules established in the project sessions.

## Future V migration invariant

Before retiring any project path or version:

1. Inventory every project-owned file in the old live tree.
2. Carry every unique artifact into the new project root, or keep an explicit versioned snapshot inside that root.
3. Update `WORK-INDEX.md`, manifests and routing documentation.
4. Verify that no current project artifact exists only in a retired path or `INFRA/MIGRATION/`.
5. Verify the Sakurai/Tsubaki pair at the same semantic project coordinate.
6. Only then retire the old live path.

Git history remains evidence, but **Git history alone is not an acceptable home for a project work product that should still be findable.**
