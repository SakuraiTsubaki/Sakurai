# Pokémon Green (Japan) ROM census — initial inventory

Date: 2026-09-05 (Asia/Seoul)

## Scope

This inventory covers the two project ROM inputs currently mounted for **Pocket Monsters Midori / Pokémon Green (Japan)**. The ROM binaries themselves are intentionally excluded from GitHub. This report stores only metadata, hashes, checksums, and aggregate comparison statistics.

## Inputs

| Revision | Size | Banks | Header title | Mask ROM version | SGB | SHA-1 | SHA-256 |
|---|---:|---:|---|---:|---:|---|---|
| Rev 0 | 524,288 B | 32 | `POKEMON GREEN` | 0 | `0x03` | `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` | `6576b4e0979e93d4a6fa02db893c294b7aeab3b841b1acc8658bc10b3554f33c` |
| Rev A | 524,288 B | 32 | `POKEMON GREEN` | 1 | `0x03` | `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` | `3f0dc460ca8d06be1c9ac96307c939c0ea7baa366b40c2f1f4ad63242b6c4816` |

Both images have valid Game Boy header checksums and valid global checksums. Both report cartridge type `0x03`, ROM size code `0x04`, RAM size code `0x03`, and SGB flag `0x03`.

## Revision-level comparison

- Differing bytes: **46,168 / 524,288 (8.805847%)**
- First differing offset: `0x000051`
- Last differing offset: `0x07FFFF`
- Identical 16 KiB banks: `1B`
- Changed 16 KiB banks: `00`, `01`, `02`, `03`, `04`, `05`, `06`, `07`, `08`, `09`, `0A`, `0B`, `0C`, `0D`, `0E`, `0F`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `1A`, `1C`, `1D`, `1E`, `1F`

The revision delta is therefore **not** limited to the cartridge header. Interpretation of each changed region is deferred until code/data/text/graphics ownership is mapped; this census deliberately avoids guessing semantics from raw offsets alone.

## Byte differences by 16 KiB bank

| Bank | Different bytes | Difference | Status |
|---:|---:|---:|---|
| 00 | 13,109 | 80.0110% | changed |
| 01 | 11,803 | 72.0398% | changed |
| 02 | 18 | 0.1099% | changed |
| 03 | 366 | 2.2339% | changed |
| 04 | 233 | 1.4221% | changed |
| 05 | 83 | 0.5066% | changed |
| 06 | 348 | 2.1240% | changed |
| 07 | 560 | 3.4180% | changed |
| 08 | 60 | 0.3662% | changed |
| 09 | 519 | 3.1677% | changed |
| 0A | 14 | 0.0854% | changed |
| 0B | 13 | 0.0793% | changed |
| 0C | 32 | 0.1953% | changed |
| 0D | 65 | 0.3967% | changed |
| 0E | 79 | 0.4822% | changed |
| 0F | 15,403 | 94.0125% | changed |
| 10 | 135 | 0.8240% | changed |
| 11 | 307 | 1.8738% | changed |
| 12 | 406 | 2.4780% | changed |
| 13 | 36 | 0.2197% | changed |
| 14 | 379 | 2.3132% | changed |
| 15 | 313 | 1.9104% | changed |
| 16 | 330 | 2.0142% | changed |
| 17 | 397 | 2.4231% | changed |
| 18 | 359 | 2.1912% | changed |
| 19 | 32 | 0.1953% | changed |
| 1A | 2 | 0.0122% | changed |
| 1B | 0 | 0.0000% | same |
| 1C | 203 | 1.2390% | changed |
| 1D | 425 | 2.5940% | changed |
| 1E | 132 | 0.8057% | changed |
| 1F | 7 | 0.0427% | changed |

## Next census layers

1. ROM bank ownership map: code, text, maps, graphics, audio, tables, free/unused candidates.
2. Pointer/reference census, including banked pointers and table roots.
3. Japanese text encoding/font/output routine census.
4. Map/event/NPC/trainer/wild/item/battle/system data census.
5. Rev 0 ↔ Rev A semantic diff after ownership mapping.
6. Only after Green is fully mapped: compare against Red/Blue/Yellow reference ROMs for the RBY ENGLISH → G workstream.

## Reproducibility

`tools/rom_census.py` reproduces the inventory and per-bank comparison from two locally supplied ROM files. It does not contain or emit ROM payload bytes.
