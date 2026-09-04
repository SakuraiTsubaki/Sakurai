# Pokémon Emerald multi-language ROM census

Generated from project-local ROM inputs. **ROM binaries are intentionally not included in this repository.**

- Uploaded files: **7**
- Unique binaries by SHA-256: **6**
- Duplicate groups: **1**

## Inventory

| Language | Game code | Size | Version | Header checksum | SHA-256 | File |
|---|---:|---:|---:|---|---|---|
| Japanese | `BPEJ` | 16,777,216 | 0 | OK (`6D`) | `33f5610b9186b4add09fef68895deb00f552b997b3d133b5a961e5123506343c` | `Pocket Monsters - Emerald (Japan).gba` |
| Spanish | `BPES` | 16,777,216 | 0 | OK (`64`) | `e32c82bd10f174cf4019123b36f3ef7729105fb6634d9aa6b61413ee5101a55e` | `Pokemon - Edicion Esmeralda (Spain).gba` |
| English | `BPEE` | 16,777,216 | 0 | OK (`72`) | `a9dec84dfe7f62ab2220bafaef7479da0929d066ece16a6885f6226db19085af` | `Pokemon - Emerald Version (U).gba` |
| English | `BPEE` | 16,777,216 | 0 | OK (`72`) | `a9dec84dfe7f62ab2220bafaef7479da0929d066ece16a6885f6226db19085af` | `Pokemon - Emerald Version (USA, Europe).gba` |
| German | `BPED` | 16,777,216 | 0 | OK (`73`) | `7c599c56849efeebeb93bd71f714932ae4cdf980db51c9c1016b4431057f71d4` | `Pokemon - Smaragd-Edition (Germany).gba` |
| French | `BPEF` | 16,777,216 | 0 | OK (`71`) | `e79b40e6189550b4870b06918a5c59e04d3a2e1d7c92718aeda92181201f51e4` | `Pokemon - Version Emeraude (France).gba` |
| Italian | `BPEI` | 16,777,216 | 0 | OK (`6E`) | `63cbff3500b657cb6966568beb0780de3655d3a0b2e5ac6e0ec33d5d01a916ad` | `Pokemon - Versione Smeraldo (Italy).gba` |

## Exact duplicates

- `Pokemon - Emerald Version (U).gba` = `Pokemon - Emerald Version (USA, Europe).gba`

## Pairwise binary difference summary

| A | B | Differing bytes | % of ROM | First diff | Last diff | Identical 64 KiB blocks |
|---|---|---:|---:|---|---|---:|
| `BPEJ` | `BPES` | 13,394,712 | 79.838705% | 0x000000AF | 0x00F3F7C7 | 36/256 |
| `BPEJ` | `BPEE` | 13,390,435 | 79.813212% | 0x000000AF | 0x00F3F7C7 | 36/256 |
| `BPEJ` | `BPEE` | 13,390,435 | 79.813212% | 0x000000AF | 0x00F3F7C7 | 36/256 |
| `BPEJ` | `BPED` | 13,386,784 | 79.791451% | 0x000000AF | 0x00F3F7C7 | 36/256 |
| `BPEJ` | `BPEF` | 13,362,861 | 79.648858% | 0x000000AF | 0x00F3F7C7 | 36/256 |
| `BPEJ` | `BPEI` | 13,352,629 | 79.587871% | 0x000000AF | 0x00F3F7C7 | 36/256 |
| `BPES` | `BPEE` | 10,158,364 | 60.548568% | 0x000000AF | 0x00DEA0C9 | 69/256 |
| `BPES` | `BPEE` | 10,158,364 | 60.548568% | 0x000000AF | 0x00DEA0C9 | 69/256 |
| `BPES` | `BPED` | 10,744,509 | 64.042264% | 0x000000AF | 0x00DEA0C9 | 68/256 |
| `BPES` | `BPEF` | 9,927,235 | 59.170932% | 0x000000AF | 0x00DEA128 | 69/256 |
| `BPES` | `BPEI` | 10,199,886 | 60.796058% | 0x000000AF | 0x00DEA0C9 | 69/256 |
| `BPEE` | `BPEE` | 0 | 0.000000% | - | - | 256/256 |
| `BPEE` | `BPED` | 10,785,193 | 64.284760% | 0x000000AF | 0x00DEA07A | 68/256 |
| `BPEE` | `BPEF` | 10,409,185 | 62.043577% | 0x000000AF | 0x00DEA128 | 69/256 |
| `BPEE` | `BPEI` | 10,494,578 | 62.552559% | 0x000000AF | 0x00DE9F90 | 69/256 |
| `BPEE` | `BPED` | 10,785,193 | 64.284760% | 0x000000AF | 0x00DEA07A | 68/256 |
| `BPEE` | `BPEF` | 10,409,185 | 62.043577% | 0x000000AF | 0x00DEA128 | 69/256 |
| `BPEE` | `BPEI` | 10,494,578 | 62.552559% | 0x000000AF | 0x00DE9F90 | 69/256 |
| `BPED` | `BPEF` | 10,740,226 | 64.016736% | 0x000000AF | 0x00DEA128 | 68/256 |
| `BPED` | `BPEI` | 10,399,592 | 61.986399% | 0x000000AF | 0x00DEA07A | 69/256 |
| `BPEF` | `BPEI` | 10,402,855 | 62.005848% | 0x000000AF | 0x00DEA128 | 69/256 |

## Header observations

- All files are exactly 16 MiB (16,777,216 bytes).
- Internal title is `POKEMON EMER` for every file.
- Maker code is `01` for every file.
- Software version byte is `0` for every file.
- Game codes identify language/region: `BPEJ`, `BPEE`, `BPED`, `BPEF`, `BPEI`, `BPES`.
- The two English-labeled files are byte-for-byte identical and therefore count as one unique binary.

## Policy

- ROM files are local analysis inputs only and must never be committed.
- Commit only hashes, metadata, derived reports, scripts, patches/diffs that do not contain the original ROM, and other non-ROM artifacts.
