# Exact symbol and section workflow

The authoritative semantic address layer is the RGBDS `.map/.sym` output from the exact matching `Narishma-gb/pokegreen` build.

## Locked artifacts

`symbols-lock.json` pins the symbols branch commit plus byte size and Git blob SHA-1 for:

- `pokegreen.map` / `pokegreen.sym` — REV-0
- `pokegreen11.map` / `pokegreen11.sym` — REV-A

The raw files need not be embedded: the reproducible workset fetcher downloads immutable commit URLs and refuses files whose size or Git blob ID differs.

## Derived tables

`parse_rgbds_symbols.py` creates revision-specific section and symbol CSVs, cross-references ROM symbols to file offsets/sections, and compares revision addresses. `map_diff_to_sections.py` then splits every binary diff run at the union of REV-0 and REV-A section boundaries and aggregates changed bytes for each section pair.

This keeps ROM-derived binary facts independent while semantic names and section boundaries remain traceable to the pinned byte-exact disassembly build.
