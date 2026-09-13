# Bank 01 — integrated survey + disassembly pass

## Semantic role

Both the canonical English disassembly and the Japanese multi-revision disassembly assign Bank 01 to the same broad module set. This is strong evidence that the **semantic organization is conserved even though byte locations diverge heavily between JP and international builds**.

### Known module sequence

- `data/sprites/facings.asm`
- `engine/battle/safari_zone.asm`
- `engine/movie/title.asm`
- `engine/pokemon/load_mon_data.asm`
- `data/items/prices.asm`
- `data/items/names.asm`
- `data/text/unused_names.asm`
- `engine/gfx/sprite_oam.asm`
- `engine/link/print_waiting_text.asm`
- `engine/overworld/sprite_collisions.asm`
- `engine/events/pick_up_item.asm`
- `engine/overworld/movement.asm`
- `engine/link/cable_club.asm`
- `engine/menus/main_menu.asm`
- `engine/movie/oak_speech/oak_speech.asm`
- `engine/overworld/special_warps.asm`
- `engine/debug/debug_party.asm`
- `engine/menus/naming_screen.asm`
- `engine/movie/oak_speech/oak_speech2.asm`
- `engine/items/subtract_paid_money.asm`
- `engine/menus/swap_items.asm`
- `engine/events/pokemart.asm`
- `engine/pokemon/learn_move.asm`
- `engine/events/pokecenter.asm`
- `engine/events/set_blackout_map.asm`
- `engine/menus/display_text_id_init.asm`
- `engine/menus/draw_start_menu.asm`
- `engine/link/cable_club_npc.asm`
- `engine/menus/text_box.asm`
- `engine/battle/move_effects/drain_hp.asm`
- `engine/menus/players_pc.asm`
- `engine/pokemon/remove_mon.asm`
- `engine/events/display_pokedex.asm`

## Actual ROM comparison

| Pair | Changed bytes | Diff runs | >=32-byte anchors | Anchored bytes | Largest anchor |
|---|---:|---:|---:|---:|---:|
| JP0A->JPB | 883 | 581 | 90 | 11,059 | 1,152 |
| JPB->JPC | 43 | 35 | 2 | 16,136 | 16,079 |
| JPC->JPD | 299 | 10 | 2 | 16,077 | 15,310 |
| JPD->EN | 15,534 | 322 | 40 | 2,858 | 293 |
| EN->FR | 14,150 | 317 | 55 | 4,782 | 1,213 |
| EN->DE | 14,035 | 351 | 55 | 4,882 | 1,303 |
| EN->IT | 14,011 | 341 | 64 | 5,482 | 1,303 |
| EN->ES | 14,090 | 353 | 57 | 4,969 | 1,251 |

## Interpretation

- `JPB → JPC` changes only 43 bytes in Bank 01 and has a 16,079-byte anchor: these two revisions are nearly layout-identical here.
- `JPC → JPD` changes 299 bytes and retains a 15,310-byte anchor: Rev D is still structurally very close in this bank.
- `JP0A → JPB` changes 883 bytes but 11,059 bytes are recoverable through >=32-byte anchors, so most module bodies can be mapped without assuming fixed addresses.
- `JPD → EN` changes 15,534 bytes; only 2,858 bytes are covered by >=32-byte anchors. The same semantic modules exist, but localization/CGB-era rebuild changes make direct address transfer unsafe.
- EN↔FR/DE/IT/ES also changes most bytes in this bank; language-specific strings and resulting pointer/layout shifts dominate.

## Disassembly action in the same pass

1. Use the known module order only as a semantic hypothesis, not as an address map.
2. Promote executable regions reachable from Bank 00 calls to labels/functions first.
3. Match long exact anchors to carry labels across JP revisions and international languages.
4. Treat embedded item names, menu strings, Oak speech text, naming/UI data and pointers as data until their tables are proven.
5. Keep every unresolved byte in exact form, so semantic promotion never sacrifices rebuildability.

## Status

**Survey:** semantic-reviewed  
**Disassembly:** semantic-in-progress  
**Rebuild safety:** Stage-0 byte-exact PASS  
**Next:** function-boundary discovery from cross-bank calls and long anchors; then module-by-module symbolic promotion.
