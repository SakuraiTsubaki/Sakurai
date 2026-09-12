# Sakurai

Pokémon source identity, reverse engineering, comparison, localization research, technical design, and verification repository.

## Canonical path architecture: v8

```text
GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/...
GEN-XX/<GAME-ID>/TARGET/<TARGET-ID>/...
GEN-XX/<GAME-ID>/COMPARE/<COMPARISON-ID>/...
GEN-XX/<GAME-ID>/SHARED/...
GEN-XX/<GAME-ID>/REFERENCE/<REFERENCE-ID>/...

GEN-XX/TARGET/<TARGET-ID>/...       # same-generation, multi-game target only
GEN-XX/COMPARE/<COMPARISON-ID>/...  # same-generation, multi-game comparison only
GEN-XX/SHARED/...
GEN-XX/REFERENCE/<REFERENCE-ID>/...

CROSS-GEN/TARGET|COMPARE|SHARED|REFERENCE/...
INFRA/...
```

v8 is game-ownership-first. A single-game project is stored with its game instead of in a detached repository-wide project root. Generation-level and cross-generation branches are reserved for genuinely multi-game scopes.

`RELEASE-ID` is the canonical technical release/build identity. Language, market, revision, game/product/title code, version fields, hashes, and provenance remain explicit manifest data; they are not duplicated into extra path levels unless they are part of the registered release ID.

Sakurai owns identity, ROM/native structure, code, pointers, tables, text/data/event/map/system research, comparisons, crosswalks, technical specifications, citations, and verification evidence.

## GitHub upload policy

Only complete ROM binaries are excluded from GitHub. This includes original ROM images and modified/rebuilt ROM images.

All other project outputs are committed to GitHub under their truthful owner, including analysis, documentation, source code, scripts, tools, CSV/JSON/YAML/Markdown, manifests, hashes, comparison tables, logs, test and verification results, patches, build/reproduction metadata, extraction indexes, and other non-ROM artifacts.

See `STRUCTURE.md` and `MIGRATION.md`.