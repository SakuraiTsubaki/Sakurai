# HGSS → GSC Story Integration — Phase 10

## Scope

Kanto postgame main structure after the first S.S. Aqua arrival: Vermilion → Power Plant / Cerulean Machine Part case → Lavender Expansion Card → Poké Flute / Snorlax → Diglett Cave / western Kanto → Kanto Gym network → Copycat / Magnet Train → Cinnabar / Blue → all eight Kanto Badges → upgraded Pokémon League → Oak / Mt. Silver unlock → HGSS restored Kanto legendary content → Mt. Silver / Red.

Detailed event/system matrix: `hgss_to_gsc_story_phase10.csv` (**55 rows**).

## Direct verification of uploaded Korean HG/SS ROMs

Uploaded ROMs rechecked directly:

- HeartGold: game code `IPKK`, SHA-1 `5834fb3a2d751c48501d47d6a56898d7af6ccf9e`
- SoulSilver: game code `IPGK`, SHA-1 `0330e6449306606114a92bdbb3f9d3d51d392b96`

Field-script NARC:

- path: `a/0/1/2`
- size: `372012` bytes
- members: `965`
- SHA-1: `0b911f52fda9c9324295a9bc7db2350433097529`
- HeartGold = SoulSilver NARC: **byte-identical**

### Phase 10 members checked directly

| Index | Script role | Size | SHA-1 | HG=SS |
|---:|---|---:|---|---|
| 196 | R10R0202 — Power Plant | 856 | `e1c08907f6e3a93f173e406dea74c97684cc7036` | Yes |
| 760 | T04GYM0101 — Cerulean Gym / Rocket / Machine Part / Misty | 1072 | `5a8c72ac0f3d280588aa1079629e5c019c58c1e9` | Yes |
| 215 | R24 — Rocket encounter | 572 | `c1bf4577a79fbf8fb020ff8bcd7209ead1e235d8` | Yes |
| 216 | R25 — Misty / Suicune chain | 2080 | `bc1ffb33b4d6f4e0ef1c41fabbf9f984c09d6370` | Yes |
| 775 | T05R0701 — Lavender Radio Tower / Expansion Card | 248 | `a4d95803c9b4795e7b108c0af18d5d387113eb08` | Yes |
| 197 | R11 — Snorlax | 236 | `8d816a3a1703466a8b0c565d578224340d51aac4` | Yes |
| 841 | T11R0802 — Copycat 2F / Lost Item / Pass | 1096 | `8324041542aa05257c4f3d8574bc10999a35892d` | Yes |
| 776 | T06 — Vermilion / Steven / Suicune-Eusine | 2280 | `9d6b24c1354954209caa5d589286b634ef6e7c86` | Yes |
| 778 | T06GYM0101 — Lt. Surge | 1096 | `f8c10d34373d0d39a36b6ef1f6455817cd21090a` | Yes |
| 752 | T03GYM0101 — Brock | 548 | `8979da79ae7f6c0b5d112e2685d8a9dfc26d45d5` | Yes |
| 786 | T07GYM0101 — Erika | 512 | `e8086a706de1ecc8eea893893a7675bda9ce3c86` | Yes |
| 809 | T08GYM0101 — Janine | 2052 | `01f83835b788be946fc684fe372e64e1aa357434` | Yes |
| 829 | T11GYM0101 — Sabrina | 580 | `2d43b384944dae8d4c9d4f51f4fd8330a3eeffa6` | Yes |
| 15 | D11R0106 — Seafoam Gym / Blaine | 1220 | `43e68c6dcededc50ee0115ba0ecf02a5a6c05cd3` | Yes |
| 815 | T09 — Cinnabar / Blue seven-badge gate | 1228 | `d18801b7e7b63a606d22c2c4af1fb0fca95f5931` | Yes |
| 743 | T02GYM0101 — Viridian Gym / Blue | 1204 | `f546a78df5305c580bd1fc5a4d6c220ccc87a87d` | Yes |
| 740 | T01R0301 — Oak Lab / HM08 / Mt. Silver unlock | 2516 | `08593ab8fd67f2aea46acac153d12c1637f7da61` | Yes |
| 213 | R22R0101 — League Reception Gate / Mt. Silver branch | 1484 | `0a25ca5fa2baff9ddce8decb6cebfc1236a49fae` | Yes |
| 191 | R10 — Zapdos | 748 | `ebb33e4b10a82e3d36c82358f5aaf2ddb5712422` | Yes |
| 14 | D11R0105 — Articuno | 132 | `2135a57a015ce4c9a80075d114b368104f57732b` | Yes |
| 106 | D41R0105 — Moltres | 132 | `1e611a807c23fc87e10ee0dcbc545ffe423d85ee` | Yes |
| 11 | D03R0103 — Cerulean Cave Mewtwo | 132 | `88b4a18e46527446f0bc12258cecc631b10eae8c` | Yes |
| 107 | D41R0108 — Mt. Silver Red | 236 | `a4d74506583d559a0f8486f5528e91ecfb166b23` | Yes |

