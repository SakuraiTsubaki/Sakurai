# Crystal source-level reconstruction roadmap

The full-byte baseline is Phase 0. Each later phase must preserve the same source-ROM identity and add a regression test proving lossless extraction/reinsertion or exact rebuild where applicable.

## Phase 0 — forensic baseline (complete)
- immutable ROM identities and header validation
- 16 KiB bank coverage and SHA-256 map
- 256-byte page coverage and SHA-256 map
- constant/fill runs and entropy classification
- all-region pairwise bank/byte comparison
- USA/Europe Rev0↔Rev1 exact changed-byte map
- heuristic LR35902 JP/CALL candidate map
- file-offset/bank/CPU-address maps
- same-offset cross-version bank/page equivalence map
- exhaustive 16-bit word target-class summary
- exact temporary bank split→reassemble roundtrip for all seven ROMs

## Phase 0.5 — source baseline bridge (English complete as a pinned reference)
- pin `pret/pokecrystal` source reference and toolchain expectation
- bind USA/Europe Rev0 and Rev1 to exact upstream build SHA-1 identities
- retain independent local ROM identities as the acceptance oracle
- do not import raw ROM binaries into the source repository

## Phase 1 — executable structure
- reset/interrupt vectors and entry flow
- recursive code discovery from known entry points
- bank-switch routines and far-call conventions
- ROM0/ROMX call graph
- RAM/HRAM/I/O references
- symbol table with confidence/provenance

## Phase 2 — pointer graph and typed data
- local 16-bit pointer tables
- banked/far pointers
- pointer ownership and target ranges
- data-table stride inference
- cross-version table alignment

## Phase 3 — game data decoders
- species/base stats/evolutions/learnsets
- moves/items/trainers/wild encounters
- maps/events/scripts/warps/objects
- Pokédex/order/index tables
- party/box/save/SRAM structures

## Phase 4 — text/localization
- character maps and control codes per language
- string boundaries/pointer ownership
- text boxes/menu strings/battle text
- exact extract→reinsert regression

## Phase 5 — visual/audio assets
- tiles/2bpp sprites/tilemaps/palettes/animations
- cries/music/SFX command streams
- deduplication by decoded and raw hashes
- extract→reinsert regression

## Phase 6 — assembler-grade reconstruction
- RGBDS-compatible sections and bank layout
- symbolic labels and generated data includes
- binary-blob fallbacks only for not-yet-decoded ranges
- coverage report must reach 100% with no overlapping ownership
- build output SHA-1/SHA-256 must match each target source ROM exactly

## Phase 7 — modification foundation
Only after exact rebuild is proven:
- 4 MiB/MBC30-capable layout plan
- 8-bit→16-bit species-ID migration
- save/SRAM format versioning
- expanded species/forms/varieties tables
- automated regression ROM tests
