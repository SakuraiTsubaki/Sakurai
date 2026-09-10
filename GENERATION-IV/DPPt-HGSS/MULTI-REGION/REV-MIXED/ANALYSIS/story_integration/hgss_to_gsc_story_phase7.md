# HGSS → GSC Story Integration — Phase 7

## Scope

Goldenrod Rocket takeover → Team Rocket disguise → rival reveal → Radio Tower first ascent → fake Director → Basement Key → Goldenrod Underground → rival + switch puzzle → true Director → Card Key → second Radio Tower ascent → Proton/Ariana/Petrel/Archer hierarchy → Observation Deck → Team Rocket disband → Gold/Silver/HGSS wing rewards vs Crystal Clear Bell → Blackthorn handoff.

The detailed comparison matrix is `hgss_to_gsc_story_phase7.csv` (**42 rows**).

## Direct uploaded-ROM verification

Uploaded Korean HeartGold (`IPKK`) and SoulSilver (`IPGK`) were checked directly.

Their field-script NARC `a/0/1/2` remains byte-identical:

- size: `372012`
- members: `965`
- SHA-1: `0b911f52fda9c9324295a9bc7db2350433097529`
- HG = SS: **Yes**

### Phase 7 script members

| Index | Role | Size | Korean HG/SS member SHA-1 | HG=SS |
|---:|---|---:|---|---|
| 29 | D23R0101 — Goldenrod Radio Tower 1F / disguise reveal | 2992 | `dd860ac5f10aa073e811c42e03bbb3edbcc151c9` | Yes |
| 30 | D23R0102 — Radio Tower 2F | 1636 | `4b113c3c96996e947430b7d83ffbc6479098895e` | Yes |
| 31 | D23R0103 — Radio Tower 3F / Card Key shutter | 512 | `93ba1c232a96c9c638c3808c1ba5e239f6f055ed` | Yes |
| 32 | D23R0104 — Radio Tower 4F / Proton | 552 | `139637a1cb2964db15de745851bee6cef929677a` | Yes |
| 33 | D23R0105 — Radio Tower 5F / Petrel + Ariana | 868 | `9cee1c1b063c6c1ac00e61021865c94a040b7ad3` | Yes |
| 34 | D23R0106 — Observation Deck / Archer | 848 | `ba4f7c17653721dc4605e29977dd992f01e72810` | Yes |
| 94 | D37R0102 — Goldenrod Tunnel B1F / Rocket costume | 5484 | `8e1d77f5f369dc7881ed539c14dd9006e4912e23` | Yes |
| 96 | D37R0104 — Goldenrod Tunnel B2F / colored-gate puzzle + rival | 1808 | `b509e60f19d4ecbbb7f0406943df43b9ebe8caa5` | Yes |
| 97 | D37R0105 — Goldenrod Tunnel Warehouse / Director | 108 | `407fcf3d73a5ec96409b212a873d23882985328b` | Yes |

The identical script bytes do **not** mean HeartGold and SoulSilver produce identical story rewards. `D23R0106` performs a runtime game-version check and chooses the corresponding wing.

## Core conclusions

### 1. Radio Tower takeover must remain order-independent

Gen II and HGSS both avoid a simple “Pryce alone starts the takeover” architecture.

Crystal/Gen II standard scripts distinguish a Goldenrod pre-occupation state from the full Radio Tower occupation, while HGSS uses `VAR_MIDGAME_BADGES`. Chuck, Jasmine and Pryce each increment that midgame counter; whichever one becomes the third completed Leader advances the Rocket takeover state.

Target architecture:

`MIDGAME_BADGE_FACTS`
→ `GOLDENROD_ROCKET_PRESTAGE`
→ `RADIO_TOWER_TAKEOVER_ACTIVE`.

The order of Chuck/Jasmine/Pryce remains flexible.

### 2. Rocket disguise is a real system, not a sprite gag

HGSS has:
- `FLAG_SYS_ROCKET_COSTUME`;
- a Rocket player-avatar state/transition;
- script commands to set/check/clear costume state;
- field-action restrictions while disguised;
- NPC dialogue conditioned on the disguise;
- a dedicated story removal scene.

The player obtains the uniform in Goldenrod Tunnel after being mistaken for a newly recruited Rocket member. At Radio Tower 1F a grunt initially accepts the disguise, then Silver exposes the player and the game explicitly returns the avatar to normal and clears the costume flag.

