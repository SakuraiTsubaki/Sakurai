# Generation V → ポケットモンスター — project structure v6

Canonical project root: `PROJECTS/CROSS-GEN/GEN5-TO-POCKET-MONSTERS/`.

This project is cross-generation and many-to-many: Generation V source material is integrated into Generation II and Generation III targets. Official source/release facts live only in `LIBRARY`; transformation logic lives here.

## Sakurai research sections

- `MANIFESTS/` — source/target locks, provenance, status, routing.
- `INPUTS/` — project-facing references to locked source/dump identities.
- `CROSSWALK/` — Generation V → target correspondence tables by domain.
- `ANALYSIS/` — project-specific compatibility and delta analysis.
- `DESIGN/` — engine/data-model/compatibility design.
- `DIFFS/` — derived source-vs-target deltas.
- `TOOLS/` — research-only parsers, validators, report generators.
- `REPORTS/` — human-readable audits and phase reports.
- `VERIFICATION/` — regression evidence and source-vs-port validation.

## ROM ownership

Original ROM binaries never enter Git. Exact observed-file facts belong under `LIBRARY/.../SOURCE/.../<RELEASE-ID>/DUMPS/<DUMP-ID>/`; release identity and native facts belong under the matching release.

## Production ownership

Converted assets, insertion-ready data, patches and build products belong in `SakuraiTsubaki/Tsubaki/PROJECTS/CROSS-GEN/GEN5-TO-POCKET-MONSTERS/` and use the same release, dump and target IDs.

## No new legacy paths

Do not create new project work under `PROJECTS/GEN-05/GEN5-TO-POCKET-MONSTERS`, `GENERATION-*`, `_SHARED`, `MULTI`, `REV-ALL`, `REV-UNKNOWN`, `MISC`, `OTHER`, or `GENERAL`. Pre-v6 material belongs only in `LEGACY/PRE-V6-2026-09-12/` until equivalence migration is complete.
