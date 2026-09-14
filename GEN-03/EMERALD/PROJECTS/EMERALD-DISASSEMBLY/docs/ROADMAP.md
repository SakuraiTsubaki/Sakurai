# Roadmap

## Phase 0 — Bootstrap

- record reference ROM identities and headers
- establish ROM-safe repository policy
- add inspection/verification tools
- define exact-reconstruction rules

## Phase 1 — Whole-ROM survey

- generate address-space maps for every reference release
- locate code, data, graphics, text, audio, maps and script regions
- compare regional/language releases and identify shared vs variant ranges
- assign stable symbols/labels to known structures

## Phase 2 — Source extraction

- disassemble executable code and unresolved assembly
- decode text and character maps
- recover structured Pokémon, move, item, trainer and encounter data
- extract graphics to viewable/editable assets with palettes and layout metadata
- extract music, SFX, cries, samples and sound tables
- recover maps, layouts, events and scripts

## Phase 3 — Reassembly

- build each target from repository source/assets
- remove dependencies on local reference-ROM slices
- reduce and ultimately eliminate unexplained `INCBIN` regions
- reproduce exact ROM layout, alignment and compressed byte streams

## Phase 4 — Exact verification

- byte-for-byte comparison against each reference ROM
- SHA-1/SHA-256 verification
- clean-clone reproducibility tests
- CI checks that prevent accidental ROM commits

## Phase 5 — Modernization baseline

Only after exact reconstruction is stable, maintain modernization work separately so the original reconstruction remains reproducible and auditable.
