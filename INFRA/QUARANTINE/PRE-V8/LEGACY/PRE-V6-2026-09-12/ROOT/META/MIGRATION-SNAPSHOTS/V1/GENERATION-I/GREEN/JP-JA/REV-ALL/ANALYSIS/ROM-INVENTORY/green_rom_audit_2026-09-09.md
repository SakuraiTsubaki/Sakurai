# Pocket Monsters Green (Japan) ROM audit — 2026-09-09

## Source ROMs

| Revision | Size | Banks | SHA-1 | SHA-256 | Header/global checksum |
|---|---:|---:|---|---|---|
| Rev 0 | 524288 | 32 | `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` | `6576b4e0979e93d4a6fa02db893c294b7aeab3b841b1acc8658bc10b3554f33c` | PASS / PASS |
| Rev A | 524288 | 32 | `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` | `3f0dc460ca8d06be1c9ac96307c939c0ea7baa366b40c2f1f4ad63242b6c4816` | PASS / PASS |

Both ROMs identify as `POKEMON GREEN`, are SGB-enabled, MBC1+RAM+BATTERY, 4 Mbit ROM / 256 Kbit RAM. Revision byte is `00` for Rev 0 and `01` for Rev A.

## Revision difference overview

- Total differing bytes: **46,168 / 524,288** (8.8058%).
- Contiguous differing ranges: **5,436**.
- Completely identical 16 KiB banks: **1 / 32** — bank `1B`.
- Different banks: **31 / 32**.
- Largest bank deltas: `0F` = 15,403 bytes, `00` = 13,109 bytes, `01` = 11,803 bytes.
- Therefore Rev A is not a tiny header-only patch; it contains broad code/data changes and/or relocation across most ROM banks.

## Per-bank Rev 0 ↔ Rev A comparison

| Bank | Different bytes | Similarity | Status |
|---:|---:|---:|---|
| 00 | 13109 | 19.989014% | different |
| 01 | 11803 | 27.960205% | different |
| 02 | 18 | 99.890137% | different |
| 03 | 366 | 97.766113% | different |
| 04 | 233 | 98.577881% | different |
| 05 | 83 | 99.493408% | different |
| 06 | 348 | 97.875977% | different |
| 07 | 560 | 96.582031% | different |
| 08 | 60 | 99.633789% | different |
| 09 | 519 | 96.832275% | different |
| 0A | 14 | 99.914551% | different |
| 0B | 13 | 99.920654% | different |
| 0C | 32 | 99.804688% | different |
| 0D | 65 | 99.603271% | different |
| 0E | 79 | 99.517822% | different |
| 0F | 15403 | 5.987549% | different |
| 10 | 135 | 99.176025% | different |
| 11 | 307 | 98.126221% | different |
| 12 | 406 | 97.521973% | different |
| 13 | 36 | 99.780273% | different |
| 14 | 379 | 97.686768% | different |
| 15 | 313 | 98.089600% | different |
| 16 | 330 | 97.985840% | different |
| 17 | 397 | 97.576904% | different |
| 18 | 359 | 97.808838% | different |
| 19 | 32 | 99.804688% | different |
| 1A | 2 | 99.987793% | different |
| 1B | 0 | 100.000000% | same |
| 1C | 203 | 98.760986% | different |
| 1D | 425 | 97.406006% | different |
| 1E | 132 | 99.194336% | different |
| 1F | 7 | 99.957275% | different |

No ROM binary is included. Original ROMs are treated as read-only analysis sources.
