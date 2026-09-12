# HGSS → GSC Story Integration — Phase 8

## Scope

Route 44 → Ice Path → Blackthorn City → Clair → Dragon's Den / Dragon Shrine → Rising Badge → Professor Elm / Master Ball → Ecruteak Dance Theater / five Kimono Girls → Clear Bell or Tidal Bell → Bell Tower or Whirl Islands → Ho-Oh / Lugia → New Bark east-exit / Route 27 handoff.

Detailed matrix: `hgss_to_gsc_story_phase8.csv` (**50 rows**).

## Direct verification of uploaded Korean HG/SS ROMs

The uploaded Korean HeartGold (`IPKK`) and SoulSilver (`IPGK`) source ROMs were parsed directly.

Their complete field-script NARC `a/0/1/2` remains byte-identical:

- NARC size: `372012`
- members: `965`
- SHA-1: `0b911f52fda9c9324295a9bc7db2350433097529`
- HG = SS: **Yes**

### Phase 8 checked members

| Index | Role | Size | Korean HG/SS member SHA-1 | HG=SS |
|---:|---|---:|---|---|
| 21 | D17R0110 — Bell Tower summit / Ho-Oh ritual | 2412 | `419aa8f5d37f87a5d84580677b2a9bdb70c6b9fa` | Yes |
| 99 | D39R0101 — Ice Path 1F / HM07 + Kimono Girl | 1044 | `42f411c512036ae21b08c0d6b1557b505b991253` | Yes |
| 104 | D40R0107 — Whirl Islands bottom / Lugia ritual | 3032 | `e9d02af4a9fb5b651d72f15371236e000e49e156` | Yes |
| 112 | D44R0103 — Dragon Shrine / quiz + Rising Badge + Dratini | 1840 | `ac8d973a57fa3e9e8b384b7a61f644340eac61a4` | Yes |
| 257 | R44 — Route 44 | 60 | `17f591fd00d1f9c884e74ffd4e78819385595752` | Yes |
| 842 | T20 — New Bark Town / east-exit gate | 5964 | `e9f12fa8897de031c5fcb64b6295f4a3b8749998` | Yes |
| 843 | T20R0101 — Elm Lab / Master Ball + Kimono redirect | 4440 | `f6b402c841d48ce9d2219ecdd118c97f6b8b1c3a` | Yes |
| 928 | T27R0501 — Ecruteak Dance Theater / five Kimono Girls | 3508 | `66446c5085f13dcd964f6622eb195110efcc8d70` | Yes |
| 943 | T30GYM0101 — Blackthorn Gym / Clair | 1044 | `71cb25d513f187109d9e1f5cae6a3a9ed5d3963b` | Yes |

The byte-identical scripts intentionally branch on game version at runtime. Ho-Oh/Lugia level, ritual destination, ritual bell and later opposite-wing acquisition therefore differ even though the checked HG/SS script members are identical.

## Major structural conclusions

### 1. Ice Path remains a full dungeon, not an HM corridor

Gold/Silver and Crystal place HM07 Waterfall on Ice Path 1F. HGSS retains the HM07 object state and adds a Kimono Girl story beat on the same floor.

Target rule:
- preserve all GSC floors, items, hidden items, boulder/ice puzzles and trainers;
- add HGSS geometry/content as a remake layer;
- retain the HGSS Ice Path Kimono Girl event as a separate story flag;
- one shared `WATERFALL_ENTITLEMENT`.

There is **no HM-number collision** here: both Gen II and HGSS use HM07 for Waterfall.

### 2. Clair defeat and Rising Badge are separate facts

Shared backbone:

`CLAIR_DEFEATED`
→ `DRAGONS_DEN_TRIAL`
→ `RISING_BADGE_OBTAINED`.

The trial differs by version.

#### Gold / Silver
The original qualification is **Dragon Fang**. Picking up the Dragon Fang in Dragon's Den triggers Clair's arrival and the Rising Badge award.

