# External technical-reference census — Pocket Monsters Aka / Pokémon Red

Research restart date: **2026-09-14**

This file records public technical references that are useful for reconstruction but are not first-party Pokémon sources. They are deliberately ranked below exact per-release disassemblies when byte-level claims conflict.

## Reference classes

### Hardware baseline — Pan Docs

- Main: https://gbdev.io/pandocs/
- Memory map: https://gbdev.io/pandocs/Memory_Map.html
- Serial / Link Cable: https://gbdev.io/pandocs/Serial_Data_Transfer_%28Link_Cable%29.html
- MBC1: https://gbdev.io/pandocs/MBC1.html
- MBC3: https://gbdev.io/pandocs/MBC3.html
- MBC5: https://gbdev.io/pandocs/MBC5.html
- SGB detection/functions: https://gbdev.io/pandocs/SGB_Unlocking.html

**Classification:** technical hardware baseline.

Use for Game Boy address-space, serial-register, mapper, and SGB hardware semantics. Do not use it to infer which mapper a specific Pokémon release uses without cartridge-header/disassembly evidence.

### Data Crystal — Red/Blue ROM/RAM/maps/text

- Overview: https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Red_and_Blue
- ROM map: https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Red_and_Blue/ROM_map
- RAM map: https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Red_and_Blue/RAM_map
- Notes/map structures: https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Red_and_Blue%3ANotes
- Text table: https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Red_and_Blue%3ATBL

**Classification:** C — specialist community reference.

Useful discoveries include map-header structure, RAM/SRAM layout notes, debug-name locations in western Red/Blue, text encoding references, and ROM-region indices.

**Critical warning:** the RAM-map article explicitly notes that more Japanese-version differences still need to be added. The overview also mixes several regional releases. Therefore western addresses, mapper metadata, and labels must never be copied into Japanese Aka without verification against `Narishma-gb/pokegreen` or other exact Japanese source evidence.

### Glitch City Wiki — natural glitch index

- https://glitchcity.wiki/List_of_natural_glitches_in_Generation_I

**Classification:** C — specialist community research / discovery index.

The page explicitly identifies itself as incomplete. Use it to seed a glitch test matrix, then verify each claimed game/version condition against source code and, where possible, multiple independent reproductions.

### Bulbapedia — comparative secondary reference

Useful for locating documented regional/VC differences and bibliography leads. Treat as C unless a claim points to an official or primary source.

## Initial technical claims accepted only as search leads

The following are **not yet promoted to project facts solely from these references**:

- exact western ROM offsets listed in Data Crystal;
- claims of “unused” RAM/ROM without a source-reference audit;
- glitch applicability ranges from community lists;
- mapper/header statements that collapse Japanese and international releases;
- any debug-content claim not matched to the exact Japanese Red revision.

## Verification pipeline

For every technical claim:

1. identify exact game / language / region / revision;
2. locate the relevant public disassembly symbol, table, or routine;
3. compare with hardware semantics when needed using Pan Docs;
4. use community references only as corroboration or lead generation;
5. record disagreement instead of flattening sources;
6. only then promote the claim into reconstruction docs or source.

## Immediate follow-up queues

- Japanese Red/Green SRAM and save-layout audit versus western Data Crystal maps.
- Japanese versus western map-header and connection-structure comparison.
- Japanese character map/control-code census versus western text tables.
- Link protocol audit from source routines against Pan Docs serial semantics.
- Natural-glitch matrix by RGBY + region/revision, starting with battle calculation, encounter, map, save/Hall-of-Fame, and link glitches.
- Debug/unused-data audit with exact source symbols and reachability status.
