# FireRed ROM-derived ownership model

This FireRed subtree uses four distinct ownership layers. Raw ROM binaries are never committed.

1. `RELEASES/<RELEASE-ID>/MANIFESTS` — official-build identity and release-level facts only.
2. `RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/...` — observations calculated from one exact supplied ROM image.
3. `COMPARISONS/<COMPARISON-ID>/...` — relationships between two or more releases/dumps.
4. `PROJECTS/<PROJECT-ID>/...` — localization, modernization, extraction/conversion pipelines, patches, builds and other derived work.

## Repository ownership

- **Sakurai** owns identity, reverse engineering, ROM structure research, dump observations, comparisons, scripts and verification evidence.
- **Tsubaki** owns production-facing extraction locks, conversion tooling, generated/converted assets, patches and build inputs.

Exact IDs are shared across both repositories. A production artifact must reference the Sakurai release/dump identity that produced it.

## Promotion rule

Dump-derived facts stay under `DUMPS/<DUMP-ID>` until verified against the canonical release. This is mandatory for the supplied `BPRE-R0` and `BPRE-R1` images because their SHA-1 values do not match the canonical preservation references recorded by the repository.

## FireRed release set

`BPRJ-R0`, `BPRJ-R1`, `BPRE-R0`, `BPRE-R1`, `BPRF-R0`, `BPRD-R0`, `BPRI-R0`, `BPRS-R0`.
