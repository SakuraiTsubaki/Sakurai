# Repository layout v3 — Sakurai / GSCRGBY

Status: canonical project layout proposal — 2026-09-13.

`projects/gscrgby/` is the public, reproducible side of GSCRGBY. Repository-global `GEN-XX/` and `CROSS-GEN/` remain canonical for non-GSCRGBY material, but **new GSCRGBY work does not go there**.

## 1. Public project tree

```text
projects/gscrgby/
├── engine/
│   └── gen1/
│       ├── asm/
│       ├── data/
│       └── formats/
├── sources/
│   ├── gen1/
│   │   ├── red/
│   │   ├── green/
│   │   ├── blue/
│   │   └── yellow/
│   └── gen2/
│       ├── gold/
│       ├── silver/
│       └── crystal/
├── integration/
│   ├── maps/
│   ├── tilesets/
│   ├── blocks/
│   ├── objects/
│   ├── warps/
│   ├── events/
│   ├── scripts/
│   ├── text/
│   └── localization/
├── patches/
├── manifests/
│   ├── roms/
│   ├── sources/
│   └── promotion/
├── tools/
│   ├── extract/
│   ├── convert/
│   └── validate/
├── tests/
└── docs/
```

Directories are created only when they contain material; this document defines ownership, not empty placeholders.

## 2. What belongs in Sakurai

Sakurai receives only material that is safe to publish and reproducible without committing a commercial ROM image:

- portable source or data definitions used by the Gen I target engine;
- normalized RGBY/GSC source descriptors with stable schemas;
- conversion and validation tools;
- distributable IPS/BPS or equivalent delta patches;
- tests and non-ROM fixtures;
- public ROM fingerprints, source locks, and build manifests;
- promoted map/tileset/block/object/warp/event/script/text/localization data;
- design documents that no longer depend on private exploratory notes.

Never commit `.gb`, `.gbc`, full ROM dumps, or build outputs that contain unmodified commercial ROM data.

## 3. Tsubaki → Sakurai promotion contract

Private evidence lives first in `SakuraiTsubaki/Tsubaki/workspaces/gscrgby/`. A result is promoted only when all four gates are satisfied:

1. **Input identity** — exact ROM/repository fingerprint is recorded.
2. **Transform** — extraction/conversion steps are documented or scripted.
3. **Stable schema** — output format and semantic ownership are fixed.
4. **Validation** — a test, comparison, checksum, or reproducibility report passes.

Promotion destinations:

```text
Tsubaki/workspaces/gscrgby/reference/roms
  -> Sakurai/projects/gscrgby/manifests/roms

Tsubaki/workspaces/gscrgby/reference/layouts
  -> Sakurai/projects/gscrgby/sources/<generation>/<game>/formats

Tsubaki/workspaces/gscrgby/extraction/<generation>/<game>
  -> Sakurai/projects/gscrgby/sources/<generation>/<game>

Tsubaki/workspaces/gscrgby/analysis/kanto
  -> Sakurai/projects/gscrgby/integration

Tsubaki/workspaces/gscrgby/analysis/localization
  -> Sakurai/projects/gscrgby/integration/localization

Tsubaki/workspaces/gscrgby/experiments
  -> no automatic destination; promote only after the four gates pass
```

## 4. Source-repository rule

A dedicated source repository stays canonical for its own implementation. GSCRGBY does not vendor an entire disassembly merely to use it as evidence.

For example, `SakuraiTsubaki/pokegold-kr` remains the implementation/disassembly source for Korean Gold/Silver. GSCRGBY stores an exact commit lock plus promoted, project-specific formats/data/tools. Private offset/bank research stays in Tsubaki until promoted.

## 5. Legacy cutover

For GSCRGBY only:

```text
GEN-01/...   -> migration source; frozen for new GSCRGBY additions
GEN-02/...   -> migration source; frozen for new GSCRGBY additions
CROSS-GEN/...-> migration source; frozen for new GSCRGBY additions
```

Migrate verified content into `projects/gscrgby/` by semantic owner. Delete duplicate legacy copies only in a dedicated cleanup PR after path-equivalence tests pass.

## 6. Naming rules

- path segments are lowercase descriptive nouns inside the project tree;
- game directories use `red`, `green`, `blue`, `yellow`, `gold`, `silver`, `crystal`;
- technical release/dump IDs remain in manifests rather than being invented as project directory names;
- avoid `misc`, `other`, `general`, `all`, `multi`, `unknown`, or similar catch-all owner directories.
