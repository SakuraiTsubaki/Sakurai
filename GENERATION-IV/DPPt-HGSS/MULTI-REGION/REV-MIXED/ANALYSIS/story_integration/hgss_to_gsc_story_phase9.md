# HGSS → GSC Story Integration — Phase 9

## Scope

Route 27 → Tohjo Falls → Route 26 → Pokémon League Reception Gate → Victory Road → final pre-League rival → Indigo Plateau → Will → Koga → Bruno → Karen → Champion Lance → Hall of Fame → credits → Professor Elm / S.S. Ticket → Olivine Port → Professor Oak / National Dex → S.S. Aqua first voyage → Vermilion / Kanto opening.

Detailed event/system matrix: `hgss_to_gsc_story_phase9.csv` (**55 rows**).

## Direct verification of uploaded Korean HG/SS ROMs

The uploaded Korean HeartGold (`IPKK`) and SoulSilver (`IPGK`) ROMs were parsed directly again.

Field-script NARC:

- path: `a/0/1/2`
- size: `372012` bytes
- members: `965`
- SHA-1: `0b911f52fda9c9324295a9bc7db2350433097529`
- HeartGold = SoulSilver: **byte-identical**

### Phase 9 members checked directly

| Index | Script role | Size | SHA-1 | HG=SS |
|---:|---|---:|---|---|
| 221 | R27 — Route 27 / first step into Kanto | 252 | `b871de285877da5f7517533bea4f507706aa29f2` | Yes |
| 218 | R26 — Route 26 | 508 | `b9e0ff66050881e976af2ce09230dadbf47a2226` | Yes |
| 213 | R22R0101 — Pokémon League Reception Gate | 1484 | `0a25ca5fa2baff9ddce8decb6cebfc1236a49fae` | Yes |
| 110 | D43R0103 — Victory Road / final rival | 928 | `c5aa47827e499114dbd4b374df2f8d61816f1e77` | Yes |
| 113 | D45R0101 — Tohjo Falls main | 12 | `48b4ee58ea434e371436817766ba24a2dc74957c` | Yes |
| 114 | D45R0102 — Tohjo Falls hidden Giovanni room | 1040 | `9b5af5970c6b1345e5288264c1410867675912c4` | Yes |
| 819 | T10R0101 — Indigo Plateau lobby | 1428 | `912448e4075b1f142d4aaed8128c20d3af604460` | Yes |
| 820 | T10R0201 — Will | 228 | `930c0552065e65a29846bffb37243fbfe5c193b5` | Yes |
| 821 | T10R0301 — Koga | 228 | `d95dfb0ae6d6a08ed88886c76da41d484740d0d5` | Yes |
| 822 | T10R0401 — Bruno | 232 | `ce919bf36ec86aa6df1142dacd318fce1436989f` | Yes |
| 823 | T10R0501 — Karen | 232 | `883b4779e48fd240c921e9c6152d28ef4d194cca` | Yes |
| 824 | T10R0601 — Champion Lance | 980 | `3d7c57989e8cae327ee45443828f165fd46f14e7` | Yes |
| 825 | T10R0701 — Hall of Fame | 664 | `8c1c2334813075d957a5743286487068e1560baf` | Yes |
| 843 | T20R0101 — Elm Lab / S.S. Ticket | 4440 | `f6b402c841d48ce9d2219ecdd118c97f6b8b1c3a` | Yes |
| 152 | P01R0101 — Olivine Port / Oak National Dex | 1060 | `29515cae169b0be3bc386e2c9ad152fc6c33d6ed` | Yes |
| 156 | P01R0301 — S.S. Aqua main deck/state | 796 | `57ef943ada2dd7cef3cb1f24762e1411c8a6a97b` | Yes |
| 157 | P01R0302 — S.S. Aqua section | 864 | `b639aa602a05a4028550f5ad9683576885c086cf` | Yes |
| 158 | P01R0303 — S.S. Aqua section | 720 | `8c7c76e0f9f994f9596e85fe239e1a23955a119d` | Yes |
| 161 | P01R0306 — S.S. Aqua grandfather/granddaughter | 308 | `2529b7072efcada2d40198161f20d26d4bd7d8e2` | Yes |
| 162 | P01R0307 — S.S. Aqua section | 592 | `8754d5f043227e7217e1f5ce2084611b7e50241c` | Yes |

