# Architecture v13 — Draft

Status: **draft**. This document does not change the live canonical tree yet.

## Why v13 exists

v12 repeats too many ownership categories across game, generation, and cross-generation scopes. `PROJECTS`, `COMPARES`, `REFERENCES`, `SHARED`, `KNOWLEDGE`, `VERIFY`, `CATALOGS`, `REPORTS`, `TABLES`, `ANALYSIS`, and `TOOLS` can all compete as possible homes for the same work. Release identity is also encoded through an unnecessarily deep platform/package/release path.

v13 reduces the model to one rule:

> **Put work under the thing that owns it. Everything else is a document, manifest, asset, or tool inside that owner.**

## Proposed root

```text
.github/
GEN-XX/
CROSS-GEN/
INFRA/
README.md
STRUCTURE.md
```

## Game-owned work

```text
GEN-XX/<GAME-ID>/
├── RELEASES/
│   └── <RELEASE-ID>/
├── PROJECTS/
│   └── <PROJECT-ID>/
└── SHARED/
```

Only these three ownership classes exist below a game.

### RELEASES

A release is an official target identity. Platform, package kind, region, language, revision, version, hashes, and dump observations are **metadata**, not extra path layers.

```text
GEN-XX/<GAME-ID>/RELEASES/<RELEASE-ID>/
├── manifest.json
├── research/
├── verification/
└── references/
```

Exact dump observations belong in the release manifest or a small `dumps/` registry. ROM image bytes are never committed.

### PROJECTS

All derived work owned by one project stays together.

```text
GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/
├── README.md
├── docs/
├── source/
├── data/
├── assets/
├── manifests/
├── tools/
├── tests/
└── verification/
```

Create only directories the project actually needs.

Analysis, reports, tables, comparisons, design notes, scripts, and references do **not** get competing top-level ownership roots. They live inside `docs/`, `data/`, `manifests/`, `tools/`, or another truthful project-local directory.

### SHARED

`SHARED/` is only for material genuinely owned by the game and reused by multiple releases/projects. It is not a miscellaneous folder.

## Generation-wide work

Only real generation-wide projects live here:

```text
GEN-XX/PROJECTS/<PROJECT-ID>/
GEN-XX/SHARED/
```

No generation-level `COMPARES`, `REFERENCES`, `KNOWLEDGE`, `VERIFY`, `CATALOGS`, `REPORTS`, `TABLES`, `ANALYSIS`, or `TOOLS` roots.

## Cross-generation work

```text
CROSS-GEN/<PROJECT-ID>/
├── README.md
├── docs/
├── data/
├── assets/
├── manifests/
├── tools/
├── tests/
└── verification/
```

`CROSS-GEN` is itself a project-owner space. There is no additional `PROJECTS/COMPARES/REFERENCES/SHARED` layer unless a future need is demonstrated.

## INFRA

```text
INFRA/
├── DOCS/
├── MANIFESTS/
├── TOOLS/
└── ARCHITECTURE/
```

INFRA contains repository-wide policy, schemas, validators, and tooling only. Game/project research does not belong here.

## Comparison and reference rule

Comparisons and references are relationships, not owners.

- A comparison owned by one project lives under that project's `docs/` or `data/`.
- A release comparison owned by the game lives under `SHARED/`.
- External references are recorded in manifests or `docs/references/` inside the owning release/project.

Do not create standalone `COMPARES/` or `REFERENCES/` ownership trees.

## Verification rule

Verification is evidence attached to an owner, not a global owner category.

Use the owning release/project's `verification/` directory and manifest fields. Do not create separate game-level `VERIFY/` ownership trees.

## Sakurai role

Sakurai remains the curated research/control repository. It keeps identity, provenance, analysis, comparisons, localization research, schemas, reports, citations, research tooling, and verification evidence that are worth curating.

The path coordinate must match Tsubaki whenever the same artifact exists in both repositories.

## ROM policy

Complete playable ROM image files are excluded. Metadata, hashes, manifests, documentation, source, scripts, patches, extracted/reconstructed assets, and verification evidence are eligible when appropriate to Sakurai's curated role.

## Migration principle

Do not migrate until this draft is accepted. When accepted, migrate owner-by-owner and verify each move before deleting the old live path. Git history remains the historical record.
