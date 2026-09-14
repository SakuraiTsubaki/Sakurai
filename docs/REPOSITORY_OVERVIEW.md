# Repository Overview

Sakurai is the curated research and control repository for the Pokémon reverse-engineering workspace.

## What belongs here

Sakurai keeps the material required to identify, explain, compare, verify, and govern project work:

- release and dump identity
- provenance and hashes
- reverse-engineering notes and findings
- comparisons and cross-version analysis
- localization research
- schemas, tables, reports, and technical design
- research tooling and reproducibility metadata
- citations and verification evidence

Sakurai is intentionally selective. It does not need to mirror every production artifact that exists in Tsubaki.

## Relationship to Tsubaki

| Sakurai | Tsubaki |
| --- | --- |
| Curated research/control subset | Complete eligible non-ROM superset |
| Identity, provenance, analysis, verification | Source, assets, tools, outputs, intermediates, plus eligible Sakurai material |
| Keeps evidence needed to support claims | Keeps the full non-ROM production/archive record |
| May reference a Tsubaki artifact instead of duplicating it when appropriate | Preserves eligible project artifacts even when they are binary or intermediate |

Shared semantic coordinates should identify the same generation, game, release, dump, project, comparison, reference, and target in both repositories.

## Repository-wide entry points

- `README.md` — repository landing page
- `STRUCTURE.md` — current canonical path architecture
- `INFRA/DOCS/README.md` — documentation hub
- `INFRA/MANIFESTS/README.md` — manifest conventions
- `CONTRIBUTING.md` — contribution rules
- `.github/` — validation, issue templates, pull-request template, and CI

## Core principle

A claim in Sakurai should be traceable to evidence. Unknown or inferred information should remain explicitly marked as such until verification improves it.
