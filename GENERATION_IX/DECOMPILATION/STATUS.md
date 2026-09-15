# Generation IX Decompilation Status

**State:** ACTIVE — all defined workstreams opened

## Current execution layer

The repositories have moved beyond empty setup. The current common tooling layer consists of:

- deterministic extracted-tree inventory generation;
- per-file SHA-256 and whole-tree digest generation;
- inventory-to-inventory comparison;
- exhaustive structural summary generation by section, extension, top-level path and file size;
- unit tests;
- GitHub Actions validation in each title repository.

## Current blockers

The GitHub repositories intentionally do not contain retail game images, console keys, raw update packages or raw decrypted proprietary dumps. Therefore executable addresses, real resource-path inventories, binary signatures and function bodies cannot be truthfully populated until verified local research material is inventoried.

This is an input boundary, not a scope reduction. All workstreams remain active.

## Next evidence transition

For each title and each target revision:

1. Run the inventory tool on the verified local extracted tree.
2. Commit only the resulting permissible manifests/hashes/reports.
3. Generate structural reports.
4. Run within-title revision comparisons.
5. Run Scarlet ↔ Violet equivalent-revision comparisons.
6. Identify executable modules and resource-container families.
7. Begin multiple source-reconstruction tracks in parallel once their inputs are observed.

## Current primary software lines

- Pokémon Scarlet: Ver. 4.0.0 primary current comparison target.
- Pokémon Violet: Ver. 4.0.0 primary current comparison target.
- Pokémon Legends: Z-A: Ver. 2.0.2 primary current comparison target.

Historical versions remain mandatory comparison targets.
