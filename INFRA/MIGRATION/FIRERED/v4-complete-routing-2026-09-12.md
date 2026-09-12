# FireRed v4 complete routing — 2026-09-12

This pass finishes the FireRed ownership split across Sakurai and Tsubaki without changing the repository-wide v4 identity model.

## Sakurai

- Eight supplied FireRed dumps now each own an `ANALYSIS/summary.json` below their exact `DUMPS/<DUMP-ID>` path.
- The summaries record reproducible ROM-layout fingerprints, pointer-density heuristics, GBA LZ10 distribution heuristics and large 0x00/0xFF run candidates. These are dump observations, not automatic release facts or certified free-space maps.
- `LIBRARY/GEN-03/GBA/FIRERED/SHARED/ROUTING.md` is the FireRed routing contract.
- Korean glyph proof-of-concept research moved from the misleading project `IMPLEMENTATION/.../ANALYSIS` path into `PROJECTS/FIRERED-KR-LOCALIZATION/REPORTS/...`.

## Tsubaki handoff

- Production source consumption is rooted under `PROJECTS/FIRERED-ROM-EXTRACTION/IMPLEMENTATION/`.
- The temporary top-level project `SOURCE/rom-production-index.json` path is superseded by `IMPLEMENTATION/_SHARED/INDEXES/source-index.json`.
- The Korean localization production target now exists separately in Tsubaki with an exact base-dump lock.
- Cross-generation FireRed consumers must store canonical release identity separately from exact observed dump identity.

## Invariant

`RELEASE != DUMP != PROJECT OUTPUT`.

Raw ROM binaries remain local and are never committed.
