# Pokémon Crystal 7-ROM full structural census — pass 1

This pass performs byte-exact structural census over all 7 project ROMs and all 128 16-KiB banks per ROM. It does **not** claim that repeated 00/FF ranges are safe free space; they are only candidates pending reference/pointer analysis.

## Coverage
- ROMs: 7
- Banks per ROM: 128
- Total banks inspected: 896
- Bytes inspected: 14,680,064
- EN Rev0→RevA differing bytes: 584
- EN revision changed contiguous ranges: 79
- EN revision affected banks: 00, 10, 11, 3E, 47, 5C, 7E, 7F
- Banks byte-identical across all seven: 30, 31, 37, 3B, 3C, 3D, 4B, 4C, 7A

## Structural summary
| ROM | mean entropy | candidate fill bytes (>=32 runs) | banks with >=1KiB candidate fill | lowest entropy bank | highest entropy bank |
|---|---:|---:|---:|---|---|
| JP | 4.8831 | 650,212 | 62 | 60 (-0.000) | 48 (7.293) |
| EN-Rev0 | 5.4406 | 474,227 | 86 | 75 (-0.000) | 48 (7.291) |
| EN-RevA | 5.4406 | 474,214 | 86 | 75 (-0.000) | 48 (7.291) |
| DE | 5.5404 | 434,478 | 80 | 7A (-0.000) | 48 (7.291) |
| FR | 5.4383 | 491,832 | 87 | 7A (-0.000) | 48 (7.291) |
| IT | 5.4371 | 483,182 | 86 | 7A (-0.000) | 48 (7.291) |
| ES | 5.4881 | 468,314 | 86 | 7A (-0.000) | 48 (7.291) |

## Important interpretation rule
- `00`/`FF` runs are **not yet declared free space**. They can be padding, reserved capacity, lookup-table sentinels, or runtime-sensitive regions. Safe-space status requires cross-reference and code/data reachability checks.
- Same-offset equality across localizations is a structural clue, not proof of identical semantics.
- Printable-ASCII scan is only a heuristic; Pokémon Crystal uses a custom character encoding and must be decoded with the proper charmap in a later pass.

## Generated ledgers
- `bank_census.csv`
- `cross_rom_bank_matrix.csv`
- `fill_runs_ge64.csv`
- `en_rev0_reva_changed_ranges.csv`
- `same_offset_identical_runs_ge256.csv`
- `ascii_heuristic_summary.csv`
- `rom_structural_summary.csv`
