# Pokémon Yellow reproducible workspace — status

## Scope

- Input files scanned: **14**
- Byte-unique canonical ROMs: **9**
- Canonical bank splits: **576** × 16 KiB
- Lossless split/rebuild tests passed: **9/9**
- Deterministic IPS relationship patch tests passed: **8/8**

## Cross-version bank identity

- Identical across EN/DE/FR/IT/ES: **17** banks — 0C 1A 1B 21 22 23 24 25 31 32 33 34 35 36 37 38 39
- Identical across EN/DE/FR/IT/ES + JP Rev D: **16** banks — 0C 1B 21 22 23 24 25 31 32 33 34 35 36 37 38 39
- Identical across all four JP revisions: **3** banks — 19 1B 32
- Identical across all 9 canonical ROMs: **2** banks — 1B 32

## Reproducibility boundary

Source-control contains hashes, manifests, analyses, scripts, reference locks and tests. Literal bank slices and ROM-derived binary patches remain local-only.

The EN semantic reference is pinned to pret/pokeyellow commit `e89ead154b9968aa50eed9328ff2b38b6c194382`.