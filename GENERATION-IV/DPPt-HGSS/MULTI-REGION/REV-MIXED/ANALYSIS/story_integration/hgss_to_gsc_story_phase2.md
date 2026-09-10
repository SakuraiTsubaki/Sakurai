# HGSS → GSC Story Integration — Phase 2

## Scope

Second event-integration pass covering Route 30 / Mr. Pokémon's house through Violet City, Sprout Tower, Falkner, the Togepi Egg delivery, and the first HGSS Kimono Girl story hook.

The design rule remains unchanged: G/S/C progression facts stay authoritative where they already exist; HGSS-only actors, choreography, rewards, and state tracking are added around them. When two versions award the same functional progression at different locations, use a shared completion flag rather than duplicating the reward.

## Direct verification of uploaded HG/SS ROMs

The uploaded Korean HeartGold and SoulSilver ROMs were parsed through the NDS filesystem. `a/0/1/2` is the field-script NARC used in Phase 1. The following Phase 2 entries are byte-identical between the uploaded HG and SS copies:

| Script | Decomp label | Size | SHA-1 of script entry | HG = SS |
|---:|---|---:|---|---|
| 225 | `R29 — Route 29` | 2580 | `c4f38f8461b76cb7efeb563b4eb722b8eee2f346` | Yes |
| 227 | `R30 — Route 30` | 764 | `2219d622c9c906f33f744e360f80c5932b743d7a` | Yes |
| 229 | `R30R0201 — Mr. Pokémon's House` | 1116 | `37d4927366d1e7fe8dc974b3a87baf474fec83fe` | Yes |
| 16 | `D15R0101 — Sprout Tower 1F` | 100 | `ba7f4ec1c8155e8ba2fa9712ffaa98a4612ae75f` | Yes |
| 17 | `D15R0102 — Sprout Tower 2F` | 56 | `5f5977073068007c1349b41f5f4f00bb1ea00a7d` | Yes |
| 18 | `D15R0103 — Sprout Tower 3F` | 424 | `09f4d12c1dd1b80ffa8049da0fae3bd7042b04b3` | Yes |
| 857 | `T22 — Violet City` | 3244 | `aa3a3ab502aabe1c19590bb477caa914e3089543` | Yes |
| 858 | `T22FS0101 — Violet Poké Mart` | 388 | `89bb5d07e47ade351b8d579b3a3785b22dbef7c0` | Yes |
| 859 | `T22GYM0101 — Violet Gym` | 516 | `fe9526c49abe885e4b7cfc995c45f76abd26aeba` | Yes |

Result: this early-Johto Phase 2 story block can use one shared HGSS event specification. No HG-vs-SS script divergence was found in the checked entries.

## Event integration matrix

