# Pokémon Black / White — internal NARC delta baseline

Source: read-only supplied SweeTnDs IRBO/IRAO ROM images. This document records byte-level facts; semantic labels are separated by confidence.

## Summary

| NARC path | Black members | White members | differing members | differing indices |
|---|---:|---:|---:|---|
| `a/0/2/6` | 15 | 15 | 8 | 0, 1, 2, 3, 4, 6, 7, 8 |
| `a/0/8/6` | 1 | 1 | 1 | 0 |
| `a/1/2/6` | 112 | 112 | 29 | 0, 5, 6, 49, 52, 53, 58, 69, 71, 75, 77, 79, 80, 81, 82, 83, 84, 95, 98, 99, 100, 101, 102, 104, 105, 106, 107, 108, 109 |
| `a/1/7/8` | 649 | 649 | 26 | 10, 11, 13, 14, 197, 199, 366, 367, 428, 429, 537, 538, 545, 546, 547, 548, 573, 574, 575, 576, 577, 578, 626, 627, 628, 629 |
| `a/2/3/1` | 73 | 73 | 2 | 1, 63 |

Total differing NARC members across the five top-level version-different NitroFS archives: **66**.

## Interpretation status

- `a/0/2/6`: externally documented as the BW title-screen archive.
- `a/1/2/6`: externally documented as BW wild-encounter data.
- `a/1/7/8`: 649 fixed-size 249-byte members; 26 differ. A species-indexed availability/Pokédex-related role is plausible but remains provisional until code/reference confirmation.
- `a/0/8/6`: unresolved.
- `a/2/3/1`: unresolved.

Changed zero-based members in `a/1/7/8`: `10, 11, 13, 14, 197, 199, 366, 367, 428, 429, 537, 538, 545, 546, 547, 548, 573, 574, 575, 576, 577, 578, 626, 627, 628, 629`.

## V4 provenance

Migrated from the historical pre-V4 BW ROM baseline. Detailed per-member hashes remain reproducible from the exact locked SweeTnDs dump observations and the baseline scanner; release facts must not be inferred from the dump labels alone.