The binary equality does **not** mean there are no version differences. HGSS scripts frequently use runtime version checks or shared variables, so both ROMs can contain identical script bytecode while selecting different content later.

---

## Major conclusions

### Route 27 / Tohjo Falls

The “first step into Kanto” scene is original GSC content and HGSS preserves it. Tohjo Falls remains the normal Waterfall-based traversal dungeon, with the GSC Moon Stone retained. HGSS additionally contains the separate hidden `D45R0102` Giovanni room; this is a special Celebi/time-slip event and is not part of ordinary League progression.

### League Reception Gate / Victory Road

GSC explicitly checks all eight Johto badges at the Reception Gate. HGSS retains the eight-badge officer presentation and expands the same facility with later west-Kanto and Mt. Silver gate states. Victory Road's final rival battle is also legacy GSC story content; HGSS keeps the encounter position while dispatching to one of three remake rival trainer records according to starter choice.

### Indigo Plateau state machine

GSC already resets Will/Koga/Bruno/Karen/Lance room scenes and per-run defeat/door flags from the Indigo Plateau hub. HGSS preserves this run structure. Permanent `GAME_CLEAR`, League clear count and per-run progress therefore must be separate save states.

### First League trainer data

Gold/Silver and Crystal retain the same initial League party records. HGSS deliberately keeps much of the species/level skeleton but changes moves, held items, ability selection, trainer items, AI flags and per-Pokémon difficulty.

First-run Champion Lance:

| Source | Party levels |
|---|---|
| G/S | 44 / 47 / 47 / 46 / 46 / 50 |
| Crystal | 44 / 47 / 47 / 46 / 46 / 50 |
| HGSS | 46 / 49 / 49 / 48 / 48 / 50 |

HGSS Lance also has four Full Restores, AI flags, difficulty 250 on party entries, an ability override on Aerodactyl and a Sitrus Berry on the Lv50 Dragonite. A faithful backport therefore requires trainer-structure expansion rather than copying only species and levels.

### Hall of Fame

GSC Hall of Fame is already a world-state transaction: Elite Four clear, several actor/event states, Olivine postgame state, healing and the S.S. Ticket phone handoff are committed before the Hall-of-Fame/credits routine. HGSS expands this with a non-Egg party Hall-of-Fame animation, League-win statistics and per-species static/roamer restoration logic.

The HGSS source also documents a SoulSilver Hall-of-Fame code mistake: the SoulSilver Groudon branch checks the Kyogre caught flag. The original bug is documented; the integrated implementation uses the correct semantic species check.

### S.S. Ticket / Olivine / National Dex

The post-League S.S. Ticket and Fast Ship route are GSC legacy structure. HGSS adds Professor Oak at Olivine Port. Oak explicitly performs `NatDexFlagAction 1` and `EnableMassOutbreaks`, so National Dex and mass-outbreak unlocks are stored independently from S.S. Ticket ownership.

### S.S. Aqua

The missing-granddaughter first voyage is also original GSC content. HGSS preserves it with a multi-map voyage state machine. Metal Coat reward ownership is separated from the voyage-complete/arrival state so a full bag cannot permanently erase the reward. Arrival in Vermilion establishes the post-League Kanto handoff.

### HGSS upgraded Elite Four

HGSS League room scripts test the Kanto-badge counter against 8 and select `*_2` trainer records after all eight Kanto badges. G/S and Crystal do not have this remake upgraded-League dispatcher. The target uses a semantic `LEAGUE_TEAM_TIER` rather than raw variable checks.

## Recommended Phase 9 state architecture