The byte equality above means the two Korean ROMs use shared field-script bytecode for these maps. It does **not** mean the games have no version-specific behavior. For example, the shared Vermilion script performs a runtime game-version check and selects Latias for HeartGold versus Latios for SoulSilver.

---

## 1. Kanto must remain an open postgame region

The original Gen II Kanto design is comparatively non-linear. After arriving in Vermilion, the player is not supposed to follow a single eight-Gym corridor. Local world states matter more than a universal Gym order:

- the Power Plant theft case controls Misty's absence, Kanto radio restoration and several downstream side quests;
- Snorlax blocks the Diglett Cave side of the region until the Poké Flute channel is available;
- Blaine has relocated because Cinnabar's Gym no longer exists;
- Blue/Green's return-to-Viridian rule differs materially between GSC and HGSS.

Integration therefore uses independent semantic predicates rather than one monolithic `KANTO_STORY_STAGE`.

Recommended permanent states include:

```text
KANTO_POWER_PLANT_CASE_STARTED
KANTO_MACHINE_PART_ROCKET_DEFEATED
KANTO_MACHINE_PART_OBTAINED
KANTO_POWER_RESTORED
KANTO_EXPN_CARD_OBTAINED
KANTO_SNORLAX_RESOLVED
KANTO_COPYCAT_DOLL_REQUESTED
KANTO_LOST_ITEM_OBTAINED
KANTO_MAGNET_TRAIN_PASS_OBTAINED
KANTO_BADGE_COUNT = 0..8 (derived/validated)
BLUE_RETURNED_TO_VIRIDIAN
MT_SILVER_ACCESS_GRANTED
RED_DEFEATED
```

Source-specific flags remain mapped to these semantic facts and are not deleted.

---

## 2. Power Plant → Cerulean → Machine Part is legacy GSC story

The stolen Machine Part arc is already fully authored in Gold/Silver and Crystal. The Gen II Power Plant manager sets the investigation in motion, exposes the Cerulean Gym Rocket state, and later consumes `MACHINE_PART` to restore Kanto power.

The HGSS remake preserves this same story skeleton in more explicit map/actor state:

1. Power Plant `R10R0202` records that the manager's story was heard.
2. The guard scene exposes the Cerulean Gym Rocket.
3. `T04GYM0101` runs the Rocket escape scene.
4. Route 24 handles the Rocket follow-up/battle.
5. The Machine Part becomes obtainable in Cerulean Gym.
6. Returning it to the Power Plant changes the facility to its repaired state and sets permanent power-restored state.

This must be documented as **legacy GSC story retained and expanded by HGSS**, not as an HGSS-original quest.

### Reward conflict

The repair reward is source-dependent:

- GSC/Crystal: TM07 Zap Cannon.
- HGSS: TM57 Charge Beam.

The target must never overwrite TM07 merely to look like HGSS. Once the TM table is expanded, HGSS TM57 can coexist as a remake-layer reward or selectable source-mode reward.

---

## 3. Misty and the Machine Part must use separate states

Misty's temporary absence and the stolen Machine Part use overlapping maps but are not the same state.

The integration keeps at minimum:

