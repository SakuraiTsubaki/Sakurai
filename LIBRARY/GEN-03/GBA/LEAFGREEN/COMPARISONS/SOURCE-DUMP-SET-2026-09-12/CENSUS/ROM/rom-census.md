# Pokémon LeafGreen source ROM census — 2026-09-12

Seven supplied 16 MiB GBA images were inspected directly. No ROM binary is committed.

| Release | Market | Language | Header ver | SHA-1 | Header checksum |
|---|---|---|---:|---|---|
| `BPGD-R0` | Germany | German | 0 | `0802d1fb185ee3ed48d9a22afb25e66424076dac` | valid |
| `BPGE-R0` | USA | English | 0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | valid |
| `BPGE-R1` | Europe | English | 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | valid |
| `BPGF-R0` | France | French | 0 | `4b5758c14d0a07b70ef3ef0bd7fa5e7ce6978672` | valid |
| `BPGI-R0` | Italy | Italian | 0 | `a1dfea1493d26d1f024be8ba1de3d193fcfc651e` | valid |
| `BPGJ-R0` | Japan | Japanese | 0 | `5946f1b59e8d71cc61249661464d864185c92a5f` | valid |
| `BPGS-R0` | Spain | Spanish | 0 | `f9ebee5d228cb695f18ef2ced41630a09fa9eb05` | valid |

## Structural findings

- Every source is exactly 16,777,216 bytes (256 × 64 KiB banks).
- All seven GBA header checksums validate.
- `BPGE-R0` and `BPGE-R1` are one English game-code lineage separated by header version.
- Pairwise byte identity is recorded separately from release identity; similar binaries are not collapsed into one release.
- The English R0/R1 pair has 142 exactly identical 64 KiB banks, the largest same-position exact-bank count among this seven-ROM set.
- ROM filenames are dump provenance only. Canonical v4 release identity is header-native `<GAME-CODE>-R<HEADER-VERSION>`.

## Repository split

- Sakurai: release/dump identity, census, reverse engineering, comparisons, verification.
- Tsubaki: production-oriented asset indices, deduplication inputs, converters, patches, and build outputs.
