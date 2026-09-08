# Output schema notes

## identity.json
Source identity (filename, size, MD5/SHA-1/SHA-256/CRC32) plus decoded Game Boy header.

## header.json
Decoded cartridge header, stored/calculated header checksum and global checksum.

## bank_manifest.csv
One row per 16 KiB bank. Includes file range, CPU mapping window, SHA-256, CRC32, entropy, byte diversity, fill metrics and all-00/all-FF flags.

## page_manifest.csv
One row per 256-byte page. This is the fine-grained full-ROM coverage ledger. `classification` is heuristic only.

## fill_runs_ge32.csv
Every constant-byte run of length >= 32, including runs that cross bank boundaries.

## branch_call_immediate_candidates.csv
Every byte position whose byte pattern can decode as an LR35902 immediate JP/CALL to ROM address space. It intentionally over-approximates; data bytes may be false positives.

## pairwise_diff_summary.csv
For every supplied ROM pair: total differing byte positions and exact lists of identical/different 16 KiB banks.

## usa_europe_rev0_rev1_changed_bytes.csv
Patch-like changed-byte ledger for the 584 positions that differ between the supplied USA/Europe revisions. It contains no unchanged ROM data and requires a source ROM to be useful.
