# RBY ROM census — canonical v4.1 ownership package

This directory is a ROM-derived comparison package for the exact 12-source set used by `PROJECTS/RBY-ENGLISH-RELOCALIZATION`.

## Files

- `rom-inventory.csv.gz` — exact file identity, Game Boy header fields, checksums and hashes.
- `bank-fingerprints.csv.gz` — SHA-256 and structural statistics for every 16 KiB ROM bank (608 rows).
- `shared-bank-groups.csv.gz` — exact bank hashes shared by two or more releases (81 groups).
- `padding-candidates.csv.gz` — long 00/FF runs split by bank (472 rows).

## Ownership

These tables are research/verification evidence and belong in **Sakurai**. They are not production assets and are not copied to Tsubaki.

## Safety rule

`padding-candidates.csv.gz` is **not a free-space map**. Every row is labeled `UNVERIFIED-PADDING-CANDIDATE`. A candidate becomes allocatable only after code, pointer, table, text, graphics, map/event and other ownership checks prove it safe.

## Important ROM facts confirmed by the census

- All 12 supplied images pass both Game Boy header and global checksum verification.
- Japanese Red/Green/Blue are 32 banks (512 KiB).
- Japanese Pikachu and English Red/Blue/Yellow are 64 banks (1 MiB).
- Bank `1B` is byte-identical across all 12 supplied images, but this does **not** imply that it is unused.
- Red/Green revision and Pikachu revision differences span many banks, so revisions remain independent immutable release identities.
