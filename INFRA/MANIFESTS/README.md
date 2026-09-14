# Manifest Guide

This directory defines repository-wide manifest conventions for Sakurai. Project-specific manifests still belong under their truthful canonical owner paths.

Use [`example.asset-manifest.json`](example.asset-manifest.json) as a reusable starting point.

Useful fields include semantic coordinate, owner path, category, target/release identity, source/provenance, address/offset/range/symbol, repository path, size, hashes, generation tool/command, verification state, shared identities, pair relationship, and notes.

## Rules

- Do not invent unknown metadata; use `TBD`, `unknown`, or null explicitly.
- Prefer stable semantic IDs and cryptographic hashes when identity matters.
- Verify byte/hash identity before deduplicating.
- Preserve provenance for shared representative artifacts.
- Keep complete playable ROM image files out of GitHub.
