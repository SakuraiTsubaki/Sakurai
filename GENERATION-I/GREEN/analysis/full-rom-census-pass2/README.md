# Pokémon Green full ROM census — pass 2

This pass is generated from the two uploaded Japanese Green ROMs and cross-checked against the `Narishma-gb/pokegreen` symbol/source layout. ROM binaries are not included.

## Correct ROM identity
- Rev 0 SHA-1: `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196`
- Rev A SHA-1: `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`
- Size: 524,288 bytes each (32 × 16 KiB banks)
- Raw same-offset difference: 46,168 bytes (8.805847%), 5,436 contiguous runs.

## Map/object census
- Map ID slots: 248 (parsed 226, explicit UNUSED_MAP slots 22)
- Unique parsed map headers: 223
- Unique parsed object resources: 223
- Slot-level connections: 78
- Slot-level warps: 813
- Slot-level background/sign events: 204
- Slot-level object events: 924 (normal 472, item 106, trainer 334, static battle Pokémon 12)
- Map slots with semantic object/header changes in Rev A: 0

## Wild encounters
- Unique wild-data resources: 59
- Map slots with grass encounter data: 55
- Map slots with water encounter data: 3
- Expanded slot encounter rows: 580

## Pokémon / moves / trainers
- Internal Pokémon index slots: 190
- Real Pokédex species: 151
- MissingNo internal slots: 39
- Unique Pokédex entry pointers (including MissingNo entry): 152
- Base-stat records: 151
- Evolution rows: 72
- Level-up learnset rows: 728
- Moves: 165
- Trainer classes: 47
- Trainer party records: 415
- Trainer objects cross-checked against class/party data: 334, invalid references: 0

## Revision-stability check
Core table ranges checked: 15; byte-identical: 15. This includes the full 8,640-byte Pokédex entry data region (`bank 10:$45DA-$6799`).
Non-identical checked ranges: none.

## Notes
- The 22 explicit `UNUSED_MAP_*` IDs preserve their raw pointer/bank combinations instead of being dereferenced as playable maps. Some deliberately use dummy bank bytes with reused pointers.
- Three non-unused copy slots share complete header/object resources with another map slot; parsed playable content therefore resolves to 223 unique map resources from 226 parsed slots.
- Object event parsing follows the actual macro encoding: ordinary 6-byte events, item events +1 byte, and 8-byte battle objects. Battle objects are split into trainer objects (`OPP_ID_OFFSET + class`) and static Pokémon battles (internal species ID + level).
- Wild data is expanded into one row per `(map, terrain, encounter slot)` while retaining pointer-alias information.
- Pokémon internal index and Pokédex number are deliberately separate columns.
- Shared Japanese glyph tiles that are ambiguous in the original font are rendered as `べ/ベ`, `ぺ/ペ`, `へ/ヘ`, or `り/リ` rather than guessed.
- Heuristic scans and source-confirmed tables remain separate; this pass focuses on source-confirmed table structures.