Backport requirements:
- save persistence;
- avatar graphics;
- menu/field-action compatibility;
- NPC reaction hook;
- atomic removal;
- whiteout/save-reload recovery.

### 3. Ordinary Radio Tower content stays alive

The takeover is an alternate **state of the existing tower**, not a replacement dungeon.

Preserve:
- 1F reception;
- Radio Card quiz;
- Lucky Number Show;
- Crystal's Buena / Blue Card / Password Show;
- DJs and civilian dialogue;
- post-clear gifts;
- signs and ordinary objects.

All should switch behavior through occupation flags.

### 4. First ascent → fake Director → underground detour → second ascent is preserved

Shared skeleton:

`Tower 1F`
→ `2F`
→ `3F`
→ `4F`
→ `5F fake Director`
→ `Basement Key`
→ `Underground`
→ `rival`
→ `switch puzzle`
→ `Warehouse`
→ `true Director`
→ `Card Key`
→ `3F shutter`
→ `upper Tower`
→ `final commander`.

Do not flatten this into one uninterrupted tower climb.

### 5. Petrel is an authored expansion of the fake-Director role

GSC/Crystal:
- fake Director = anonymous `EXECUTIVEM_3`;
- defeat grants Basement Key.

HGSS:
- the Director actor visibly reveals **Petrel**;
- battle = `TRAINER_EXECUTIVE_PETREL_PETREL`;
- defeat grants `ITEM_BASEMENT_KEY`.

The integrated project keeps the anonymous Executive record **and** Petrel. The old record is not silently renamed or deleted.

### 6. Petrel also activates an HGSS-only Kimono Girl story beat

After Petrel:
- `FLAG_HIDE_UNDERGROUND_KIMONO_GIRL` is cleared;
- an Underground Kimono Girl scene becomes active;
- the later tunnel script hides her again and advances its own variable.

This is preserved as HGSS content, but it is **not** treated as the later five-Kimono-Girl ritual.

### 7. Both Underground puzzle implementations survive

Gen II/Crystal:
- 3 standard switches + emergency switch;
- 11 door groups;
- `wUndergroundSwitchPositions` values 0–7;
- door event flags and callback reconstruction.

HGSS:
- redesigned colored-room puzzle;
- red / green / blue switches toggle bordering gates;
- separate purple gate;
- ten temporary gate states.

These are mechanically different. The HGSS puzzle must not erase the Gen II puzzle data.

### 8. The Underground rival battle is shared, not duplicated

Both generations place an important Silver battle in this detour, with roster selected from the player's starter path.

The target uses one story battle and retains both source roster/layout definitions for validation.

### 9. True Director + Card Key remains the same story fact

In both GSC/Crystal and HGSS the true Director is in the warehouse and provides the Card Key.

The 3F shutter opening becomes a persistent global fact so save/reload never closes it incorrectly.

### 10. Named HGSS Executives are additions, not destructive renames

Preserve the anonymous GSC Executive trainer/dialogue records.

HGSS tower command chain:

- **4F: Proton**
- **5F: Ariana**
- **5F office/fake Director: Petrel**
- **Observation Deck: Archer**

Integrated approach:
- keep each anonymous GSC record in the data set;
- add all four named HGSS executives;
- if a legacy Executive is moved to make both encounters playable, mark that placement as **project integration modification**.

### 11. Archer requires the HGSS Observation Deck expansion

GSC/Crystal final commander is an anonymous male Executive on 5F.

HGSS places Archer on a separate Observation Deck (`D23R0106`).

Do not compress the existing fifth floor. Add the Observation Deck as expanded map content.

### 12. Radio Tower clear is atomic

Archer/final-boss completion should commit:

1. `RADIO_TOWER_CLEARED`
2. `ROCKET_TAKEOVER_ACTIVE = false`
3. Team Rocket disband fact
4. Rocket actor removal
5. civilian restoration
6. Director restoration
7. normal music/state
8. costume forced off
9. Card Key shutter preserved open
10. Blackthorn progression released.

A save between substeps must not produce a half-occupied Goldenrod.

## Reward divergence after the takeover

### Gold / Silver

`pret/pokegold` checks game version:
- **Gold → Rainbow Wing**
- **Silver → Silver Wing**

