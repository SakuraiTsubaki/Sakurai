# REV-0 → REV-A binary comparison

The revisions differ at 46,168 byte positions grouped into 5,436 contiguous runs. Bank 1B is byte-identical. The remaining changed banks are listed in `bank-diff-summary.csv`.

The reproducibility package uses newline-delimited JSON deltas with `offset`, `old`, and `new` hex strings. The patcher validates the preimage before every write, preventing application to the wrong ROM revision.

The large changes in Banks 00, 01, and 0F must not be interpreted as thousands of independent fixes: relocated code/data and pointer changes can amplify binary differences. The contiguous-run map is the stable starting point for semantic diffing.
