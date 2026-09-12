# Sakurai ↔ Tsubaki Repository Pair Contract v7

Status: **canonical for all new work** as of 2026-09-12.

## Canonical roots

New work is written only to generation-first owners:

```text
GEN-XX/
CROSS-GEN/
INFRA/
```

The former top-level `LIBRARY/`, `PROJECTS/`, and `LEGACY/` roots are retired. Pre-v7 quarantine, when still required, lives only under `INFRA/QUARANTINE/PRE-V7/` and receives no new work.

## Official source identity

```text
GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

- `RELEASE-ID` identifies the official software/build identity.
- `DUMP-ID` identifies an exact observed image under that release.
- Bad/modified/trimmed/overdumped/incomplete observations never create fake releases.
- Platform, package, market, language, revision, product/title ID, hashes, and provenance are explicit manifest fields.

## Derived targets

```text
GEN-XX/TARGET/<TARGET-ID>/
CROSS-GEN/TARGET/<TARGET-ID>/
```

Target IDs must resolve to exact source release/dump locks through manifests. A project-produced localization, modernization, port, integration, or rebuild must never masquerade as an official `SOURCE` release.

## Relationships

- same-game relation → `GEN-XX/<GAME-ID>/COMPARE/<COMPARISON-ID>/`
- same-generation cross-game relation → `GEN-XX/COMPARE/<COMPARISON-ID>/`
- cross-generation relation → `CROSS-GEN/COMPARE/<COMPARISON-ID>/`
- identity-independent reusable material → matching `SHARED/`
- external/secondary material → matching `REFERENCE/`

## Repository responsibility

### Sakurai

Source of truth for:

- release and dump identity;
- hashes, provenance, registries and manifests;
- ROM/native structure, banks, pointers, tables, code and symbols;
- text/data/event/map/system research;
- comparisons, crosswalks and technical design;
- reproducible research tools, tests, citations and verification evidence.

### Tsubaki

Source of truth for:

- verified extracted source assets;
- sprites, graphics, palettes, fonts, icons, tilesets, UI and audio production resources;
- normalized and converted resources;
- implementation inputs and generated implementation artifacts;
- patches, build recipes/results, catalogs and production-side verification.

The same `GEN-XX`, `GAME-ID`, `PLATFORM-ID`, `PACKAGE-KIND`, `RELEASE-ID`, `DUMP-ID`, `TARGET-ID`, `COMPARISON-ID`, reference ID, and shared-resource ID mean the same thing in both repositories.

## ROM-derived artifact rule

Original ROM/executable binaries are never committed. Arbitrary unclassified raw banks/chunks are not production assets.

1. identity/hash/header/native-structure fact → Sakurai `SOURCE`;
2. decoded table/reverse-engineering result → Sakurai `SOURCE`;
3. relationship/deduplication evidence → Sakurai `COMPARE`;
4. bounded verified source asset → Tsubaki `SOURCE`;
5. target-produced/converted asset → Tsubaki `TARGET`;
6. patch/build product → Tsubaki `TARGET`.

## Migration invariant

Every live artifact has exactly one semantic owner. Path-only migration preserves blob bytes. Duplicate live copies are not retained merely to preserve obsolete paths; Git history is the permanent archive.