```text
CERULEAN_ROCKET_INTRUSION_ACTIVE
ROUTE24_ROCKET_RESOLVED
MISTY_ROUTE25_SCENE_RESOLVED
MISTY_RETURNED_TO_GYM
MACHINE_PART_AVAILABLE
MACHINE_PART_CLAIMED
```

This becomes especially important when the HGSS Route 25 Suicune scene is added to a Crystal target. Suicune progression must never prevent Misty from returning or vice versa.

---

## 4. Radio restoration → Poké Flute → Snorlax

After power is restored, HGSS Lavender Radio Tower checks the permanent restored-power flag before giving the Expansion Card. This mirrors the functional dependency of Gen II Kanto radio progression.

The Snorlax event is not a generic "use item" event. The engine checks whether the Poké Flute radio channel is actually playing. HGSS preserves that design explicitly with `RadioMusicIsPlaying 5`.

Both generations use a level-50 Snorlax roadblock. HGSS improves the state granularity by keeping:

- currently engaging static Pokémon;
- Snorlax encounter resolved/met;
- Snorlax specifically caught.

The backport should adopt this granularity while preserving the original road-opening semantics.

---

## 5. Copycat / Lost Item / Magnet Train is preserved, not collapsed into power restoration

Power restoration enables the wider rail-related world state but does not itself grant rail travel.

The Gen II sequence is:

```text
Power restored
→ Copycat mentions lost Poké Doll
→ Vermilion Fan Club gives LOST_ITEM
→ return LOST_ITEM to Copycat
→ receive PASS
→ Magnet Train usable
```

HGSS keeps the same logical quest. Its Copycat script explicitly consumes `ITEM_LOST_ITEM` and gives `ITEM_PASS`.

The target therefore separates:

```text
KANTO_POWER_RESTORED
MAGNET_TRAIN_PASS_OBTAINED
```

so neither state can accidentally substitute for the other.

---

## 6. Kanto Gyms: preserve source reward and puzzle differences

HGSS adds a consistent first-battle architecture to Kanto Leaders:

- badge check;
- trainer battle;
- badge award;
- `VAR_UNK_4135 += 1`;
- one-time TM award;
- separate TM-obtained flag so a full Bag does not permanently lose the reward;
- later phone/rematch availability logic.

### HGSS Kanto Leader TM rewards

| Leader | Badge | HGSS TM |
|---|---|---|
| Brock | Boulder | TM80 |
| Misty | Cascade | TM03 |
| Lt. Surge | Thunder | TM34 |
| Erika | Rainbow | TM19 |
| Janine | Soul | TM84 |
| Sabrina | Marsh | TM48 |
| Blaine | Volcano | TM50 |
| Blue | Earth | TM92 |

These HGSS rewards are **not permission to rewrite Gen II rewards**. For example, the checked Gold/Silver Vermilion Gym and Pewter Gym scripts award their Badges without the HGSS Leader TM reward. The integration records each source reward independently.

### Lt. Surge puzzle difference

Gen II explicitly says the Vermilion traps are not active. HGSS implements an active can/switch puzzle with initialization/resampling state.

Therefore two legitimate source modes exist:

```text
GSC_SURGE_GYM_LAYOUT_RULES
HGSS_SURGE_GYM_LAYOUT_RULES
```

A future unified map may contain both implementations, but one must not be falsely documented as the original behavior of the other.

---

## 7. Blue/Green ordering is a real GSC ↔ HGSS conflict

This is one of the most important Phase 10 findings.

### Gold/Silver

The Cinnabar Blue script simply:

- talks to the player;
- teleports/disappears Blue from Cinnabar;
- clears the Viridian Gym Blue event flag.

There is no Kanto-badge-count check in that scene.

### HGSS

The shared `T09` Cinnabar script compares `VAR_UNK_4135` against `7`.

- `< 7`: Blue refuses to return for the real challenge.
- `>= 7`: Blue leaves Cinnabar and Viridian Gym is unlocked for the story challenge.

So the integration must expose an explicit compatibility rule:

