# Generation V → ポケットモンスター — project structure v4

This project is cross-generation and many-to-many. Official source/release facts live only in `LIBRARY`; transformation logic lives here under `PROJECTS/GEN5-TO-POCKET-MONSTERS`.

## Canonical research tree

- `MANIFESTS/` — source/target locks, provenance, status, routing.
- `CROSSWALK/` — Generation V → target correspondence tables by domain.
- `DESIGN/` — integration/engine/data-model/compatibility design.
- `VERIFICATION/` — test matrices, regression evidence, source-vs-port validation.
- `TOOLS/` — research-only parsers, validators, report generators.
- `REPORTS/` — human-readable audits and phase reports.

## ROM ownership

Original ROM binaries never enter Git. Exact supplied-file observations belong to `LIBRARY/.../DUMPS/<DUMP-ID>/`; official build facts belong to `LIBRARY/.../RELEASES/<RELEASE-ID>/`.

## Production ownership

Converted assets, insertion-ready data, patches and build products belong in `SakuraiTsubaki/Tsubaki/PROJECTS/GEN5-TO-POCKET-MONSTERS` and must reference the same release IDs used by Sakurai.

## No new legacy paths

Do not create new content under `GENERATION-*`, `GEN-*`, `GAMES/*`, `MULTI`, `REV-ALL`, `MISC`, `OTHER`, or `GENERAL`. Existing legacy material is migration input only.