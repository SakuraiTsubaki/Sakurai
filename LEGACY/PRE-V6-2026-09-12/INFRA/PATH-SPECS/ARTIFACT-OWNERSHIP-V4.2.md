# Repository pair artifact ownership — v4.2

Status: canonical clarification layered on Repository Structure v4. It does not replace the v4 identity spine; it makes the Sakurai/Tsubaki ownership split and artifact lifecycle explicit.

## Identity stays shared

Both repositories MUST use the same `GEN-XX`, platform, `GAME-ID`, `RELEASE-ID`, `DUMP-ID`, `COMPARISON-ID`, `PROJECT-ID`, and `TARGET-ID`. Moving an artifact between responsibility classes never changes its identity.

## Repository responsibilities

### Sakurai — evidence, meaning, reproducibility

Owns authoritative release/dump identity, hashes, provenance, ROM/header observations, reverse engineering, structural maps, data/text/event/map interpretation, symbol/disassembly work, cross-release factual comparison, research scripts, test definitions, and verification evidence.

Canonical release domains include:

`MANIFESTS`, `DUMPS/*/MANIFESTS`, `ANALYSIS`, `STRUCTURE`, `DATA`, `TEXT`, `MAPS`, `EVENTS`, `DISASSEMBLY`, `SYMBOLS`, `TOOLS`, `TESTS`, `VERIFICATION`, `REPORTS`.

### Tsubaki — production assets and implementation

Owns extracted production assets, normalized/converted resources, asset deduplication, build inputs, target implementation, patches, generated outputs, and production verification.

Canonical release domains include:

`MANIFESTS` (binding mirror only), `DUMPS/*/<ASSET-DOMAIN>`, `SPRITES`, `GRAPHICS`, `PALETTES`, `FONTS`, `ICONS`, `TILESETS`, `UI`, `AUDIO`, `TITLE`, `CONVERTED`, `TOOLS`, `VERIFICATION`.

Canonical project domains include:

`SOURCE`, `CONVERTED`, `IMPLEMENTATION`, `PATCHES`, `BUILD`, `TOOLS`, `VERIFICATION`.

## Artifact lifecycle

1. **OBSERVED** — exact property of one supplied file. Owner: Sakurai dump node.
2. **EXTRACTED** — asset bytes/decoded resource obtained from one dump but not yet proven release-representative. Owner: Tsubaki dump node.
3. **VERIFIED-RELEASE** — evidence shows the fact/asset represents the release. Promote to the corresponding release-level domain.
4. **CROSS-RELEASE** — equality/delta/dedup spanning releases. Owner: `COMPARISONS/<COMPARISON-ID>` in the repository responsible for that artifact type.
5. **DERIVED** — modernization, localization, port, expansion, patch, or build product. Owner: `PROJECTS/<PROJECT-ID>`; never `LIBRARY`.

## No duplicate live ownership

A generated artifact gets one canonical live owner. The other repository may contain a small manifest/reference pointing to that owner, but not a second authoritative copy. Git history is the archive for old paths.

## ROM binaries

Original ROM/executable binaries are read-only local inputs and MUST NOT be committed. Hashes, provenance, structural measurements, legal metadata, scripts, and independently generated/converted assets may be tracked according to repository policy.