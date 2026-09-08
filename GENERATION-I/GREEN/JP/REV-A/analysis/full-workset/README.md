# Pokémon Green JP — Full Reproducible Workset

Canonical inputs:

- REV-0 SHA-1 `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196`
- REV-A SHA-1 `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`

The ROM-free workset covers all 32 banks and 2,048 pages per ROM, all 46,168 changed bytes and 5,436 contiguous diff runs, bidirectional deterministic revision deltas, exact source/RGBDS provenance, pinned `.map/.sym` build products, Game Boy CPU↔ROM-offset conversion, RGBDS section/symbol indexing, and exact diff→section attribution tooling.

The local release additionally contains deterministic regeneration/tests and a deterministic ZIP builder. Final release ZIP SHA-256: `678c712a8071257eaea36616d40ec30643b719af1d71aee038df3e6a50ab2572`.

Original `.gb` files are never committed. Heuristic pointer/filler candidates are not treated as authoritative semantic labels or proven free space.
