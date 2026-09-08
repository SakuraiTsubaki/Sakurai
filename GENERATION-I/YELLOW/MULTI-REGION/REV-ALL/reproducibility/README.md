# Pokémon Yellow — reproducible ROM workspace

This workspace turns the supplied Pokémon Yellow ROM set into deterministic, verifiable work material without treating filenames as identity.

## What is reproduced

1. Identify all input files by MD5/SHA-1/SHA-256 and cartridge header.
2. Collapse exact duplicate aliases into canonical ROM identities.
3. Split every canonical 1 MiB image into 64 × 16 KiB banks.
4. Reassemble the banks and verify an exact SHA-1 byte match.
5. Produce bank/page hashes, entropy, bank-equivalence classes and pairwise differences.
6. Produce deterministic relationship patches and verify exact target reconstruction.
7. Produce heuristic text and pointer candidate inventories that can be regenerated from the originals.
8. Pin the external `pret/pokeyellow` semantic reference by commit/tree for the canonical English build.

## Repository policy

- Git stores scripts, manifests, checksums, reports, tables, tests and reference locks.
- Raw bank slices and ROM-derived binary patches remain local-only and are not committed.
- Original ROM images are never committed.

See `RUNBOOK.md` and `reports/STATUS.md` for the exact verified state.