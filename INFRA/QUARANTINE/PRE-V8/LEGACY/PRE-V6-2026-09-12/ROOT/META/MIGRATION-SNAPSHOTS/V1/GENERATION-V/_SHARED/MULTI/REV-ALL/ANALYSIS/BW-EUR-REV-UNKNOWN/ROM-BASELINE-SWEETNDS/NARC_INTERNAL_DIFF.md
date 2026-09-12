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

- `a/0/2/6`: externally documented as the BW title-screen archive. Eight of 15 members differ between Black and White.
- `a/1/2/6`: externally documented as BW wild-encounter data. 29 of 112 encounter records differ between versions.
- `a/1/7/8`: 649 fixed-size 249-byte members; 26 differ. The member count and changed-index pattern strongly indicate a species-indexed table associated with version-dependent Pokédex/availability data, but this semantic label remains **provisional** until code/reference-level confirmation.
- `a/0/8/6`: one-member archive, payload differs; semantic role unresolved in this pass.
- `a/2/3/1`: 73 members; only members 1 and 63 differ; semantic role unresolved in this pass.

### `a/1/7/8` changed member pattern

Changed zero-based member indices: `10, 11, 13, 14, 197, 199, 366, 367, 428, 429, 537, 538, 545, 546, 547, 548, 573, 574, 575, 576, 577, 578, 626, 627, 628, 629`.

If (and only if) member 0 corresponds to National Pokédex #001, these indices map to species numbers: `11, 12, 14, 15, 198, 200, 367, 368, 429, 430, 538, 539, 546, 547, 548, 549, 574, 575, 576, 577, 578, 579, 627, 628, 629, 630`. This alignment includes multiple well-known Black/White version-skewed families (for example Throh/Sawk, Cottonee/Petilil lines, Gothita/Solosis lines, Rufflet/Vullaby lines), which is evidence for a species-indexed availability/Pokédex-related role. It is not yet a final label.

## Reproducibility

See `narc_internal_diff.csv` for member sizes and SHA-1 hashes. A later catalogue pass must decode each archive structure and establish field semantics rather than relying on path folklore or pattern matching alone.
