# Sakurai

Pokémon research, reverse-engineering, census, comparison, integration-design, and verification repository.

## Canonical path model: v4

Active work is divided by responsibility rather than by one universal game/locale/revision chain:

- `LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/RELEASES/<RELEASE-ID>/...` — facts owned by one exact official software build
- `.../DUMPS/<DUMP-ID>/...` — observations tied to one exact supplied/observed ROM or executable image
- `LIBRARY/.../COMPARISONS/<COMPARISON-ID>/...` — relationships among official releases
- `PROJECTS/<PROJECT-ID>/...` — modernization, ports, integrations, cross-generation work, and target-specific implementation specifications
- `INFRA/...` — release registries, schemas, validators, migration maps, and repository-wide tooling

**RELEASE and DUMP are different identities.** A bad, incomplete, modified, or duplicate dump never becomes a fake official release.

Legacy `GAMES/`, `GENERATION-*`, standalone `GEN-*`, `META/`, `MULTI`, and `REV-ALL` paths are migration sources only. New work must use v4.

Sakurai and Tsubaki share the same release IDs, project IDs, and target IDs. See `STRUCTURE.md` and `MIGRATION.md` before routing new material.

Original ROM/executable binaries are never stored in this repository.
