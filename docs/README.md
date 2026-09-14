# Documentation Hub

This directory is the repository-wide documentation portal for Sakurai, the curated research/control projection of the combined Disassembly + Decompilation corpus.

## Quick links

| Document | Purpose |
| --- | --- |
| [Aggregation Model](AGGREGATION_MODEL.md) | How 12 Disassembly + 34 Decompilation repositories become Sakurai + Tsubaki |
| [Repository Structure](REPOSITORY_STRUCTURE.md) | Aggregate tree and migration rules |
| [Repository Overview](REPOSITORY_OVERVIEW.md) | What Sakurai owns and how it differs from Tsubaki |
| [Repository Workflow](WORKFLOW.md) | Standard identity → evidence → research → verification flow |
| [Project Status](PROJECT_STATUS.md) | Current repository-wide status |
| [Roadmap](ROADMAP.md) | Long-term priorities |
| [Version Coordinates](VERSIONS.md) | Release/version identity conventions |
| [Research Guide](RESEARCH_GUIDE.md) | Evidence and research workflow |
| [Verification](VERIFICATION.md) | Evidence levels and matching criteria |
| [Project Standards](PROJECT_STANDARDS.md) | Naming, ownership, provenance, and data rules |
| [Asset Workflow](ASSET_WORKFLOW.md) | Curated evidence/asset workflow |
| [Repository Pairing](PAIRING.md) | Sakurai ↔ Tsubaki relationship |
| [Manifest Guide](../manifests/README.md) | Reusable manifest conventions |
| [Upstream Registry](../manifests/upstream-repositories.json) | Authoritative 46-repository source list |
| [Contributing](../CONTRIBUTING.md) | Contribution expectations |

## Aggregate flow

1. Identify the exact upstream family and repository.
2. Identify the exact target/version/revision represented by the material.
3. Capture provenance and evidence before interpretation.
4. Keep hypotheses separate from observed findings.
5. Normalize only when semantics are truly shared across repositories.
6. Reproduce or match the result when practical.
7. Assign the appropriate verification level.
8. Place the curated result under the matching `projects/disassembly/` or `projects/decompilation/` namespace, or use `shared/` / `derived/` only when those ownership rules genuinely apply.
9. Pair eligible production/archive artifacts with Tsubaki.

## Navigation rules

- Use `AGGREGATION_MODEL.md` first when deciding how source repositories feed Sakurai and Tsubaki.
- Use `REPOSITORY_STRUCTURE.md` for destination paths.
- Use `REPOSITORY_OVERVIEW.md` when deciding whether material belongs in Sakurai or Tsubaki.
- Use `PROJECT_STANDARDS.md` for naming, provenance, ownership, and deduplication rules.
- Use `RESEARCH_GUIDE.md` and `VERIFICATION.md` before promoting a claim from hypothesis to verified finding.
- Use `PAIRING.md` when the same semantic material exists in both aggregate repositories.

Do not invent a replacement V-numbered architecture. The upstream registry plus the aggregate model are the source of truth.
