# Pokémon Emerald ROM Inventory

Repository path policy: `GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`.

This inventory was generated from locally uploaded ROMs. Original ROM binaries are treated as read-only inputs and are **not** committed to GitHub.

## Identified ROMs

| Language / Region | Source filename | GBA game code | Revision | Size | SHA-1 | MD5 | SHA-256 |
|---|---|---:|---:|---:|---|---|---|
| Japanese / Japan | `Pocket Monsters - Emerald (Japan).gba` | `BPEJ` | 0 | 16,777,216 bytes | `d7cf8f156ba9c455d164e1ea780a6bf1945465c2` | `92eecf93f1ab828bdf2a83daddacf3e5` | `33f5610b9186b4add09fef68895deb00f552b997b3d133b5a961e5123506343c` |
| Spanish / Spain | `Pokemon - Edicion Esmeralda (Spain).gba` | `BPES` | 0 | 16,777,216 bytes | `fe1558a3dcb0360ab558969e09b690888b846dd9` | `67b770405f7b87589e0342513b25fe9b` | `e32c82bd10f174cf4019123b36f3ef7729105fb6634d9aa6b61413ee5101a55e` |
| Italian / Italy | `Pokemon - Versione Smeraldo (Italy).gba` | `BPEI` | 0 | 16,777,216 bytes | `1692db322400c3141c5de2db38469913ceb1f4d4` | `c3e85be7372bbd5e43f6334a565968c1` | `63cbff3500b657cb6966568beb0780de3655d3a0b2e5ac6e0ec33d5d01a916ad` |
| German / Germany | `Pokemon - Smaragd-Edition (Germany).gba` | `BPED` | 0 | 16,777,216 bytes | `61c2eb2b380b1a75f0c94b767a2d4c26cd7ce4e3` | `f793a854654b467211fc32c4062cb183` | `7c599c56849efeebeb93bd71f714932ae4cdf980db51c9c1016b4431057f71d4` |
| English / USA-Europe | `Pokemon - Emerald Version (U).gba` | `BPEE` | 0 | 16,777,216 bytes | `f3ae088181bf583e55daf962a92bb46f4f1d07b7` | `605b89b67018abcea91e693a4dd25be3` | `a9dec84dfe7f62ab2220bafaef7479da0929d066ece16a6885f6226db19085af` |
| English / USA-Europe | `Pokemon - Emerald Version (USA, Europe).gba` | `BPEE` | 0 | 16,777,216 bytes | `f3ae088181bf583e55daf962a92bb46f4f1d07b7` | `605b89b67018abcea91e693a4dd25be3` | `a9dec84dfe7f62ab2220bafaef7479da0929d066ece16a6885f6226db19085af` |
| French / France | `Pokemon - Version Emeraude (France).gba` | `BPEF` | 0 | 16,777,216 bytes | `ca666651374d89ca439007bed54d839eb7bd14d0` | `2c00e335288a96650e34785b5e2a7588` | `e79b40e6189550b4870b06918a5c59e04d3a2e1d7c92718aeda92181201f51e4` |

## Deduplication note

The two English source filenames are byte-for-byte identical: same size, header metadata, SHA-1, MD5, and SHA-256. They represent one unique ROM image for inventory and analysis purposes.

## Unique baseline set

- 6 unique Emerald Rev 0 ROM images
- Game title header: `POKEMON EMER`
- Maker code: `01`
- Revision byte: `0` for every identified image

## GitHub handling rule

- Do not commit original ROMs.
- Commit analysis, documentation, source code, scripts, patches, manifests, and other distributable outputs.
- Place each artifact under `GENERATION-III/EMERALD/<LANGUAGE-REGION>/REV-0/<WORK-TYPE>/` when language-specific.
- Use `MULTI-REGION` only for artifacts, like this inventory, that intentionally cover several language/region variants together.
