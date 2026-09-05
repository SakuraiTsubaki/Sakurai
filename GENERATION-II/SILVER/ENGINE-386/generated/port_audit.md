# ENGINE-386 upstream port audit

Reference: `pokecrystal16 master..expand-mon-ID` (29 commits)
Target: `pret/pokegold`

- Changed paths: **398**
- Mechanical per-species base-stat files excluded from manual audit: **251**
- Audited non-mechanical paths: **147**
- Same paths present in pokegold: **116**
- Upstream patches that apply cleanly without hand-porting: **59**

## Priority engine surface

| Path | Category | Exists | Similarity | Clean apply |
|---|---|---:|---:|---:|
| `constants/16_bit_locking_constants.asm` | constants | no | - | no |
| `constants/16_bit_translation_constants.asm` | constants | no | - | no |
| `constants/npc_trade_constants.asm` | constants | yes | 0.977 | yes |
| `constants/pokemon_constants.asm` | constants | yes | 0.2007 | yes |
| `constants/pokemon_data_constants.asm` | constants | yes | 0.4697 | no |
| `constants/script_constants.asm` | constants | yes | 0.9531 | no |
| `data/pokemon/base_stats.asm` | pokemon_data | yes | 0.9922 | yes |
| `data/pokemon/cries.asm` | pokemon_data | yes | 1.0 | yes |
| `data/pokemon/dex_order_alpha.asm` | pokemon_data | yes | 1.0 | yes |
| `data/pokemon/dex_order_new.asm` | pokemon_data | yes | 1.0 | yes |
| `data/pokemon/egg_move_pointers.asm` | pokemon_data | yes | 0.9991 | yes |
| `data/pokemon/evos_attacks.asm` | pokemon_data | yes | 0.9975 | no |
| `data/pokemon/evos_attacks_pointers.asm` | pokemon_data | yes | 1.0 | yes |
| `data/pokemon/first_stages.asm` | pokemon_data | no | - | no |
| `data/pokemon/names.asm` | pokemon_data | yes | 1.0 | yes |
| `data/pokemon/palettes.asm` | pokemon_data | yes | 0.9996 | no |
| `data/pokemon/pic_pointers.asm` | pokemon_data | yes | 0.8355 | no |
| `engine/16/macros.asm` | engine | no | - | no |
| `engine/16/table_functions.asm` | engine | no | - | no |
| `engine/battle/core.asm` | engine | yes | 0.8581 | no |
| `engine/battle/effect_commands.asm` | engine | yes | 0.9755 | yes |
| `engine/battle/read_trainer_party.asm` | engine | yes | 0.2113 | no |
| `engine/battle/trainer_huds.asm` | engine | yes | 0.9882 | yes |
| `engine/events/battle_tower/battle_tower.asm` | engine | no | - | no |
| `engine/events/battle_tower/load_trainer.asm` | engine | no | - | no |
| `engine/events/bug_contest/judging.asm` | engine | yes | 0.9965 | yes |
| `engine/events/daycare.asm` | engine | yes | 0.9909 | yes |
| `engine/events/dratini.asm` | engine | no | - | no |
| `engine/events/fish.asm` | engine | yes | 0.9734 | yes |
| `engine/events/halloffame.asm` | engine | yes | 0.9631 | no |
| `engine/events/lucky_number.asm` | engine | yes | 0.9731 | no |
| `engine/events/magikarp.asm` | engine | yes | 0.9957 | yes |
| `engine/events/npc_trade.asm` | engine | yes | 0.9297 | yes |
| `engine/events/odd_egg.asm` | engine | no | - | no |
| `engine/events/overworld.asm` | engine | yes | 0.9858 | yes |
| `engine/events/pokerus/pokerus.asm` | engine | yes | 1.0 | yes |
| `engine/events/print_unown.asm` | engine | yes | 0.8807 | no |
| `engine/events/prof_oaks_pc.asm` | engine | yes | 1.0 | yes |
| `engine/events/shuckle.asm` | engine | yes | 0.9822 | yes |
| `engine/events/specials.asm` | engine | yes | 0.9217 | yes |
| `engine/events/treemons.asm` | engine | yes | 0.9714 | yes |
| `engine/events/unown_walls.asm` | engine | no | - | no |
| `engine/gfx/color.asm` | engine | yes | 0.8994 | yes |
| `engine/gfx/load_pics.asm` | engine | yes | 0.5016 | no |
| `engine/gfx/mon_icons.asm` | engine | yes | 0.4099 | yes |
| `engine/gfx/pic_animation.asm` | engine | no | - | no |
| `engine/gfx/sgb_layouts.asm` | engine | yes | 0.9948 | yes |
| `engine/items/item_effects.asm` | engine | yes | 0.9597 | no |
| `engine/link/init_list.asm` | engine | yes | 1.0 | yes |
| `engine/link/link.asm` | engine | yes | 0.6316 | no |
| `engine/link/mystery_gift.asm` | engine | yes | 0.7913 | no |
| `engine/link/mystery_gift_2.asm` | engine | yes | 1.0 | yes |
| `engine/link/time_capsule.asm` | engine | yes | 0.9834 | yes |
| `engine/menus/intro_menu.asm` | engine | yes | 0.7097 | no |
| `engine/menus/save.asm` | engine | yes | 0.4428 | no |
| `engine/menus/trainer_card.asm` | engine | yes | 0.9701 | yes |
| `engine/movie/evolution_animation.asm` | engine | yes | 0.7579 | no |
| `engine/movie/trade_animation.asm` | engine | yes | 0.9379 | no |
| `engine/overworld/decorations.asm` | engine | yes | 0.9978 | yes |
| `engine/overworld/events.asm` | engine | yes | 0.9483 | yes |
| `engine/overworld/overworld.asm` | engine | yes | 0.4995 | no |
| `engine/overworld/scripting.asm` | engine | yes | 0.9266 | no |
| `engine/overworld/variables.asm` | engine | yes | 0.9142 | no |
| `engine/overworld/warp_connection.asm` | engine | no | - | no |
| `engine/overworld/wildmons.asm` | engine | yes | 0.943 | no |
| `engine/pokedex/pokedex.asm` | engine | yes | 0.993 | no |
| `engine/pokedex/pokedex_2.asm` | engine | yes | 0.9809 | no |
| `engine/pokegear/radio.asm` | engine | yes | 0.8334 | no |
| `engine/pokemon/bills_pc.asm` | engine | yes | 0.978 | yes |
| `engine/pokemon/bills_pc_top.asm` | engine | yes | 1.0 | yes |
| `engine/pokemon/breeding.asm` | engine | yes | 0.9874 | yes |
| `engine/pokemon/correct_party_errors.asm` | engine | no | - | no |
| `engine/pokemon/evolve.asm` | engine | yes | 0.9937 | no |
| `engine/pokemon/mail_2.asm` | engine | yes | 0.2413 | no |
| `engine/pokemon/mon_menu.asm` | engine | yes | 0.9946 | yes |
| `engine/pokemon/mon_stats.asm` | engine | yes | 0.9797 | yes |
| `engine/pokemon/move_mon.asm` | engine | yes | 0.9803 | yes |
| `engine/pokemon/party_menu.asm` | engine | yes | 0.9524 | no |
| `engine/pokemon/search_owned.asm` | engine | no | - | no |
| `engine/pokemon/stats_screen.asm` | engine | yes | 0.3531 | no |
| `engine/printer/print_party.asm` | engine | yes | 0.9626 | no |
| `engine/printer/printer.asm` | engine | yes | 0.9972 | yes |
| `engine/rtc/rtc.asm` | engine | yes | 0.9018 | yes |
| `home/16bit.asm` | engine | no | - | no |
| `home/array.asm` | engine | yes | 0.783 | yes |
| `home/battle.asm` | engine | yes | 0.8995 | no |
| `home/copy_name.asm` | engine | yes | 1.0 | yes |
| `home/indirection.asm` | engine | no | - | no |
| `home/init.asm` | engine | yes | 0.6525 | no |
| `home/names.asm` | engine | yes | 0.8879 | no |
| `home/pokedex_flags.asm` | engine | yes | 1.0 | yes |
| `home/pokemon.asm` | engine | yes | 0.6622 | no |
| `home/serial.asm` | engine | yes | 0.9658 | no |
| `home/sram.asm` | engine | yes | 0.9063 | yes |

This is a port-surface audit only. A cleanly applying hunk is not considered functionally validated until Silver builds and runtime regression tests pass.
