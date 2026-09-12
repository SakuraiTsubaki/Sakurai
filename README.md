# Sakurai

Pokémon research, reverse-engineering, census, comparison, integration-design, and verification repository.

## Canonical path model: v5

New source research uses:

`LIBRARY/GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/...`

Exact supplied/observed images remain below `DUMPS/<DUMP-ID>/`; same-game comparisons use `<GAME-ID>/COMPARE/`; cross-game generation comparisons use `GEN-XX/COMPARE/`; derived modernization/port/integration work belongs under `PROJECTS/<PROJECT-ID>/`; repository-wide schemas and tooling belong under `INFRA/`.

Release identity is technical first. Market/language are manifest metadata when a stronger native or release-specific technical key exists. For the supplied Silver ROMs, observed stable header tokens produce `AAXJ-HV0`, `AAXJ-HV1`, `AAXE-HV0`, `AAXD-HV0`, `AAXF-HV0`, `AAXI-HV0`, `AAXS-HV0`, and `AAXK-HV0`.

**RELEASE and DUMP are different identities.** A modified, incomplete, bad, duplicate, or merely user-supplied image never becomes a fake official release.

Legacy `GAMES/`, `GENERATION-*`, standalone `GEN-*`, and old v4 platform-first `LIBRARY/GEN-XX/<PLATFORM>/...` trees are migration inputs only. Git history is the archive; new live work uses v5.

Sakurai is authoritative for identity, ROM/native structure research, semantic domain analysis, comparisons, design evidence, and verification. Tsubaki uses the same IDs for production assets and implementation outputs.

Original ROM/executable binaries are never stored in this repository.
