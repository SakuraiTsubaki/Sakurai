# Repository Structure v9

Status: **canonical redesign proposal** — 2026-09-13.

Sakurai is the **reference and specification repository** for the RGBY → GSC Kanto restoration project. It answers **what is true in the source games and what the restored Kanto must preserve**. It does not own build outputs, extracted copyrighted assets, patches, or implementation binaries.

## 1. Canonical roots

```text
catalog/
research/
spec/
schemas/
docs/
```

Generation is metadata and a research sub-axis, not the top-level ownership model. New canonical work must not be rooted under `GEN-01/`, `GEN-02/`, `CROSS-GEN/`, `LIBRARY/`, or `PROJECTS/`.

## 2. catalog — source identity

```text
catalog/
└── roms/
    ├── manifest.json
    └── README.md
```

The ROM catalog stores identifiers, filenames, cryptographic hashes, sizes, and header facts needed to identify local source images. **ROM binaries are never committed.**

Stable logical ROM IDs are shared with Tsubaki. A logical ID identifies one exact source release/dump used by the project.

## 3. research — observed facts

```text
research/
├── gen1/
│   └── kanto/
│       ├── geography/
│       ├── maps/
│       ├── connections/
│       ├── facilities/
│       ├── dungeons/
│       ├── events/
│       └── version-differences/
├── gen2/
│   └── kanto/
│       ├── geography/
│       ├── maps/
│       ├── connections/
│       ├── facilities/
│       ├── dungeons/
│       ├── events/
│       ├── systems/
│       └── version-differences/
└── comparisons/
    └── kanto/
```

`research/` contains facts and measurements derived from legitimate local source analysis: dimensions, coordinates, connection graphs, event inventories, behavior notes, checksums, and comparison results. Large/raw copyrighted asset dumps stay local and are not repository content.

## 4. spec — restoration contract

```text
spec/
└── kanto/
    ├── README.md
    ├── geography/
    ├── connections/
    ├── facilities/
    ├── dungeons/
    ├── events/
    ├── trainers/
    ├── encounters/
    └── localization/
```

The project invariant is:

> **Space and geography follow Generation I; era, engine, and systems follow Generation II.**

The specification records the desired restored result without embedding implementation details from Tsubaki.

## 5. schemas — shared machine contracts

```text
schemas/
├── rom-manifest.schema.json
├── map-observation.schema.json
├── connection.schema.json
└── event-inventory.schema.json
```

Schemas define portable data contracts. Tsubaki may consume them but Sakurai remains authoritative for the reference schema definitions.

## 6. docs — architecture and decisions

```text
docs/
├── architecture/
│   ├── REPOSITORY_BOUNDARY.md
│   └── MIGRATION_V9.md
└── decisions/
```

Architecture decisions belong here. Historical v8 paths remain in Git history and are migration inputs, not destinations for new work.

## 7. Sakurai ↔ Tsubaki boundary

Sakurai owns:

- exact ROM identity catalog and checksums
- observed Gen I / Gen II facts and comparisons
- Kanto restoration requirements and acceptance criteria
- canonical schemas and naming rules
- verification expectations

Tsubaki owns:

- local-ROM scanners and extractors
- normalization and conversion tools
- implementation source
- generated intermediate data
- tests, builds, patches, and packaging

The two repositories share stable logical IDs and schema versions. They do **not** mirror the same directory tree.

## 8. Source-material rule

Never commit original ROM images or bulk/raw extracted copyrighted graphics, audio, text, or map dumps. Store source images under Tsubaki's ignored local input directory and regenerate derived implementation inputs locally.

## 9. Project-specific routing

```text
catalog/roms/manifest.json
research/gen1/kanto/maps/pallet-town/
research/gen2/kanto/maps/pallet-town/
research/comparisons/kanto/pallet-town/
spec/kanto/geography/pallet-town/
spec/kanto/events/pallet-town/
```

This makes the restored Kanto itself the stable domain while generation/version differences become evidence feeding the specification.