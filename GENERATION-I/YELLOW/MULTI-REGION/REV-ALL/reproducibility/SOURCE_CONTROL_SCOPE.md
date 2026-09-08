# Source-control boundary

## Tracked in Sakurai

The repository stores the reproducibility layer: documentation, canonical ROM identities, cryptographic hashes, revision/localization relationships, rebuild verification results, source-reference locks, tests, and source code for the reusable inspection/rebuild tools.

## Kept local-only

The following are intentionally excluded from GitHub because they contain literal or directly reconstructive ROM-derived binary bytes:

- original `.gb` / `.gbc` ROM images;
- the 576 raw 16 KiB bank slices;
- generated IPS relationship patch binaries;
- temporary reconstructed ROM images.

## Generated large tables

Large compressed candidate inventories (page analysis, heuristic text inventory, detailed contiguous-difference ranges) are included in the downloadable public reproducibility package and are reproducible from the supplied source ROMs. Their summary/verification records are tracked in GitHub.

The local full-private package additionally contains the bank slices and generated relationship patches used by the exact-lossless regression tests.