#### Crystal
Dragon Fang remains in the map, but the source explicitly comments that its special pickup script is left over from the GS event. Crystal moves qualification to the **Dragon Shrine five-question test**.

#### HGSS
HGSS inherits the Dragon Shrine test. Wrong answers are retryable but set a persistent failure fact. Passing the test causes Clair to give the Rising Badge.

The target therefore keeps both official trial implementations. Neither is rewritten as if it had always existed in all versions.

### 3. Dragon Shrine answer quality has real data consequences

Crystal and HGSS distinguish a perfect quiz from a run containing a wrong answer.

HGSS gift logic:
- species: Dratini
- level: 15
- if the quiz was perfect: force `MOVE_EXTREME_SPEED`
- nickname prompt is offered
- gift state is persisted.

The integrated save model should store semantic `DRAGON_QUIZ_PERFECT`, while retaining the original source flags for traceability.

### 4. Clair's TM rewards diverge and Crystal contains a duplicate-reward bug

- Gold / Silver: **TM24 DragonBreath**
- Crystal: **TM24 DragonBreath**
- HGSS: **TM59 Dragon Pulse**

The Crystal Dragon's Den source explicitly labels a bug in which Clair can give TM24 twice.

Target behavior:
- preserve the original bug in documentation;
- fix it with one successful-claim flag;
- retain legacy TM24;
- add Gen IV TM59 under the expanded TM namespace.

### 5. Master Ball handoff is the HGSS bridge into the Kimono Girl finale

G/S and Crystal already make Elm's Master Ball reward depend on Rising Badge and use a retry-safe successful-receipt event.

HGSS expands the scene:
1. Dragon Shrine completion changes Elm/New Bark scene state;
2. return to Elm;
3. Master Ball is awarded;
4. Elm explains the Master Ball;
5. Elm says the Kimono Girls are waiting in Ecruteak;
6. New Bark's east-exit state advances.

The physical reward and the story redirect must be separately tracked.

### 6. HGSS Master Ball handoff has a boundary anomaly

