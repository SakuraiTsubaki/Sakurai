# Sakurai ↔ Tsubaki Pair Sync Policy — v11

Status: **mandatory** — 2026-09-13.

## Invariant

Tsubaki is the complete non-ROM superset. Sakurai is a curated knowledge/research subset.

For every non-ROM artifact committed to Sakurai, an equivalent artifact MUST exist in Tsubaki at the same semantic v11 coordinate. Tsubaki may contain additional production/data artifacts that do not exist in Sakurai.

A Tsubaki-only artifact is valid. A Sakurai-only non-ROM artifact is a synchronization defect.

## Upload rule

Only complete original or modified/playable ROM images are excluded. Everything else is eligible and expected in Tsubaki: metadata, hashes, observations, headers, indexes, analysis, documentation, source, scripts, tools, CSV/JSON/YAML/Markdown, schemas, tables, manifests, catalogs, extracted assets, normalized/converted assets, implementation, patches, build recipes/metadata/logs, tests, reports and verification evidence.

## Workflow

1. Assign the semantic v11 coordinate.
2. Commit the non-ROM artifact to Tsubaki first or in the same work cycle.
3. Mirror research/control artifacts to Sakurai without changing their semantic coordinate.
4. Verify hashes/content for mirrored files.
5. Record intentional generated-format transformations explicitly rather than silently diverging.

## ROM safety

Do not use the superset rule to reconstruct or commit a complete playable ROM image. Extracted project resources and bounded byte ranges are allowed when they are legitimate non-ROM project artifacts and retain provenance.
