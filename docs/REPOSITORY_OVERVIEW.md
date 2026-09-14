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
| Curated research/control record | Complete eligible non-ROM production/archive record |
| Identity, provenance, analysis, verification | Source, assets, tools, outputs, intermediates, plus eligible supporting research |
| Keeps evidence needed to support claims | Keeps the full non-ROM artifact set needed to inspect, reproduce, or continue work |

Shared semantic coordinates should identify the same generation, game, release, revision, project, comparison, reference, and target in both repositories.

## Repository-wide entry points

- `README.md` — repository landing page
- `docs/README.md` — documentation hub
- `docs/REPOSITORY_STRUCTURE.md` — current repository-wide tree conventions
- `manifests/README.md` — reusable manifest conventions
- `CONTRIBUTING.md` — contribution rules
- `.github/` — validation, issue templates, pull-request template, and CI

## Tree policy

The repository-wide operating layout follows the Decompilation repository family: documentation and reusable manifests are first-class root directories. Historical V12 routing is not the canonical model for new organization work.

Generation and cross-generation content will be simplified incrementally so unique research is preserved while redundant routing layers are removed.

## Core principle

A claim in Sakurai should be traceable to evidence. Unknown or inferred information should remain explicitly marked until verification improves it.
