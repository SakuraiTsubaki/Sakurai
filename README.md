# Sakurai

Pokémon research, reverse-engineering, census, comparison, verification, localization, and documentation repository.

## Canonical path model: v4

The repository separates **official release identity**, **exact observed dumps**, and **derived projects**.

```text
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/RELEASES/<RELEASE-ID>/...
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/COMPARISONS/<COMPARISON-ID>/...
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/SHARED/...
PROJECTS/<PROJECT-ID>/...
INFRA/...
```

- `LIBRARY` owns facts about original official releases and exact supplied/observed dumps.
- `PROJECTS` owns localization, modernization, ports, integrations, rebuilds, patches, and project-specific verification.
- `INFRA` owns repository-wide release registries, ROM-set catalogs, schemas, validators, migration maps, shared tooling, and CI support.

For GB/GBC, release IDs use market/language plus the header version, for example `JP-JA-HV0`, `KR-KO-HV0`, and `US-EU-EN-HV1`. Exact uploaded files are tracked separately under `DUMPS/<DUMP-ID>` with hashes and provenance.

See `STRUCTURE.md` and `MIGRATION.md`. The current Generation I/II GS Korean project source set is registered under `INFRA/REGISTRY/ROM-SETS/`.

Original ROM/executable binaries are never committed.
