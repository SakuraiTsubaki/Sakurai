# Generation VIII Decompilation — Master Tracker

This document tracks the active Generation VIII source-reconstruction effort across the five canonical game repositories. It is an index and research-control document; each game repository remains canonical for its own reconstructed source, manifests, tools, and verification evidence.

## Active targets

| Target | Canonical repository | Current stage | Immediate gate |
| --- | --- | --- | --- |
| Pokémon Sword | `SakuraiTsubaki/PocketMonsters-Sword-Decompilation` | Phase 0 — target intake | Verified local base/update/DLC inventory |
| Pokémon Shield | `SakuraiTsubaki/PocketMonsters-Shield-Decompilation` | Phase 0 — target intake | Verified local base/update/DLC inventory |
| Pokémon Brilliant Diamond | `SakuraiTsubaki/PocketMonsters-BrilliantDiamond-Decompilation` | Phase 0 — target intake | Verified local base/update inventory |
| Pokémon Shining Pearl | `SakuraiTsubaki/PocketMonsters-ShiningPearl-Decompilation` | Phase 0 — target intake | Verified local base/update inventory |
| Pokémon Legends: Arceus | `SakuraiTsubaki/PokemonLegends-Arceus-Decompilation` | Phase 0 — target intake | Verified local base/update revision inventory |

## Generation VIII scope

The active decompilation program covers:

- Pokémon Sword and Pokémon Shield;
- The Isle of Armor and The Crown Tundra as distinct Expansion Pass content targets;
- Pokémon Brilliant Diamond and Pokémon Shining Pearl as independent remake targets;
- Pokémon Legends: Arceus as an independent system/runtime/data target;
- update/revision differences, version-exclusive code/data/assets, and direct Pokémon HOME or save-link behavior when it is represented in the target games.

The five projects are developed in parallel. Sword is not a master implementation for Shield, BDSP, or PLA.

## Shared Phase 0 contract

Each canonical repository now uses the same evidence contract:

1. retail game images, complete redistributed game binaries, and console keys remain outside Git;
2. local extracted trees are inventoried by relative path, size, and SHA-256;
3. external title IDs, update histories, and public build identifiers are `reference_only` until independently matched to local material;
4. ExeFS and RomFS structure is recorded from observed files before semantic interpretation;
5. reconstructed source/data advances through `Unverified -> Observed -> Reproduced -> Matched`;
6. cross-version deduplication requires byte/hash evidence.

## Pairwise / cross-title rules

### Sword / Shield

Map both independently first. Compare matching revisions only after target identity is established. Preserve version-exclusive encounters, trainers, text, events, assets, executable differences, and Expansion Pass conditions.

### Brilliant Diamond / Shining Pearl

Map both independently first. The Nintendo DS Diamond/Pearl/Platinum games are comparison references, not assumed implementation templates. Base versus update content must also be preserved because major functionality shipped through updates.

### Pokémon Legends: Arceus

Keep PLA independent. Do not project conventional Sword/Shield or BDSP subsystem boundaries onto it. Field capture, research tasks, Strong/Agile Style, action order, Alpha Pokémon, space-time distortions, mass outbreaks, Massive Mass Outbreaks, rides, crafting, and mission/request systems become separate tracks only after their underlying code/data boundaries are observed.

## Immediate analysis order

1. Acquire or locate lawful local extractions for each target.
2. Run each repository's `tools/hash_tree.py` against the selected extraction.
3. Commit sanitized metadata manifests only; never commit complete game dumps or keys.
4. Build exact ExeFS inventories and executable section maps.
5. Build exact RomFS inventories and base/update/dlc difference maps.
6. Select one small, deterministic reconstruction candidate per title.
7. Expand subsystem-by-subsystem while continuously recording revision differences.

## Current input availability

No Generation VIII ExeFS/RomFS extraction is currently present in the connected File Library. Therefore executable offsets, internal field names, and filesystem paths that have not been directly observed remain intentionally unfilled rather than guessed.

## Repository artifacts established

All five canonical repositories now have an active decompilation start workflow. Sword, Shield, Brilliant Diamond, Shining Pearl, and Pokémon Legends: Arceus have active analysis queues; the non-Sword repositories have deterministic local-tree hashing and game-specific target manifests, while Sword already had those artifacts from its initial Phase 0 commit.

Update this tracker whenever a title advances from target intake to executable mapping, bounded reconstruction, or exact matching.
