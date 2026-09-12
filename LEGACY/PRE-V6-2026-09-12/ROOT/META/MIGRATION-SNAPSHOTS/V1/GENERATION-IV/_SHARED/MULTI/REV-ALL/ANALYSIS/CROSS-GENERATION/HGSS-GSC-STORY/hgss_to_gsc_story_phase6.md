# HGSS → GSC Story Integration — Phase 6

## Scope

Route 42 → Mt. Mortar branch → Mahogany Town → Route 43 → Lake of Rage → Red Gyarados → Lance → Mahogany suspicious shop → Team Rocket Headquarters B1F/B2F/B3F → Petrel/Ariana expansion → Electrode generator → Whirlpool → Pryce → Rocket Radio Tower takeover activation handshake.

The detailed event-by-event matrix is stored in `hgss_to_gsc_story_phase6.csv` (32 rows).

## Direct verification of uploaded Korean HG/SS ROMs

The Korean HeartGold (`IPKK`) and SoulSilver (`IPGK`) source ROMs were checked directly. Their complete field-script NARC `a/0/1/2` remains byte-identical:

- NARC size: `372012`
- members: `965`
- SHA-1: `0b911f52fda9c9324295a9bc7db2350433097529`
- HG = SS: **Yes**

Phase 6 member hashes:

| Index | Role | Size | SHA-1 | HG=SS |
|---:|---|---:|---|---|
| 88 | D35R0101 — Mahogany souvenir shop / hidden entrance | 1372 | `2eef0ff38f1afc0b629748ddb006bf5177ee8a12` | Yes |
| 89 | D35R0102 — Team Rocket HQ B1F | 4668 | `5797c4b2045313feaa48a08c77be1eb7502d672b` | Yes |
| 90 | D35R0103 — Team Rocket HQ B2F | 2800 | `0979a7d95a6c232910912568ee4d6406139dfdfc` | Yes |
| 91 | D35R0104 — Team Rocket HQ B3F | 1420 | `def9bf4e44bec9e6c6382fdac4b6b7000e5556c9` | Yes |
| 252 | R42 — Route 42 | 936 | `1b02603d85c3b43d956e9c71aa2c43e9ea2b5672` | Yes |
| 255 | R43 — Route 43 | 48 | `39aab2efece5e4e5ecf5e6fc6ea4f2bbe44d7d97` | Yes |
| 256 | R43R0201 — Route 43 gatehouse | 544 | `a6d3fee83138376126084bc51537248c62c127a7` | Yes |
| 930 | T28 — Mahogany Town | 876 | `7ac08d68e7dd46537e808446b59681afe14c5824` | Yes |
| 932 | T28GYM0101 — Mahogany Gym / Pryce | 528 | `e1401e5456acfe693ed8dbd359e20b4111b25e9a` | Yes |
| 938 | T29 — Lake of Rage | 1960 | `8b16a24df8f1550e96f544fb9d0587626d78b567` | Yes |

This only proves equality for this field-script archive. Text NARCs, map matrices, encounter data, graphics, sound, trainer data and version-exclusive mascot data remain independent verification targets.

## Phase 6 integration decisions

### 1. Crystal and HGSS Suicune diverge at Route 42

The shared HGSS path established in the prior phase is:
`Burned Tower → Cianwood → Eusine battle → Route 42`.

At Route 42:
- **Crystal** activates its Route 36 Suicune scene.
- **HGSS** activates the later Vermilion Suicune state.

Therefore:
- `SUICUNE_WAYPOINT_ROUTE42_SEEN`
- `CRYSTAL_SUICUNE_NEXT_ROUTE36`
- `HGSS_SUICUNE_NEXT_VERMILION`
- one global `SUICUNE_CAUGHT`

No later branch may create a second catchable Suicune after the global caught state is set.

### 2. Route 42 Strength is a moved official reward

HGSS gives HM04 Strength from the Route 42 hiker event. The Gen II source obtains Strength through its legacy Olivine-side event.

Do not delete either event:
- `EVENT_GSC_HM04_STRENGTH_SOURCE`
- `EVENT_HGSS_HM04_STRENGTH_SOURCE`
- `EVENT_HM04_STRENGTH_CLAIMED`

Only the HM itself is single-instance.

### 3. Route 43 Rocket occupation remains intact

Crystal's Route 43 gate implements a ¥1000 Rocket shakedown. HGSS preserves the ¥1000 subtraction and uses explicit Rocket/guard visibility flags.

After the hideout:
- Rockets disappear;
- the legitimate guard returns;
- TM36 Sludge Bomb becomes obtainable.

All three are tied to one hideout-clear transaction rather than separate loosely synchronized room flags.

### 4. Red Gyarados is retained exactly as a major fixed encounter

