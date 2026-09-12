# Pokémon Blue — 6-ROM full bank survey and disassembly baseline

Generated 2026-09-09 from the six uploaded read-only ROMs. No ROM binary is included.

## ROM identity

| Region | Banks | Mapper | SHA-1 | Existing exact disassembly |
|---|---:|---|---|---|
| JP | 32 | MBC1+RAM+BATTERY | `0da501e3e5c51ab8fef55b092dcdd7e6b050e424` | Narishma-gb/pokeblue |
| EN | 64 | MBC3+RAM+BATTERY | `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2` | pret/pokered |
| FR | 64 | MBC5+RAM+BATTERY | `47faa910d0e073c600665bf9c83b6bd17babdf8a` | einstein95/pokered-fr |
| DE | 64 | MBC5+RAM+BATTERY | `20e72dc6f41493eee1fdd0cef54214e6c3389688` | einstein95/pokered-de |
| IT | 64 | MBC5+RAM+BATTERY | `f69ed1a1332f04c24c7db899a09019bb045fa8b3` | not located |
| ES | 64 | MBC5+RAM+BATTERY | `7715e7b133e8634df48918b9138374110212a108` | einstein95/pokered-es |

All six header checksums and global checksums validate. Header version byte is 0 for all six.

## Round-trip baseline

A local lossless RGBDS source bootstrap was generated for all six ROMs with every byte represented as source data. Independent reconstruction reproduces the original SHA-1 for 6/6 ROMs. The byte-complete source itself is intentionally not committed because it would effectively redistribute the ROM content.

## Bank map

