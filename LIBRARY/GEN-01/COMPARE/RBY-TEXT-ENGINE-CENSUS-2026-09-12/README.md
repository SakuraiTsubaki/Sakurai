# RBY text-engine census — v6

ROM-derived cross-game discovery dataset for all 12 source/reference builds used by `PROJECTS/GEN-01/RBY-ENGLISH-RELOCALIZATION`.

## Contents

- `ANALYSIS/bank-text-signature.csv.gz` — 608 rows, one per 16 KiB ROM bank, including terminator/control/glyph signatures and conservative candidate-string counts.

The scanner counts the Generation I English text-system signatures used for discovery: `0x50` terminators, dialogue controls `0x4F/0x51/0x55/0x58`, English glyph ranges, and conservative terminated glyph runs. The meaning of these bytes was cross-checked against pret/pokered commit `a1a22aaf84d1675bcdbaeb194592379d586d838e`; that repository is a technical reference, not a translation source.

## Key observation

English Red and Blue each produced 1,079 conservative terminated candidate strings and have nearly identical high-scoring bank patterns. English Yellow produced 1,166 and is materially reorganized: its strongest banks shift to 0x27, 0x28, 0x2A, 0x3A and 0x2B. Yellow therefore needs its own text-bank/pointer map instead of inheriting Red/Blue positions.

## Safety rule

This census is a discovery index only. A high text score does not prove ownership, and a low score or long `00`/`FF` run does not prove free space. Allocation requires semantic pointer/code/table/graphics/map/event ownership analysis.
