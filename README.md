# Sakurai

Pokémon research, reverse-engineering, census, comparison, verification, and documentation repository.

## Canonical path model: v3

All active game data lives under `GAMES/GEN-XX/<GAME-ID>/`.

- `RELEASES/<RELEASE-ID>/<WORK-TYPE>/...` — one exact official build per immutable release ID
- `COMPARISONS/<COMPARISON-ID>/<WORK-TYPE>/...` — relationships across releases
- `PROJECTS/<PROJECT-ID>/COMMON/<WORK-TYPE>/...`
- `PROJECTS/<PROJECT-ID>/TARGETS/<TARGET-ID>/<WORK-TYPE>/...`
- `SHARED/<WORK-TYPE>/...` — genuinely release-independent material

Locale, region, platform, revision/update version, hashes, and provenance are release metadata rather than universal path levels.

Pre-v3 trees are frozen under `META/MIGRATION-SNAPSHOTS/`. New work must not recreate `GENERATION-*` or standalone `GEN-*` roots.

See `STRUCTURE.md` and `MIGRATION.md` before routing files. ROM binaries and copyrighted original game images are not stored here.
