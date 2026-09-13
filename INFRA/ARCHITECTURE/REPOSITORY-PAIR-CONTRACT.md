# Sakurai ↔ Tsubaki Repository Pair Contract v11

Status: **canonical** — 2026-09-13.

## Shared coordinate grammar

```text
GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/
GEN-XX/<GAME-ID>/COMPARES/<COMPARE-ID>/
GEN-XX/<GAME-ID>/REFERENCES/<REFERENCE-ID>/
GEN-XX/<GAME-ID>/SHARED/<ARTIFACT-CLASS>/
GEN-XX/PROJECTS/<PROJECT-ID>/
GEN-XX/COMPARES/<COMPARE-ID>/
CROSS-GEN/PROJECTS/<PROJECT-ID>/
CROSS-GEN/COMPARES/<COMPARE-ID>/
INFRA/
```

Exact dump observations are nested under a release as `DUMPS/DUMP-SHA256-<FIRST-16-UPPERCASE>/`. Both repositories use identical generation, game, release, dump, project, comparison, reference, and shared-resource identifiers.

## Tsubaki

Tsubaki is the **complete non-ROM project superset**. Every newly generated non-ROM project artifact belongs in Tsubaki when that project is tracked there: identity, provenance, hashes, analyses, reports, tables, schemas, tools, extracted assets, normalized/converted assets, translation data, implementation data, patches, build recipes/logs, and verification evidence.

## Sakurai

Sakurai is the research/control subset. It stores identity and provenance, hashes, analyses, reverse engineering, tables, comparisons, reports, schemas/specifications, research tools, and verification evidence. Production-only assets and build products do not need to be duplicated into Sakurai.

## Pair invariant

Anything committed to Sakurai for an actively paired project must also be eligible and expected to exist in Tsubaki at the same semantic coordinate. A task is incomplete if a new research artifact exists only in Sakurai while Tsubaki tracks the project.

## ROM exclusion

Never commit original, modified, rebuilt, or otherwise playable ROM images. Do not evade this rule by committing a lossless bank/chunk decomposition whose practical purpose is reconstructing the ROM. Hashes, manifests, patches, discrete extracted assets, translation/implementation data, build recipes, analysis tables, and verification evidence are allowed.

## Legacy paths

`SOURCE`, `TARGET`, `COMPARE`, and `REFERENCE` ownership branches from v9 and older are migration inputs only. New work uses `RELEASES`, `PROJECTS`, `COMPARES`, `REFERENCES`, and `SHARED`.
