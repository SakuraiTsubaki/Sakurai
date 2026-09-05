# Pokémon FireRed Multi-Region Semantic Census — Stage 3

## Scope

This stage moves beyond whole-ROM/bank identity into decoded game semantics across all eight FireRed ROMs in the FIRE RED workspace.

Targets:

- Japanese Rev 0 / Rev 1 (`BPRJ`)
- English Rev 0 / Rev 1 (`BPRE`)
- German (`BPRD`)
- French (`BPRF`)
- Italian (`BPRI`)
- Spanish (`BPRS`)

Original ROM binaries are not stored in GitHub. This directory contains only analysis results and reproducible tooling.

## Method

Tables were not accepted solely from known community offsets. The census uses structure, record counts, internal pointer validity, terminators, repeated-record invariants, exact chunk relocation, and cross-ROM normalized semantic hashes. The `pret/pokefirered` decompilation is used as a structural reference for record layouts and symbol meaning; physical locations are verified against the eight workspace ROMs.

## High-confidence semantic table map

All offsets are file offsets from the start of each 16 MiB ROM.

| ROM | Trainers | Species names | SpeciesInfo | BattleMoves | Evolutions | Level-up ptrs | Wild headers | Map groups |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| JP Rev 1 | `0x001F97F0` | `0x001FF4D0` | `0x0020C9A4` | `0x00208E24` | `0x00211974` | `0x002159D4` | `0x0038C2F4` | `0x00311F70` |
| JP Rev 0 | `0x001FDFD8` | `0x00203CB8` | `0x0021118C` | `0x0020D60C` | `0x0021615C` | `0x0021A1BC` | `0x00390B34` | `0x00316758` |
| ES | `0x0023A234` | `0x0024164C` | `0x0024FF4C` | `0x0024C3CC` | `0x00254F1C` | `0x00258F7C` | `0x003C53A8` | `0x0034DE70` |
| DE | `0x0023E998` | `0x00245DB0` | `0x002546A8` | `0x00250B28` | `0x00259678` | `0x0025D6D8` | `0x003C9B04` | `0x003525CC` |
| EN Rev 0 | `0x0023EAC8` | `0x00245EE0` | `0x00254784` | `0x00250C04` | `0x00259754` | `0x0025D7B4` | `0x003C9CB8` | `0x003526A8` |
| EN Rev 1 | `0x0023EB38` | `0x00245F50` | `0x002547F4` | `0x00250C74` | `0x002597C4` | `0x0025D824` | `0x003C9D28` | `0x00352718` |
| FR | `0x00238ED4` | `0x002402EC` | `0x0024EBD4` | `0x0024B054` | `0x00253BA4` | `0x00257C04` | `0x003C4030` | `0x0034CAF8` |
| IT | `0x00237B6C` | `0x0023EF84` | `0x0024D864` | `0x00249CE4` | `0x00252834` | `0x00256894` | `0x003C2CC0` | `0x0034B788` |

The full table map, including trainer-class names, move names, items, dex mappings, cry conversion, TM/HM compatibility, egg moves, tutor moves, and TM move lists, is in the machine-readable Stage 3 bundle.

## Gameplay tables proven byte-identical across all eight ROMs

The following tables relocate between builds but have identical bytes after extraction:

| Table | Logical entries | ROM stride / size | SHA-256 |
|---|---:|---:|---|
| `gSpeciesInfo` | 412 | 28 bytes | `59d52667e509ee461319621ee493d4046b7af1337d9b1d9648497dccf660e7ae` |
| `gBattleMoves` | 355 | 12 bytes | `87bba4759789bd783ed2b3af3433e0bfa20ecdb8f1e2f5369624050119a52c3d` |
| `gEvolutionTable` | 412 × 5 | 6 bytes/evolution | `eacade6e06cf02d0c851d43d196d3dc99755ae2267da748d08b130e49bd770ed` |
| TM/HM compatibility | 412 | 8 bytes | `0294ac314df2c75dc8ca465d54297999d289e6e1dc371a91415f190c8d3ede1e` |
| Egg moves | 1,139 u16 | 2 bytes | `6c8a2954fe56483e3d0486e7f5424e67318fa7dc538f675265b06a65557d745f` |
| National-dex mapping | 412 u16 | 2 bytes | `15fa702a78675bba92fb0fea2468306c98ecf595eac6b0e88e5883905bbcb96a` |
| Secondary/regional dex mapping | 412 u16 | 2 bytes | `83be44217e5b0297b86a64aedc2d71d84038ad4b2775f9d33504f6bb9d857b8a` |
| Cry conversion | 412 u16 | 2 bytes | `811534f5a5d9217c43354480e93b31ff7d3c9ba8cbe222a149e6bc90aed7d072` |
| Move tutor list | 16 u16 | 2 bytes | `2e73d29460d402b26e4396f3110d6fb9bb7bf3a8a914561eebf0687ab826f7fe` |
| TM/HM move list | 58 u16 | 2 bytes | `28ce32b542191a0ad3a99d8722c488fe6a27988ff96c01bc13030fd7ed9f27d4` |

The 58-entry TM/HM move list occurs twice in every ROM; both copies are identical within each ROM and across all eight ROMs.

## Trainer system

- Trainer records: **743** (indices 0–742)
- Nonzero party pointers: **742**
- Unique party pointers: **742**
- Double-battle entries: **33**
- Every trainer record validates against its party format.
- The trainer table ends exactly at `gSpeciesNames` in every ROM.

