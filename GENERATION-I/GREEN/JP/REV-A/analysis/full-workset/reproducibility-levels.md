# Pokémon Green JP full-workset reproducibility levels

- **L0 — Input identity: COMPLETE.** REV-0 SHA-1 `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196`; REV-A SHA-1 `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`. Header and global checksums validate.
- **L1 — Byte coverage: COMPLETE.** Every ROM byte is covered exactly once by one of 32 × 16 KiB bank fingerprints and one of 2048 × 256-byte page fingerprints.
- **L2 — Revision relationship: COMPLETE.** 46,168 changed byte positions and 5,436 contiguous diff runs are reproducibly generated; deterministic deltas exist both directions.
- **L3 — Bank semantics: COMPLETE at section-name level.** All banks 00–1F are mapped to the exact upstream `layout.link` section names.
- **L4 — Source provenance: COMPLETE.** Exact upstream repository commit and RGBDS version are pinned.
- **L5 — Exact symbol/section address rebuild: REPRODUCIBLE.** Build pinned `Narishma-gb/pokegreen` commit `953f41b34108621b2bf13c3b1e53abfc9c3e5aec` with RGBDS 1.0.3 and `DEBUG=1` to emit `.map`/`.sym`. The resulting Green ROM SHA-1 values must match the canonical inputs exactly.

Large generated candidate tables are intentionally regenerated from the read-only ROM inputs instead of embedding ROM bytes in GitHub. Candidate pointer/filler scans are heuristics, not authoritative semantic labels.
