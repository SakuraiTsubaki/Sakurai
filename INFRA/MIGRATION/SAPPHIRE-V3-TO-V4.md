# Sapphire repository migration — v4

Sapphire now uses the repository-wide v4 identity model.

## Canonical source identity

`LIBRARY/GEN-03/GBA/SAPPHIRE/`

Registered releases: `AXPJ-R0`, `AXPD-R1`, `AXPE-R0`, `AXPE-R1`, `AXPE-R2`, `AXPF-R0`, `AXPF-R1`, `AXPI-R0`, and `AXPI-R1`.

Exact observed images are identified separately as `DUMPS/PROJECT-<SHA1-8>/`. The canonical ROM-set registry is `INFRA/REGISTRY/ROM-SETS/SAPPHIRE/source-set.tsv`. Original ROM binaries are never committed.

Cross-release research belongs under `LIBRARY/GEN-03/GBA/SAPPHIRE/COMPARISONS/`, not under ambiguous `MULTI/REV-ALL` paths.

## Repository ownership

- **Sakurai:** release/dump identity, hashes, reverse engineering, analysis, disassembly, diffs, reports, verification, research tooling.
- **Tsubaki:** production source locks, extracted/converted assets, deduplication fingerprints, patches, build inputs, implementation outputs.

Derived patches are projects, not source releases. The historical Sapphire BW-direct-parameter IPS files therefore belong under `Tsubaki:PROJECTS/SAPPHIRE-BW-DIRECT-PARAMS/`.
