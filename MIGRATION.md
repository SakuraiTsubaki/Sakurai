# Repository Migration — v11

Status: **active cutover** — 2026-09-13.

## Mapping

```text
SOURCE/...       -> RELEASES/...
TARGET/...       -> PROJECTS/...
COMPARE/...      -> COMPARISONS/...
COMPARES/...     -> COMPARISONS/...
REFERENCE/...    -> REFERENCES/...
```

Legacy roots such as `LIBRARY/`, `projects/`, `GENERATION-*`, and pre-v11 layouts are read-only migration inputs.

## Repository rule

Sakurai remains the canonical evidence source. Tsubaki is a superset: every non-ROM project artifact produced during extraction, normalization, conversion, implementation, patching, building, testing, analysis or verification is committed there.

## ROM rule

Never commit a playable ROM image and never evade this rule by committing a complete byte-for-byte chunk decomposition.
