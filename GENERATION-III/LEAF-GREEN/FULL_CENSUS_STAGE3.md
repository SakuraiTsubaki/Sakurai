# Pokémon LeafGreen Full-ROM Census — Stage 3

All seven 16 MiB project ROMs were scanned end-to-end. Source ROM images are excluded from repository artifacts.

## Full-image coverage

- `coverage_16k.csv` fingerprints every 16 KiB block of all seven ROMs: **7,168 rows**, covering all **117,440,512 input bytes**.
- `cross_version_16k.csv` compares every same-offset 16 KiB block across versions.
- Identical same-offset blocks: **340 / 1,024** across all seven; **466 / 1,024** across all six international builds; **569 / 1,024** between English Rev 0 and Rev 1.
- `entropy_64k.csv` covers every 64 KiB region with Shannon entropy plus `0x00`/`0xFF` density.

## Exhaustive differences against USA Rev 0

| Other | Exact differing bytes | Contiguous runs | Largest run | Median run |
|---|---:|---:|---:|---:|
| JP `BPGJ` | 10,470,545 | 380,493 | 260,856 | 5 |
| DE `BPGD` | 7,808,533 | 445,947 | 5,999 | 3 |
| ES `BPGS` | 6,995,053 | 298,597 | 4,877 | 5 |
| EN Rev 1 `BPGE` | 6,424,014 | 421,811 | 3,282 | 3 |
| FR `BPGF` | 7,018,388 | 307,929 | 5,429 | 4 |
| IT `BPGI` | 8,048,315 | 380,559 | 4,753 | 5 |

The exact run inventories are retained losslessly as gzip-compressed CSVs (`diff_runs_vs_usa.csv.gz` and `english_rev0_rev1_diff_runs.csv.gz`). This avoids repository files above GitHub's normal size limit while preserving every run offset and length.

### English Rev 0 → Rev 1

- Exact difference islands: **421,811**.
- This is not a header-only revision: byte differences are distributed throughout the image.
- The exact inventory includes a diagnostic prefix capped at 16 bytes per island; it does not export full ROM spans.

## Structure candidates

| Code | Strict pointer-table candidates | Pointer entries | Valid aligned LZ77 headers | Non-overlap LZ77 set | ASCII runs | Intl text candidates |
|---|---:|---:|---:|---:|---:|---:|
| BPGJ | 1,718 | 24,064 | 3,740 | 3,739 | 78,538 | — |
| BPGD | 1,710 | 23,879 | 3,726 | 3,725 | 76,782 | 11,830 |
| BPGS | 1,712 | 23,889 | 3,726 | 3,725 | 76,640 | 11,163 |
| BPGE Rev 1 | 1,713 | 23,974 | 3,726 | 3,725 | 77,049 | 11,777 |
| BPGE Rev 0 | 1,713 | 23,974 | 3,726 | 3,725 | 77,033 | 11,778 |
| BPGF | 1,712 | 23,901 | 3,726 | 3,725 | 76,855 | 11,676 |
| BPGI | 1,711 | 23,884 | 3,728 | 3,726 | 76,767 | 11,750 |

## Confidence rules

- **Coverage and difference maps are exact byte-level measurements.**
- **LZ77 rows** pass complete GBA LZ77 stream-boundary validation. Semantic type remains unassigned. This stage enumerates 4-byte-aligned headers, matching normal GBA asset alignment; an explicit unaligned-exception pass can be done separately.
- **Pointer tables** are strict runs of at least four consecutive 32-bit aligned values targeting the current 16 MiB ROM window. They are structural candidates until callers and table semantics are verified.
- **International text candidates** are `0xFF`-terminated Generation III encoding heuristics. Raw candidate bodies are not exported in this stage: offsets, lengths, quality metrics, and SHA-256 are retained.
- **Japanese text is not guessed using the international character map.** It requires a dedicated JP character-table/font pass.
- ASCII inventory is retained in compressed form because an unrestricted printable-run census is large and includes many incidental binary coincidences.

## Known embedded signatures

`known_signatures.csv` records exact offsets for known engine/library identifiers such as `PokemonSioInfo`, `FLASH1M_V103`, and `AGBJ01`. For example, `FLASH1M_V103` exists exactly once in every ROM, but its offset shifts by build/language, reinforcing that JP and international layouts cannot share hard-coded offsets.

## Generated inventories

- `coverage_16k.csv` — complete 16 KiB full-image fingerprint map
- `cross_version_16k.csv` — same-offset cross-version identity map
- `entropy_64k.csv` — full 64 KiB entropy/fill map
- `diff_runs_summary.csv` — compact exact-difference summary
- `diff_runs_vs_usa.csv.gz` — all exact difference islands vs USA Rev 0
- `english_rev0_rev1_diff_runs.csv.gz` — all exact English revision islands
- `pointer_tables.csv` — strict ROM-pointer table candidates
- `lz77_candidates.csv` — all validated aligned LZ77 header candidates
- `lz77_nonoverlap_candidates.csv` — conservative non-overlapping LZ77 candidate set
- `ascii_runs.csv.gz` — exhaustive printable ASCII-run inventory
- `text_candidates_international.csv` — hashed international text-like candidates
- `repeated_4k_blocks.csv` — exact repeated non-constant 4 KiB block groups (none found at this block size)
- `asset_census_summary.csv` — candidate totals per ROM
- `known_signatures.csv` — engine/library signature locations