Localization changes the physical structure:

- Japanese trainer record: **32 bytes**, trainer name field **6 bytes**
- Western trainer record: **40 bytes**, trainer name field **12 bytes**
- Japanese trainer-class name width: **11 bytes**
- Western trainer-class name width: **13 bytes**
- Trainer classes: **107**

After removing localized text and relocation-specific pointers, every trainer's numeric metadata and every party member are semantically identical across all eight ROMs.

Normalized trainer semantic SHA-256:
`f5c727c80e7976e331ed2baeccd32e1e33a5567e89cffbbc78dfeb25aecebfd3`

Mismatch count versus EN Rev 0: **0 for every ROM**.

## Level-up learnsets

- Pointer table entries: **412**
- Unique learnset arrays: **411** (`SPECIES_NONE` shares Bulbasaur's learnset pointer)
- Packed format: `(level << 9) | move`
- Terminator: `0xFFFF`
- Total decoded move records across the 412 species slots: **4,047**
- Maximum moves in one learnset: **18**
- Invalid decoded entries: **0**

Normalized per-species vector SHA-256, identical for all eight ROMs:
`167f403b1a095f6a7a5a33087c756f14753cbb3a7bd158fb5e0644157e2c02c2`

## Wild encounter system

- Headers: **132** plus one sentinel
- Unique map keys: **124**
- Unique `WildPokemonInfo` blocks: **227**
- Unique wild slot arrays: **227**
- Total referenced wild slots: **2,176**
- Invalid slots: **0**

Normalized wild-encounter semantic SHA-256, identical for all eight ROMs:
`ef33b4d03bc4ea60181aad955835ac79000d0f61f6821271a1b1bfbbc9898a52`

Thus the tested FireRed language/revision builds have the same wild species/level/rate semantics despite relocation.

## Map system

- Map groups: **43**
- Map-header pointers: **425**
- Unique map headers: **425**
- Unique map layouts referenced: **309**
- Unique event blocks: **425**
- Unique map-script pointers: **425**
- Unique connection blocks: **62**
- Warps: **1,294**
- Coordinate events: **228**
- Background events: **702**
- Map connections: **116**

Western builds contain **1,648 object events**. Both Japanese builds contain **1,647**.

### Verified Japanese-vs-Western map difference: Route 7

Across all 425 `(mapGroup, mapNum)` positions, the only event-count difference identified in this pass is group **3**, map **25** = **Route 7**:

- Japanese Rev 0 / Rev 1: **0 object events**
- EN/DE/FR/IT/ES: **1 object event**

The western/decomp map defines that object as a clone of the Celadon border CUT tree: `OBJ_EVENT_GFX_CUT_TREE`, position `(-8, 12)`, target `LOCALID_CELADON_BORDER_TREE`, target map `MAP_CELADON_CITY`.

This is a real map/event-structure difference, not a translated string difference. All compared map header scalar values and aggregate warp/coord/bg/connection counts otherwise matched in this pass.

## Pokémon and trainer graphics tables

- Pokémon front sprite table: **440 entries**
- Pokémon back sprite table: **440 entries**
- Normal palette table: **440 entries**
- Shiny palette table: **440 entries**
- Trainer picture table: **148 entries**
- Trainer palette table: **148 entries**
- Every referenced target in these six tables validated as compressed data.

Pokémon front compressed images are identical across all eight ROMs:
`19133f3ca84f3c3ce5ab0e3d7a8b1d55e36d7084f1c8c39b2182bbc45aec6b2f`

Pokémon back compressed images are also identical:
`79fb7f1e9590a7d750c13bd8c109c159360f80043e37d497aff5170a4d2fda6d`

Trainer palettes are identical across all eight:
`aababaf07121608982991ed0289d9c135c9e092ba3f883d87b03854e8a3be23b`

However, Japanese builds form a distinct graphic family for Pokémon normal palettes, Pokémon shiny palettes, and trainer pictures. Both Japanese revisions match each other, while all six western ROMs match each other for those categories. Therefore the region distinction is actual graphic content, not merely pointer relocation.

## Localization-layout findings

- Species names: JP **6-byte** records; western **11-byte** records
- Move names: JP **8-byte** records; western **13-byte** records
- Item structures: JP **40 bytes**; western **44 bytes**
- Trainer names: JP **6-byte** field; western **12-byte** field
- Trainer structures: JP **32 bytes**; western **40 bytes**

This explains substantial relocation of later tables while gameplay data itself remains identical.

## Reproducibility

`fire_red_semantic_census.py` validates the Stage 3 anchors against the eight ROMs without modifying them. A fresh verification run produced zero invalid level-up entries, zero invalid wild slots, valid wild sentinels, valid map groups, and exact trainer-table boundaries for all eight ROMs.

The three largest detailed CSV ledgers are stored as gzip-compressed, base64-wrapped text archives so all analysis data can be versioned through the text-only connector without storing ROM bytes. See `README_DATA_ARCHIVES.md`.

## Status and next semantic layers

Stage 3 proves the major gameplay skeleton and multiple content-equality/difference classes. It does **not** claim every ROM byte has a semantic label yet.

Next layers: Pokédex structures/descriptions; abilities; remaining item/UI lookup tables; full script/text ownership graph; charset/fonts; all layout/tileset/metatile/event records; audio; save/flags/vars/quest-log/mystery-gift/wireless/e-Reader; the JP Rev 0-only late-ROM region; and final verified patch-safe free-space mapping.
