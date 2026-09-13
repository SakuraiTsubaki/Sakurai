# Artifact routing — RBY ENGLISH → G

## Upstream shared English-system research

Generation-wide RBY English text/character/UI system research belongs to `GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION`. The Green target consumes that work rather than duplicating it.

## Sakurai: evidence / Green-specific research plane

Commit here:

- Green release and dump identity, hashes, cartridge/header observations
- ROM bank maps, occupancy/free-space candidates and revision deltas
- pointer maps, symbols, reverse-engineering notes and disassembly-derived annotations
- Green text indexes and Green-specific text/code/UI/name-entry observations
- map/event/NPC/trainer/item/wild/battle/system inventories
- Green JP ↔ Red/Blue/Yellow JP ↔ Red/Blue/Yellow English comparison matrices
- official-name crosswalks, translation provenance and correction records
- Green-specific specifications, citations, QA plans, test logs and verification evidence
- reproducible analysis tools whose primary purpose is inspection/research

## Tsubaki: production / implementation plane

Commit there:

- verified ROM-derived production indexes and extraction manifests
- extracted/normalized/converted build assets
- insertion-ready character/font/text/UI data used by the Green build
- implementation source, ASM/INC/data files, relocation tables and bank-aware dispatch code
- build tools, rebuild scripts and deterministic materialization recipes
- IPS/BPS/xdelta or equivalent patches
- linker/map/symbol/build metadata, checksums and non-ROM build outputs
- production tests, regression fixtures and verification reports

## Excluded

Only complete original or modified ROM binaries are excluded from GitHub. Everything else is committed under its truthful owner.

## Ownership rule

Do not keep authoritative duplicate copies in both repositories. Sakurai is authoritative for facts/evidence; Tsubaki is authoritative for production artifacts. Cross-repository references use the same generation/game/platform/package/release/dump/target IDs.
