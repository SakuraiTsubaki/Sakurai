# FireRed v6 full source migration — 2026-09-12

FireRed source ownership is re-keyed to the repository-wide v6 contract.

Canonical source root: `LIBRARY/GEN-03/FIRERED/SOURCE/GBA/CART/`.

Canonical release IDs are `BPRJ-HV0`, `BPRJ-HV1`, `BPRE-HV0`, `BPRE-HV1`, `BPRF-HV0`, `BPRD-HV0`, `BPRI-HV0`, and `BPRS-HV0`.

The exact supplied images remain dump identities under `DUMPS/<DUMP-ID>`. The two supplied BPRE images are reference-mismatch and remain dump-scoped. Raw ROM binaries are never committed.

Release identity lives in `IDENTITY`, GBA header/layout facts in `NATIVE`, exact-dump research in each dump's `REPORTS`, and same-game relationships in `COMPARE`.

Sakurai owns source identity, reverse engineering, comparisons and verification. Tsubaki owns production source references, extracted/normalized assets, conversion, implementation, patches and builds.