Required source facts:
- species: Gyarados
- level: 30
- forced shiny
- Red Scale reward
- Lance becomes available after the encounter

The target should use HGSS-style explicit static outcome/caught tracking while retaining the original GSC event and side content.

Recommended state:
- `EVENT_RED_GYARADOS_STARTED`
- `EVENT_RED_GYARADOS_RESOLVED`
- `EVENT_RED_GYARADOS_CAUGHT`
- `EVENT_RED_SCALE_CLAIMED`
- `EVENT_RED_SCALE_EXCHANGED`

Mr. Pokémon's Red Scale → Exp. Share exchange remains intact.

### 5. Lance recruitment keeps the player's refusal choice

GSC/Crystal and HGSS both permit declining Lance's request and agreeing later.

Do not auto-accept the Rocket investigation after Red Gyarados.

### 6. Mahogany secret-shop scene is an excellent direct backport

Keep:
- suspicious shop state;
- Lance;
- Dragonite;
- Hyper Beam/attack presentation;
- hidden staircase reveal;
- post-reveal shop state.

HGSS movement/sound/follower handling replaces only presentation plumbing, not the GSC event facts.

### 7. Rocket HQ security/trap content is not reduced

The GSC B1F contains:
- five separately tracked security-camera regions;
- repeated Rocket response battles;
- twenty-one individual exploding-trap coordinates;
- Koffing / Voltorb / Geodude trap encounters.

HGSS rebuilds the alarm presentation and still contains Rocket trap battles.

The integrated target must preserve the entire GSC encounter set. Map conversion may move coordinates, but “representative” reduction is prohibited.

### 8. The two GSC boss passwords survive HGSS voice recognition

GSC:
- `SLOWPOKETAIL`
- `RATICATE TAIL`
- then Murkrow provides `HAIL GIOVANNI`

HGSS:
- retains the investigation;
- Petrel is exposed;
- Murkrow mimics Petrel's voice;
- voice recognition unlocks the transmitter door.

Merged expanded sequence:

`learn password A`
→ `learn password B`
→ `legacy executive/security layer`
→ `Petrel disguised as Giovanni`
→ `defeat Petrel`
→ `Murkrow follows`
→ `HAIL GIOVANNI source fact retained`
→ `Petrel voice imitation`
→ `voice-authenticated transmitter door`.

The added dependency chain is a **project integration rule**, while each source fact remains separately documented.

### 9. Unnamed GSC executives are not deleted

Gen II has generic male/female Rocket Executive trainer records performing roles later assigned to named HGSS executives.

Preservation architecture:
- keep `EXECUTIVEM_4` battle/data/dialogue;
- keep `EXECUTIVEF_2` battle/data/dialogue;
- add **Petrel** as the named B3F authority;
- add **Ariana** as the named B2F authority.

For the full integrated storyline, the generic executives can be relocated to preceding command/security encounters. That relocation is explicitly marked **project integration modification**, not original HGSS canon.

### 10. Petrel's Giovanni disguise is added in full

HGSS B3F actually stages a Giovanni object, reveals Petrel, then starts `TRAINER_EXECUTIVE_PETREL_PETREL_2`.

This is not a cosmetic rename of the Gen II executive. It is a distinct authored scene and must receive its own actor/state flags.

### 11. Ariana battle upgrades the GSC confrontation to a real partner Multi Battle

GSC:
- player battles the female Executive;
- Lance separately deals with the assisting grunt.

HGSS:
- actual `MultiBattle`
- player + Lance
- versus Ariana + Rocket Grunt 25.

The integrated build retains the GSC single-battle record and uses the HGSS partner Multi Battle as the expanded main confrontation once the double-battle system is available.

### 12. Electrode generator remains six objects / three player battles

GSC and HGSS both retain the core generator logic:
- six Electrode;
- player resolves three;
- Lance handles the opposite side;
- Lv.23 player-facing static encounters.

Track each player-side Electrode separately and make final shutdown atomic.

### 13. Whirlpool has a real HM-number conflict

- GSC/Crystal: **HM06 Whirlpool**
- HGSS: **HM05 Whirlpool**
- HGSS `sTMHMMoves`: HM05 → `MOVE_WHIRLPOOL`, HM06 → `MOVE_ROCK_SMASH`

Architecture:
- common move entitlement: `MOVE_WHIRLPOOL`
- source records: `GSC_HM06_WHIRLPOOL`, `HGSS_HM05_WHIRLPOOL`
- field-use permission: `Glacier Badge + MOVE_WHIRLPOOL`

Never key the field engine directly to a generation-specific HM item number.

### 14. Rocket Hideout clear must be atomic

