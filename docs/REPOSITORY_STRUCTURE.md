# Repository Structure

Sakurai is the curated research/control projection of the combined **Disassembly + Decompilation** repository universe.

The source repositories are not flattened into one anonymous generation tree. Their repository identity is preserved so every aggregate item can be traced back to its exact upstream origin.

```text
README.md
CONTRIBUTING.md
.editorconfig
.gitattributes
.gitignore
.github/

docs/
├── README.md
├── AGGREGATION_MODEL.md
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
├── example.asset-manifest.json
└── upstream-repositories.json

projects/
├── disassembly/
│   └── <UPSTREAM-REPOSITORY>/
└── decompilation/
    └── <UPSTREAM-REPOSITORY>/

shared/        verified material genuinely shared across upstream repositories
derived/       cross-repository or higher-level work derived from multiple upstreams
```

## Aggregate rule

The authoritative equation is:

```text
Disassembly series + Decompilation series -> Sakurai + Tsubaki
```

For Sakurai, each upstream repository contributes only the curated research/control subset that belongs here: identity, provenance, hashes, analysis, comparisons, documentation, research tooling, manifests, and verification evidence.

The full upstream list is maintained in `manifests/upstream-repositories.json`.

## Upstream namespaces

- `projects/disassembly/<UPSTREAM-REPOSITORY>/` preserves the source identity of material originating from the Disassembly series.
- `projects/decompilation/<UPSTREAM-REPOSITORY>/` preserves the source identity of material originating from the Decompilation series.
- Repository names are preserved as the namespace key so games present in both families, such as Ruby, Sapphire, Emerald, FireRed, and LeafGreen, cannot collide.

## Shared and derived material

Use `shared/` only when one representative artifact is proven equivalent across multiple upstream repositories. Record all upstream relationships and the verification method in a manifest.

Use `derived/` for genuine cross-repository work whose owner is the combined corpus rather than one upstream repository. Cross-generation comparisons and projects belong here when they are truly derived from multiple sources.

## Migration rules

- Existing `GEN-*`, `CROSS-GEN`, and `INFRA` trees are migration inputs, not the final architecture.
- Move material only after its upstream repository or genuine shared/derived ownership is identified.
- Preserve unique material during migration.
- Do not force Disassembly source layout into Decompilation conventions or vice versa.
- Do not deduplicate based only on similar appearance or names; verify identity first.
- Do not create V-numbered repository architectures.
- Do not create empty directory trees solely for appearance.
- Complete playable ROM image files are not committed.

## Source of truth

See [`AGGREGATION_MODEL.md`](AGGREGATION_MODEL.md) for the projection rules and [`../manifests/upstream-repositories.json`](../manifests/upstream-repositories.json) for the current 46-repository upstream registry.
