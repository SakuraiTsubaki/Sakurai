# Sakurai ↔ Tsubaki Repository Pair Contract v8

Status: **canonical redesign candidate**, 2026-09-12.

## Shared identity grammar

```text
GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
GEN-XX/<GAME-ID>/TARGET/<TARGET-ID>/
GEN-XX/<GAME-ID>/COMPARE/<COMPARISON-ID>/
GEN-XX/<GAME-ID>/SHARED/
GEN-XX/<GAME-ID>/REFERENCE/<REFERENCE-ID>/
```

Same-generation multi-game work may use `GEN-XX/TARGET|COMPARE|SHARED|REFERENCE`. Cross-generation work uses `CROSS-GEN/TARGET|COMPARE|SHARED|REFERENCE`.

Both repositories use identical generation, game, platform, package, release, dump, target, comparison, reference, and resource identifiers.

## Sakurai responsibility

- release/dump identity, hashes and provenance
- ROM/native structure, banks, pointers, tables, code and symbols
- text/data/event/map/system research
- comparisons and crosswalks
- technical design/specification
- reproducible research tooling
- citations and verification evidence

## Tsubaki responsibility

- verified extracted source assets
- sprites, graphics, palettes, fonts, icons, tilesets, UI and audio production resources
- normalized and converted resources
- implementation inputs and generated implementation artifacts
- patches, build recipes/results and production catalogs
- production-side verification

## Routing invariant

1. official release fact → game `SOURCE`
2. exact observed dump → release `DUMPS/<DUMP-ID>`
3. single-game derived work → game `TARGET/<TARGET-ID>`
4. same-generation multi-game derived work → generation `TARGET/<TARGET-ID>`
5. cross-generation derived work → `CROSS-GEN/TARGET/<TARGET-ID>`
6. comparisons follow the same scope rule
7. reusable identity-independent material → matching `SHARED`
8. external secondary material → matching `REFERENCE`
9. repository-wide rule/tool/schema → `INFRA`

Original ROM/executable binaries are never committed. Path-only migration preserves blob bytes. Every live artifact has exactly one semantic owner; Git history is the archive.