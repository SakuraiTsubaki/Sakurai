# Repository Migration — v10

Status: **active cutover** — 2026-09-13.

The canonical migration specification is [`INFRA/ARCHITECTURE/MIGRATION-V10.md`](INFRA/ARCHITECTURE/MIGRATION-V10.md). v10 supersedes v9 for all new paths while preserving verified legacy data until it has been mapped and checked.

## Ownership mapping

```text
GEN-XX/<GAME>/SOURCE/<PLATFORM>/<PACKAGE>/<RELEASE>/...
  → GEN-XX/<GAME>/RELEASES/<PLATFORM>/<PACKAGE>/<RELEASE>/...

GEN-XX/<GAME>/TARGET/<TARGET-ID>/...
  → GEN-XX/<GAME>/PROJECTS/<PROJECT-ID>/...

GEN-XX/<GAME>/COMPARE/<ID>/...
  → GEN-XX/<GAME>/COMPARES/<ID>/...

GEN-XX/<GAME>/REFERENCE/<ID>/...
  → GEN-XX/<GAME>/REFERENCES/<ID>/...
```

Generation-level and cross-generation work follows the same pluralized v10 vocabulary.

## Cutover rules

1. Stop creating new v9 `SOURCE`, `TARGET`, `COMPARE`, and `REFERENCE` paths.
2. Register observed ROM images under `RELEASES/.../DUMPS/<DUMP-ID>` without committing ROM bytes.
3. Keep conceptual release identity separate from exact dump identity.
4. Map each legacy subtree to a v10 coordinate before moving or recreating content.
5. Preserve exact blobs for path-only migrations and verify provenance before deduplication.
6. Repair internal and cross-repository references to v10 coordinates.
7. Quarantine unresolved unique leftovers only when necessary; do not use quarantine as a new ownership model.
8. Remove duplicate legacy copies only after verification; Git history remains the archive.
9. Never commit an original, modified, rebuilt, patched, trimmed, padded, decrypted, or otherwise playable ROM image.

## Initial v10 ROM corpus

The 2026-09-13 baseline registers **25 locally observed Gen I–III ROM images**. Sakurai stores the observation registry and verification metadata. Tsubaki stores the corresponding production/extraction queue. Both sides use identical release IDs, dump IDs, SHA-256 values, and semantic coordinates.
