# Pokémon Black / White Phase 4 — Map relation graph

## Scope

This phase reconstructs the BW1 field-zone relationship graph directly from the uploaded ROMs. The structural spine is `/a/0/1/2` (427 x 0x30-byte zone headers), joined to `/a/1/2/5` (zone entities), `/a/0/5/7` (map/init script containers), `/a/0/0/2` text member 89 (English map names), and `/a/1/2/6` (wild encounters).

## ROM-derived invariants

- 427 ZoneHeaders, each 48 bytes.
- ZoneHeader `zoneId` is a permutation-free identity mapping 0..426: every value occurs exactly once.
- Zone-entities NARC has 428 members. Member 427 is a special 4-byte zero entry and is the only member not directly referenced by a ZoneHeader.
- `mapScriptsIndex = 2 * zoneHeaderIndex` and `initializationScriptsIndex = 2 * zoneHeaderIndex + 1` for all 427 zones. Thus script members 0..853 are 427 exact zone pairs. Members 854..898 (45 files) are outside the per-zone pair range and are retained as global/special candidates.
- Exactly 112 ZoneHeaders contain encounter IDs 0..111, each exactly once. The other 315 have packed encounter value 0xFFFF (low 13-bit index = 0x1FFF), meaning no encounter container.
- Zone headers, zone entities, script archive, and system text archive are byte-identical between the uploaded Black and White ROMs. The encounter archive is version-specific; 29 of 112 members differ.
- Fixed zone-entity totals: 662 interactables, 2,257 NPCs, 886 warps, 373 triggers. Tail sections contain 296 initialization entries and 72 trigger-related entries.
- Warp target zones resolve to 0..426 except six records using 0xFFFF, preserved as special targets.

## ZoneHeader field layout

The parser uses the 0x30-byte layout documented by BeaterLibrary and validates every referenced index against these BW1 ROMs. Unknown fields remain unknown/candidate and are not promoted to facts. See `zone_headers.csv` in the generated working package.

## Version policy

Black and White share map topology here. Version differences are attached at the encounter-member level rather than duplicating false structural differences. The generated `zone_links.csv` has one row per zone per version so the version-specific encounter SHA and `encounter_differs_bw` flag remain explicit.

## Next boundary

Phase 5 should disassemble the 427 main map-script containers plus the 45 global/special script members, resolve NPC/trigger/interactable script identifiers, and connect commands to flags, variables, trainers, items, static Pokémon, text, and story progression.
