# Repository Migration Policy

Version upgrades are **canonical ownership migrations, not snapshot duplication**.

## Canonical cutover rules

1. Define the new canonical path before changing repository layout.
2. Compare the retiring path and the new canonical owner file-by-file.
3. Move or merge every unique non-ROM artifact into the canonical owner.
4. Verify hashes, internal references, manifests, validation data, and any affected build/reproduction workflow.
5. Delete retired duplicate project paths from the current tree after verification.
6. Update live internal references to the canonical coordinates during the same cutover.
7. Use Git commits/tags/history for historical recovery. Do **not** retain duplicate `PRE-V*`, quarantine, migration, snapshot, or redirect trees solely to preserve history.
8. A version cutover is incomplete while the same project's current work must be browsed from more than one root.

## Canonical path families

Live ownership uses `GEN-XX`, `CROSS-GEN`, and `INFRA`. Project work belongs under the single truthful canonical project owner, such as:

```text
GEN-XX/<GAME-ID>/PROJECTS/<PROJECT-ID>/
GEN-XX/PROJECTS/<PROJECT-ID>/
CROSS-GEN/PROJECTS/<PROJECT-ID>/
```

Release material uses `RELEASES`; relations and external references use `COMPARES` and `REFERENCES`.

## ROM policy

Complete playable ROM image files remain excluded. Every other eligible project artifact is merged into its canonical owner rather than duplicated across migration/history paths.
