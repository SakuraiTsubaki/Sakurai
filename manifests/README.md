# Manifest Guide

This directory defines repository-wide manifest conventions for Sakurai's combined Disassembly + Decompilation aggregate.

## Upstream registry

[`upstream-repositories.json`](upstream-repositories.json) is the authoritative list of the current source universe:

- 12 Disassembly repositories
- 34 Decompilation repositories
- 46 repositories total

Every aggregated record should preserve enough identity to trace it back to that registry.

## Recommended source fields

In addition to the normal asset/research fields, aggregated records should include these when applicable:

- `source_family` — `disassembly` or `decompilation`
- `source_repository` — exact upstream repository name
- `source_path` — original repository-relative path
- `source_revision` — commit/tag/ref when known
- `target` — game/version/region/language/revision/build identity
- `aggregate_path` — Sakurai destination path
- `hashes` — identity-sensitive hashes
- `verification` — Unverified / Observed / Reproduced / Matched
- `shared_with` — other upstreams proven equivalent
- `notes`

Use [`example.asset-manifest.json`](example.asset-manifest.json) as a reusable starting point.

## Rules

- Do not invent unknown metadata; use `TBD`, `unknown`, or null explicitly.
- Preserve the exact upstream family and repository identity.
- Prefer stable semantic IDs and cryptographic hashes when identity matters.
- Verify byte/hash identity or another documented equivalence test before deduplicating.
- Preserve provenance for shared representative records.
- Project-specific manifests belong under the matching `projects/disassembly/<repo>/` or `projects/decompilation/<repo>/` owner unless they genuinely describe `shared/` or `derived/` material.
- Keep complete playable ROM image files out of GitHub.
