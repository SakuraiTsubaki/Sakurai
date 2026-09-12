# Repository Migration — v4

## Status

v4 is the canonical model. It replaces the v3 `GAMES/...` model before large-scale migration continues.

Legacy trees remain migration inputs only. New work must use `LIBRARY`, `PROJECTS`, or `INFRA` ownership.

## Canonical ownership

```text
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/RELEASES/<RELEASE-ID>/...
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/COMPARISONS/<COMPARISON-ID>/...
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/SHARED/...
PROJECTS/<PROJECT-ID>/...
INFRA/...
```

A release is one official software/build identity. A dump is one exact observed file attached below a release. A project consumes one or more releases and produces derived work.

## GB/GBC release IDs

GB/GBC release identity uses:

`<MARKET>-<LANGUAGE>-HV<HEADER-VERSION>`

Examples:

- `JP-JA-HV0`
- `JP-JA-HV1`
- `KR-KO-HV0`
- `US-EU-EN-HV0`
- `US-EU-EN-HV1`

Preservation-set labels such as Rev A, Rev 0A, Rev B/C/D are retained in manifests when they add human-readable provenance. The header version remains the canonical build discriminator in the release ID.

## Dump identity

Exact supplied files belong under:

`.../RELEASES/<RELEASE-ID>/DUMPS/<PROVENANCE>-<SHA1-PREFIX>/`

The dump manifest records original filename, complete hashes, size, source/provenance, preservation label, header observations, and quality/classification status. Duplicate identical files never create duplicate releases.

## GS Korean → Pokémon project

The current 23 supplied Generation I/II ROMs are registered in:

`INFRA/REGISTRY/ROM-SETS/GS-KOREAN-POKEMON-GEN1-GEN2-2026-09-12.yaml`

Important routing invariants:

- Korean Gold and Silver are real official source releases and belong in `LIBRARY`.
- No Korean Crystal source ROM is present in this source set; a Korean Crystal result is derived project output under `PROJECTS`, not a fabricated library release.
- Shared USA/Europe English ROMs use `US-EU-EN` release identity.
- Japanese Yellow revisions are separate official builds through their distinct header versions; preservation labels `Rev 0A/B/C/D` remain manifest metadata.
- GS Korean Gold/Silver may be implementation references for another target ROM without becoming that target game's source release.

## Migration invariant

Each artifact gets exactly one truthful owner:

- official release fact → `LIBRARY/.../RELEASES`
- exact supplied-file observation → `.../DUMPS`
- relationship between releases → `LIBRARY/.../COMPARISONS`
- derived translation/modernization/port → `PROJECTS/...`
- repository-wide catalog/schema/tool → `INFRA/...`

Do not keep duplicate live copies to preserve legacy paths. Git history and migration registries are the archive.
