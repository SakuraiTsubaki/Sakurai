# Pokémon LeafGreen ROM Inventory

> Analysis metadata only. Original ROM binaries are intentionally **not committed** to GitHub.

## Repository hierarchy

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

Current path:

`GENERATION-III/LEAFGREEN/MULTI-REGION/REV-MULTI/ANALYSIS/`

## Verified source ROMs

| Language / Region | Source filename | GBA game code | ROM revision byte | Size | SHA-1 | MD5 |
|---|---|---:|---:|---:|---|---|
| English / USA | `Pokemon - Leaf Green Version (USA).gba` | `BPGE` | `0` | 16,777,216 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | `612ca9473451fa42b51d1711031ed5f6` |
| Italian / Italy | `Pokemon - Versione Verde Foglia (Italy).gba` | `BPGI` | `0` | 16,777,216 | `a1dfea1493d26d1f024be8ba1de3d193fcfc651e` | `1e52f38082b252e04173efb340a9286e` |
| German / Germany | `Pokemon - Blattgruene Edition (Germany).gba` | `BPGD` | `0` | 16,777,216 | `0802d1fb185ee3ed48d9a22afb25e66424076dac` | `4dd5e72f942a921d3fe53d21a39f4cba` |
| Spanish / Spain | `Pokemon - Edicion Verde Hoja (Spain).gba` | `BPGS` | `0` | 16,777,216 | `f9ebee5d228cb695f18ef2ced41630a09fa9eb05` | `765178ed4d402033ef7ed6b82d059f5a` |
| French / France | `Pokemon - Version Vert Feuille (France).gba` | `BPGF` | `0` | 16,777,216 | `4b5758c14d0a07b70ef3ef0bd7fa5e7ce6978672` | `c5bc831107f459816508b45d9392afc9` |
| English / Europe | `Pokemon - Leaf Green Version (Europe) (Rev 1).gba` | `BPGE` | `1` | 16,777,216 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | `9d33a02159e018d09073e700e1fd10fd` |
| Japanese / Japan | `Pocket Monsters - Leaf Green (Japan).gba` | `BPGJ` | `0` | 16,777,216 | `5946f1b59e8d71cc61249661464d864185c92a5f` | `138a71a5be83f3f3d7af3d31916a5fc7` |

All seven files report the GBA internal title `POKEMON LEAF`, maker code `01`, and a size of 16 MiB.

## Per-ROM destination convention

Future language-specific outputs should use the same hierarchy, for example:

- `GENERATION-III/LEAFGREEN/EN-USA/REV-0/<WORK-TYPE>/`
- `GENERATION-III/LEAFGREEN/EN-EUROPE/REV-1/<WORK-TYPE>/`
- `GENERATION-III/LEAFGREEN/JA-JP/REV-0/<WORK-TYPE>/`
- `GENERATION-III/LEAFGREEN/IT-IT/REV-0/<WORK-TYPE>/`
- `GENERATION-III/LEAFGREEN/DE-DE/REV-0/<WORK-TYPE>/`
- `GENERATION-III/LEAFGREEN/ES-ES/REV-0/<WORK-TYPE>/`
- `GENERATION-III/LEAFGREEN/FR-FR/REV-0/<WORK-TYPE>/`

Cross-version surveys and inventories may live under `MULTI-REGION/REV-MULTI`.

## Handling policy

- Uploaded original ROMs are read-only reference inputs.
- Original ROM binaries and other redistributable copyrighted game binaries are never committed.
- GitHub may contain analysis, documentation, source code, scripts, patch files, manifests, checksums, and other distributable project outputs.
- ROM-derived output should be organized under the exact hierarchy above before commit.

Generated from direct header/hash verification of the uploaded LeafGreen ROM set on 2026-09-07 (Asia/Seoul).
