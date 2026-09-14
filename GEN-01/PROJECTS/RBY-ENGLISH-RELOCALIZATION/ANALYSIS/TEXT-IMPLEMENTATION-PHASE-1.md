# RBY text implementation census — phase 1

Status: ROM-derived bank census complete for the 12 supplied source/reference builds.

## What was measured

Every 16 KiB ROM bank was scanned for Generation I English text-system byte signatures: the 0x50 string terminator, dialogue control bytes such as 0x4F/0x51/0x55/0x58, English glyph-code ranges, and conservative terminated glyph runs. The result contains **608 bank rows** across all 12 ROMs. This is a discovery index, not a substitute for pointer/code ownership analysis.

## English implementation-reference observations

- Red US/EU: 1079 conservative terminated candidate strings; top banks include 0x22, 0x10, 0x07, 0x01 and 0x2C.
- Blue US/EU: 1079 conservative terminated candidate strings; its highest-scoring bank pattern is extremely close to Red.
- Yellow US/EU: 1166 conservative terminated candidate strings; strongest banks shift substantially, with 0x27, 0x28, 0x2A, 0x3A and 0x2B leading.

The supplied English ROMs directly contain the expected 0x50 terminator/control-byte population. Encoding semantics are cross-checked against pret/pokered's `constants/charmap.asm`, where 0x50 is the string terminator and 0x4F/0x51/0x55/0x58 are LINE/PARA/CONT/PROMPT controls.

## Command layer

The rendered-character/control layer is separate from the text-command stream. The command dispatcher uses opcodes 0x00–0x17 plus TX_END=0x50. TX_FAR=0x17 is especially important for relocation: it carries a banked pointer and the processor temporarily changes the loaded ROM bank before recursively processing the target command stream. This mechanism is relevant when moving translated English text away from original Japanese offsets.

## Routing decision — v9

- Raw/cross-ROM scan evidence belongs to `GEN-01/COMPARE/RBY-TEXT-ENGINE-CENSUS-2026-09-12/` in Sakurai.
- Official source-release observations belong to `GEN-01/<GAME>/SOURCE/GB/CART/<RELEASE-ID>/` in Sakurai.
- Project interpretation/specification belongs to `GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION/ANALYSIS` and `DESIGN` in Sakurai.
- Build-facing charmap/command manifests belong to `GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION/IMPLEMENTATION/ENGLISH-TEXT/` in Tsubaki.
- Production source locks belong to `GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION/IMPLEMENTATION/SOURCE-LOCK/` in Tsubaki.
- Existing font/HUD/Pokédex/town-map exact bytes remain owned by their English source releases under `GEN-01/<GAME>/SOURCE/GB/CART/<RELEASE-ID>/` in Tsubaki; they are not duplicated into the target.
- No new work uses the retired `LIBRARY/` or `PROJECTS/` prefixes.

## Next technical slice

Resolve actual text pointer tables, text-bank ownership, `TextCommandProcessor`/`PlaceString` machine-code locations in each supplied build, naming-screen input tables, and Japanese-vs-English home-bank routine deltas. Only after those references are resolved should candidate free space be promoted to allocatable space.
