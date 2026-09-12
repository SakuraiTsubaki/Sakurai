# HGSS → GSC Story Integration — Phase 4

## Scope

Route 34 / Day-Care → Goldenrod City → Radio Card / Whitney → Goldenrod Underground → Routes 35–37 → Sudowoodo → Ecruteak City → Burned Tower → Suicune/Eusine divergence → Ecruteak Dance Theater.

Fixed rule: **preserve G/S/C facts and progression freedom → retain Crystal expansions → add HGSS choreography, characters, and state → keep conflicting official variants traceable → prevent duplicate rewards and captures.**

The detailed 24-row event matrix is stored in `hgss_to_gsc_story_phase4.csv`.

## Direct verification of uploaded Korean HG/SS ROMs

The uploaded Korean HeartGold and SoulSilver ROMs were parsed through the NDS filesystem. Phase 4 field scripts were extracted from `a/0/1/2`.

| Index | Script | Size | SHA-1 | HG = SS |
|---:|---|---:|---|---|
| 23 | `D18R0101` Burned Tower 1F | 380 | `58a4e43d94df55de28f5fbd9c1385203405c229f` | Yes |
| 24 | `D18R0102` Burned Tower B1F | 872 | `1f03975f66695498d05e4a25d4d68374bfc86f64` | Yes |
| 29 | `D23R0101` Goldenrod Radio Tower 1F | 2992 | `dd860ac5f10aa073e811c42e03bbb3edbcc151c9` | Yes |
| 93 | `D37R0101` Goldenrod Tunnel 1F | 1204 | `33ebf8e834786a074d5c4f243323e5d1156f09c1` | Yes |
| 237 | `R34` Route 34 | 2744 | `f03cedf653a0ae1a8ceccdf5b07915c995cd834f` | Yes |
| 238 | `R34R0101` Day-Care | 532 | `b4b878a07fcf1136347cf8a0635199fb47c5dabd` | Yes |
| 240 | `R35` Route 35 | 596 | `bd859011d64cb5787dde1e634632cc7698ab671e` | Yes |
| 243 | `R36` Route 36 | 1552 | `2df5bf1cd1bf7f2243afb28993a29029baa25134` | Yes |
| 246 | `R37` Route 37 | 432 | `bd7c467c14ecbf543ddf664d13ce588491a7919c` | Yes |
| 885 | `T25` Goldenrod City | 2268 | `2bde63dd26099a8319514860ea9a887f08039e0a` | Yes |
| 886 | `T25GYM0101` Goldenrod Gym | 744 | `51b9232ea4b4d381c6843486299ef003a8c43837` | Yes |
| 920 | `T27` Ecruteak City | 1244 | `e016f7a427fa9c447aae476dd020f211fe4c534a` | Yes |
| 928 | `T27R0501` Ecruteak Dance Theater | 3508 | `66446c5085f13dcd964f6622eb195110efcc8d70` | Yes |

No HG-vs-SS byte difference was found in these 13 checked main-story field scripts. This only establishes commonality for the checked script layer; encounters, version-exclusive Pokémon, graphics, text resources, music, and later mascot events remain separate audit targets.

## Integration decisions

### Route 34 / Day-Care

GSC Day-Care access and mechanics remain intact. HGSS adds the opposite-gender protagonist + Marill introduction and registers both Day-Care contacts.

Use:
- `EVENT_HGSS_DAYCARE_INTRO_SEEN`
- `EVENT_DAYCARE_MAN_REGISTERED`
- `EVENT_DAYCARE_LADY_REGISTERED`

The HGSS presentation must never become a prerequisite for the original Day-Care function.

### Goldenrod Radio Card and Whitney

GSC/Crystal let the five-question Radio Card quiz exist independently from the Whitney challenge. HGSS stages Whitney at the quiz before she returns to the Gym.

Use:
- `VAR_WHITNEY_LOCATION = UNRESOLVED | RADIO_TOWER | GYM | POST_BADGE`
- `EVENT_RADIO_CARD_OBTAINED`
- `EVENT_HGSS_WHITNEY_RADIO_CAMEO_SEEN`

If the Radio Tower is visited first, play the HGSS cameo. If the Gym is challenged first, keep GSC freedom and suppress/convert the later cameo. The Radio quiz never becomes a false mandatory gym gate.

Whitney's battle itself has no reward conflict: GSC, Crystal and HGSS all preserve the crying sequence, Plain Badge and TM45 Attract.

### Goldenrod Underground

Preserve all GSC persistent content:
- Coin Case
- haircut brothers
- weekday/time merchants
- trainers
- later Basement Key / switch infrastructure

Add HGSS separately:
- opposite-gender protagonist + Marill tunnel scene
- Fashion Case
- remake-specific choreography

`ITEM_FASHION_CASE` must only become active when the accessory/fashion subsystem is actually implemented. Do not replace it with an unrelated item.

Early exploration state, service state and future Rocket-takeover state must remain independent.

### Sudowoodo / Rock Smash

GSC, Crystal and HGSS all keep the fixed Lv.20 Sudowoodo encounter after using the SquirtBottle. Import HGSS's explicit static-encounter result handling while preserving the original encounter.

Track at least:
- `EVENT_SUDOWOODO_TRIGGERED`
- `EVENT_SUDOWOODO_CLEARED`
- `EVENT_SUDOWOODO_CAUGHT`

Rock Smash is a real data conflict:
- GSC/Crystal: `TM08 Rock Smash`
- HGSS: `HM06 Rock Smash`

Do not overwrite the GSC TM08 record. Preserve its source reward, then after Gen IV HM expansion register/add the HGSS HM06 representation separately:
- `EVENT_GSC_TM08_ROCK_SMASH_CLAIMED`
- `EVENT_HGSS_HM06_ROCK_SMASH_REGISTERED`

