# GS Korean → Pocket Monsters — v4 path routing

This project follows the repository-wide v4 identity model. Original ROM binaries are never committed.

## 1. Original-release facts

Facts that describe one official ROM/build belong to `LIBRARY`, not to the project tree.

```text
LIBRARY/GEN-01/GB/<GAME>/RELEASES/<RELEASE-ID>/...
LIBRARY/GEN-01/GBC/<GAME>/RELEASES/<RELEASE-ID>/...
LIBRARY/GEN-02/GBC/<GAME>/RELEASES/<RELEASE-ID>/...
```

Examples: header metadata, per-release pointer maps, bank ownership, text-engine addresses, revision-only differences, checksum/provenance records.

## 2. Exact supplied-file observations

A specific uploaded/dumped file is a `DUMP`, not a new release:

```text
LIBRARY/.../RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/...
```

## 3. Cross-release research

Version/revision comparisons belong to:

```text
LIBRARY/.../COMPARISONS/<COMPARISON-ID>/...
```

Generation/platform-wide comparisons may use `_SHARED` as the game scope.

## 4. Project-owned research and design

```text
PROJECTS/GS-KOREAN-TO-POCKET-MONSTERS/
├── MANIFESTS/
├── CROSSWALK/
├── DESIGN/
├── IMPLEMENTATION/
├── VERIFICATION/
├── TOOLS/
└── REPORTS/
```

- `MANIFESTS`: source/target release locks and routing policy.
- `CROSSWALK`: Japanese/English source → modern Korean terminology mappings.
- `DESIGN`: Hangul engine, pointer relocation, UI, SRAM/name handling specifications.
- `IMPLEMENTATION`: research-side implementation specifications and target maps; distributable production assets remain in Tsubaki.
- `VERIFICATION`: round-trip, checksum, event, text, pointer, and UI verification evidence.
- `TOOLS`: extractors, decoders, diff tools, validators.
- `REPORTS`: source census, bank audits, translation audit reports.

## 5. Repository ownership contract

Sakurai owns analysis, reverse engineering, manifests, source maps, decoded research tables, specifications, tools, and verification evidence.

Tsubaki owns reusable fonts/graphics/assets, converted resources, build inputs, patches, generated insertion data, and final production artifacts.

Release IDs, dump IDs, project IDs, and target IDs must mean exactly the same thing in both repositories.
