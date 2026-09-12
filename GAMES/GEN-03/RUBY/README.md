# Pokémon Ruby — canonical v3 routing

This game root is based on the currently uploaded and locally verified Pokémon Ruby source ROM set.

Original ROM binaries are read-only source material and are **not** committed to GitHub. GitHub stores only release identities, hashes, manifests, analysis, source maps, tools, patches, extracted/derived assets, and verification results.

## Canonical release IDs

| Release ID | Source file identity | Game code | Header rev | Build |
|---|---|---:|---:|---|
| `GBA-JP-JA-AXVJ-REV-0` | Pocket Monsters - Ruby (Japan) | AXVJ | 0 | Retail |
| `GBA-US-EN-AXVE-REV-0` | Pokemon - Ruby Version (USA) | AXVE | 0 | Retail |
| `GBA-EU-EN-AXVE-REV-1` | Pokemon - Ruby Version (Europe) (Rev 1) | AXVE | 1 | Retail |
| `GBA-US-EU-EN-AXVE-REV-2` | Pokemon - Ruby Version (USA, Europe) (Rev 2) | AXVE | 2 | Retail |
| `GBA-EU-DE-AXVD-REV-0` | Pokemon - Rubin-Edition (Germany) | AXVD | 0 | Retail |
| `GBA-EU-DE-AXVD-REV-0-DEBUG` | Pokemon - Rubin-Edition (Germany) (Debug Version) | AXVD | 0 | Debug |
| `GBA-EU-DE-AXVD-REV-1` | Pokemon - Rubin-Edition (Germany) (Rev 1) | AXVD | 1 | Retail |
| `GBA-EU-FR-AXVF-REV-0` | Pokemon - Version Rubis (France) | AXVF | 0 | Retail |
| `GBA-EU-FR-AXVF-REV-1` | Pokemon - Version Rubis (France) (Rev 1) | AXVF | 1 | Retail |
| `GBA-EU-IT-AXVI-REV-0` | Pokemon - Versione Rubino (Italy) | AXVI | 0 | Retail |
| `GBA-EU-IT-AXVI-REV-1` | Pokemon - Versione Rubino (Italy) (Rev 1) | AXVI | 1 | Retail |
| `GBA-EU-ES-AXVS-REV-0` | Pokemon - Edicion Rubi (Spain) | AXVS | 0 | Retail |
| `GBA-EU-ES-AXVS-REV-1` | Pokemon - Edicion Rubi (Spain) (Rev 1) | AXVS | 1 | Retail |

Each exact source build belongs under:

`GAMES/GEN-03/RUBY/RELEASES/<RELEASE-ID>/<WORK-TYPE>/...`

Cross-release work belongs under:

`GAMES/GEN-03/RUBY/COMPARISONS/<COMPARISON-ID>/<WORK-TYPE>/...`

The replacement for legacy `MULTI/REV-ALL` is normally:

`GAMES/GEN-03/RUBY/COMPARISONS/ALL-RELEASES/<WORK-TYPE>/...`

Modernization and other derived work belongs under:

`GAMES/GEN-03/RUBY/PROJECTS/<PROJECT-ID>/COMMON/<WORK-TYPE>/...`
`GAMES/GEN-03/RUBY/PROJECTS/<PROJECT-ID>/TARGETS/<TARGET-ID>/<WORK-TYPE>/...`

## Source coverage note

The current uploaded set contains 13 verified ROMs: 12 retail builds and one German debug build. A Japanese Rev 1 retail build is known externally but is not present in the current project source set; no live release directory is created for it until that ROM is supplied and verified.

## Legacy migration

Do not add new work under `GENERATION-III/RUBY/MULTI/REV-ALL/...`.

Route release-specific facts to `RELEASES`, multi-ROM audits/diffs to `COMPARISONS`, derived modernization work to `PROJECTS`, and only genuinely release-independent material to `SHARED`.
