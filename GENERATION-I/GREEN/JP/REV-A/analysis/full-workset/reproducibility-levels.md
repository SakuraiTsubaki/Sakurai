# Reproducibility levels

- **L0 — Input identity: COMPLETE.** Both canonical ROM hashes and header/global checksums are fixed.
- **L1 — Byte coverage: COMPLETE.** Every byte belongs to exactly one 16 KiB bank and one 256-byte page fingerprint.
- **L2 — Revision relationship: COMPLETE.** Every differing byte and contiguous diff run is recorded; deterministic deltas exist both directions.
- **L3 — Bank semantics: COMPLETE.** All 32 ROM banks map to the exact upstream `layout.link` section families.
- **L4 — Source provenance: COMPLETE.** Source commit `953f41b34108621b2bf13c3b1e53abfc9c3e5aec` and RGBDS `1.0.3` are pinned.
- **L5 — Exact `.map/.sym` provenance: COMPLETE.** Four REV-0/REV-A build artifacts are pinned by immutable symbols commit, byte size and Git blob SHA-1; a verified fetcher is included.
- **L6 — Byte → section/symbol indexing: IMPLEMENTED AND TESTED.** Parsers convert RGBDS addresses to ROM file offsets, compare symbols/sections between revisions, and attribute every diff run to exact section boundaries whenever the pinned raw `.map/.sym` files are available. The parser/attribution logic is regression-tested with synthetic RGBDS fixtures in this package.
- **L7 — Independent source rebuild: REPRODUCIBLE.** `build/fetch_and_build_upstream.sh` checks out the exact source commit, requires RGBDS 1.0.3, does a clean `DEBUG=1` build and rejects outputs whose SHA-1 differs from the canonical Green ROMs. It was not executed in this sandbox because outbound Git/source downloads are blocked.

Heuristic pointer/filler scans remain explicitly marked candidates. Authoritative semantic names come from the pinned exact-build source and `.map/.sym` outputs.
