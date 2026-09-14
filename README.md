# Sakurai

![Status](https://img.shields.io/badge/status-canonical_v12-active-success)
![Project](https://img.shields.io/badge/project-research_control-blue)
![ROMs](https://img.shields.io/badge/ROM_binaries-not_included-success)

Pokémon source identity, reverse engineering, comparison, localization research, technical design, and verification repository.

## 🎯 Role

Sakurai is the **curated research/control subset** of the repository pair. It owns release and dump identity, provenance, hashes, reverse-engineering analysis, comparisons, localization research, tables, schemas, reports, research tooling, citations, and verification evidence.

Tsubaki is the complete eligible non-ROM superset. Both repositories use the same semantic generation, game, release, dump, comparison, reference, project, and target coordinates.

## 🧭 Repository overview

Sakurai is where project claims are identified, sourced, compared, and verified. It keeps the evidence and control layer needed to explain *what a target is*, *where a fact came from*, *how variants differ*, and *how a result was verified*.

- Start with [Repository Overview](INFRA/DOCS/REPOSITORY_OVERVIEW.md) for the repository's role.
- Follow [Repository Workflow](INFRA/DOCS/WORKFLOW.md) for the standard research/control flow.
- Use [Documentation Hub](INFRA/DOCS/README.md) for the complete documentation index.
- Use [Manifest Guide](INFRA/MANIFESTS/README.md) for reusable provenance/asset records.

## 🗂️ Canonical architecture: v12

Current work lives only under:

```text
GEN-XX/<GAME-ID>/RELEASES|PROJECTS|COMPARES|REFERENCES|SHARED
GEN-XX/PROJECTS|COMPARES|REFERENCES|SHARED
CROSS-GEN/PROJECTS|COMPARES|REFERENCES|SHARED
INFRA/
```

A project has one live owner path. Project-specific analysis, comparisons, reports, tools, manifests, verification material, design, inputs, and other work products stay under that project root instead of being split across historical or version-specific trees.

Version updates modify the current tree directly. If a path changes, unique work is merged into the new canonical path and the old live path is removed in the same update. Git commits, tags, and pull requests are the history; no separate migration/history tree is required.

## 🔬 Working flow

```text
Target / owner identity
        ↓
Provenance + evidence
        ↓
Research / comparison
        ↓
Reproducibility checks
        ↓
Verification level
        ↓
Curated control record
        ↕
Tsubaki production/archive artifacts
```

Unknown or inferred information remains explicitly marked until stronger evidence is available.

## 📌 Repository policy

- Sakurai stores curated research/control material rather than every eligible project artifact.
- Verified identity and provenance should be represented with stable semantic IDs and hashes.
- Hypotheses must be distinguished from observed, reproduced, or matched evidence.
- Complete playable ROM image files are not committed.
- Repository-wide documentation and standards live under `INFRA/DOCS/`.
- Shared manifest conventions and reusable examples live under `INFRA/MANIFESTS/`.

## 📚 Documentation

| Document | Purpose |
| --- | --- |
| [Documentation Hub](INFRA/DOCS/README.md) | Central entry point for repository-wide documentation |
| [Repository Overview](INFRA/DOCS/REPOSITORY_OVERVIEW.md) | What Sakurai owns and how it differs from Tsubaki |
| [Repository Workflow](INFRA/DOCS/WORKFLOW.md) | Standard evidence → research → verification flow |
| [Project Status](INFRA/DOCS/PROJECT_STATUS.md) | Current canonical-architecture and curation status |
| [Roadmap](INFRA/DOCS/ROADMAP.md) | Long-term repository and verification priorities |
| [Version Coordinates](INFRA/DOCS/VERSIONS.md) | Release, platform, package, revision, and dump identity rules |
| [Research Guide](INFRA/DOCS/RESEARCH_GUIDE.md) | Evidence, citations, uncertainty, and reproducibility |
| [Verification](INFRA/DOCS/VERIFICATION.md) | Unverified, Observed, Reproduced, and Matched criteria |
| [Repository Structure](INFRA/DOCS/REPOSITORY_STRUCTURE.md) | How documentation fits the current canonical tree |
| [Project Standards](INFRA/DOCS/PROJECT_STANDARDS.md) | Naming, provenance, ownership, and repository-wide conventions |
| [Asset Workflow](INFRA/DOCS/ASSET_WORKFLOW.md) | Curated asset/evidence handling and deduplication |
| [Repository Pairing](INFRA/DOCS/PAIRING.md) | Sakurai ↔ Tsubaki synchronization rules |
| [Manifest Guide](INFRA/MANIFESTS/README.md) | Shared manifest fields and reusable example |
| [Contributing](CONTRIBUTING.md) | Contribution and pull-request expectations |
| [Canonical Structure](STRUCTURE.md) | Current path architecture |

**Only complete playable ROM image files are excluded from GitHub.**