```text
if STORY_ORDER_MODE == GSC:
    Blue returns after Cinnabar conversation
elif STORY_ORDER_MODE == HGSS:
    Blue returns only when Kanto badge count >= 7
```

The project must never claim that "Blue is canonically always the eighth Kanto Leader" for GSC.

---

## 8. Eight Kanto Badges also switch the HGSS Pokémon League tier

HGSS uses the same Kanto badge counter for more than Blue.

The checked Will, Koga, Bruno, Karen and Lance scripts compare `VAR_UNK_4135` with `8`. Once all eight Kanto Badges are counted, they select their `_2` upgraded trainer records.

Integration model:

```text
LEAGUE_TIER_1 = original first-clear teams
LEAGUE_TIER_2_HGSS = all 8 Kanto Badges
```

GSC/Crystal League records remain available as their own source data and must not be erased by the HGSS stronger tier.

---

## 9. Oak and Mt. Silver: same destination, different prerequisites

### GSC / Crystal family

Professor Oak reads the badge state. With all 16 badges, he sets `EVENT_OPENED_MT_SILVER` and directs the player toward the Indigo Plateau gate.

This is a direct all-badges entitlement.

### HGSS

The Earth Badge aftermath advances a separate Oak-related variable chain. Oak Lab then gives HM08 Rock Climb and sets `FLAG_UNLOCKED_MT_SILVER`.

Because Rock Climb does not exist in Gen II, the semantic states must be separate:

```text
MT_SILVER_ACCESS_GRANTED
ROCK_CLIMB_OBTAINED
```

A GSC-mode target cannot be forced to require a field move that did not exist in its source game. An HGSS-mode expanded target can require/use Rock Climb where the remake map geometry needs it.

---

## 10. HGSS restores/introduces major Kanto legendary encounters

These are not to be retroactively labeled as GSC content.

Directly verified HGSS field scripts include:

- Zapdos — Lv.50 near the Power Plant;
- Articuno — Lv.50 in Seafoam Islands;
- Moltres — Lv.50 in Mt. Silver Cave;
- Mewtwo — Lv.70 in Cerulean Cave.

Each uses static-encounter state and caught/result handling. They should be added as HGSS-origin optional content after the corresponding maps and save flags are expanded.

Cerulean Cave itself is likewise restored content relative to GSC Kanto and should be integrated as a real multi-map location, not as a single Mewtwo room.

---

## 11. Vermilion contains real HG/SS version branching despite identical script bytes

The directly checked Korean HG and SS `T06` script members are byte-identical. Nevertheless, the script calls `GetGameVersion` and branches at runtime.

From the decompilation constants:

- `VERSION_HEARTGOLD = 7`
- `VERSION_SOULSILVER = 8`

The Vermilion Steven scene selects:

- HeartGold → Latias roaming encounter;
- SoulSilver → Latios roaming encounter.

Therefore the project's ROM-diff rule is:

> byte-identical scripts may still encode version-specific behavior through runtime branching.

Binary equality is never sufficient by itself to collapse HG and SS behavior records.

---

## 12. Crystal Suicune story must remain authoritative when integrating HGSS Kanto chase scenes

HGSS Vermilion contains an authored Suicune + Eusine scene and advances the chase toward Route 14. Route 25 also participates later in the chain.

Crystal, however, already has its own Suicune-focused narrative and capture resolution at Tin/Bell Tower.

The project rule remains:

```text
if CRYSTAL_SUICUNE_CAPTURED:
    HGSS Kanto Eusine scenes become post-capture epilogue/acknowledgement
else:
    HGSS Kanto chase may continue using its own stage variable
```

Never respawn a captured Crystal Suicune or rewrite Crystal's original resolution simply to reproduce HGSS event order.

---

## 13. Red must keep both Gen II and HGSS authored battle records

### GSC Red

| Pokémon | Level |
|---|---:|
| Pikachu | 81 |
| Espeon | 73 |
| Snorlax | 75 |
| Venusaur | 77 |
| Charizard | 77 |
| Blastoise | 77 |

### HGSS Red

