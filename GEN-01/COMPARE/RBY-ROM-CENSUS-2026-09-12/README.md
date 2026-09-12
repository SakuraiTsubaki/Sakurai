# RBY ROM census — canonical comparison

Cross-game ROM-derived census for the 12 exact source dumps consumed by `GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION`.

- `bank-fingerprints.csv.gz`: 608 16 KiB bank fingerprints.
- `shared-bank-groups.csv.gz`: 81 exact-hash bank groups across releases.
- `padding-candidates.csv.gz`: 472 guarded `UNVERIFIED-PADDING-CANDIDATE` runs.
- `rom-inventory.csv.gz`: exact dump identity/header/hash inventory.

Source releases are owned at `GEN-01/<GAME>/SOURCE/GB/CART/<RELEASE-ID>/`.

This is comparison/research evidence, not free-space allocation authority. Identical banks remain owned by their source releases. Long 00/FF runs are not allocatable until pointer/code/data ownership is proven.