| ID | Event | Gold / Silver | Crystal | HeartGold / SoulSilver | Integration decision |
|---|---|---|---|---|---|
| PH2-001 | Route 30 pre-quest trainer battle blockade | Two youngsters' Pokémon are shown battling on Route 30; the scene occupies the route before the Mystery Egg quest is completed. | Same core blocking/battle spectacle, with the same Joey/Mikey setup and visible Pokémon actors. | Keeps the staged battle idea but uses explicit Rattata/Pidgey Pokémon objects and scripted animation in `R30`. | Preserve the GSC route gate and event timing. Treat HGSS as a presentation variant: retain the existing visible-Pokémon battle staging, optionally adopting HGSS's Rattata/Pidgey pairing and choreography instead of GSC's Rattata/Rattata pairing; do not change when the path opens. |
| PH2-002 | Mr. Pokémon gives the Mystery Egg | Mr. Pokémon receives the player, gives the Mystery Egg, explains the Day-Care origin, and turns the conversation over to Oak. | Same core scene and story fact. | Same story fact with longer movement choreography, follower handling, healing transition, and scene-variable updates. | Keep the GSC Mystery Egg flag and item handoff authoritative. Backport HGSS movement/healing choreography around the same completion state. |
| PH2-003 | Professor Oak gives the Pokédex | Oak evaluates the player, gives the Pokédex, then leaves for Goldenrod. | Same core scene. | Same sequence, plus registers Professor Oak as a Pokégear phone contact before leaving. | Preserve the GSC Pokédex acquisition and Oak departure. Add Oak's phone registration as an HGSS extension if the expanded phonebook is enabled. |
| PH2-004 | Elm panic call after Mr. Pokémon's house | The robbery call is armed by the Mr. Pokémon house sequence and triggers the return to New Bark. | Same core progression. | `R30` explicitly sets the Elm panic-call flag, places the phone call, and advances the Route 30 scene variable. | Keep the original GSC robbery-call story flag as canonical; adopt HGSS's explicit call-state bookkeeping to prevent duplicate or missed calls. |
| PH2-005 | Route 29 catching tutorial | Optional tutorial by the tutorial man; player may decline. Demonstrates catching a Lv. 5 Rattata and can be repeated later. | Same core optional/repeatable tutorial. | Replaced by the opposite-gender friend and Marill. The main scene proceeds directly into the tutorial and then gives 5 Poké Balls. | Preserve GSC player choice. If accepted, use the HGSS friend + Marill staging. Use one shared starter-ball receipt flag so rewards do not duplicate. |
| PH2-006 | First five Poké Balls | Elm's aide supplies 5 Poké Balls after the Mystery Egg is returned. | Same core reward structure. | The Route 29 friend gives 5 Poké Balls immediately after the catching demonstration. | Keep both scenes but only one actual reward. Whichever scene runs first sets the shared receipt flag; the later scene changes to acknowledgement/tutorial dialogue. |
| PH2-007 | HGSS Apricorn Box scene on Route 30 | No Apricorn Box key-item scene; Gen II handles the relevant field/item structure differently. | Same Gen II structural baseline. | A dedicated Route 30 Apricorn man scene gives the Apricorn Box and sets `FLAG_GOT_APRICORN_BOX`. | Backport only when the Gen IV-style Apricorn inventory/UI layer is implemented. Never gate main-story progression on this new key item. |
| PH2-008 | Violet City school guide / Earl | Earl and the Trainer School remain an early-city tutorial element. | Same core role. | Retains the school-guide concept with expanded pathing/escort scripting in Violet City. | Keep the GSC Earl event and backport only expanded movement/escort presentation. |
| PH2-009 | Sprout Tower vs. Violet Gym ordering | Sprout Tower and Falkner are loosely coupled; the Elder's Flash reward references the badge for field use, without HGSS's explicit before/after guide-state swap. | Same essential ordering freedom. | Defeating Elder Li flips the Violet Gym guide from a pre-Sprout object state to a post-Sprout state, making the tower an explicit early progression beat. | Do not delete GSC freedom. Let the Gym be entered early and use the HGSS guide as a soft gate/recommendation; branch follow-up dialogue if Falkner was beaten first. |
| PH2-010 | Sprout Tower rival/Elder confrontation | Rival has already beaten the Elder; Elder criticizes his harsh treatment of Pokémon. Rival dismisses the lecture and escapes. | Same core scene and characterization. | Preserves the same confrontation and dialogue role, with expanded movement/disappearance animation and dedicated state flags. | Treat the GSC scene as canonical. Backport HGSS choreography and safer completion flags without rewriting rival characterization. |
| PH2-011 | Sprout Tower Flash reward | Elder gives HM05 Flash after battle. | Same HM05 reward. | Elder gives TM70 Flash, then flips Violet Gym guide state flags. | For the GSC engine, keep HM05 as the canonical story reward. Record TM70 as the Gen IV counterpart and expose it only after expanded TM/HM architecture exists. |
| PH2-012 | Falkner / Zephyr Badge | Falkner awards Zephyr Badge and TM31 Mud-Slap; the badge sequence initiates Elm's assistant call. | Same core badge/TM/call sequence. | Same badge progression, but reward is TM51 Roost; winning sets Violet/Elm scene state for the Togepi Egg handoff. | Keep badge and Elm-call progression identical. Preserve TM31 and add TM51 only as an explicitly documented project integration reward after TM expansion. |
| PH2-013 | Togepi Egg handoff location | Elm's aide delivers the Togepi Egg in Violet's Pokémon Center after the first badge. | Same basic handoff location/role. | Elm calls after the badge, makes the aide appear in Violet Poké Mart, and the aide gives the Togepi Egg there. | Support both source locations with one shared `TOGEPI_EGG_CLAIMED` flag. First valid interaction gives the egg; the other becomes follow-up dialogue. |
| PH2-014 | First Kimono Girl story encounter in Violet | No equivalent main-story Kimono Girl event tied to the Togepi Egg. | No equivalent HGSS-style five-Kimono-Girl story chain here. | After the Poké Mart aide gives the Togepi Egg, Violet City scene state advances and exposes a Kimono Girl event on return to the overworld. | Add as the first HGSS Kimono Girl chain flag, triggered by shared Togepi Egg acquisition regardless of which aide location was used. |

