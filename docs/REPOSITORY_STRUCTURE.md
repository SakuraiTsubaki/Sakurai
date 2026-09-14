# Repository Structure

Sakurai's repository-wide operating tree follows the same convention used by the Decompilation series.

```text
README.md
CONTRIBUTING.md
.editorconfig
.gitattributes
.gitignore
.github/
docs/
├── README.md
├── PROJECT_STATUS.md
├── ROADMAP.md
├── VERSIONS.md
├── RESEARCH_GUIDE.md
├── VERIFICATION.md
├── REPOSITORY_OVERVIEW.md
├── REPOSITORY_STRUCTURE.md
├── PROJECT_STANDARDS.md
├── ASSET_WORKFLOW.md
├── WORKFLOW.md
└── PAIRING.md
manifests/
├── README.md
└── example.asset-manifest.json

GEN-XX/       generation-scoped research/project material
CROSS-GEN/    cross-generation research/project material
INFRA/        remaining infrastructure material pending simplification
```

## Rules

- `docs/` is the repository-wide documentation root.
- `manifests/` is the repository-wide reusable manifest root.
- Do not recreate `INFRA/DOCS` or `INFRA/MANIFESTS`.
- The historical V12 routing model is not authoritative for new tree work.
- Existing generation and cross-generation content should be moved only when its new owner is clear; preserve unique material during migration.
- Do not create empty directory trees solely for symmetry.
- Complete playable ROM image files are not committed.

## Migration direction

The next tree passes should simplify `GEN-XX/`, `CROSS-GEN/`, and `INFRA/` by following actual ownership and content, using the Decompilation repositories as the structural reference rather than inventing another versioned architecture.
