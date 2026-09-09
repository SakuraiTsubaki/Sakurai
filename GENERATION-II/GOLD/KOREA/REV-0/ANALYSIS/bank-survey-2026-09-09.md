# Pokémon ROM 16 KiB bank-by-bank exhaustive survey

Date: 2026-09-09

Context: GS Korean → Pocket Monsters Korean localization/retranslation project. Original ROM binaries remain local/read-only and are not uploaded.

## Scope

- 23 uploaded Gen I/II ROMs surveyed.
- 1,760 physical 16 KiB banks inspected.
- 28,835,840 bytes covered.
- 375 exact duplicate-bank SHA-1 clusters detected.
- 188 whole-bank single-byte fill instances detected.
- 33 same-index exact-bank anchor clusters are shared by at least four ROMs.

Every structural metric is evidence only. Entropy/compressibility/fill classifications are not semantic labels. A bank is not declared code, text, graphics, compressed data, or safe free space until reference/pointer/call-site tracing supports that conclusion.

## Per-bank measurements

For each physical bank the local survey records SHA-1/SHA-256/CRC32, entropy, zlib ratio, distinct-byte count, 00/FF ratio, printable-ASCII ratio, rough Pokemon Latin-glyph-byte ratio, 0x4000–0x7FFF pointer-like word ratio, rough control-flow opcode-byte ratio, longest printable sequence, longest repeated-byte run, >=64/256/1024/4096-byte fill-run counts, structural class, first/last 16 bytes, and exact-bank relationships.

## Revision and regional aligned-bank deltas

| Pair | Banks | Exact | Changed | Differing bytes | Most changed bank |
|---|---:|---:|---:|---:|---:|
| JP Red Rev0 → RevA | 32 | 1 | 31 | 46,167 | `$0F` (15,402) |
| JP Green Rev0 → RevA | 32 | 1 | 31 | 46,168 | `$0F` (15,403) |
| JP Pikachu 0A → B | 64 | 3 | 61 | 307,668 | `$2B` (16,378) |
| JP Pikachu B → C | 64 | 4 | 60 | 39,485 | `$27` (3,203) |
| JP Pikachu C → D | 64 | 3 | 61 | 245,538 | `$27` (16,263) |
| JP Gold Rev0 → RevA | 64 | 54 | 10 | 10,841 | `$23` (10,821) |
| JP Silver Rev0 → RevA | 64 | 48 | 16 | 19,150 | `$23` (10,787) |
| EN Crystal Rev0 → RevA | 128 | 120 | 8 | 584 | `$5C` (546) |
| KR Gold ↔ Silver | 128 | 92 | 36 | 264,639 | `$15` (16,160) |
| EN Gold ↔ Silver | 128 | 84 | 44 | 285,225 | `$15` (16,165) |

Important correction over the earlier rough audit: JP Red Rev0↔RevA affects 31 of 32 aligned bank indices, not a small handful of banks. The total differing-byte count remains 46,167. This exhaustive aligned-bank table is now the canonical comparison result.

## Verified GS Korean semantic banks

These labels come from prior direct extraction/reassembly work, not entropy guesses.

| Bank | Verified role | KR Gold/Silver exact? | EN Gold same bank | JP Gold bank exists? |
|---:|---|:---:|---|:---:|
| `$68` | Pokédex description text | no | populated | no |
| `$69` | Pokédex description text | no | populated | no |
| `$6C` | Korean name/string tables | yes | populated | no |
| `$78` | Hangul table/font resource block | yes | whole-bank `00` fill | no |
| `$79` | Hangul table/font resource block | yes | whole-bank `00` fill | no |
| `$7A` | Hangul table/font resource block | yes | whole-bank `00` fill | no |

`$6C` was previously losslessly extracted/reassembled as 830 records: 256 item-name slots + 67 trainer-class names + 256 Pokémon-name slots + 251 move names.

`$78–$7A` are populated and byte-identical between Korean Gold and Silver, while the same physical banks are whole-bank fill in English Gold/Silver and are outside the 1 MiB address range of Japanese Gold/Silver. This is strong byte-structural evidence that the Korean release uses extended-ROM banks for Korean-specific resources.

## Exact same-index anchors

Some complete 16 KiB banks survive unchanged across many ROMs and are useful structural anchors. Their meaning is not inferred solely from identity.

- Bank `$1B`: byte-identical across 12 Gen I ROMs in this source set.
- Banks `$30`, `$3B`, `$3D`: byte-identical across 11 Gen II ROMs.
- Banks `$0C`, `$2A`, `$37`, `$3C`: byte-identical across 8 Gen II Gold/Silver-family ROMs in the detected clusters.
- Bank `$2B`: one exact bank image occurs at the same index in 6 Gen II Gold/Silver-family ROMs.
- 33 same-index exact-bank clusters are shared by at least four ROMs.

These anchors are candidates for engine/resource lineage mapping and for locating regions that regionalization did not touch.

## Fill-space rule

Whole-bank `00`/`FF` and long fill runs are recorded as candidates only. They are not approved relocation space. A candidate becomes allocatable only after bank-switch reachability, direct/far pointer tables, call/jump references, decompression/resource references, and data-table references are checked.

## Local reproducible outputs

The completed local package contains:

- `BANK_SURVEY_REPORT.md`
- `bank_inventory.csv` / `bank_inventory.json` — all 1,760 banks
- `bank_maps/` — one bank map per ROM
- `free_space_runs_ge64.csv`
- `whole_bank_fill_candidates.csv`
- `exact_bank_clusters.csv`
- `same_index_consensus.csv`
- `same_index_exact_anchors_ge4roms.csv`
- `related_pair_bank_diffs.csv`
- `related_pair_summary.csv`
- `all_rom_pairwise_similarity.csv`
- `family_bank_matrix.csv`
- `gs_korean_bank_focus.csv`
- `GS_KOREAN_BANK_FOCUS.md`
- survey/build scripts and a bundled ZIP

## Next pass

1. Trace MBC bank-switch writes and reachable far calls/jumps.
2. Detect local and far pointer tables and build cross-bank reference graphs.
3. Mark fill candidates referenced/unreferenced; only unreferenced candidates can become approved relocation space.
4. Resolve semantic bank roles using text tables, decompression entry points, map/event tables, graphics/audio references and known GS Korean extraction results.
5. Isolate Korean-only changes by comparing KR Gold/Silver with JP and EN Gold/Silver at routine/table granularity, then prepare separate implementation maps for JP and EN target ROMs.
