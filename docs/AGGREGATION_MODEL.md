# Aggregation Model

Sakurai and Tsubaki are not independent repository families that merely imitate the Disassembly or Decompilation repositories. They are aggregate repositories produced from both upstream series.

## Source equation

```text
Disassembly series + Decompilation series
                     ↓
          shared upstream universe
                ↙           ↘
           Sakurai         Tsubaki
```

The current upstream universe contains **46 repositories**:

- **12 Disassembly repositories** — Generations I–III
- **34 Decompilation repositories** — Generations III–X

The authoritative list is maintained in [`../manifests/upstream-repositories.json`](../manifests/upstream-repositories.json).

## Sakurai projection

Sakurai is the curated research/control projection of the combined upstream universe.

From both repository series it aggregates material such as:

- target/release/revision identity
- provenance and hashes
- reverse-engineering analysis
- architecture and format research
- comparisons and localization research
- symbol/address/offset knowledge
- verification evidence
- manifests and inventories needed to support claims
- research tooling and reproducibility documentation

A source repository remains the provenance origin. Aggregation must not erase which Disassembly or Decompilation repository produced a record.

## Tsubaki projection

Tsubaki is the complete eligible non-ROM production/archive projection of the same combined upstream universe.

From both repository series it aggregates all eligible project material, including:

- reconstructed/disassembled/decompiled source
- structured data
- graphics, sprites, PNG previews, palettes, fonts, maps, text, and audio
- extraction/conversion/repacking/rebuild tools
- manifests, inventories, hashes, and provenance
- tests, logs, intermediate outputs, and reproducible generated material
- research material needed to understand or verify an artifact

Complete playable ROM images remain excluded.

## Identity rule

Every aggregated item should retain enough source identity to answer:

1. Which upstream family produced it: `disassembly` or `decompilation`?
2. Which exact upstream repository produced it?
3. Which game/target/version/revision does it describe?
4. Has an equivalent item already been aggregated from the other series?
5. If deduplicated, where is the representative item and what verified identity proves equivalence?

## Tree rule

The central repositories must be able to represent the **union** of both upstream families without forcing one family into the other family's internal implementation layout.

Therefore:

- root-level operating files (`README.md`, `docs/`, `manifests/`, `.github/`, contribution/config files) are shared;
- imported project material must preserve upstream repository identity in metadata and manifests;
- common artifact classes may be normalized when semantics are truly shared;
- family-specific source layouts remain intact when normalization would lose information;
- deduplication requires verified byte/hash identity or another documented equivalence test;
- no V-numbered repository architecture is the source of truth.

## Migration principle

Existing `GEN-*`, `CROSS-GEN`, and `INFRA` material is migration input. It should be retained, normalized, or relocated only after it can be mapped back to one or more of the 46 upstream repositories or to genuine cross-series infrastructure.

The target state is simple: if the two upstream series are combined and projected according to the rules above, the result must be Sakurai and Tsubaki.
