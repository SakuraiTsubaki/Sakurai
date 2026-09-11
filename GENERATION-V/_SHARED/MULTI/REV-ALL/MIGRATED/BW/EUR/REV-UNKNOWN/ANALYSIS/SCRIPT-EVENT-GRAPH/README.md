# Pokémon Black / White Phase 5 — Script / Event Graph

## Scope

Phase 5 continues directly from the completed Phase 4 map relation graph. The target is the BW1 script NARC `/a/0/5/7` (899 members) and its links from ZoneHeader + zone entities (NPCs, interactables, triggers, initialization entries).

## Locked BW1 script format

Primary ROM evidence remains the uploaded Black/White ROMs. External technical references are used only to label and parse structures.

The field script format uses:

- a leading table of 32-bit relative offsets;
- each offset resolves as `pointer_position + rel32 + 4`;
- the pointer table terminator is `0xFD13`;
- opcodes are little-endian `u16`;
- opcode argument widths are command-specific (1, 2, or 4 bytes);
- relative call/jump arguments resolve from the position immediately after the command;
- movement sequences referenced by the Actor movement command are separate 4-byte movement records terminated by movement opcode `0xFE`.

FrostsGen5Editor contains a dedicated `bw1CommandList`; BW1 must not be decoded with the BW2 command table. This distinction is now a hard Phase 5 rule.

## High-value BW1 command families already identified

### VM / control flow
- `0x02 VMHalt`
- `0x04 VMCall(rel32)`
- `0x05 VMReturn`
- `0x1B RTCallGlobalAsync(script)`
- `0x1C RTCallGlobal(script)`
- `0x1D RTEndGlobal`
- `0x1E VMJump(rel32)`
- `0x1F VMJumpIf(cond, rel32)`
- `0x20 VMCallIf(cond, rel32)`
- `0x21 RTReserveScript(script)`

### flags / variables
- `0x23 FlagSet(flag)`
- `0x24 FlagReset(flag)`
- `0x25 FlagGet(flag, dest)`
- `0x26..0x2D` arithmetic / assignment variable operations (`Work*`)

### messages / dynamic words
- `0x34 MsgSystem`
- `0x35 MsgSystemAsync`
- `0x38 MsgInfo`
- `0x3A MsgMulti`
- `0x3C MsgActorEx`
- `0x3D MsgActor`
- `0x43 MsgPlaceSign`
- `0x48 MsgActorGendered`
- `0x49 MsgActorVersioned`
- `0x4D..` dynamic item/move/Pokémon/place/trainer-class word insertion family

### actors / NPCs
- `0x64 ActorCmdExec(actor, rel32)`
- actor spawn/show/hide/position/movement commands follow in the same BW1 table

### trainers
The BW1 header explicitly defines `CallTrainerBattle`, `CallTrainerMultiBattle`, trainer-eye commands, trainer battle result handling, trainer flags and trainer prize-item lookup. These are to be linked against Phase 3 trainer IDs rather than inferred from text.

### items / Pokémon / battles
The BW1 command set explicitly includes item add/sub/check operations; party/box Pokémon add and egg operations; and `CallWildBattle(species, level, flags)`. These will produce typed item/species/static-encounter edges.

## Phase 4 linkage invariant carried forward

For ZoneHeader index `z` (0..426):

- map script container = `/a/0/5/7` member `2*z`
- initialization script container = `/a/0/5/7` member `2*z+1`

Members 854..898 are outside the 427 zone pairs and remain global/special candidates until command-level analysis proves their role.

## Required outputs when ROM execution is available

- `script_members.csv` — 899-member structure/validity/entry-count audit
- `script_entries.csv` — every pointer-table entry
- `script_commands.csv` — every decoded opcode with byte offset, parameters and resolved targets
- `script_edges.csv` — call/jump/global-call/event semantic edges
- `zone_script_bindings.csv` — NPC/interactable/trigger/init entry to map-script entry bindings
- `event_flag_edges.csv`
- `event_variable_edges.csv`
- `event_text_edges.csv`
- `event_trainer_edges.csv`
- `event_item_edges.csv`
- `event_pokemon_edges.csv`
- `event_zone_edges.csv`
- `command_usage_summary.csv`

## Current execution note

The analysis environment's local container/Python transport is currently returning `TransportTimeoutError`, so the ROM-wide 899-member run has not been falsely marked complete. Command-table research and parser specification are being preserved here so the project state is not lost or reset.
