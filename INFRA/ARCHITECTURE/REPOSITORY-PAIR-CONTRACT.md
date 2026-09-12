# Sakurai ↔ Tsubaki Repository Pair Contract v4.1

Status: canonical for all new work.

## Canonical roots

Only these roots receive new project content:

- `LIBRARY/` — artifacts owned by an official release or a relationship between official releases.
- `PROJECTS/` — derived localization, modernization, port, integration, build, patch, and target work.
- `INFRA/` — shared schemas, registries, validators, migration maps, and repository-wide tooling.
- `.github/` and repository documentation.

`GAMES/`, `META/`, `GENERATION-*`, and standalone `GEN-*` roots are migration-only. New work must not be added there. A legacy root is deleted once every non-placeholder artifact under it has one canonical owner. Placeholder-only roots should be removed immediately.

## Identity hierarchy

```text
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/
├── RELEASES/<RELEASE-ID>/
│   ├── MANIFESTS/
│   └── DUMPS/<DUMP-ID>/...
├── COMPARISONS/<COMPARISON-ID>/...
└── SHARED/...
```

- `RELEASE-ID` identifies the official software/build.
- `DUMP-ID` identifies an exact observed file and its provenance/hash state.
- A bad, modified, overdumped, trimmed, incomplete, or otherwise non-canonical dump never creates a fake release.
- `COMPARISONS` owns relationships among releases of one game. Generation-wide comparisons use the reserved `_SHARED` game scope.
- `SHARED` is only for release-independent material.

## Project hierarchy

```text
PROJECTS/<PROJECT-ID>/
```

Project IDs and target IDs must resolve to canonical release identities through manifests/release locks. A project-produced localization must never masquerade as an official release.

## Repository responsibility

### Sakurai

Source of truth for:

- release and dump identity;
- manifests, hashes, provenance, registries;
- analysis, census, structure, data and text research;
- maps/events research;
- disassembly, symbols and reverse engineering;
- reproducible research tools, tests and verification;
- reports, crosswalks and technical design specifications.

### Tsubaki

Source of truth for:

- sprites, graphics, palettes, fonts, icons and tilesets;
- UI, title graphics and audio production assets;
- intentionally extracted and identified source assets;
- converted resources and format-normalized assets;
- patches, build inputs and generated implementation outputs;
- production tooling and production-side verification.

The same release ID, dump ID, project ID and target ID mean the same thing in both repositories.

## ROM-derived artifact rule

Original ROM/executable binaries are never committed. Arbitrary raw banks or unclassified ROM chunks are also not production assets.

ROM-derived material is routed as follows:

1. identity/hash/header/structure fact → Sakurai;
2. decoded table or reverse-engineering result → Sakurai;
3. cross-release comparison/deduplication evidence → Sakurai;
4. intentionally bounded source asset whose identity is verified → Tsubaki `LIBRARY`;
5. converted/project-produced asset → Tsubaki `PROJECTS`;
6. patch/build product → Tsubaki `PROJECTS`.

A bank survey may identify candidate asset ranges, but Tsubaki extraction requires per-asset boundary and format verification first.

## Migration invariant

Every live artifact has exactly one semantic owner. Do not retain duplicate live copies solely to preserve an obsolete path; Git history is the archive. Migration must preserve blob bytes when an artifact is only being re-homed.
