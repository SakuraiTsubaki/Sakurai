# Sakurai

![Status](https://img.shields.io/badge/status-active-success)
![Project](https://img.shields.io/badge/project-research_control-blue)
![ROMs](https://img.shields.io/badge/ROM_binaries-not_included-success)

Pokémon source identity, reverse engineering, comparison, localization research, technical design, and verification repository.

## 🌸 Aggregate model

Sakurai is not a standalone repository family. It is one projection of the combined Disassembly and Decompilation series.

```text
Disassembly series (12 repositories)
                 +
Decompilation series (34 repositories)
                 ↓
       combined upstream corpus
           ↙             ↘
      Sakurai           Tsubaki
 research/control     full non-ROM archive
```

**Current upstream total: 46 repositories.**

- [Aggregation model](docs/AGGREGATION_MODEL.md)
- [Upstream repository registry](manifests/upstream-repositories.json)

## 🎯 Role

Sakurai is the **curated research/control projection** of that 46-repository corpus. It aggregates target identity, provenance, hashes, reverse-engineering analysis, comparisons, localization research, schemas, reports, research tooling, citations, manifests, and verification evidence from both source families.

Tsubaki is the complete eligible non-ROM production/archive projection of the same corpus.

## 🌸 Repository pair

| Area | Sakurai | Tsubaki |
| --- | --- | --- |
| Upstream universe | Disassembly + Decompilation | Disassembly + Decompilation |
| Primary role | Curated research / control | Complete eligible non-ROM production / archive |
| Identity & provenance | Primary control record | Preserved with artifacts |
| Research & comparisons | Curated findings and evidence | Eligible supporting outputs |
| Source / implementation | When needed for research/control | Full eligible project material |
| Graphics / sprites / PNG | Curated evidence when useful | Full eligible source and human-viewable assets |
| Build / extraction outputs | Reproducibility evidence as needed | Eligible outputs and intermediates retained |
| Complete playable ROM images | Never committed | Never committed |

**Rule of thumb:** if the question is *“What is this, where did it come from, and how do we know?”*, it belongs in Sakurai's projection.

## 🗂️ Aggregate tree

```text
README.md
CONTRIBUTING.md
.github/
docs/
manifests/

projects/
├── disassembly/
│   └── <UPSTREAM-REPOSITORY>/
└── decompilation/
    └── <UPSTREAM-REPOSITORY>/

shared/
derived/
```

### `projects/disassembly/`
Curated research/control material originating from the 12 Disassembly repositories.

### `projects/decompilation/`
Curated research/control material originating from the 34 Decompilation repositories.

### `shared/`
Material proven to be genuinely shared across multiple upstream repositories. Deduplication requires verified identity and preserved provenance.

### `derived/`
Research/control work whose owner is the combined corpus rather than one source repository, such as cross-generation or cross-series comparisons.

Existing `GEN-*`, `CROSS-GEN`, and remaining `INFRA` content is migration input and will be mapped into this aggregate model without discarding unique work.

## 🔬 Working flow

```text
Upstream repository
      ↓
Target identity + provenance
      ↓
Research / comparison
      ↓
Reproducibility checks
      ↓
Verification level
      ↓
Sakurai control record
      ↕
Tsubaki artifact record
```

Unknown or inferred information remains explicitly marked until stronger evidence is available.

## 📌 Repository policy

- Preserve the exact upstream family and repository identity for aggregated material.
- Hypotheses must be distinguished from observed, reproduced, or matched evidence.
- Common material is deduplicated only after equivalence is verified.
- Complete playable ROM image files are not committed.
- Repository-wide documentation lives under `docs/`.
- Repository-wide manifests and the upstream registry live under `manifests/`.
- Do not recreate V-numbered repository architectures.

## 📚 Documentation

| Document | Purpose |
| --- | --- |
| [Aggregation Model](docs/AGGREGATION_MODEL.md) | How Disassembly + Decompilation become Sakurai + Tsubaki |
| [Repository Structure](docs/REPOSITORY_STRUCTURE.md) | Aggregate tree and migration rules |
| [Documentation Hub](docs/README.md) | Central documentation index |
| [Repository Overview](docs/REPOSITORY_OVERVIEW.md) | Sakurai role and relationship to Tsubaki |
| [Repository Workflow](docs/WORKFLOW.md) | Evidence → research → verification flow |
| [Project Status](docs/PROJECT_STATUS.md) | Current migration and repository status |
| [Roadmap](docs/ROADMAP.md) | Long-term priorities |
| [Research Guide](docs/RESEARCH_GUIDE.md) | Evidence, citations, uncertainty, and reproducibility |
| [Verification](docs/VERIFICATION.md) | Verification levels and matching criteria |
| [Project Standards](docs/PROJECT_STANDARDS.md) | Naming, provenance, ownership, and conventions |
| [Repository Pairing](docs/PAIRING.md) | Sakurai ↔ Tsubaki synchronization rules |
| [Manifest Guide](manifests/README.md) | Manifest conventions |
| [Upstream Registry](manifests/upstream-repositories.json) | All 46 source repositories |
| [Contributing](CONTRIBUTING.md) | Contribution expectations |

**Complete playable ROM image files are excluded from GitHub.**
