# Sakurai / Tsubaki ROM artifact routing contract

Canonical path architecture: v4.

## Sakurai = source of truth for what the ROM is

Route here when the artifact answers **what exists in the original build, where it is, how it behaves, or how releases differ**.

### Original release ownership

`LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/RELEASES/<RELEASE-ID>/`

Use the following domains:

- `MANIFESTS` — release identity, exact observed dump bindings, hashes, provenance
- `ANALYSIS` — reverse-engineering findings and semantic interpretation
- `STRUCTURE` — ROM layout, banks, sections, NitroFS/NARC/file-system structure, pointer topology
- `DATA` — normalized original tables and parameter catalogs
- `TEXT` — text indexes, encodings, pointer maps, message catalogs
- `DISASSEMBLY` / `SYMBOLS` — code maps, symbols, functions, references
- `MAPS` / `EVENTS` — original map/event/script structures
- `GRAPHICS` / `AUDIO` — structural catalogs, format analysis, dimensions, frame/palette/audio metadata, content hashes; not bulk redistributed raw assets by default
- `TOOLS` — extraction/audit/rebuild verification tools
- `VERIFICATION` — lossless round-trip tests, checksums, behavior checks

### Comparisons

`LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/COMPARISONS/<COMPARISON-ID>/`

Only derived relationships belong here: revision diffs, Black/White differences, dedup matrices, localization deltas, normalized equivalence maps.

### Cross-generation project research

`PROJECTS/GEN5-TO-POCKET-MONSTERS/`

Sakurai owns:

- `MANIFESTS`
- `CROSSWALK`
- `DESIGN`
- `VERIFICATION`
- research-side `TOOLS`
- `REPORTS`

A port/conversion specification is project-owned even when it was discovered while studying one source generation.

## Tsubaki = source of truth for what we build from the ROM

Route here when the artifact is directly consumed by production or build steps.

Canonical project root:

`PROJECTS/GEN5-TO-POCKET-MONSTERS/`

### Shared implementation

`IMPLEMENTATION/_SHARED/`

Use for source-normalized conversion rules, shared transformed resources, generated cross-target tables, common converters, and common build metadata.

### Target implementation

`IMPLEMENTATION/<TARGET-ID>/`

Each target owns its own:

- `MANIFESTS`
- `SPRITES`
- `GRAPHICS`
- `PALETTES`
- `FONTS`
- `ICONS`
- `TILESETS`
- `UI`
- `AUDIO`
- `DATA`
- `CONVERTED`
- `PATCHES`
- `BUILD`
- production-side `TOOLS`
- verification output needed by the build

Every target manifest resolves to exactly one original release in Sakurai's canonical library.

## ROM-derived payload rule

Original ROM binaries are never committed to either repository.

Exact supplied files are represented by hash/provenance manifests. Bulk unmodified copyrighted graphics/audio extracted from ROMs are not the default Git payload; they should be reproducibly extracted locally from the locked input and only transformed/project-facing outputs, fingerprints, indexes, converters, patches, and manifests are committed unless a specific asset has a separate redistribution basis.

## Decision test

- "What is this byte/table/archive/function in the original ROM?" -> Sakurai.
- "How do two official releases differ?" -> Sakurai.
- "How should Gen V behavior map onto the target engine?" -> Sakurai project `CROSSWALK` / `DESIGN`.
- "What exact converted sprite/table/patch/build input will be inserted?" -> Tsubaki.
- "What file can regenerate that converted asset from the user's local ROM?" -> Tsubaki production `TOOLS`, with original structure references pointing back to Sakurai.

Never duplicate an artifact just to make both repositories look symmetrical. Mirror identity, not payload responsibility.