One transaction must:
1. mark the HQ cleared;
2. shut down the Rocket radio signal;
3. remove active HQ Rockets;
4. restore Route 43 guard;
5. remove Route 43 toll Rockets;
6. update Mahogany NPC/shop/Gym states;
7. finish the Electrode state;
8. preserve all previously completed trap/password/rival flags.

This prevents save/reload desynchronization.

### 15. Pryce keeps both official TM rewards

- GSC/Crystal: **TM16 Icy Wind**
- HGSS: **TM07 Hail**

The Glacier Badge is shared. The TM rewards are not interchangeable.

### 16. HGSS Pryce TM07 bug is fixed, not reproduced as target behavior

The HGSS decomp script identifies a programming mistake: if TM07 cannot be accepted at the reward point (notably the max-stack case), the post-badge dialogue path does not retry the reward, and the associated claim flag is not used to recover it.

Crystal already provides the safer model: until `EVENT_GOT_TM16_ICY_WIND` is set, speaking to Pryce attempts the reward again.

Target rule:
- document the HGSS original bug;
- implement retry-until-claimed behavior;
- verify bag-full/max-stack/save-reload boundary cases.

### 17. Radio Tower takeover uses a progression handshake, not “Pryce always starts it”

Gen II Gym scripts and HGSS's `VAR_MIDGAME_BADGES` logic both accommodate midgame badge-order freedom.

HGSS Pryce:
- increments `VAR_MIDGAME_BADGES`;
- when the relevant threshold is reached, advances `VAR_SCENE_ROCKET_TAKEOVER`.

Mahogany town contains a further takeover-state script that activates Rocket flags and triggers Professor Elm's phone call.

Phase 7 will expand this into the full Radio Tower takeover state machine. Phase 6 fixes one rule now:

**do not attach takeover activation solely to defeating Pryce.**

## Primary source manifest

### `pret/pokecrystal`
- `maps/Route42.asm`
- `maps/Route36.asm`
- `maps/Route43Gate.asm`
- `maps/LakeOfRage.asm`
- `maps/MahoganyTown.asm`
- `maps/MahoganyMart1F.asm`
- `maps/TeamRocketBaseB1F.asm`
- `maps/TeamRocketBaseB2F.asm`
- `maps/TeamRocketBaseB3F.asm`
- `maps/MahoganyGym.asm`
- `maps/MrPokemonsHouse.asm`
- `engine/events/std_scripts.asm`

### `pret/pokeheartgold`
- `scr_seq_0252_R42.s`
- `scr_seq_0256_R43R0201.s`
- `scr_seq_0930_T28.s`
- `scr_seq_0932_T28GYM0101.s`
- `scr_seq_0938_T29.s`
- `scr_seq_0088_D35R0101.s`
- `scr_seq_0089_D35R0102.s`
- `scr_seq_0090_D35R0103.s`
- `scr_seq_0091_D35R0104.s`
- `scr_seq_0229_R30R0201.s`
- `include/constants/flags.h`
- `include/constants/items.h`
- `src/item.c`

### Official cross-check
The official Japanese HGSS character page confirms Team Rocket's revival and the presence of the executive group. The exact per-event implementation above is taken from the source/decomp and uploaded ROM data, not inferred from the promotional summary.

## Integrated Phase 6 route

`Route42`
→ `Crystal/HGSS Suicune branch handoff`
→ `optional Mt. Mortar`
→ `Mahogany / east blocker`
→ `Route43 Rocket toll`
→ `Lake of Rage`
→ `Lv30 shiny Red Gyarados / Red Scale`
→ `Lance request (accept/refuse)`
→ `Mahogany secret shop / Dragonite`
→ `HQ B1F cameras + full trap field`
→ `Lance heal`
→ `two GSC passwords`
→ `rival/Lance character beat`
→ `legacy male Executive preserved`
→ `Petrel/Giovanni disguise`
→ `Murkrow phrase + voice authentication`
→ `legacy female Executive preserved`
→ `Ariana + Grunt vs player + Lance`
→ `six Electrode / generator shutdown`
→ `Whirlpool entitlement`
→ `atomic HQ clear / Route43 restoration`
→ `Pryce`
→ `Glacier Badge + GSC TM16 + HGSS TM07`
→ `generic Radio Tower takeover handshake`.

## Verification queue for Phase 7

- exact six-badge/seven-badge takeover transitions in G/S, Crystal and HGSS;
- Goldenrod Rocket disguise acquisition and rival interruption;
- Radio Tower 1F–5F trainer/actor matrix;
- fake Director / Petrel;
- Basement Key and Underground Warehouse;
- switch puzzle;
- Director rescue;
- Card Key;
- Proton/Ariana/Archer placement;
- HGSS Executive hierarchy continuity;
- version-specific feather/bell rewards;
- post-takeover Kimono Girl and mascot-story transition.
