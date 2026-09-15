# Generation IX Decompilation — Master Tracker

**Overall state:** ACTIVE

This tracker coordinates the complete Generation IX decompilation effort across Pokémon Scarlet, Pokémon Violet and Pokémon Legends: Z-A. Each title retains its own repository and title-specific implementation model.

## Repository map

| Title | Repository | State |
| --- | --- | --- |
| Pokémon Scarlet | `SakuraiTsubaki/PocketMonsters-Scarlet-Decompilation` | Phase 1 active |
| Pokémon Violet | `SakuraiTsubaki/PocketMonsters-Violet-Decompilation` | Phase 1 active |
| Pokémon Legends: Z-A | `SakuraiTsubaki/PokemonLegends-Z-A-Decompilation` | Phase 1 active |

## Content boundary

### Scarlet / Violet

- [x] Base-game track opened
- [x] Version-difference track opened
- [x] Update / revision-history track opened
- [x] The Teal Mask track opened
- [x] The Indigo Disk track opened
- [x] Epilogue / additional-event track opened
- [x] Tera Raid / event-raid track opened
- [x] Distribution / Mystery Gift track opened
- [x] Pokémon HOME track opened
- [x] Online / ranked / official-rule interaction track opened
- [x] Nintendo Switch 2 behavior-difference track opened

### Pokémon Legends: Z-A

- [x] Base-game track opened
- [x] Revision / update-history track opened
- [x] Nintendo Switch / Nintendo Switch 2 Edition comparison track opened
- [x] Mega Dimension DLC track opened
- [x] Mega Evolution implementation track opened
- [x] Z Mega Evolution / DLC-specific mechanics track opened
- [x] Lumiose / Wild Zone / Battle Zone world-data track opened
- [x] Real-time battle / capture / movement track opened
- [x] Z-A Royale / quest track opened
- [x] Z-A Battle Club / online track opened
- [x] Distribution / event-content track opened
- [x] Pokémon HOME track opened

## Decompilation work matrix

Legend: **ACTIVE** = workstream is in scope and may accept evidence now; **BLOCKED: INPUT** = automation is ready but verified local target material has not yet been inventoried; **OBSERVED** and later states require evidence.

| Workstream | Scarlet | Violet | Legends Z-A |
| --- | --- | --- | --- |
| Target/revision identity | ACTIVE | ACTIVE | ACTIVE |
| Filesystem inventory | BLOCKED: INPUT | BLOCKED: INPUT | BLOCKED: INPUT |
| ExeFS/module mapping | BLOCKED: INPUT | BLOCKED: INPUT | BLOCKED: INPUT |
| RomFS/resource mapping | BLOCKED: INPUT | BLOCKED: INPUT | BLOCKED: INPUT |
| Container/archive formats | BLOCKED: INPUT | BLOCKED: INPUT | BLOCKED: INPUT |
| Executable/function reconstruction | BLOCKED: INPUT | BLOCKED: INPUT | BLOCKED: INPUT |
| Pokémon/form data | ACTIVE | ACTIVE | ACTIVE |
| Move data | ACTIVE | ACTIVE | ACTIVE |
| Ability data | ACTIVE | ACTIVE | ACTIVE |
| Item/TM/material data | ACTIVE | ACTIVE | ACTIVE |
| Battle system | ACTIVE | ACTIVE | ACTIVE |
| Terastallization / Tera Raid | ACTIVE | ACTIVE | N/A unless observed |
| Mega Evolution | N/A unless observed | N/A unless observed | ACTIVE |
| Maps/world/collision | ACTIVE | ACTIVE | ACTIVE |
| NPC/trainer data | ACTIVE | ACTIVE | ACTIVE |
| Scripts/events/quests/flags | ACTIVE | ACTIVE | ACTIVE |
| Graphics/models/textures/animation | ACTIVE | ACTIVE | ACTIVE |
| UI | ACTIVE | ACTIVE | ACTIVE |
| Audio/music/SFX | ACTIVE | ACTIVE | ACTIVE |
| Text/localization | ACTIVE | ACTIVE | ACTIVE |
| Online/communication | ACTIVE | ACTIVE | ACTIVE |
| Live/event/distribution data | ACTIVE | ACTIVE | ACTIVE |
| DLC boundaries | ACTIVE | ACTIVE | ACTIVE |
| Pokémon HOME linkage | ACTIVE | ACTIVE | ACTIVE |
| Unused/removed data | ACTIVE | ACTIVE | ACTIVE |
| Bugs/glitches/patch changes | ACTIVE | ACTIVE | ACTIVE |
| Rebuild/verification | ACTIVE | ACTIVE | ACTIVE |

## Cross-title comparison rules

1. Scarlet and Violet are compared at equivalent revisions by path, size, hash, format and semantic role.
2. A shared path or matching hash is evidence of common data; a similar name alone is not.
3. Version-exclusive assets, text, events, maps and battle data remain separate records.
4. Pokémon Legends: Z-A is not forced into Scarlet/Violet battle, world, script or data schemas.
5. Shared Generation IX species/move/item concepts may be cross-referenced only after implementation differences are recorded.
6. Latest data never overwrites historical revisions; differences are versioned.

## Immediate execution queue

1. Generate verified per-target inventories with `tools/inventory.py` in each title repository.
2. Generate structural summaries and extension/top-level statistics.
3. Compare Scarlet ↔ Violet inventories at matching revisions.
4. Compare update-to-update changes within each title.
5. Identify executable modules and major resource-container families.
6. Select multiple first reconstruction targets: one executable-side and one data-side subsystem per title where evidence permits.
7. Feed every confirmed finding back into title manifests and this master tracker.

## Completion rule

A Generation IX workstream is not considered complete from a representative sample. Completion requires exhaustive coverage of the defined scope, with unresolved records explicitly retained as unresolved rather than silently omitted.
