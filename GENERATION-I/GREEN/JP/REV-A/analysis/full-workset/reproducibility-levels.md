# Pokémon Green JP full-workset reproducibility levels

- **L0 — Input identity: COMPLETE.** REV-0 SHA-1 `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196`; REV-A SHA-1 `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`. Header and global checksums validate.
- **L1 — Byte coverage: COMPLETE.** Every ROM byte is covered exactly once by one of 32 × 16 KiB bank fingerprints and one of 2048 × 256-byte page fingerprints.
- **L2 — Revision relationship: COMPLETE.** 46,168 changed byte positions and 5,436 contiguous diff runs are reproducibly generated; deterministic deltas exist both directions.
- **L3 — Bank semantics: COMPLETE.** All banks 00–1F are mapped to the exact upstream `layout.link` section names.
- **L4 — Source provenance: COMPLETE.** Exact upstream source commit `953f41b34108621b2bf13c3b1e53abfc9c3e5aec`, key blobs and RGBDS 1.0.3 are pinned.
- **L5 — Exact semantic addresses/symbols: COMPLETE AS PINNED BUILD ARTIFACTS.** Upstream CI builds with `DEBUG=1` and publishes `pokegreen.map/.sym` and `pokegreen11.map/.sym` on the `symbols` branch. Their exact Git blob SHAs are pinned separately.
- **L6 — Independent local source rebuild: REPRODUCIBLE.** The build harness checks out the pinned source, requires RGBDS 1.0.3, builds both revisions and rejects any output whose SHA-1 is not canonical. This sandbox could not execute the network checkout itself because outbound Git/source downloads are blocked.

Large generated candidate tables are deterministically regenerated from the read-only ROM inputs instead of embedding ROM bytes in GitHub. Candidate pointer/filler scans remain heuristics; authoritative semantics come from the pinned source and `.map`/`.sym` artifacts.