HGSS also adds Berry Pots plus three Oran Berries and three Pecha Berries after Sudowoodo. This is additive and does not replace GSC berry-tree content.

### Burned Tower / Eusine / Morty

Gold/Silver provide the baseline: the three legendary beasts are released and roaming is initialized, without Eusine driving a Suicune-specific plot.

Crystal adds:
- Eusine's introduction
- Morty's investigation role
- the rival/floor-collapse presentation
- a dedicated Suicune narrative

HGSS retains the Crystal-style character layer and expands the Suicune chase further.

Integration order:
1. preserve the G/S beast-release fact;
2. preserve Crystal's Eusine/Morty and rival/collapse story;
3. add HGSS follower-safe choreography and extended chase states.

### Legendary beast state model

Never use one `SUICUNE_DONE` flag.

Shared:
- `EVENT_BEASTS_RELEASED`
- `EVENT_RAIKOU_ROAMING_ACTIVE`
- `EVENT_ENTEI_ROAMING_ACTIVE`
- `EVENT_SUICUNE_CAUGHT`

Source-aware:
- `EVENT_GS_SUICUNE_ROAMING_AVAILABLE`
- `EVENT_CRYSTAL_SUICUNE_STORY_ACTIVE`
- `EVENT_HGSS_SUICUNE_STORY_ACTIVE`

HGSS B1F explicitly creates two roamers after the release while Suicune enters its dedicated story path. Gold/Silver preserve the older roaming-Suicune source behavior; Crystal preserves its own Suicune story.

All Crystal and HGSS waypoint flags remain separate. Catching Suicune through any valid route sets the one global caught state. Later waypoints become Eusine epilogue/dialogue only and must never create a second catchable Suicune.

### Ecruteak Dance Theater / Kimono Girls

GSC/Crystal:
- five Kimono Girls are individual early trainers;
- defeating all five is the prerequisite for HM03 Surf.

HGSS:
- an early Rocket Grunt harasses a Kimono Girl;
- defeating the Grunt resolves the scene and HM03 is awarded at this stage;
- the five-sister consecutive challenge is repurposed as a later major story event.

Do not replace either structure.

Keep separate:
- five GSC individual battle flags;
- `EVENT_HGSS_KIMONO_VIOLET_SEEN`
- `EVENT_HGSS_KIMONO_ILEX_SEEN`
- `EVENT_HGSS_KIMONO_ECRUTEAK_RESCUED`
- `EVENT_HGSS_KIMONO_GAUNTLET_DONE`

For Surf:
- `EVENT_HM03_SURF_CLAIMED`
- `VAR_HM03_SURF_SOURCE = GSC_FIVE_KIMONO | HGSS_RESCUE`

Either official-derived prerequisite may grant HM03 once in the integrated build. Completing the other event chain later still resolves its story and dialogue, but never awards a duplicate HM03.

The later HGSS five-sister gauntlet must have its own teams and completion state; it cannot reuse the early GSC trainer-clear flags.

## Integrated Phase 4 route

`Route 34`
→ `GSC Day-Care + HGSS friend/Marill introduction`
→ `Goldenrod free exploration`
→ `optional Radio Card + conditional Whitney cameo`
→ `Whitney / Plain Badge / TM45`
→ `GSC Underground services + HGSS Fashion Case event`
→ `Routes 35–36`
→ `SquirtBottle / Lv.20 Sudowoodo`
→ `GSC TM08 provenance + HGSS HM06 registration + Berry Pots`
→ `Route 37`
→ `Ecruteak`
→ `Crystal/HGSS Eusine + Morty + Burned Tower rival`
→ `three beasts released`
→ `Raikou/Entei roaming + version-aware Suicune state`
→ `GSC five Kimono battles retained`
→ `HGSS Rocket/Kimono rescue added`
→ `HM03 awarded once`
→ `HGSS later five-sister gauntlet retained separately`.

## Primary source manifest

`pret/pokegold`
- `maps/BurnedTowerB1F.asm`

`pret/pokecrystal`
- `maps/RadioTower1F.asm`
- `maps/GoldenrodGym.asm`
- `maps/GoldenrodUnderground.asm`
- `maps/Route36.asm`
- `maps/BurnedTower1F.asm`
- `maps/BurnedTowerB1F.asm`
- `maps/DanceTheater.asm`

`pret/pokeheartgold`
- `scr_seq_0023_D18R0101.s`
- `scr_seq_0024_D18R0102.s`
- `scr_seq_0029_D23R0101.s`
- `scr_seq_0093_D37R0101.s`
- `scr_seq_0237_R34.s`
- `scr_seq_0238_R34R0101.s`
- `scr_seq_0240_R35.s`
- `scr_seq_0243_R36.s`
- `scr_seq_0246_R37.s`
- `scr_seq_0886_T25GYM0101.s`
- `scr_seq_0920_T27.s`
- `scr_seq_0928_T27R0501.s`
- later Suicune scripts `T06`, `R42`, `R14`, `R25` used only to confirm that the HGSS chase continues beyond this phase.

Direct binary verification:
- uploaded Korean HeartGold ROM
- uploaded Korean SoulSilver ROM
- field-script NARC `a/0/1/2`

## Deferred, not omitted

Later chronological passes will separately verify:
- the complete Crystal Suicune waypoint order and activation conditions;
- the complete HGSS Suicune route through Kanto, including retries/failure states;
- Morty Gym;
- Pokéathlon/National Park remake additions;
- Goldenrod Radio Tower takeover and Underground infiltration;
- the exact late HGSS five-Kimono teams and mascot-summon requirements;
- map, graphics, sound, animation and UI conversion.

These are deferred so later official states are not prematurely collapsed into Phase 4.
