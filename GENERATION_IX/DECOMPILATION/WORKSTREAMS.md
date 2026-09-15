# Generation IX Decompilation Workstreams

All workstreams below are active. A workstream may be blocked on verified local input, but it is not out of scope.

## 01 — Target identity and revision history

Track base applications, updates, DLC boundaries, platform variants, hashes, metadata and comparison targets. Historical revisions are preserved.

## 02 — Filesystem and resource inventory

Inventory every observed file and directory; record relative path, section, size, hash and structural classification. No representative sampling is accepted as complete coverage.

## 03 — Executable and function reconstruction

Map executable modules, sections, code/data regions, imports/exports where applicable, functions, call relationships, globals, constants and reconstructed symbols.

## 04 — Containers and serialization

Identify and document archives, compression, tables, schemas, offsets, indices, serialization formats and resource-loading relationships.

## 05 — Pokémon and forms

Track every in-scope species/form record, parameters, type data, stats, abilities, evolution/form rules, game-specific availability and title-specific implementation differences.

## 06 — Moves

Track every in-scope move record, parameters and special behavior. Scarlet/Violet and Z-A behavior are not assumed identical.

## 07 — Abilities

Track every in-scope ability record and special-case processing.

## 08 — Items and materials

Track standard items, held items, key items, evolution items, TMs, materials, food/picnic ingredients, Mega Stones and title-specific item classes.

## 09 — Battle systems

Scarlet/Violet: Terastallization, Tera Types, Tera Raid Battles and associated battle processing.

Z-A: real-time command flow, targeting, move timing, Mega Evolution, Mega Power, Z Mega Evolution and title-specific battle-state processing.

## 10 — Maps, world and collision

Track every field, interior, cave, zone, boundary, collision/navigation layer, connection, placement and world-state variation represented in data.

## 11 — Encounters

Track wild encounters, fixed encounters, outbreaks, special spawns, alpha Pokémon, raids and conditional encounter logic as applicable to each title.

## 12 — NPCs and trainers

Track named and unnamed NPCs, trainers, parties, battle conditions, rewards, affiliations, placement, progression variants and repeatability.

## 13 — Scripts, events, quests and flags

Track story scripts, cutscenes, quests/missions, flags, state machines, school content, postgame changes, DLC events and event-only spaces.

## 14 — Graphics and animation

Track models, textures, materials, shaders where observable, effects, animations, icons, sprites, tiles and presentation resources.

## 15 — UI

Track menus, HUD, battle UI, map UI, boxes, shops, communication UI and DLC/title-specific interface states.

## 16 — Text and localization

Track message resources, identifiers, languages, regional differences, version-specific wording and text-system formats.

## 17 — Audio

Track music, sound effects, voices where applicable, banks/containers, cue relationships and title/version differences.

## 18 — Communication and online

Track Union Circle, trades, battles, raids, Z-A Battle Club, Ranked Battles, server-delivered/client-side rule data and other communications as applicable.

## 19 — Events and distributions

Track Mystery Gift, official distributions, limited-time event raids, reward campaigns and client-side live-event data. Server-only facts are documented separately from recoverable client data.

## 20 — DLC and update differences

Track every observed addition, deletion and modification across revisions and DLC boundaries. Later versions never erase the earlier state from the research record.

## 21 — Pokémon HOME and linked titles

Track compatibility data, transfer restrictions, marks/metadata changes and linked-title behavior represented in Generation IX software or official linkage documentation.

## 22 — Unused, removed and legacy data

Record data that exists but is unused, unreachable, removed, leftover or of unknown purpose. Existence is not treated as proof of an intended feature.

## 23 — Bugs, glitches and patch behavior

Separate intended mechanics from bugs. Track reproduction conditions, affected versions and fix boundaries.

## 24 — Rebuild and verification

Build reproducible extraction-independent analysis tooling, parsers, schemas, reconstructed source and tests. Validation states are Unverified → Observed → Reproduced → Mapped → Matched.

## Coordination rule

Scarlet and Violet are compared aggressively but remain separate records. Pokémon Legends: Z-A is independently reconstructed and only cross-referenced where matching evidence exists.
