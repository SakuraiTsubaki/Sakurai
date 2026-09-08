# Verification Status

All four reproducibility layers were independently regenerated from the eight verified source ROMs and compared file-for-file by SHA-256.

| Layer | Reference files | Regenerated files | Missing | Extra | Changed | Result |
|---|---:|---:|---:|---:|---:|---|
| Phase 0 — physical corpus | 138 | 138 | 0 | 0 | 0 | PASS |
| Phase 1 — structural survey | 105 | 105 | 0 | 0 | 0 | PASS |
| Phase 2 — fixed-bank alignment | 10 | 10 | 0 | 0 | 0 | PASS |
| Phase 3 — full-ROM atlas | 99 | 99 | 0 | 0 | 0 | PASS |

Phase 3 additionally validates the source-segment coverage contract against the original ROM bytes: every segment is gapless, non-overlapping, and ends exactly at the source ROM size for all eight targets.
