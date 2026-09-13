# Repository Structure v11

Status: **canonical** — 2026-09-13.

## Canonical coordinates

```text
GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/
GEN-XX/<GAME-ID>/COMPARES/<COMPARE-ID>/
GEN-XX/<GAME-ID>/REFERENCES/<REFERENCE-ID>/
GEN-XX/<GAME-ID>/SHARED/
GEN-XX/PROJECTS|COMPARES|REFERENCES|SHARED/
CROSS-GEN/PROJECTS|COMPARES|REFERENCES|SHARED/
INFRA/
```

Exact dump observations use
`DUMPS/DUMP-SHA256-<FIRST-16-UPPERCASE>/` and record the full hash in
`OBSERVATION.json`. Artifact-class directories are created only when populated.

## Repository invariant

- **Tsubaki** is the complete archive/production superset of every eligible project-produced non-ROM artifact.
- **Sakurai** is the curated knowledge/control subset.
- Shared semantic coordinates and IDs are identical in both repositories.
- Therefore `Sakurai ⊆ Tsubaki`, except repository-specific metadata.

## ROM exclusion

Original, modified, rebuilt, or otherwise playable ROM images are never
committed and must not be disguised as lossless banks or chunks. Hashes,
manifests, scripts, source, discrete extracted assets, patches, build metadata,
and verification results are tracked.

See [`INFRA/ARCHITECTURE/V11.md`](INFRA/ARCHITECTURE/V11.md). Retired
`SOURCE`, `TARGET`, `COMPARE`, and `REFERENCE` roots are migration-only.