The checked HGSS Elm scene:
- sets item variable to `1` (Master Ball's item ID);
- tests item space;
- gives the item if space exists;
- if the space test fails, calls the bag-full routine;
- then still continues the Master Ball explanation, Kimono Girl redirect and subsequent scene transition.

The integrated target must **not** advance the reward transaction irreversibly without preserving a retrievable Master Ball entitlement. The safer GSC retry behavior is adopted.

### 7. The Kimono Girls are legacy characters before they are HGSS story machinery

Do not describe the five Kimono Girls as new HGSS actors.

GSC already has the Dance Theater trainer set and the legacy Surf reward route. HGSS:
- adds an earlier Rocket/Kimono Girl rescue beat;
- moves the HM03 Surf handoff to that expanded sequence;
- later reuses the five women for the mandatory post-eighth-badge gauntlet.

One physical HM03 is shared; all original battles and source reward provenance remain documented.

### 8. HGSS adds a five-battle late-game gauntlet

The checked Dance Theater script runs, in sequence:

1. Zuki
2. Naoko
3. Miki
4. Sayo
5. Kuni

Every battle checks the battle result. Whiteout/retry must be tested at every position in the sequence.

This late gauntlet is distinct from the original GSC Dance Theater progression.

### 9. Clear Bell has a cross-version provenance collision

Crystal:
- Radio Tower Director gives **Clear Bell (`とうめいなスズ`)**;
- it belongs to the Crystal Suicune/Tin Tower storyline.

HeartGold:
- the Kimono Girls give **Clear Bell** only after the late five-battle sequence;
- it belongs to the Ho-Oh summoning ritual.

SoulSilver instead receives the new **Tidal Bell (`うみなりのスズ`)**.

The item can be physically shared, but quest provenance cannot. Recommended flags:

- `CRYSTAL_CLEAR_BELL_FROM_DIRECTOR`
- `HGSS_CLEAR_BELL_FROM_KIMONO`
- `HGSS_TIDAL_BELL_FROM_KIMONO`
- `HAS_CLEAR_BELL`
- `HAS_TIDAL_BELL`.

This prevents a Crystal-integrated save from receiving a meaningless duplicate Clear Bell while still allowing the HGSS ritual state to progress.

## Legendary encounter matrix

| Source | Ho-Oh | Lugia | Primary story rule |
|---|---:|---:|---|
| Gold | Lv.40 | Lv.70 | wings unlock optional fixed encounters |
| Silver | Lv.70 | Lv.40 | wings unlock optional fixed encounters |
| Crystal | Lv.60 | Lv.60 | Crystal Suicune branch is the Johto legendary story focus |
| HeartGold | Lv.45 primary | Lv.70 secondary | five Kimono Girls + Clear Bell ritual required for primary progression |
| SoulSilver | Lv.70 secondary | Lv.45 primary | five Kimono Girls + Tidal Bell ritual required for primary progression |

These values are retained independently; there is no single “Gen II value” or “Gen IV value.”

### Crystal's Suicune climax is not replaced

Crystal's Tin Tower 1F sequence is its own authored event:
- Raikou and Entei may approach/leave;
- fixed Suicune battle: **Lv.40**;
- prior Cianwood / Route 42 / Route 36 Suicune waypoints are closed out;
- Eusine and the sages enter after the battle.

HGSS instead continues Suicune's pursuit into Kanto. The Crystal sequence stays available under its own branch state.

## HGSS ritual implementation

### HeartGold

The five Kimono Girls are enabled at the Bell Tower summit. The ritual uses:
- Clear Bell animation;
- synchronized dancer movement;
- dedicated sound effects;
- camera movement;
- special visual effects;
- Ho-Oh appearance cinematic.

Primary Ho-Oh: **Lv.45**.

### SoulSilver

The five Kimono Girls are enabled at the bottom of Whirl Islands. The corresponding ritual uses:
- Tidal Bell route;
- synchronized dancer movement;
- water/wave presentation;
- camera/effect choreography;
- Lugia appearance cinematic.

Primary Lugia: **Lv.45**.

The target hardware may require redrawing/resequencing the visuals, but the event's authored phases, timing relationships, audio cues and state changes are retained.

## The crucial pre-League divergence

### G/S and Crystal
The eighth badge releases the normal eastward League route without requiring an HGSS-style primary-mascot ritual.

### HGSS
The checked scripts form a real gate:

`Dragon Shrine passed`
→ `VAR_SCENE_NEW_BARK_EAST_EXIT = 1`
→ `Elm / Master Ball`
→ `VAR_SCENE_NEW_BARK_EAST_EXIT = 2`
→ `friend intercepts at New Bark east exit and moves the player west`
→ `Dance Theater`
→ `five Kimono Girls`
→ `Bell Tower/Whirl Islands ritual`
→ `primary mascot encounter resolved`
→ `VAR_SCENE_NEW_BARK_EAST_EXIT = 3`
→ eastbound League progression released.

Importantly, HGSS separates **encounter resolved** from **caught**. Catching sets `FLAG_CAUGHT_HO_OH` or `FLAG_CAUGHT_LUGIA`, while a non-whiteout resolved battle advances the story. The integrated game must never require capture if the source only requires encounter resolution.

## Secondary mascot in HGSS

The later Pewter script is version-aware:

- HeartGold → Silver Wing → Lugia enabled
- SoulSilver → Rainbow Wing → Ho-Oh enabled

The Kimono Girls remain hidden for this secondary encounter. The ritual is **not rerun**.

This is preserved as a later/post-League legendary-access state, not folded into the mandatory primary ritual.

## Recommended state architecture

```text
CLAIR_DEFEATED

GS_DRAGON_FANG_TRIAL_COMPLETE
CRYSTAL_DRAGON_SHRINE_COMPLETE
HGSS_DRAGON_SHRINE_COMPLETE
DRAGON_QUIZ_PERFECT
RISING_BADGE_OBTAINED

MASTER_BALL_FROM_ELM_ENTITLED
MASTER_BALL_FROM_ELM_CLAIMED

KIMONO_EARLY_EVENTS[]
KIMONO_LATE_GAUNTLET_PROGRESS 0..5
KIMONO_LATE_GAUNTLET_COMPLETE

CRYSTAL_CLEAR_BELL_FROM_DIRECTOR
HGSS_CLEAR_BELL_FROM_KIMONO
HGSS_TIDAL_BELL_FROM_KIMONO

HGSS_PRIMARY_RITUAL_READY
HGSS_PRIMARY_RITUAL_STARTED
HGSS_PRIMARY_MASCOT_RESOLVED

HO_OH_ENCOUNTER_RESOLVED
HO_OH_CAUGHT
LUGIA_ENCOUNTER_RESOLVED
LUGIA_CAUGHT
SUICUNE_ENCOUNTER_RESOLVED
SUICUNE_CAUGHT

HGSS_SECONDARY_WING_CLAIMED
JOHTO_LEAGUE_ROUTE_RELEASED
```

## Source-compatibility rule

For an HGSS-story integrated playthrough, the primary mascot ritual can be the canonical pre-League route.

However the engine must still be capable of reproducing:
- G/S: League route without mandatory mascot ritual;
- Crystal: its Suicune/Clear Bell ordering;
- HGSS: mandatory primary mascot resolution.

That distinction is a **project integration policy**, not a claim that all original games used the same gate.

## Primary source manifest

### `pret/pokegold`
- `maps/IcePath1F.asm`
- `maps/DragonsDenB1F.asm`
- `maps/ElmsLab.asm`
- `maps/TinTowerRoof.asm`
- `maps/WhirlIslandLugiaChamber.asm`

### `pret/pokecrystal`
- `maps/IcePath1F.asm`
- `maps/BlackthornGym1F.asm`
- `maps/DragonsDenB1F.asm`
- `maps/DragonShrine.asm`
- `maps/ElmsLab.asm`
- `maps/TinTower1F.asm`
- `maps/TinTowerRoof.asm`
- `maps/WhirlIslandLugiaChamber.asm`

### `pret/pokeheartgold`
- `scr_seq_0257_R44.s`
- `scr_seq_0099_D39R0101.s`
- `scr_seq_0943_T30GYM0101.s`
- `scr_seq_0112_D44R0103.s`
- `scr_seq_0843_T20R0101.s`
- `scr_seq_0842_T20.s`
- `scr_seq_0928_T27R0501.s`
- `scr_seq_0021_D17R0110.s`
- `scr_seq_0104_D40R0107.s`
- `scr_seq_0750_T03.s`
- `src/item.c`
- player/map/flag constants used by the above scripts

## Phase 8 integrated flow

```text
Route 44
→ Ice Path
→ HM07 Waterfall + preserved cave content
→ HGSS Ice Path Kimono Girl beat
→ Blackthorn
→ Clair battle
→ source-specific Dragon's Den qualification
   ├─ G/S: Dragon Fang
   └─ Crystal/HGSS: Dragon Shrine quiz
→ Rising Badge
→ Clair TM rewards retained separately
→ Elm / Master Ball
→ [HGSS story mode] Ecruteak Dance Theater
→ five Kimono Girls
→ HeartGold: Clear Bell / Bell Tower / Ho-Oh Lv45
   or
→ SoulSilver: Tidal Bell / Whirl Islands / Lugia Lv45
→ primary mascot encounter resolved
→ New Bark east-exit released
→ Route 27 / Pokémon League route.
```

## Deferred, not omitted — Phase 9

- Route 27
- Tohjo Falls
- Kanto/Johto boundary check
- Route 26
- Victory Road
- final pre-League rival battle
- Indigo Plateau
- Elite Four / Champion Lance
- Hall of Fame
- postgame start
- S.S. Aqua handoff
- Kanto opening state
- exact G/S vs Crystal vs HGSS League trainer/team/rule differences
- secondary legendary access timing after the League.
