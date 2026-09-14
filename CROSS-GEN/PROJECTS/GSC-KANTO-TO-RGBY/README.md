# GSC Kanto → RGBY

Canonical project ID: `GSC-KANTO-TO-RGBY`.

This project ports Generation II Kanto content into a Generation I RGBY engine while preserving version, region, revision, event, map, text, and localization differences as explicit data.

## Canonical project location

`CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/`

This is the live project root. Current GSCRGBY work must be discoverable here; `INFRA/MIGRATION/PRE-V12/...` is historical evidence only and is not a working location.

## Project navigation

- `INPUTS/` — curated provenance and source locks.
- `ANALYSIS/` — validated reverse-engineering conclusions and cross-generation Kanto research.
- `TOOLS/` — reproducible research, inventory, conversion, and validation tools.
- `MANIFESTS/` — ROM baselines, routing history, source repositories, and migration records.
- `SPEC/` — project rules, repository contracts, event/localization policy, and historical layout specifications.
- `SESSION-INDEX.md` — maps the ChatGPT project sessions to their canonical GitHub artifacts.
- `PROJECT.json` — canonical project identity/ownership metadata.

## Pair contract

The semantic coordinate is identical in both repositories:

`CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/`

- **Sakurai** is the curated knowledge/control subset: release and dump identity, hashes, provenance, schemas, mappings, reverse-engineering conclusions, reports, specifications, research tools, and verification.
- **Tsubaki** is the complete non-ROM superset. Every project artifact that is eligible for GitHub and is not an original/modified playable ROM image belongs there, including all Sakurai-class artifacts plus upstream source mirrors, extracted/normalized/converted assets, implementation data, patches, build recipes/logs, tools, tests, experiments, and intermediate evidence.

Therefore Sakurai project artifacts are expected to have a Tsubaki counterpart at the same semantic coordinate, except repository-specific metadata.

## Pre-v12 recovery

The surviving public `projects/gscrgby` artifacts were promoted back into this canonical project root after the v12 redesign. Older layout/routing documents are retained under explicit versioned filenames in `SPEC/` and `MANIFESTS/`; curated provenance is under `INPUTS/`; validated Kanto/Gen II conclusions are under `ANALYSIS/`; research tooling is under `TOOLS/`.

The preserved copies below `INFRA/MIGRATION/PRE-V12/` remain immutable migration evidence and are not the place to look for current work.

## Primary Korean Generation II inputs

- Gold: `GEN-02/GOLD/RELEASES/GBC/CART/AAUK-HV0/`
- Silver: `GEN-02/SILVER/RELEASES/GBC/CART/AAXK-HV0/`

Exact dump hashes are recorded in `MANIFESTS/ROM-BASELINES.json`. ROM images themselves are never committed.

See `PROJECT.json`, `MANIFESTS/UPSTREAM-LOCKS.json`, `MANIFESTS/PATH-MIGRATION-V11.json`, and `SPEC/REPOSITORY-SPLIT.md`.