## State-machine rules fixed in Phase 2

### First Poké Balls
Use one shared completion state:
- `EVENT_STARTER_POKE_BALLS_RECEIVED`
- `EVENT_HGSS_ROUTE29_FRIEND_TUTORIAL_SEEN`

GSC aide and HGSS friend scenes both remain, but only the first eligible scene transfers the five Poké Balls.

### Togepi Egg
Use one shared acquisition state across the GSC Pokémon Center and HGSS Poké Mart placements:
- `EVENT_TOGEPI_EGG_CLAIMED`
- `EVENT_TOGEPI_EGG_AIDE_PC_SEEN`
- `EVENT_TOGEPI_EGG_AIDE_MART_SEEN`

### Kimono Girl chain
The first HGSS Kimono Girl event should test the story fact, not the building:
- `EVENT_HGSS_KIMONO_VIOLET_SEEN`

It becomes available after `EVENT_TOGEPI_EGG_CLAIMED`, regardless of which aide location delivered the egg.

### Sprout Tower / Gym ordering
Preserve GSC freedom while importing HGSS narrative guidance:
- Gym remains enterable before Sprout Tower.
- HGSS-style guide state can recommend/redirect toward Sprout Tower.
- If Falkner is beaten first, Elder and guide follow-up dialogue branch accordingly.
- If Sprout Tower is cleared first, normal HGSS-style ordering is shown.

## Reward conflicts recorded for later data-system integration

- Elder: GSC `HM05 Flash` vs HGSS `TM70 Flash`
- Falkner: GSC `TM31 Mud-Slap` vs HGSS `TM51 Roost`

These are not to be solved by overwriting GSC data. The original GSC reward remains available; Gen IV reward exposure is handled additively after TM/HM expansion and is marked as a project integration rule.

## Source trail

- https://github.com/pret/pokegold/blob/master/maps/MrPokemonsHouse.asm
- https://github.com/pret/pokecrystal/blob/master/maps/MrPokemonsHouse.asm
- https://github.com/pret/pokecrystal/blob/master/maps/Route29.asm
- https://github.com/pret/pokecrystal/blob/master/maps/Route30.asm
- https://github.com/pret/pokecrystal/blob/master/maps/SproutTower3F.asm
- https://github.com/pret/pokegold/blob/master/maps/VioletGym.asm
- https://github.com/pret/pokecrystal/blob/master/maps/VioletGym.asm
- https://github.com/pret/pokeheartgold/blob/master/files/fielddata/script/scr_seq/scr_seq_0225_R29.s
- https://github.com/pret/pokeheartgold/blob/master/files/fielddata/script/scr_seq/scr_seq_0227_R30.s
- https://github.com/pret/pokeheartgold/blob/master/files/fielddata/script/scr_seq/scr_seq_0229_R30R0201.s
- https://github.com/pret/pokeheartgold/blob/master/files/fielddata/script/scr_seq/scr_seq_0018_D15R0103.s
- https://github.com/pret/pokeheartgold/blob/master/files/fielddata/script/scr_seq/scr_seq_0857_T22.s
- https://github.com/pret/pokeheartgold/blob/master/files/fielddata/script/scr_seq/scr_seq_0858_T22FS0101.s
- https://github.com/pret/pokeheartgold/blob/master/files/fielddata/script/scr_seq/scr_seq_0859_T22GYM0101.s
- https://github.com/pret/pokeheartgold/blob/master/files/fielddata/script/scr_seq/scr_seq_0630_T22_hdr.s

## Next comparison block

Phase 3:
1. Route 32 / Ruins of Alph access
2. Union Cave
3. Azalea Town
4. Slowpoke Well
5. Team Rocket's first major GSC ↔ HGSS comparison
6. Bugsy
7. Azalea rival battle
8. Ilex Forest / Farfetch'd
9. second Kimono Girl encounter and HGSS-only connective scenes
