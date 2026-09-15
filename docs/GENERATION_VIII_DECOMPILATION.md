# Generation VIII Decompilation — Master Tracker

This document tracks the active **Generation VIII-wide** source-reconstruction and data-census program. Each game repository remains canonical for its own reconstructed source, manifests, tools, and verification evidence; `Sakurai` is the cross-title research-control index and `Tsubaki` is the non-ROM asset workspace.

## Active canonical targets

| Target | Canonical repository | Current stage | Full-scope epic | Immediate gate |
| --- | --- | --- | --- | --- |
| Pokémon Sword | `SakuraiTsubaki/PocketMonsters-Sword-Decompilation` | Phase 0 — target intake | #1 | Verified local base/update/DLC inventory |
| Pokémon Shield | `SakuraiTsubaki/PocketMonsters-Shield-Decompilation` | Phase 0 — target intake | #1 | Verified local base/update/DLC inventory |
| Pokémon Brilliant Diamond | `SakuraiTsubaki/PocketMonsters-BrilliantDiamond-Decompilation` | Phase 0 — target intake | #1 | Verified local base/update inventory |
| Pokémon Shining Pearl | `SakuraiTsubaki/PocketMonsters-ShiningPearl-Decompilation` | Phase 0 — target intake | #1 | Verified local base/update inventory |
| Pokémon Legends: Arceus | `SakuraiTsubaki/PokemonLegends-Arceus-Decompilation` | Phase 0 — target intake | #1 | Verified local base/update revision inventory |

## Generation VIII program scope

The active program covers all of the following, without reducing the generation to Sword alone or to a representative subset:

- Pokémon Sword and Pokémon Shield;
- The Isle of Armor and The Crown Tundra as distinct Expansion Pass content targets;
- Pokémon Brilliant Diamond and Pokémon Shining Pearl as independent Generation VIII remake targets;
- Pokémon Legends: Arceus as an independent runtime/data/system target;
- every materially relevant base/update/revision difference;
- version-exclusive code, data, encounters, trainers, scripts, text and assets;
- Pokémon, forms, stats, evolution, encounters, raids, research tasks and game-specific parameters;
- every move, ability, item and battle-system record by title/revision;
- every map/subarea/interior and world-connectivity record;
- every character, trainer, NPC, battle-team variant, script, event, quest/request and progression state;
- UI, localization, models, textures, animations, VFX, audio and other non-ROM assets;
- Pokémon HOME-facing game behavior, save-data linkage, local/online communication, Mystery Gift and official distribution hooks represented by the games;
- official distributions and event-table overrides;
- patch history, fixed/unfixed bugs, translation/data/display errors;
- unused/dummy/debug/deleted shipped data and development traces with evidence grading;
- reproducible extraction, conversion, reconstruction and verification tooling.

## Active cross-title epics in Sakurai

- **#122 — Full decompilation program master epic:** whole-generation control checklist.
- **#123 — Connected systems:** HOME, save linkage, online/local behavior, distributions and patch-facing integration.
- **#124 — Official distributions/event-data census:** exhaustive Generation VIII gift/event corpus.
- **#126 — Version/patch/unused-data/bug census:** historical revision preservation and edge-data research.
- **#127 — Complete data census:** Pokémon, moves, items, maps, trainers, scripts and text.
- **#128 — Official-source linked-bonus/HOME baseline:** official-reference facts awaiting local-game verification.
- **#129 — Maps/world connectivity census:** complete map/subarea/connectivity reconstruction.
- **#131 — Characters/trainers/NPCs census:** every actor and every distinct battle-team/state variant.
- **#133 — Moves/abilities/items/battle systems:** complete title-specific mechanical parameter census.

## Asset program

`SakuraiTsubaki/Tsubaki` issue **#103** tracks full Generation VIII non-ROM asset extraction/reconstruction: models, textures, animations, VFX, map/environment resources, UI/icons/fonts, audio, materials/shaders, update/DLC variants and evidenced unused assets.

Asset deduplication requires byte/hash or equivalent structural evidence; visually identical material is not assumed identical. Provenance remains attached to every title/revision that uses a shared asset.

## Official connected-systems baseline

`docs/GENERATION_VIII_CONNECTED_SYSTEMS_BASELINE.md` records current official-reference facts for HOME compatibility, HOME move handling, BDSP save-record bonuses, PLA save-record bonuses, PLA-linked BDSP distribution behavior, and revision-sensitive Daybreak content. These remain `Reference only` until matched to local game material.

## Shared Phase 0 evidence contract

1. Retail game images, complete redistributed game binaries and console keys remain outside Git.
2. Local extracted trees are inventoried by relative path, size and SHA-256.
3. External title IDs, update histories, public build identifiers and official web behavior are `Reference only` until independently matched to local material.
4. ExeFS and RomFS structure is recorded from observed files before semantic interpretation.
5. Reconstructed source/data advances through `Unverified -> Reference only/Observed -> Reproduced -> Matched` as appropriate.
6. Cross-version and cross-title deduplication requires byte/hash or equivalent evidence.
7. Unknown offsets, paths, field names, symbols or internal types stay unknown rather than being guessed.

## Cross-title rules

### Sword / Shield

Map both independently first. Compare only matching identified revisions. Preserve version-exclusive gyms, encounters, trainers, text, events, assets, executable differences and Expansion Pass conditions. Isle of Armor and Crown Tundra remain large independent content tracks inside the paired projects.

### Brilliant Diamond / Shining Pearl

Map both independently first. Original Nintendo DS Diamond/Pearl/Platinum are comparison references, not assumed implementation templates. Base-versus-update state is preserved because substantial content and functionality changed through updates.

### Pokémon Legends: Arceus

Keep PLA independent. Do not project Sword/Shield or BDSP subsystem boundaries onto it. Field capture, wild behavior, research tasks, Strong/Agile Style, action order, Effort Levels, Alpha Pokémon, outbreaks, Massive Mass Outbreaks, space-time distortions, rides, crafting, missions and requests are independent analysis tracks.

## Immediate execution order

1. Locate lawful local extractions for every exact target/revision.
2. Run each repository's `tools/hash_tree.py` and record sanitized target identity.
3. Build complete ExeFS inventories and executable/metadata maps.
4. Build complete RomFS inventories and base/update/DLC/version difference maps.
5. Populate the parallel content censuses while executable mapping proceeds.
6. Select one bounded reconstruction candidate per title with an explicit verification method.
7. Expand subsystem-by-subsystem and keep every revision/title distinction intact.
8. Extract/reconstruct non-ROM assets into Tsubaki with exact provenance and deduplication evidence.
9. Reconcile official web/archive references with actual game-side flags/tables/scripts/files.
10. Continue until every listed workstream has exhaustive coverage or an explicitly evidenced terminal status.

## Current hard gate

No Generation VIII ExeFS/RomFS extraction is currently present in the connected File Library. Therefore executable offsets, Build IDs, internal field names and filesystem paths that have not been directly observed remain intentionally unfilled rather than guessed.

The program itself is active now: all five canonical game repositories, the connected-systems research tracks, the complete data/map/character/mechanics censuses, distribution/history research, and the Tsubaki asset pipeline have been opened in parallel.