| Pokémon | Level | Notable data |
|---|---:|---|
| Pikachu | 88 | Light Ball; Volt Tackle / Iron Tail / Quick Attack / Thunderbolt |
| Lapras | 80 | replaces Espeon |
| Snorlax | 82 | Gen IV moveset incl. Giga Impact |
| Venusaur | 84 | incl. Frenzy Plant |
| Charizard | 84 | incl. Blast Burn |
| Blastoise | 84 | incl. Hydro Cannon |

The HGSS record is not a "correction" of GSC Red. Both are official source records and both remain traceable.

---

## 14. Red victory aftermath is materially expanded in HGSS

GSC's Red script preserves the minimalist finale:

- silent Red encounter;
- battle;
- Red disappears;
- party heal;
- credits.

HGSS adds several persistent outcomes after victory:

1. Red is hidden and completion variables are set.
2. If not already enabled, Oak's Lab Bulbasaur/Charmander/Squirtle choice objects are unhidden.
3. Every current party member receives `RIBBON_LEGEND`.
4. Credits run through the HGSS Hall-of-Fame/credits command path.
5. Loss executes an explicit WhiteOut and must not set victory rewards.

The starter reward and Legend Ribbon require their own data/UI/save systems before backporting. They must not be approximated with unrelated legacy flags.

---

## 15. Recommended Phase 10 state separation

```text
# Power Plant case
EVENT_KANTO_POWER_PLANT_CASE_STARTED
EVENT_KANTO_ROUTE24_ROCKET_RESOLVED
EVENT_KANTO_MACHINE_PART_CLAIMED
EVENT_KANTO_POWER_RESTORED

# Radio / Snorlax
EVENT_KANTO_EXPN_CARD_OBTAINED
EVENT_KANTO_SNORLAX_ENGAGED
EVENT_KANTO_SNORLAX_RESOLVED
EVENT_KANTO_SNORLAX_CAUGHT

# Copycat / train
EVENT_KANTO_COPYCAT_DOLL_REQUESTED
EVENT_KANTO_LOST_ITEM_OBTAINED
EVENT_KANTO_LOST_ITEM_RETURNED
EVENT_KANTO_MAGNET_PASS_OBTAINED

# Gyms
KANTO_BADGE_COUNT_DERIVED
EVENT_BLUE_RETURNED_TO_VIRIDIAN
STORY_ORDER_MODE = GSC | HGSS

# Mt. Silver
EVENT_MT_SILVER_ACCESS_GRANTED
EVENT_HGSS_ROCK_CLIMB_OBTAINED
EVENT_RED_DEFEATED
EVENT_HGSS_KANTO_STARTERS_UNLOCKED

# Crystal/HGSS Suicune coexistence
EVENT_CRYSTAL_SUICUNE_CAPTURED
VAR_HGSS_SUICUNE_KANTO_STAGE

# HGSS version roamers
VAR_HGSS_KANTO_ROAMER_SPECIES
EVENT_HGSS_KANTO_ROAMER_CREATED
```

Derived counters should be reconstructable from authoritative badge/event bits after load so save corruption or missed increment logic cannot permanently break progression.

---

## 16. Required regression tests

Phase 10 implementation is not considered complete merely because Red can be reached.

Minimum verification set:

