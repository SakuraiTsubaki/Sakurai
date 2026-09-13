# GSC Kanto → RGBY

Canonical v11 project ID: `GSC-KANTO-TO-RGBY`.

This project ports Generation II Kanto content into a Generation I RGBY engine while preserving version, region, revision, event, map, text, and localization differences as explicit data.

## Pair contract

The semantic coordinate is identical in both repositories:

`CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/`

- **Sakurai** is the curated knowledge/control subset: release and dump identity, hashes, provenance, schemas, mappings, reverse-engineering conclusions, reports, specifications, research tools, and verification.
- **Tsubaki** is the complete non-ROM superset. Every project artifact that is eligible for GitHub and is not an original/modified playable ROM image belongs there, including all Sakurai-class artifacts plus upstream source mirrors, extracted/normalized/converted assets, implementation data, patches, build recipes/logs, tools, tests, and experiments.

Therefore Sakurai project artifacts are expected to have a Tsubaki counterpart at the same semantic coordinate, except repository-specific metadata.

## Primary Korean Generation II inputs

- Gold: `GEN-02/GOLD/RELEASES/GBC/CART/AAUK-HV0/`
- Silver: `GEN-02/SILVER/RELEASES/GBC/CART/AAXK-HV0/`

Exact dump hashes are recorded in `MANIFESTS/ROM-BASELINES.json`. ROM images themselves are never committed.

See `PROJECT.json`, `MANIFESTS/UPSTREAM-LOCKS.json`, and `SPEC/REPOSITORY-SPLIT.md`.
