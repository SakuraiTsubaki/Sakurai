# Project Standards

## Canonical ownership

Every project or artifact family has one live owner path. Move/merge the current tree when ownership changes; do not create parallel migration/history trees.

## Semantic IDs

Use stable, explicit IDs. Avoid ambiguous catch-all IDs such as `ALL`, `MULTI`, `MISC`, `OTHER`, or `GENERAL` where the architecture forbids them.

## Provenance

Record where facts and artifacts came from. For identity-sensitive material, prefer cryptographic hashes and exact source revisions.

## Unknown values

Do not guess. Use `TBD`, `unknown`, or null fields until verified.

## Deduplication

Do not merge assets or records solely because they look or sound identical. Verify byte/hash identity when exact sameness matters, and preserve provenance for every semantic coordinate sharing the representative artifact.

## Repository boundary

Sakurai is curated research/control material. Tsubaki is the complete eligible non-ROM superset. Shared material should use the same semantic coordinates in both repositories.

## ROM policy

Complete playable ROM image files are excluded from GitHub.
