# Sakurai — Research-Control Aggregate

![Status](https://img.shields.io/badge/status-initial_setup-lightgrey)
![Project](https://img.shields.io/badge/project-research--control-blue)
![ROMs](https://img.shields.io/badge/ROM_binaries-not_included-success)

Cross-repository **research and control aggregation layer** for the complete project ecosystem.

**Sakurai is the research-control subset of Tsubaki.** Tsubaki is the complete non-ROM superset across the repository ecosystem; Sakurai focuses on the evidence, identity, analysis, specifications, comparison, and verification needed to understand and control that corpus.

## 🎯 Goals

- Aggregate research/control knowledge from all Disassembly, Decompilation, and special project repositories.
- Track release identity, provenance, analysis, comparisons, specifications, verification, and project relationships.
- Keep every research/control claim reproducible and connected to its originating repository or artifact.
- Provide a stable top-level view without recreating migration trees or repeatedly relocating project material.

## 🚧 Status

This repository is in its **initial setup** stage. Repository coverage and research/control indexes will be added progressively.

## 🗂️ Planned scope

- Repository and project registry
- Release/build/version identity
- Provenance and source relationships
- Cross-repository research and comparisons
- Specifications and control documents
- Verification and reproducibility records
- Stable IDs, manifests, indexes, and tooling

## 📌 Repository policy

Retail, modified, rebuilt, trimmed, padded, or otherwise playable ROM images are **not included**.

Individual repositories remain the canonical homes of their game/project work. Sakurai aggregates the **research-control view** of that ecosystem. Historical structures belong to Git history rather than live `legacy`, `migration`, or structure-version trees.

## 🧭 Roadmap

- [ ] Establish the complete repository registry
- [ ] Define stable repository/project/release/artifact identifiers
- [ ] Build research and provenance indexes
- [ ] Connect Disassembly, Decompilation, and special-project relationships
- [ ] Add verification and reproducibility workflows

## 📚 Documentation

| Document | Purpose |
| --- | --- |
| [Project status](docs/PROJECT_STATUS.md) | Current aggregate coverage and next milestones |
| [Roadmap](docs/ROADMAP.md) | Recommended aggregation and control-layer progression |
| [Version coverage](docs/VERSIONS.md) | Repository/project/release coverage inventory |
| [Research guide](docs/RESEARCH_GUIDE.md) | Evidence, confidence, and cross-repository research workflow |
| [Verification guide](docs/VERIFICATION.md) | Identity, provenance, reproduction, and matching standards |
| [Repository structure](docs/REPOSITORY_STRUCTURE.md) | Stable live-tree organization policy |
| [Documentation hub](docs/README.md) | Entry point for aggregate research/control documentation |

## 🧱 Repository structure

The live tree starts intentionally small. Real material may grow into areas such as `registry/`, `research/`, `specs/`, `comparisons/`, `verification/`, `tools/`, `manifests/`, and `docs/`.

Do not create structural-version roots, migration mirrors, or duplicate historical trees. Git history is the history layer.

See [Repository Structure](docs/REPOSITORY_STRUCTURE.md) for the full organization policy.

## 🔬 Research and verification

Every finding should identify its originating repository/project and exact target when differences matter. Hypotheses must remain distinct from observed, reproduced, and matched results.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules, evidence expectations, commit guidance, and pull-request requirements.
