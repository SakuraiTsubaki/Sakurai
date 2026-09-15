# Generation II Disassembly — Target Matrix

## Core retail ROM inventory currently under direct control

| Family | Verified/inventoried targets | Bank layout | Canonical repository | Source reconstruction front |
| --- | ---: | --- | --- | --- |
| Pocket Monsters Kin / Pokémon Gold | 8 | JP Rev.0/Rev.A: 64 banks; western/Korean targets: 128 banks | `SakuraiTsubaki/PocketMonsters-Kin-Disassembly` | Bank 00 |
| Pocket Monsters Gin / Pokémon Silver | 8 | JP Rev.0/Rev.A: 64 banks; western/Korean targets: 128 banks | `SakuraiTsubaki/PocketMonsters-Gin-Disassembly` | Bank 00 |
| Pocket Monsters Crystal Version / Pokémon Crystal | 7 | 128 banks | `SakuraiTsubaki/PocketMonsters-Crystal-Disassembly` | Bank 00 |

Total currently inventoried core retail ROM targets: **23**.

## Gold targets

- Japan Rev.0
- Japan Rev.A
- USA/Europe English Rev.0
- Germany Rev.0
- France Rev.0
- Italy Rev.0
- Spain Rev.0
- Korea Rev.0

## Silver targets

- Japan Rev.0
- Japan Rev.A
- USA/Europe English Rev.0
- Germany Rev.0
- France Rev.0
- Italy Rev.0
- Spain Rev.0
- Korea Rev.0

## Crystal targets currently inventoried

- Japan Rev.0
- USA/Europe English Rev.0
- USA/Europe English Rev.A
- Spain Rev.0
- Germany Rev.0
- France Rev.0
- Italy Rev.0

The absence of a target from the current inventory is not treated as proof that no other release/revision exists; additional revisions or region-specific builds must be added only after evidence is verified.

## Parallel technical fronts

Every target family is being investigated across the same major technical axes: ROM/banks/sections/pointers, code/control flow, data structures, SRAM/save/RTC, maps and world data, scripts/events/flags, Pokémon/moves/items/trainers/NPCs, encounters, battle and field systems, time/day/night/weekday systems, Pokégear/phone/radio, breeding/eggs/friendship/gender, communications and Time Capsule, graphics/sprites/tiles/fonts/palettes/animation/UI, audio/music/SFX/cries/radio, text/encoding/localization, unused/debug/development remnants, bugs/glitches/revision fixes, and exact-match rebuild verification.

## Cross-title comparison fronts

- Gold ↔ Silver common code/data and version-exclusive differences
- Gold/Silver ↔ Crystal additions, removals, modifications, relocation, and behavioral changes
- Japanese ↔ western ↔ Korean encoding, font, UI, ROM layout, text, bug fixes, communication behavior, and data-placement differences
- Generation I ↔ Generation II Kanto maps, locations, NPCs, trainers, encounters, scripts, music, story state, and Time Capsule conversion rules
- Generation II ↔ later games only as a separate comparison layer after original behavior is established

## Direct ecosystem fronts

- Generation I Time Capsule compatibility
- Link trade and link battle protocols
- Mystery Gift / infrared behavior
- Mobile System GB and Pokémon Communication Center
- Pokémon Stadium 2 connectivity and transfer-facing structures
- Official event distributions and payloads
- Region-specific services/peripherals directly connected to Generation II

## Execution rule

Bank 00 is the first source-reconstruction front, but it is not the only active workstream. Whole-ROM classification and subsystem inventories proceed in parallel so that every later bank can move from unknown bytes to identified structure and then to verified source without losing version, region, language, or revision provenance.
