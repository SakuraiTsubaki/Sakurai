# Pokémon Gold — v3 canonical root

This directory is the canonical v3 home for the currently audited Pokémon Gold source ROM set.

## Branches

```text
GAMES/GEN-02/GOLD/
  RELEASES/       exact official source builds
  COMPARISONS/    cross-release / cross-revision research
  PROJECTS/       modernization, localization, rebuild, expansion
  SHARED/         genuinely release-independent Gold material
```

Original ROM binaries are never committed.

## Audited exact releases

| Release ID | Source label | Header code | Rev | Size | 16 KiB banks | CGB flag |
|---|---|---:|---:|---:|---:|---:|
| `GBC-JP-JA-AAUJ-REV-0` | Pocket Monsters Kin (Japan) | AAUJ | 0 | 1 MiB | 64 | 0x80 |
| `GBC-JP-JA-AAUJ-REV-A` | Pocket Monsters Kin (Japan) (Rev A) | AAUJ | 1 | 1 MiB | 64 | 0x80 |
| `GBC-US-EU-EN-AAUE-REV-0` | Pokemon - Gold Version (USA, Europe) | AAUE | 0 | 2 MiB | 128 | 0x80 |
| `GBC-EU-DE-AAUD-REV-0` | Pokemon - Goldene Edition (Germany) | AAUD | 0 | 2 MiB | 128 | 0x80 |
| `GBC-EU-FR-AAUF-REV-0` | Pokemon - Version Or (France) | AAUF | 0 | 2 MiB | 128 | 0x80 |
| `GBC-EU-IT-AAUI-REV-0` | Pokemon - Versione Oro (Italy) | AAUI | 0 | 2 MiB | 128 | 0x80 |
| `GBC-EU-ES-AAUS-REV-0` | Pokemon - Edicion Oro (Spain) | AAUS | 0 | 2 MiB | 128 | 0x80 |
| `GBC-KR-KO-AAUK-REV-0` | Pocket Monsters Geum (Korea) | AAUK | 0 | 2 MiB | 128 | 0xC0 |

The exact hashes/checksums are recorded in `RELEASES/catalog.json`.

## Canonical routing examples

Source-only Korean ROM analysis:

`GAMES/GEN-02/GOLD/RELEASES/GBC-KR-KO-AAUK-REV-0/ANALYSIS/...`

Japanese revision comparison:

`GAMES/GEN-02/GOLD/COMPARISONS/GBC-JP-JA-AAUJ-REV-0--GBC-JP-JA-AAUJ-REV-A/DIFFS/...`

All-release ROM census:

`GAMES/GEN-02/GOLD/COMPARISONS/ALL-8-AUDITED-RELEASES/CENSUS/...`

Korean modernization work:

`GAMES/GEN-02/GOLD/PROJECTS/MODERNIZATION/TARGETS/KR-KO-MODERN/...`

Its project/target manifest must identify `GBC-KR-KO-AAUK-REV-0` as the original base for work derived from the Korean retail ROM.

## Legacy migration rule

`GENERATION-II/GOLD/...` is now a legacy source tree. Do not add new work there.

Do not bulk-move `GENERATION-II/GOLD/KR-KO/REV-0/ANALYSIS`: it mixes direct source-ROM research with modernization/official-name replacement work. Classify each artifact first, then move it into `RELEASES`, `COMPARISONS`, `PROJECTS`, or `SHARED`.
