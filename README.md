# Sakurai

![Status](https://img.shields.io/badge/status-active-success)
![Project](https://img.shields.io/badge/project-research_control-blue)
![ROMs](https://img.shields.io/badge/ROM_binaries-not_included-success)

Pokémon source identity, reverse engineering, comparison, localization research, technical design, and verification repository.

## 🎯 Role

Sakurai is the **curated research/control repository** of the Sakurai ↔ Tsubaki pair. It owns release and dump identity, provenance, hashes, reverse-engineering analysis, comparisons, localization research, tables, schemas, reports, research tooling, citations, and verification evidence.

Tsubaki is the complete eligible non-ROM production/archive repository. Shared semantic coordinates should identify the same targets in both repositories.

## 🌸 Repository pair

| Area | Sakurai | Tsubaki |
| --- | --- | --- |
| Primary role | Curated research / control | Complete eligible non-ROM production / archive |
| Identity & provenance | Primary record | Mirrored when relevant to artifacts |
| Research & comparisons | Curated findings and evidence | Eligible working copies and supporting outputs |
| Source / implementation | When needed for research/control | Full eligible project material |
| Graphics / sprites / PNG | Curated evidence when useful | Full eligible source and human-viewable assets |
| Audio / maps / text / data | Curated research/control material | Full eligible project artifacts |
| Build / extraction outputs | Reproducibility evidence as needed | Eligible outputs and intermediates retained |
| Manifests / hashes | Identity, provenance, verification | Artifact, provenance, generation, verification |
| Complete playable ROM images | Never committed | Never committed |

**Rule of thumb:** if the question is *“What is this, where did it come from, and how do we know?”*, Sakurai owns the control record. If the question is *“What project material should be preserved so the work can be inspected, reproduced, or continued?”*, Tsubaki owns the complete eligible non-ROM artifact set.

## 🧭 Repository overview

- Start with [Repository Overview](docs/REPOSITORY_OVERVIEW.md).
- Follow [Repository Workflow](docs/WORKFLOW.md) for the standard research/control flow.
- Use [Documentation Hub](docs/README.md) for the complete documentation index.
- Use [Manifest Guide](manifests/README.md) for reusable provenance and inventory records.

## 🗂️ Repository structure

The repository-wide operating layer follows the same convention used by the Decompilation series:

```text
README.md
CONTRIBUTING.md
.editorconfig
.gitattributes
.gitignore
.github/
docs/
manifests/

GEN-XX/       project/research material grouped by generation
CROSS-GEN/    cross-generation work
INFRA/        remaining infrastructure material pending content-by-content cleanup
```

`docs/` and `manifests/` are first-class root directories. They are not nested under `INFRA/`.

The generation, cross-generation, and infrastructure content trees are being simplified separately. Their historical V12 layout is **not** the repository-wide canonical model.

## 🔬 Working flow

```text
Target identity
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
- Verified identity and provenance should use stable identifiers and hashes where practical.
- Hypotheses must be distinguished from observed, reproduced, or matched evidence.
- Complete playable ROM image files are not committed.
- Repository-wide documentation and standards live under `docs/`.
- Shared manifest conventions and reusable examples live under `manifests/`.
- Do not recreate `INFRA/DOCS` or `INFRA/MANIFESTS`.

## 📚 Documentation

| Document | Purpose |
| --- | --- |
| [Documentation Hub](docs/README.md) | Central entry point for repository-wide documentation |
| [Repository Overview](docs/REPOSITORY_OVERVIEW.md) | What Sakurai owns and how it differs from Tsubaki |
| [Repository Workflow](docs/WORKFLOW.md) | Standard evidence → research → verification flow |
| [Project Status](docs/PROJECT_STATUS.md) | Current repository and migration status |
| [Roadmap](docs/ROADMAP.md) | Long-term repository and verification priorities |
| [Version Coordinates](docs/VERSIONS.md) | Release, platform, revision, and identity rules |
| [Research Guide](docs/RESEARCH_GUIDE.md) | Evidence, citations, uncertainty, and reproducibility |
| [Verification](docs/VERIFICATION.md) | Unverified, Observed, Reproduced, and Matched criteria |
| [Repository Structure](docs/REPOSITORY_STRUCTURE.md) | Current repository-wide tree conventions |
| [Project Standards](docs/PROJECT_STANDARDS.md) | Naming, provenance, ownership, and repository-wide conventions |
| [Asset Workflow](docs/ASSET_WORKFLOW.md) | Curated asset/evidence handling and deduplication |
| [Repository Pairing](docs/PAIRING.md) | Sakurai ↔ Tsubaki synchronization rules |
| [Manifest Guide](manifests/README.md) | Shared manifest fields and reusable example |
| [Contributing](CONTRIBUTING.md) | Contribution and pull-request expectations |

**Only complete playable ROM image files are excluded from GitHub.**
