# RBY source audit — 2026-09-13

Observed local corpus: **12 ROM images** (ROM binaries remain excluded from GitHub).

- Japanese translation sources: **9** — Red 2, Green 2, Blue 1, Pikachu 4.
- English implementation references: **3** — Red 1, Blue 1, Yellow 1.
- Japanese Red/Green/Blue images are 512 KiB; Japanese Pikachu and English Red/Blue/Yellow observations are 1 MiB.
- Every observed image passes both the Game Boy header checksum and global checksum checks recorded in `rom-inventory.csv`.
- Exact images are addressed by SHA-256-derived dump IDs; ROM file contents are not committed.

## Revision observations

`revision-deltas.csv` records direct byte comparisons between consecutive Japanese header revisions. The deltas are evidence only; large differences must not be interpreted as semantic changes without bank/code/text-level analysis.

## Repository cutover

Architecture v11 corrects the previous repository split. Tsubaki now receives the complete non-ROM project artifact set, including this report and the analytical tables also stored in Sakurai.
