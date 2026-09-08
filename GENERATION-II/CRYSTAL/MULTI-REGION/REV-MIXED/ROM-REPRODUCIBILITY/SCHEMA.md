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

## address_map_banks.csv / address_map_pages.csv
Deterministic mapping from file offsets to 16 KiB ROM bank numbers and visible CPU address windows. This is address geometry, not a claim that a byte is executable code.

## same_offset_bank_equivalence.csv / same_offset_page_equivalence.csv
Groups regional/revision targets whose chunks are byte-identical at the same file offset. Equality is proven by chunk SHA-256; inequality does not imply unrelated semantics because localized data may shift later content.

## pointer_word_target_class_counts_by_bank.csv
Counts every adjacent little-endian 16-bit value in each bank by Game Boy memory target class. This is intentionally an over-approximation and must not be treated as a typed pointer table without stronger structural evidence.

## lossless_roundtrip_report.json
Proof that each supplied ROM can be temporarily split into consecutive 0x4000-byte banks and concatenated back to the exact original bytes/SHA-256. The bank binaries and rebuilt ROM are scratch artifacts and are excluded from the distributable package.

## source_bridge.json
Pinned metadata linking the two exact USA/Europe ROM identities to supported `pret/pokecrystal` source build outputs. It contains repository/build metadata and hashes only, not upstream source files or ROM binaries.