| Bank | Japanese Blue | Western Blue family | Status |
|---:|---|---|---|
| `$00` | RST/interrupt vectors; garbage header; cartridge header; Home; trailing garbage | RST/interrupt vectors; cartridge header; Home bank core | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$01` | Core engine/game flow (bank1); trailing garbage | Core engine/game flow: title, Oak intro, menus, movement, link, Pokédex display | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$02` | Audio set 1 + battle-music helper; trailing garbage | Audio set 1: SFX headers, music headers, SFX, audio engine 1, music 1 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$03` | Overworld/item core (bank3); trailing garbage | Overworld/item core: joypad, map metadata, wild mons, inventory, item effects, pathfinding, hidden-event helpers | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$04` | Move names; NPC sprites 1; font; Battle Engine 1; trailing garbage | NPC sprites 1; font graphics; Battle Engine 1 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$05` | NPC sprites 2; Battle Engine 2; trailing garbage | NPC sprites 2; Battle Engine 2 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$06` | Maps 1/2; play time; doors/ledges; trailing garbage | Maps 1/2; play time; doors and ledges | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$07` | Maps 3/4; Clear Save; Hidden Events 1; trailing garbage | Maps 3/4; Pokémon names; Hidden Events 1 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$08` | Audio set 2; Bill PC; audio engine 2; music 2 | Audio set 2; low-health alarm; Bill PC; audio engine 2; music 2 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$09` | Pokémon pics 1; Battle Engine 3; trailing garbage | Pokémon pics 1; Battle Engine 3 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$0A` | Pokémon pics 2; Battle Engine 4; trailing garbage | Pokémon pics 2; Battle Engine 4 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$0B` | Pokémon pics 3; Battle Engine 5; trailing garbage | Pokémon pics 3; Battle Engine 5 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$0C` | Pokémon pics 4; Battle Engine 6; trailing garbage | Pokémon pics 4; Battle Engine 6 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$0D` | Pokémon pics 5; slot machines; trailing garbage | Pokémon pics 5; slot machines/title2/link-versus related | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$0E` | Battle Engine 7; trailing garbage | Battle Engine 7; move/base-stat/cry/AI/evos-moves data | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$0F` | Battle Core | Battle Core and effects | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$10` | Pokédex/trade/intro/movie engine; trailing garbage | Pokédex/trade/intro/movie engine bank | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$11` | Maps 5/6; Pokédex rating; Hidden Events Core; trailing garbage | Maps 5/6; Pokédex rating; Hidden Events Core | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$12` | Maps 7/8; screen effects; trailing garbage | Maps 7/8; screen effects | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$13` | Trainer pics; Maps 9; predefs; trailing garbage | Trainer pics; Maps 9; predefs | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$14` | Maps 10; Battle Engine 8; Hidden Events 2; trailing garbage | Maps 10; Battle Engine 8; Hidden Events 2 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$15` | Maps 11/12; Battle Engine 9; diploma; trainer sight; trailing garbage | Maps 11/12; Battle Engine 9; diploma; trainer sight | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$16` | Maps 13/14; Battle Engine 10; Saffron guards; trailing garbage | Maps 13/14; Battle Engine 10; Saffron guards | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$17` | Maps 15/16; starter dex; Hidden Events 3; trailing garbage | Maps 15/16; starter dex; Hidden Events 3 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$18` | Maps 17/18; Cinnabar Lab fossils; Hidden Events 4; trailing garbage | Maps 17/18; Cinnabar Lab fossils; Hidden Events 4 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$19` | Tilesets 1; trailing garbage | Tilesets 1 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$1A` | Battle Engine 11; Version GFX; Tilesets 2; trailing garbage | Battle Engine 11; Tilesets 2 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$1B` | Tilesets 3 | Tilesets 3 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$1C` | Splash/Hall of Fame/healing/player animations/transitions/town map/icons/trades/palettes/save; trailing garbage | Splash/Hall of Fame/healing/player animations/battle transitions/town map/icons/trades/palettes/save | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$1D` | Maps 19/20/21; itemfinder/credits/vending/league-PC/hidden items; trailing garbage | Maps 19/20/21; credits/itemfinder/vending/league-PC/hidden-items | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$1E` | Battle animations/overworld effects/evolution/elevator/TM prices; trailing garbage | Battle animations; overworld cut/dust; fishing gfx; evolution; elevator; TM prices | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$1F` | Audio set 3; trailing garbage | Audio set 3: SFX/music headers, audio engine 3, music 3 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$20` | Not present (JP ROM ends at bank $1F) | Text 1 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$21` | Not present (JP ROM ends at bank $1F) | Text 2 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$22` | Not present (JP ROM ends at bank $1F) | Text 3 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$23` | Not present (JP ROM ends at bank $1F) | Text 4 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$24` | Not present (JP ROM ends at bank $1F) | Text 5 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$25` | Not present (JP ROM ends at bank $1F) | Text 6 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$26` | Not present (JP ROM ends at bank $1F) | Text 7 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$27` | Not present (JP ROM ends at bank $1F) | Text 8 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$28` | Not present (JP ROM ends at bank $1F) | Text 9 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$29` | Not present (JP ROM ends at bank $1F) | Text 10 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$2A` | Not present (JP ROM ends at bank $1F) | Text 11 | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$2B` | Not present (JP ROM ends at bank $1F) | Pokédex text | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$2C` | Not present (JP ROM ends at bank $1F) | Move names | confirmed EN/FR/DE/ES; inferred IT by matching Western layout |
| `$2D` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$2E` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$2F` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$30` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$31` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$32` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$33` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$34` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$35` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$36` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$37` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$38` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$39` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$3A` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$3B` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$3C` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$3D` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$3E` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |
| `$3F` | Not present (JP ROM ends at bank $1F) | All-zero padding bank | confirmed all-zero in EN/FR/DE/IT/ES |

## Key findings

- JP Blue ends at bank `$1F` (512 KiB, MBC1).
- Western Blue builds are 1 MiB. Meaningful data occupies `$00-$2C`; `$2D-$3F` are 19 completely zero-filled banks in EN/FR/DE/IT/ES.
- Bank `$1B` is byte-identical across all six ROMs.
- EN/FR/DE/ES use the same bank-level linker section layout through `$2C` in their exact disassembly projects.
- The Italian ROM strongly follows the same high-level Western architecture, but its labels/offsets must be ported and verified; no exact Italian full disassembly was located in the current search.

## Full disassembly procedure

1. Treat the local byte-perfect baseline as immutable.
2. Pin and import symbol maps from JP/EN/FR/DE/ES exact disassemblies.
3. Build cross-language symbol IDs per bank.
4. Port labels to Italian using conserved code islands, pointer tables, and multi-language alignment.
5. Replace Italian raw ranges with semantic SM83 instructions/data definitions bank-by-bank.
6. After each converted range/bank, require byte-identical reconstruction and original SHA-1.
7. Classify all remaining ranges as code, tables/pointers, text/scripts, maps, graphics, audio, padding/garbage, or hardware/RAM definitions.

### Exact reference repositories

- JP: `Narishma-gb/pokeblue` — builds SHA-1 `0da501e3e5c51ab8fef55b092dcdd7e6b050e424`.
- EN: `pret/pokered` — builds SHA-1 `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`.
- FR: `einstein95/pokered-fr` — builds SHA-1 `47faa910d0e073c600665bf9c83b6bd17babdf8a`.
- DE: `einstein95/pokered-de` — README target MD5 matches uploaded Blue (`a1ec7f07c7b4251d5fafc50622d546f8`).
- ES: `einstein95/pokered-es` — builds SHA-1 `7715e7b133e8634df48918b9138374110212a108`.
- IT: exact disassembly not located; use the other Western disassemblies as alignment references.
