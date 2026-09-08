# Pokémon Blue/Ao whole-ROM reproducible work corpus — v3

v3 turns the byte-exact v2 scaffold into a reproducible **work pipeline** for all six supplied Blue/Ao ROMs.

## What v3 adds

- one work-unit record for every ROM bank (352 total)
- semantic category/status/evidence/confidence per bank
- next-extractor assignment and exact completion gate per bank
- structural xref candidate counts
- 16-bit pointer-table candidate discovery
- text-like run candidates (addresses/lengths only; no dumped copyrighted text)
- 16-byte tile-unit statistics for graphics triage
- semantic coverage summary across JP/EN/DE/FR/IT/ES
- regression verification tying all of the above back to the exact local ROM hashes and v2 byte scaffold

## Non-negotiable completion rule

A semantic extractor is considered complete only when:

1. it extracts the target structure from the local read-only ROM;
2. it can reinsert/re-encode that structure;
3. the reconstructed ROM matches the original source SHA-256 exactly.

Until that gate passes, the byte-exact `INCBIN` scaffold remains authoritative.

## Copyright / repository policy

Source ROMs and generated raw bank/tile/text binaries stay local and are not committed. GitHub stores only scripts, manifests, addresses, hashes, statistics, documentation, and other ROM-free reproducibility material.
