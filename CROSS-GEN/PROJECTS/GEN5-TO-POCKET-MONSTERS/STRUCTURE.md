# Generation V → ポケットモンスター — canonical structure

Canonical project root:

`CROSS-GEN/PROJECTS/GEN5-TO-POCKET-MONSTERS/`

This is the only live Sakurai location for work belonging to this project. Generation V source research and the cross-generation integration work are not split into separate live trees.

## Direct project sections

- `BLACK/` — Pokémon Black release research, extraction, native data and analysis.
- `WHITE/` — Pokémon White release research, extraction, native data and analysis.
- `COMPARES/` — version, region, language and revision comparisons.
- `SHARED/` — shared Generation V research data and tools.
- `CROSSWALK/` — Generation V → target correspondence tables.
- `DESIGN/` — engine, data-model and compatibility design.
- `MANIFESTS/` — source/target locks, provenance, status and routing.
- `REPORTS/` — human-readable audits and phase reports.
- `TOOLS/` — parsers, validators and report generators.
- `VERIFICATION/` — regression evidence and source-vs-port validation.

## Single-location rule

Do not recreate repository-root `GEN-05/`, nested `GEN-05/`, or migration/legacy duplicates for current project work. When the project is updated, the changed artifact is updated directly in this canonical tree.

## ROM policy

Complete playable ROM images are not committed. Every other project artifact may be committed under its actual functional folder in this canonical project tree.