1. Start Power Plant case, save/reload before Cerulean Gym, verify Rocket actor state.
2. Defeat Route 24 Rocket, leave/re-enter maps, verify Machine Part availability.
3. Fill Bag before Machine Part/reward interactions and ensure no permanent loss.
4. Return Machine Part and verify repaired map, radio unlock, Copycat/Fan Club changes.
5. Obtain Expansion Card, tune away from Poké Flute, verify Snorlax stays asleep.
6. Tune to Poké Flute, lose to Snorlax, verify encounter state is recoverable.
7. Catch versus defeat Snorlax and verify road opening plus distinct caught state.
8. Copycat quest: request → item → return → PASS, including full-Bag retry where applicable.
9. Challenge Kanto Leaders in multiple legal orders under GSC mode.
10. Verify Blue returns immediately after Cinnabar conversation in GSC mode.
11. Verify Blue refuses below 7 Kanto badges and returns at 7+ in HGSS mode.
12. Fill Bag when an HGSS Leader owes a TM; verify later retry.
13. At 7 Kanto badges, verify non-Blue Leaders/League remain correct.
14. At 8 Kanto badges, verify HGSS upgraded Will/Koga/Bruno/Karen/Lance records activate.
15. Verify GSC Oak opens Mt. Silver with all 16 badges without requiring Rock Climb.
16. Verify HGSS Oak gives HM08 and sets Mt. Silver entitlement only in the remake branch.
17. Test Zapdos/Articuno/Moltres/Mewtwo capture, defeat, loss and save/reload states.
18. HeartGold branch must create Latias; SoulSilver branch must create Latios from the same shared script.
19. Crystal Suicune already captured → no Kanto Suicune respawn/deadlock.
20. Lose to Red → no starter unlock, no Legend Ribbon, no victory state.
21. Beat Red → source-specific aftermath executes exactly once where required.
22. Reload after Red/credits and validate every persistent flag/counter.

---

## Source provenance used in this phase

Primary public code references cross-checked against direct ROM extraction:

### Gen II

- `pret/pokegold/maps/PowerPlant.asm`
- `pret/pokegold/maps/CinnabarIsland.asm`
- `pret/pokegold/maps/VermilionCity.asm`
- `pret/pokegold/maps/VermilionGym.asm`
- `pret/pokegold/maps/PewterGym.asm`
- `pret/pokegold/maps/CopycatsHouse2F.asm`
- `pret/pokegold/maps/PokemonFanClub.asm`
- `pret/pokegold/maps/OaksLab.asm`
- `pret/pokegold/maps/SilverCaveRoom3.asm`
- `pret/pokegold/data/trainers/parties.asm`
- `pret/pokegold/engine/events/specials.asm`
- corresponding `pret/pokecrystal` map/event sources for Crystal-side preservation checks.

### HGSS

- `pret/pokeheartgold/files/fielddata/script/scr_seq/scr_seq_0196_R10R0202.s`
- `scr_seq_0760_T04GYM0101.s`
- `scr_seq_0215_R24.s`
- `scr_seq_0216_R25.s`
- `scr_seq_0775_T05R0701.s`
- `scr_seq_0197_R11.s`
- `scr_seq_0841_T11R0802.s`
- `scr_seq_0776_T06.s`
- `scr_seq_0778_T06GYM0101.s`
- `scr_seq_0752_T03GYM0101.s`
- `scr_seq_0786_T07GYM0101.s`
- `scr_seq_0809_T08GYM0101.s`
- `scr_seq_0829_T11GYM0101.s`
- `scr_seq_0015_D11R0106.s`
- `scr_seq_0815_T09.s`
- `scr_seq_0743_T02GYM0101.s`
- `scr_seq_0740_T01R0301.s`
- `scr_seq_0107_D41R0108.s`
- `scr_seq_0011_D03R0103.s`
- `scr_seq_0014_D11R0105.s`
- `scr_seq_0191_R10.s`
- `scr_seq_0106_D41R0105.s`
- `pret/pokeheartgold/files/poketool/trainer/trdata/trainer_data.json`
- `pret/pokeheartgold/include/config.h`

## Phase 10 result

The Kanto postgame cannot be represented as "HGSS Kanto replaces GSC Kanto." The verified structure requires coexistence:

- GSC already supplies the core Power Plant case, radio/Snorlax gate, Copycat/Pass quest, Kanto Gyms, all-badge Oak gate and Red finale.
- Crystal contributes its own source-specific Kanto/legendary/event differences and its Suicune story must remain authoritative when applicable.
- HGSS supplies expanded Gym mechanics/rewards/rematches, explicit badge-count-dependent progression, stronger League tier, restored Kanto legendary maps/encounters, version-dependent Latias/Latios, Kanto Suicune chase scenes, Rock Climb-era Mt. Silver geometry and expanded Red aftermath.

The implementation target therefore keeps **source-authored rules selectable and traceable**, with shared semantic state only where the underlying game fact is genuinely the same.