```text
JOHTO_LEAGUE_ROUTE_RELEASED
ROUTE27_KANTO_FIRST_STEP_SEEN
TOHJO_FALLS_MAIN_PROGRESS
CELEBI_TIMESLIP_EVENT_UNLOCKED
CELEBI_GIOVANNI_EVENT_STATE
GIOVANNI_SPECIAL_BATTLE_RESOLVED
JOHTO_8_BADGES
VICTORY_ROAD_ADMISSION
RIVAL_VICTORY_ROAD_TRIGGERED
RIVAL_VICTORY_ROAD_RESOLVED
LEAGUE_RUN_ACTIVE
LEAGUE_RUN_STAGE
LEAGUE_TEAM_TIER
LEAGUE_CLEAR_COUNT
GAME_CLEAR
ELM_SS_TICKET_AVAILABLE
SS_TICKET_CLAIMED
OLIVINE_OAK_POSTGAME_SCENE_SEEN
NATIONAL_DEX_UNLOCKED
MASS_OUTBREAKS_UNLOCKED
SS_AQUA_FIRST_VOYAGE_STATE
SS_AQUA_GRANDDAUGHTER_FOUND
SS_AQUA_METAL_COAT_ENTITLED
SS_AQUA_METAL_COAT_CLAIMED
SS_AQUA_FIRST_VOYAGE_COMPLETE
BOAT_DIRECTION
BOAT_ARRIVED
KANTO_POSTGAME_ACCESS_OPEN
KANTO_BADGE_COUNT
WEST_KANTO_GATE_UNLOCKED
MT_SILVER_GATE_UNLOCKED
```

## Verification requirements

Route 27 one-time boundary scene; Waterfall success/failure; Moon Stone preservation; special Giovanni event isolation; Giovanni win/loss return; Reception Gate <8/8-badge tests; three starter branches of Victory Road rival; rival whiteout/retry; per-run League reset; whiteout at each Elite Four/Champion room; initial vs eight-Kanto-badge team tier; first-clear-only Champion state; Hall of Fame/credits save integrity; S.S. Ticket retry; Oak National Dex once-only event; mass-outbreak persistence; first S.S. Aqua prerequisites; granddaughter state over map changes; Metal Coat full-bag behavior; Vermilion arrival; repeat-voyage no-repeat behavior; per-species HGSS legendary/roamer restoration; corrected SoulSilver Kyogre/Groudon semantic check.

## Primary source manifest

### pret/pokegold
`maps/Route27.asm`, `maps/TohjoFalls.asm`, `maps/Route26.asm`, `maps/VictoryRoadGate.asm`, `maps/VictoryRoad.asm`, `maps/IndigoPlateauPokecenter1F.asm`, `maps/LancesRoom.asm`, `maps/HallOfFame.asm`, `maps/ElmsLab.asm`, Fast Ship maps, `maps/VermilionPort.asm`, `data/trainers/parties.asm`.

### pret/pokecrystal
Corresponding Route/League/Hall-of-Fame/Fast-Ship maps and `data/trainers/parties.asm`.

### pret/pokeheartgold
`scr_seq_0221_R27.s`, `scr_seq_0218_R26.s`, `scr_seq_0213_R22R0101.s`, `scr_seq_0110_D43R0103.s`, `scr_seq_0114_D45R0102.s`, `scr_seq_0819_T10R0101.s`, `scr_seq_0820_T10R0201.s` through `scr_seq_0825_T10R0701.s`, `scr_seq_0843_T20R0101.s`, `scr_seq_0152_P01R0101.s`, S.S. Aqua `P01R03xx` scripts and `files/poketool/trainer/trainers.json`.

## Phase 9 integrated flow

```text
New Bark east exit
→ Route 27 / first step into Kanto
→ Tohjo Falls
   └─ separately gated Celebi/Giovanni special event
→ Route 26
→ League Reception Gate
→ Victory Road / rival
→ Indigo Plateau
→ Will → Koga → Bruno → Karen → Lance
→ Mary + Oak
→ Hall of Fame / credits / GAME_CLEAR
→ Elm / S.S. Ticket
→ Olivine Port
→ [HGSS] Oak / National Dex / mass outbreaks
→ S.S. Aqua / missing granddaughter / Metal Coat
→ Vermilion
→ Kanto postgame access
```

## Deferred, not omitted — Phase 10

Vermilion and Lt. Surge; Power Plant/Machine Part/Magnet Train dependency chain; Lavender radio expansion; Snorlax; Diglett's Cave; Pewter/Brock; Cerulean/Misty; Celadon/Erika; Fuchsia/Janine; Seafoam/Blaine; Viridian/Blue; Kanto order differences; HGSS upgraded League activation; Mt. Silver/Red; all Kanto legendary/event additions and GSC↔HGSS differences.
