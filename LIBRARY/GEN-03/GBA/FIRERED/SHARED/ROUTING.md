# FireRed artifact routing

This file is the canonical routing contract for FireRed under repository structure v4.

## Identity layers

- `RELEASES/<RELEASE-ID>/MANIFESTS/` owns official-build identity and release-level facts.
- `RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/` owns observations tied to one exact supplied ROM image.
- `COMPARISONS/<COMPARISON-ID>/` owns cross-release and cross-dump relationships.
- `PROJECTS/<PROJECT-ID>/` owns transformations such as modernization, localization and extraction pipelines.

Raw ROM binaries are never committed.

## Sakurai ownership

Sakurai is authoritative for ROM identity, hashes, provenance, reverse engineering, pointer/offset research, structure maps, text/data interpretation, version comparisons, disassembly/symbol research, project design, reports and verification evidence.

ROM-derived facts that have not been verified against a canonical release remain dump-scoped. In particular, the supplied `BPRE-R0/UPLOAD-d3b80645` and `BPRE-R1/UPLOAD-c4d0119d` images are reference-mismatch observations and must not be silently promoted to release-level facts.

## Tsubaki handoff

Production-facing material belongs in Tsubaki while preserving the exact Sakurai release/dump identity:

- source locks and extraction indexes
- converted/generated graphics, fonts, palettes, tiles, maps, audio and other build inputs
- patches and patch manifests
- target build inputs and generated implementation artifacts
- production verification tied to a specific base dump

A Tsubaki artifact must record both `release_id` and `dump_id` whenever byte compatibility depends on one exact ROM image.

## Domain routing

| Domain | Sakurai | Tsubaki |
|---|---|---|
| release/dump identity | authoritative manifests | release references / source locks |
| hashes/provenance | authoritative | copied only as compatibility locks |
| pointer/offset maps | authoritative research | consumption indexes only |
| text/data interpretation | authoritative research | encoded/converted production inputs |
| graphics/audio discovery | offsets, formats, evidence | converted/generated build assets |
| localization design | research, mapping, reports | implementation/build inputs |
| modernization specification | design and verification | patches/build implementation |
| comparisons | authoritative | only project-local compatibility reports |
| ROM binaries | prohibited | prohibited |

## FireRed release IDs

`BPRJ-R0`, `BPRJ-R1`, `BPRE-R0`, `BPRE-R1`, `BPRF-R0`, `BPRD-R0`, `BPRI-R0`, `BPRS-R0`.
