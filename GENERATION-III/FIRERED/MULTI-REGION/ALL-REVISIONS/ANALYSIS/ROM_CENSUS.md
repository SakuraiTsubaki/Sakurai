# Pokémon FireRed ROM Census — Stage 1 Baseline

## Scope

This census covers the eight FireRed ROM images currently mounted in the FIRE RED project workspace.
Original ROM binaries are intentionally excluded from GitHub. Only analysis, manifests, hashes, validation results, and reproducible tooling are published.

## Coverage

- Total ROMs: **8**
- ROM size: **16 MiB each**
- Language/region families: **6**
  - Japanese: Rev 0, Rev 1
  - English (BPRE): Rev 0, Rev 1
  - German: Rev 0
  - French: Rev 0
  - Italian: Rev 0
  - Spanish: Rev 0
- All eight ROMs have:
  - valid Nintendo GBA logo data
  - valid GBA header complement checksum
  - maker code `01`
  - fixed value `0x96`
  - 256 × 64 KiB banks

## Identity ledger

| ROM | Game code | Header rev | CRC32 (workspace file) | SHA-1 (workspace file) | Canonical verification |
|---|---|---:|---|---|---|
| Pocket Monsters - Fire Red (Japan).gba | `BPRJ` | 0 | `3b2056e9` | `04139887b6cd8f53269aca098295b006ddba6cfe` | exact reference match |
| Pocket Monsters - Fire Red (Japan) (Rev 1).gba | `BPRJ` | 1 | `bb640df7` | `7c7107b87c3ccf6e3dbceb9cf80ceeffb25a1857` | exact reference match |
| Pokemon - Fire Red Version (USA).gba | `BPRE` | 0 | `07c5cc23` | `d3b806453369b4b086c792eb3c05a02f00057f50` | canonical after final 2-byte normalization |
| Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba | `BPRE` | 1 | `29a4cddf` | `c4d0119d9bcb36687f41a8f7ca72ab7af60558e4` | canonical after final 2-byte normalization |
| Pokemon - Feuerrote Edition (Germany).gba | `BPRD` | 0 | `1a81eedf` | `18a3758ceeef2c77b315144be2c3910d6f1f69fe` | exact reference match |
| Pokemon - Version Rouge Feu (France).gba | `BPRF` | 0 | `5dc668f6` | `fc663907256f06a3a09e2d6b967bc9af4919f111` | exact reference match |
| Pokemon - Versione Rosso Fuoco (Italy).gba | `BPRI` | 0 | `73a72167` | `66a9d415205321376b4318534c0dce5f69d28362` | exact reference match |
| Pokemon - Edicion Rojo Fuego (Spain).gba | `BPRS` | 0 | `9f08064e` | `ab8f6bfe0ccdaf41188cd015c8c74c314d02296a` | exact reference match |

## English ROM tail anomaly

The two English `BPRE` images are not content-modified builds. Each differs from the recognized canonical image only at the final two bytes of the 16 MiB file:

| ROM | Offset `0x00FFFFFE` | Offset `0x00FFFFFF` | Canonical bytes | Canonical SHA-1 after normalization |
|---|---:|---:|---|---|
| BPRE Rev 0 | `00` | `19` | `FF FF` | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| BPRE Rev 1 | `00` | `18` | `FF FF` | `dd5945db9b930750cb39d00c84da8571feebf417` |

Replacing only those final two bytes with `FF FF` reproduces the recognized canonical SHA-1 exactly. The workspace ROMs themselves are left untouched; this is recorded only as a normalization fact for analysis.

Normalized checksums:

- BPRE Rev 0: CRC32 `dd88761c`, MD5 `e26ee0d44e809351c8ce2d73c7400cdd`, SHA-256 `3d0c79f1627022e18765766f6cb5ea067f6b5bf7dca115552189ad65a5c3a8ac`
- BPRE Rev 1: CRC32 `84ee4776`, MD5 `51901a6e40661b3914aa333c802e24e8`, SHA-256 `729041b940afe031302d630fdbe57c0c145f3f7b6d9b8eca5e98678d0ca4d059`

## Revision-pair binary deltas

These are byte-for-byte deltas between the project files. The English pair includes the two final-byte tags noted above.

### Japanese Rev 0 → Rev 1

- Differing bytes: **7,016,197** (**41.819793%**)
- First difference: `0x000000BC` (software revision byte)
- Last difference: `0x00FDFFFE`
- Changed 64 KiB banks: **120 / 256**

### English Rev 0 → Rev 1

- Differing bytes: **6,367,135** (**37.951082%**)
- First difference: `0x000000BC` (software revision byte)
- Last difference: `0x00FFFFFF`
- Changed 64 KiB banks: **115 / 256**

The large revision deltas are therefore real whole-build differences, not evidence that the two project ROMs are arbitrary hacks. Canonical SHA-1 verification confirms the Japanese pair directly, and confirms the English pair after removal of only the two-byte file-tail tags.

## Generated artifacts

- `rom_census.csv` — one-row-per-ROM identity/header/hash ledger
- `rom_census.json` — machine-readable ledger
- `canonical_verification.csv` / `.json` — reference-hash and tail-normalization proof
- `bank_sha256.csv` — SHA-256 for all 256 64-KiB banks in each ROM
- `pairwise_diff_summary.csv` / `.json` — all 28 ROM-pair byte-difference summaries
- `fire_red_rom_census.py` — reproducible census tool

## Next census layer

Stage 1 establishes trustworthy ROM identities. The next layer can safely move into full structural mapping: executable/code regions, pointer tables, text/charset/font systems, graphics, maps/scripts, battle data, Pokémon/move/item/trainer tables, save structures, free-space/padding regions, and cross-language/revision relocation maps.
