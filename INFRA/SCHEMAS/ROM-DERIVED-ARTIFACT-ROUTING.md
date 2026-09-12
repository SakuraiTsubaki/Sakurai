# ROM-derived artifact routing contract

This contract refines repository structure v4 for ROM-derived work. Sakurai and Tsubaki use the same game, release, dump and project identities.

## Sakurai

`LIBRARY/.../RELEASES/<RELEASE-ID>/MANIFESTS/` owns official release identity.

`LIBRARY/.../RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/` owns observations that depend on one exact supplied image: hashes, header observations, byte-range maps, bank fingerprints, pointer scans, compression candidates, string/encoding scans and verification evidence.

`LIBRARY/.../COMPARISONS/<ID>/` owns relationships derived from two or more releases/dumps: equivalence classes, deltas, dedup maps, localization boundaries and cross-release structure tables.

`INFRA/` owns generic schemas, validators, registries and reusable scanners.

## Tsubaki

`LIBRARY/.../RELEASES/<RELEASE-ID>/` owns only production assets that have been verified as release-owned and are appropriate to track. Dump-specific extraction remains dump-scoped until promoted.

`PROJECTS/<PROJECT-ID>/` owns extraction/materialization tools, conversion pipelines, patches, build inputs, generated manifests and target outputs. Project manifests reference Sakurai release/dump locks instead of duplicating research tables.

## Never commit

- raw ROM/executable images
- a second live copy solely to preserve a legacy path
- a dump-specific observation as if it were an official release fact
- generated bulk output without a manifest tying it to source release/dump identity

## Required identity chain

Every ROM-derived artifact must be traceable as:

`game -> release -> (optional dump) -> analysis/comparison/project -> artifact`