### Crystal

Crystal replaces the version wing reward with:
- **Clear Bell**
- Tin Tower entrance story-state update
- Team Rocket disband event.

That branch is critical to Crystal's Suicune storyline and remains intact.

### HeartGold / SoulSilver

The common HGSS Observation Deck script calls `GetGameVersion`:
- **HeartGold → Rainbow Wing**
- **SoulSilver → Silver Wing**

This is particularly useful for the backport architecture because the uploaded Korean HG/SS script member is identical; version behavior is data/runtime driven.

Recommended reward state:

- `GSC_GOLD_RAINBOW_WING_REWARD`
- `GSC_SILVER_SILVER_WING_REWARD`
- `CRYSTAL_CLEAR_BELL_REWARD`
- `HGSS_HG_RAINBOW_WING_REWARD`
- `HGSS_SS_SILVER_WING_REWARD`
- shared per-item claimed facts to prevent accidental duplication.

## Post-clear side rewards

Do not lose the tower's secondary rewards.

- GSC/Crystal 3F: Sunny Day TM.
- HGSS 3F: `ITEM_TM11`; Gen IV TM11 is Sunny Day.
- GSC/Crystal 4F DJ Mary: **Pink Bow**.
- HGSS 4F Mary: **BrightPowder**.

Pink Bow and BrightPowder are distinct authored rewards and both stay in the expanded item/reward model.

## Source manifest

### `pret/pokegold`
- `maps/RadioTower5F.asm`

### `pret/pokecrystal`
- `engine/events/std_scripts.asm`
- `maps/RadioTower1F.asm`
- `maps/RadioTower2F.asm`
- `maps/RadioTower3F.asm`
- `maps/RadioTower4F.asm`
- `maps/RadioTower5F.asm`
- `maps/GoldenrodUndergroundSwitchRoomEntrances.asm`
- `maps/GoldenrodUndergroundWarehouse.asm`
- relevant Gym badge-trigger scripts

### `pret/pokeheartgold`
- `scr_seq_0029_D23R0101.s`
- `scr_seq_0030_D23R0102.s`
- `scr_seq_0031_D23R0103.s`
- `scr_seq_0032_D23R0104.s`
- `scr_seq_0033_D23R0105.s`
- `scr_seq_0034_D23R0106.s`
- `scr_seq_0094_D37R0102.s`
- `scr_seq_0096_D37R0104.s`
- `scr_seq_0097_D37R0105.s`
- `src/sys_flags.c`
- `src/field_move.c`
- `src/player_avatar.c`
- `include/constants/flags.h`
- `include/constants/global_fieldmap.h`
- `include/constants/trainers.h`
- `include/constants/items.h`

## Phase 7 integrated state flow

`MIDGAME_BADGES_COMPLETE`
→ `GOLDENROD_ROCKET_PRESTAGE`
→ `TAKEOVER_ACTIVE / Elm cue`
→ `Tunnel Rocket-uniform event`
→ `ROCKET_COSTUME_ACTIVE`
→ `Radio Tower 1F admission`
→ `Silver reveals player`
→ `ROCKET_COSTUME_ACTIVE = false`
→ `first Tower ascent`
→ `legacy Executive records preserved`
→ `Petrel fake-Director reveal`
→ `BASEMENT_KEY`
→ `HGSS Underground Kimono Girl beat`
→ `Underground rival`
→ `GSC puzzle or HGSS expanded puzzle layer`
→ `true Director`
→ `CARD_KEY`
→ `3F shutter`
→ `Proton`
→ `Ariana`
→ `Archer on Observation Deck`
→ `ATOMIC_RADIO_TOWER_CLEAR`
→ `{Gold/HG: Rainbow Wing | Silver/SS: Silver Wing | Crystal: Clear Bell}`
→ `BLACKTHORN_STORY_RELEASED`.

## Deferred, not omitted — Phase 8

- Route 44 / Ice Path
- Blackthorn City
- Clair
- Dragon's Den
- badge qualification differences
- Elm / Master Ball
- HGSS Kimono Girls
- Bell Tower / Whirl Islands ritual
- HeartGold / SoulSilver mascot event differences
- Crystal Suicune / Clear Bell branch reconciliation
- exact point at which each mascot encounter becomes mandatory/optional
- save-state compatibility across the Crystal and HGSS legendary branches.
