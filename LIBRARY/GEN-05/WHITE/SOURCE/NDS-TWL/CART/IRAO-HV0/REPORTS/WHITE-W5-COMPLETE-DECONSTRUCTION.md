# Pokémon White IRAO-HV0 — W5 complete structural deconstruction

Status: **White-first full-ROM structural deconstruction corpus generated and internally cross-validated.**

Source binding: `SWEETNDS-f94d4578` / SHA-1 `f94d4578956487c09fee20809a591e858017769e`. The ROM binary itself is not committed.

## Completion definition

This phase treats “deconstruction” as six linked layers: physical ROM region → NitroFS/overlay → container/member → record schema → cross-reference → semantic confidence. Unknown values are retained, never silently discarded.

## Whole-ROM inventory

- FAT entries: **484**
- named NitroFS files: **247**
- ARM9 overlay records: **237**
- NARC archives: **237**
- NARC members exhaustively catalogued: **54,054**
- every named file and every NARC member has size, class/signature and SHA-256 in the corpus.

The `native/` manifests make the extraction reproducible without committing the source ROM.

## Text layer

Both BW1 message archives were structurally decoded with the Generation V block/table/encryption rules:

- `a/0/0/2`: **288** system/message members
- `a/0/0/3`: **472** story/field members
- total decoded message members: **760**
- total indexed strings: **56,700**
- non-empty strings: **52,419**

High-confidence banks include item names/descriptions, Pokémon names, location/map names, abilities, trainer names/classes, type names, move names and move descriptions. `domains/text/known_banks.tsv` records the verified bank map.

## Pokémon / move / item layer

The corpus includes record-level tables for:

- `a/0/1/6` personal data, including the 18 alternate-personal slots and the special final Unova-Dex lookup member
- `a/0/1/7` all eight growth tables
- `a/0/1/8` all level-up learnsets
- `a/0/1/9` all evolution records
- `a/0/2/0` base/baby-species table
- `a/0/2/1` all 560 move records
- `a/0/2/4` all 627 item records, with raw bytes retained where semantics remain unresolved
- `a/1/2/3` all 650 egg-move family records

The 1300-byte final member of personal data is proven to be the `National species ID → BW Unova Pokédex number` lookup (`0..493 → 999`, Victini `494 → 0`, Genesect `649 → 155`).

## Trainer layer

- `trdata a/0/9/2`: 616 members; trainer IDs 1..615 are 20-byte records
- `trpoke a/0/9/3`: index-aligned with trdata
- format 0/1/2/3 selects exact per-Pokémon widths **8/16/10/18 bytes**
- all 615 non-dummy trainer parties satisfy the width × party-count relation with **zero mismatches**

## Encounter layer

`a/1/2/6` contains 112 encounter members:

- 100 × 232-byte single-season structures
- 12 × 928-byte structures = exactly four 232-byte seasonal blocks

Every walking/double/special-grass/surf/rippling-surf/Super-Rod/rippling-fishing slot is emitted to `encounter_slots.tsv`.

## Zone / map / entity layer

`a/0/1/2` is **427 × 0x30-byte ZoneHeader**. The corpus decodes:

- map type/change
- texture and matrix indices
- main/init-script indices
- text container
- Spring/Summer/Autumn/Winter BGM IDs
- encounter ID and packed auxiliary bits
- zone and parent-zone IDs
- map-name index + display mode
- weather/camera fields
- battle background and field-permission flags (bike/run/Escape Rope/Fly/BGM change)
- matrix/camera boundary, name icon and Fly coordinates

The map-name index joins directly to system text member 89 (117 map/location strings).

`a/1/2/5` contains 428 entity members. Direct White totals:

- interactables/furniture: **662**
- NPCs: **2,257**
- warps: **886**
- triggers: **373**
- initialization-script references in member tails: **296**
- variable/value/script trigger-related records: **72**

All 428 entity tails parse cleanly. Record schemas preserve raw bytes and expose the field names established by current BW reverse-engineering.

## Script layer — new invariant

`a/0/5/7` contains **899** members.

For every zone `z=0..426`:

- member `2*z` = main event-script pointer container
- member `2*z+1` = **byte-identical copy of the parsed entity-member tail for the same zone**

This identity holds for all **427/427** zones. It resolves the previous ambiguity around the “initialization script container”: the odd partner is not a normal event-opcode container; it mirrors the initialization/trigger metadata stored after the entity records.

All 427 even main-script members have valid BW relative-pointer tables terminated by `0xFD13`. Among members 854..898, **44/45** also validate as pointer-script containers. Member **865** is the sole non-pointer global/special data member and is retained intact as an unresolved special structure.

Opcode-level CFG/disassembly remains a separate executable-semantics layer rather than being guessed from bytes. The public BW1 command definitions from Frost's Gen5 Editor / related BW reverse-engineering are retained as cross-check references for that next layer.

## Strong invariants revalidated

- White source SHA-1 matches the bound dump.
- `mainScriptIndex = 2 × zone` for all 427 zones.
- `initializationScriptsIndex = 2 × zone + 1` for all 427 zones.
- `zoneId = zone index` for all 427 zones.
- encounter IDs 0..111 are each referenced exactly once; 315 zones have no encounter member.
- all 427 main-script pointer tables validate.
- all 427 odd initialization members equal the corresponding entity tail byte-for-byte.
- all 428 entity tails structurally validate.

## Repository corpus

The generated corpus is split by domain under this release root. It includes physical/file/overlay/NARC manifests, Pokémon/move/item/trainer/encounter tables, decoded field structures, zone/entity/script cross-reference tables, text-bank catalogs, summary assertions and the reproducible extraction tool.

## Remaining semantic work (not hidden as “complete”)

Structural deconstruction is now broad and reproducible, but full semantic reverse engineering still has explicit open layers:

1. ARM9 and all 237 overlays: function/symbol-level disassembly and runtime call graph.
2. Event scripts: full BW1 opcode disassembly, control-flow graphs and cross-references to flags/vars/items/trainers/Pokémon/text.
3. Graphics/3D/UI/audio: format-specific decode/render plus runtime usage graph.
4. Item and several entity/ZoneHeader auxiliary fields: execution-path validation before naming unknown values.
5. Unused/dummy classification: reachability proof from code/scripts rather than labels inherited from old tools.

These are kept in `UNRESOLVED.tsv`; none are discarded or filled with invented semantics.

## External cross-check sources

- PlatinumMaster/BeaterLibrary — `ZoneHeader`, `ZoneEntities`, `Proxy`, `NPC`, `Warp`, `Trigger`, `InitializationScript`, `TriggerRelated` schemas.
- Project Pokémon / PPRE — BW archive paths, Gen V message decryption, encounter structures.
- FrostFalcon/FrostsGen5Editor — BW1 event-script command IDs/parameter widths and script-container behavior.

Direct measurements from the supplied White ROM remain authoritative when an external note conflicts.
