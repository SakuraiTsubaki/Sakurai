# Migration to v12

Status: **active canonical cutover** — 2026-09-13.

v12 removes transitional namespaces from the live ownership tree while preserving every non-ROM artifact.

## Cutover rules

1. Canonical live paths use `GEN-XX`, `CROSS-GEN`, and `INFRA` only.
2. Root `LIBRARY`, lowercase `projects`, `workspaces`, and `STRUCTURE-V2.md` are retired.
3. Live `SOURCE`, `TARGET`, `COMPARE`, and `REFERENCE` branches are retired in favor of `RELEASES`, `PROJECTS`, `COMPARES`, and `REFERENCES`.
4. A legacy tree that is byte-for-byte identical to its canonical owner is removed as a duplicate.
5. A legacy tree with no canonical owner may be promoted by reusing its existing Git tree SHA when ownership is unambiguous.
6. A legacy tree that overlaps an existing canonical owner is preserved under `INFRA/MIGRATION/PRE-V12/` until owner-by-owner equivalence and merge verification are complete.
7. Git history remains the permanent historical archive.

## Migration quarantine

```text
INFRA/MIGRATION/PRE-V12/
```

This tree is read-only evidence. It is not a destination for new project work.

## Known promotion

Sakurai Sapphire's former `SOURCE` tree had no competing canonical `RELEASES` owner and is promoted directly to `GEN-03/SAPPHIRE/RELEASES` by reusing the same Git tree object.

## Follow-up verification

After this cutover, remaining quarantined release material will be compared against canonical `RELEASES` coordinates by release ID and artifact hash. Only verified missing artifacts are merged back into the canonical owner.

## ROM policy

Complete playable ROM image files remain excluded. Every other project artifact is eligible for version control under its truthful owner.
