# RBY English Relocalization — routing v6

Status: **canonical for new RBY work**.

## Source truth

Official source/reimplementation-reference builds remain under:

```text
LIBRARY/GEN-01/<GAME-ID>/SOURCE/GB/CART/<RELEASE-ID>/
```

Japanese Red/Green/Blue/Pikachu are translation originals and build bases. Official English Red/Blue/Yellow are implementation references. Green remains an independent target; no English Green release is invented.

## Project root

All derived RBY relocalization work is generation-scoped:

```text
PROJECTS/GEN-01/RBY-ENGLISH-RELOCALIZATION/
├── MANIFESTS/
├── INPUTS/
├── CROSSWALK/
├── ANALYSIS/
├── DESIGN/
├── DIFFS/
├── TOOLS/
├── REPORTS/
└── VERIFICATION/
```

No new work may use the pre-v6 flat `PROJECTS/RBY-ENGLISH-RELOCALIZATION/` path.

## Cross-ROM research

Cross-game research belongs under `LIBRARY/GEN-01/COMPARE/<COMPARISON-ID>/`. The text-engine bank census is `RBY-TEXT-ENGINE-CENSUS-2026-09-12`.

## Tsubaki production

Tsubaki uses the same source IDs and project ID. Build-facing charmap/text-command specifications live under:

```text
PROJECTS/GEN-01/RBY-ENGLISH-RELOCALIZATION/SOURCE/ENGLISH-TEXT-IMPLEMENTATION/
```

Exact official font/UI bytes remain release-owned under `LIBRARY`, with equality represented in `COMPARE`; they are not copied into the project.

## Space relocation

Existing offsets are not translation constraints. `TX_FAR`/banked text processing is part of the implementation mechanism that must be preserved or reconstructed for relocated English text. Candidate padding is never treated as allocatable until semantic ownership is proven.
