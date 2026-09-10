# HGSS → GSC Story Integration — Phase 11

## Scope

Phase 11 leaves the one-shot main story and audits **recurring state**: Gen II phone rematches, HGSS Gym Leader phone numbers and Saffron Fighting Dojo rematches, daily/weekly RTC events, Bug-Catching Contest, Buena/Blue Card, haircut/grooming-style daily services, Friday Lapras/weekday NPCs, recurring transport, mass outbreaks, and post-story recovery/respawn state.

Detailed matrix: `hgss_to_gsc_story_phase11.csv` (**55 rows**).

The central rule is:

> **Permanent story fact ≠ unlock fact ≠ current schedule window ≠ current cycle state ≠ reward claim.**

A recurring event must never borrow a one-shot story flag merely because the same NPC or map is involved.

## Direct verification of uploaded Korean HG/SS ROMs

Uploaded Korean HeartGold (`IPKK`) and SoulSilver (`IPGK`) were parsed directly again.

Field-script NARC `a/0/1/2`:
- size: `372012` bytes
- members: `965`
- SHA-1: `0b911f52fda9c9324295a9bc7db2350433097529`
- HG = SS: **byte-identical**

Selected Phase 11 members:

| Index | Script role | Size | SHA-1 | HG=SS |
|---:|---|---:|---|---|
| 832 | T11R0101 — Saffron Fighting Dojo | 2276 | `5520403a1bc5f08714cf2c8ceda46aa444bccb41` | Yes |
| 785 | T07 — Erika scheduled-world script | 1740 | `4ab3e60933ec3b22a1d14d6ee5dde3e244f25112` | Yes |
| 260 | R47 — Chuck-related scheduled script | 716 | `b84aa0fe762e55869ca784fed75647517c289a52` | Yes |
| 815 | T09 — Blue/Blaine scheduled-world script | 1228 | `d18801b7e7b63a606d22c2c4af1fb0fca95f5931` | Yes |
| 216 | R25 — Misty / scheduled-world script | 2080 | `bc1ffb33b4d6f4e0ef1c41fabbf9f984c09d6370` | Yes |
| 249 | R39 — Route 39 scheduled/phone content | 1244 | `ccb9f7ef33ce9bb186dfb07db0f7fa20a1e7ef7c` | Yes |
| 213 | R22R0101 — League Gate / Janine contact context | 1484 | `0a25ca5fa2baff9ddce8decb6cebfc1236a49fae` | Yes |
| 919 | T26R0701 — Olivine Café / Jasmine | 1028 | `497ac60b35d1606add3d0a697ab0d75800f66c4b` | Yes |
| 5 | D01R0101 — Brock contact context | 888 | `9f7f2d45eacacd4250bf1d2cd0f8a2f04148c53f` | Yes |
| 153 | P01R0102 — Olivine Port / Sabrina | 924 | `9c97ed406d312eaaee3437124bdba90bdd23ccce` | Yes |
| 22 | D17R1101 — Morty scheduled location | 464 | `198e942d02ad2e659c1b634c7c3c7c3c3ce7e4f9` | Yes |
| 792 | T07R0104 — Falkner contact context | 728 | `63e21f9b61c0b77b9389fef344f2daa8fb3b31df` | Yes |
| 904 | T25R1006 — Whitney contact context | 2248 | `f3719e228885fccc18e3f92d1fc8c744a79a6b7d` | Yes |
| 932 | T28GYM0101 — Pryce Gym | 528 | `e1401e5456acfe693ed8dbd359e20b4111b25e9a` | Yes |
| 938 | T29 — Lake of Rage / Pryce | 1960 | `8b16a24df8f1550e96f544fb9d0587626d78b567` | Yes |
| 943 | T30GYM0101 — Clair Gym | 1044 | `71cb25d513f187109d9e1f5cae6a3a9ed5d3963b` | Yes |
| 111 | D44R0102 — Dragon's Den / Clair context | 1952 | `fe1f4b697eb92c1e2c67b30e55ce956daa18b57a` | Yes |
| 869 | T23GYM0102 — Bugsy Gym | 472 | `00f37d5594ae887719a0066be5bee42ecad4400b` | Yes |
| 115 | D46R0101 — Bugsy scheduled location context | 232 | `4c7d602a683e45a4fe6b77b0c0bb55b0e24fd4b1` | Yes |
| 151 | Bug-Catching Contest shared script | 2120 | `ec17f551c33af3f02d7a5611be28dfaa2a2154c1` | Yes |
| 25 | D22R0101 — National Park / contest context | 1892 | `cb2824840fcb72b8381d0de9ef25a8ff3aff30c2` | Yes |
| 30 | D23R0102 — Radio Tower 2F / Buena | 1636 | `4b113c3c96996e947430b7d83ffbc6479098895e` | Yes |
| 58 | D25R0103 — Union Cave B2F | 152 | `884e200bed523dcee943786b72aee0d31ac47881` | Yes |
| 94 | D37R0102 — Goldenrod Underground B1F | 5484 | `8e1d77f5f369dc7881ed539c14dd9006e4912e23` | Yes |

This continues to support a shared Korean HGSS field-script layer. It does **not** establish identity for RTC save data, phone tables, encounter tables, text, trainer data or version-specific non-script resources.

---

## 1. Gen II recurring phone content is preserved first

Gold/Silver already contain trainer phone scripts that can set `*_READY_FOR_REMATCH` events. Crystal retains and expands this architecture with explicit weekday/time checks for many contacts.

Audited Crystal examples include scheduled rematches for Joey, Liz, Reena, Gaven, Dana, Todd, Alan, Erin, Gina, Chad, Jack, Jose and Wade.

Therefore HGSS Gym Leader rematches are **not a replacement for the Gen II phone-rematch layer**. The target has at least two recurring battle families:

```text
GEN2_PHONE_TRAINER_REMATCH
HGSS_GYM_LEADER_DOJO_REMATCH
```

Each keeps its own trainer IDs, scheduling rules, dialogue and rewards.

## 2. HGSS Gym Leader rematches are a five-layer state machine

The HGSS phone code and Saffron Fighting Dojo script establish the following lifecycle:

```text
PHONE_REGISTERED
    ↓
ALL_16_BADGES_OBTAINED + WEEKDAY/TIME_WINDOW_MATCH
    ↓
REMATCH_SEEKING / BOOKED
    ↓
LEADER_VISIBLE_IN_FIGHTING_DOJO
    ↓
TRAINER_*_2 BATTLE
    ↓
BOOKING CLEARED
```

Phone registration is not the booking itself. The booking is not the Gym victory flag. A defeated dojo rematch never erases the phone contact.

The outgoing Gym Leader phone script explicitly refuses the rematch-scheduling path until the player has **all 16 Badges**.

## 3. All 16 Gym Leaders use the Fighting Dojo

The dojo script contains dedicated rematch handling for:

- Falkner
- Bugsy
- Whitney
- Morty
- Chuck
- Jasmine
- Pryce
- Clair
- Brock
- Misty
- Lt. Surge
- Erika
- Janine
- Sabrina
- Blaine
- Blue

Each uses a stronger `*_2` trainer record and persistent phone-rematch state.

### Verified HGSS call windows

The phonebook is data-driven through `rematchWeekday` and `rematchTimeOfDay`. Exact schedule was cross-checked against the in-game schedule reference:

| Day | Morning | Daytime | Night |
|---|---|---|---|
| Monday | Pryce | Janine | — |
| Tuesday | — | Blaine | Morty |
| Wednesday | Misty | Jasmine | Chuck |
| Thursday | — | Bugsy | — |
| Friday | Lt. Surge | — | Clair |
| Saturday | Falkner | Whitney | Brock |
| Sunday | Erika | Sabrina | Blue |

Registration locations/times remain separate data and are recorded row-by-row in the CSV.

## 4. Registration and rematch availability must not be merged

Examples of HGSS registration constraints include:
- Falkner at Celadon Department Store on Monday, after Soul Badge;
- Bugsy in Viridian Forest on Thursday;
- Whitney at Goldenrod Department Store during a limited daytime window;
- Morty on Bellchime Trail Monday/Tuesday;
- Chuck's number from his wife;
- Jasmine at Olivine Café during a narrow hour;
- Pryce at Lake of Rage in the morning;
- Clair in Dragon's Den after the Lance/Clair Multi Battle;
- several Kanto Leaders require all 16 Badges before their contact event;
- Blue's number is obtained from Daisy under a separate friendship/massage requirement.

This means one boolean such as `LEADER_REMATCH_UNLOCKED` is structurally wrong.

## 5. Verified suspicious Dojo-capacity code

`phone_scripts_gym_leader.c` contains an apparent capacity-check function.

It declares an array containing **all 16 Gym Leader contacts**, but the counting loop is:

```text
for (i = 0; i < 1; ++i)
```

and then compares the resulting count against 5.

The decomp source itself comments that this may have been intended to check whether the dojo is full, but stops after one iteration.

Classification:

```text
ORIGINAL_HGSS_CODE_DEFECT = verified
INTENDED_MAX_BOOKINGS = likely 5, not fully proven
```

Project policy:
- document actual HGSS code behavior;
- do not invent official semantics;
- candidate correction is to iterate all 16 and enforce the apparent five-booking capacity only after behavioral validation;
- if preserving retail behavior is the selected compatibility mode, keep the retail scheduling result instead.

## 6. Whiteout must not consume a booking

The Dojo script uses `WhiteOut` on loss and only performs the successful booking-clear path after victory.

Regression rule:

```text
lose dojo rematch
→ respawn
→ leader booking still exists
→ leader remains/reconstructs in dojo
→ rematch can be attempted again
```

## 7. Bug-Catching Contest remains Tuesday / Thursday / Saturday

Crystal gate scripts explicitly state the contest schedule:
- Tuesday
- Thursday
- Saturday

HGSS retains the same three contest days.

The contest also owns **temporary run state**:
- registration;
- time remaining;
- contestant state;
- Sport Ball/contest capture handling;
- selected catch;
- judging;
- prizes.

Do not serialize `BUG_CONTEST_COMPLETED` as a permanent one-shot story flag.

## 8. Buena is a Crystal system retained by HGSS

Crystal added:
- Buena's Password;
- Blue Card;
- weekly password selection;
- weekly-generation guard.

The Crystal radio code stores a generated password and sets a flag so a new one is not generated again in that week.

HGSS keeps:
- `ITEM_BLUE_CARD`;
- `PHONE_CONTACT_BUENA`;
- Radio Tower 2F Buena scripts;
- dedicated `buenas_password.c` radio-show code.

Use separate save fields:

```text
HAS_BLUE_CARD
BUENA_PHONE_REGISTERED
BUENA_WEEK_ID
BUENA_PASSWORD_ID
BUENA_ANSWERED_THIS_CYCLE
BUENA_POINTS
```

## 9. Daily services must be driven by the RTC reset engine

Crystal's daily-engine flags include systems such as:
- Underground haircut;
- Trainer Hall daily battle;
- Daisy grooming;
- Union Cave Lapras state;
- Mt. Moon Square Clefairy state.

HGSS likewise has explicit daily flags. `FLAG_DAILY_GOT_HAIRCUT` is present, and the day-advance code calls `ClearDailyFlags(fieldSystem)`.

Therefore the target should have one central RTC rollover transaction instead of individual map scripts trying to infer that “a new day happened.”

## 10. Friday Lapras is not a one-time static encounter

Crystal's Union Cave B2F callback checks:

```text
VAR_WEEKDAY == FRIDAY
```

to make Lapras appear and uses a dedicated engine/daily state.

This is categorically different from a one-shot legendary.

Recommended state model:

```text
UNION_LAPRAS_WEEKLY_ELIGIBLE
UNION_LAPRAS_RESOLVED_THIS_CYCLE
UNION_LAPRAS_CAUGHT_PERMANENT   # only if source rules need ownership history
```

Exact HGSS Union Cave Lapras remake data is deferred to the encounter-table pass rather than guessed from the field script alone.

## 11. Weekday siblings keep visibility and gift claims separate

Crystal exposes individual event flags for:

- Monica of Monday
- Tuscany of Tuesday
- Wesley of Wednesday
- Arthur of Thursday
- Frieda of Friday
- Santos of Saturday
- Sunny of Sunday

Two concepts must not be merged:

```text
NPC_VISIBLE_TODAY
ONE_TIME_GIFT_ALREADY_CLAIMED
```

A weekday returning does not regenerate a unique gift if the source event does not.

## 12. Goldenrod haircut and story-tunnel state are independent

HGSS explicitly has `FLAG_DAILY_GOT_HAIRCUT`.

The Goldenrod Underground/Tunnel also carries:
- Rocket occupation state;
- Rocket costume state;
- Kimono Girl events;
- shops;
- other NPC schedules.

Those are separate namespaces. Clearing the Radio Tower or advancing the Kimono story can never reset or permanently consume the haircut service.

## 13. Recurring S.S. Aqua is not the first-voyage quest

Phase 9 established the first voyage:
- missing granddaughter;
- captain;
- reunion;
- Metal Coat entitlement;
- Vermilion arrival.

Afterward, the ship becomes recurring transport controlled by weekday/direction/voyage state.

Use:

```text
SS_AQUA_FIRST_VOYAGE_COMPLETE
SS_AQUA_CURRENT_DIRECTION
SS_AQUA_TIMETABLE_ELIGIBLE
SS_AQUA_REPEAT_VOYAGE_STATE
```

Never replay the granddaughter quest when the weekly ferry returns.

## 14. Mass outbreaks have unlock state and current-event state

HGSS explicitly runs `EnableMassOutbreaks` after the post-League Oak scene.

That is only the **feature unlock**.

The current outbreak must be separate:

```text
MASS_OUTBREAKS_UNLOCKED
CURRENT_OUTBREAK_ID
CURRENT_OUTBREAK_CYCLE
CURRENT_OUTBREAK_ANNOUNCED
```

Crystal's older swarm/phone state is preserved independently; it is not silently relabeled as the HGSS subsystem.

## 15. Hall-of-Fame legendary restoration is species-specific

Phase 9 found HGSS Hall-of-Fame restoration logic for eligible uncaught static Pokémon and selected roaming states.

This does **not** justify:

```text
on Hall of Fame:
    respawn_every_legendary()
```

Each species needs its source-specific eligibility rule. Crystal Suicune, G/S roaming beasts, HGSS primary mascots and later Kanto legends are not interchangeable.

## Recommended save/state namespaces

```text
# permanent one-shot
EVENT_*
BADGE_*
ITEM_SOURCE_CLAIMED_*
STORY_BRANCH_*

# phone identity
PHONE_REGISTERED[contact]

# recurring trainer scheduling
REMATCH_WINDOW[contact]
REMATCH_SEEKING[contact]
REMATCH_BATTLE_ACTIVE[contact]

# daily
DAILY_*

# weekly
WEEKLY_*
WEEK_ID

# facility runs
BUG_CONTEST_RUN_*
SS_AQUA_REPEAT_*

# encounter scheduler
OUTBREAK_*
WEEKLY_STATIC_ENCOUNTER_*

# derived/transient
NPC_VISIBLE_NOW
DOJO_PRESENT_NOW
```

Derived map visibility is reconstructed after load from authoritative saved state rather than being the sole truth.

## Direct implementation verification queue

1. Register each of the 16 leader contacts independently.
2. Try rematch calls before 16 badges: reject.
3. Test every weekday/time-of-day rematch window.
4. Accept and decline each booking.
5. Save/reload with one or multiple leaders booked.
6. Whiteout in each dojo battle; booking survives.
7. Win; booking clears but phone remains.
8. Validate apparent Dojo-capacity bug in retail-compatible mode and corrected candidate mode.
9. Day rollover clears only daily flags.
10. Week rollover changes Buena password cycle only once.
11. Haircut cannot be repeated the same day, returns after rollover.
12. Bug Contest only opens Tue/Thu/Sat.
13. Bug Contest save/exit/whiteout/judging boundaries.
14. Friday Lapras appears/disappears/retries according to weekly state.
15. Weekday sibling NPC visibility changes without regenerating consumed unique gifts.
16. S.S. Aqua first voyage never replays on later scheduled trips.
17. Outbreak unlock persists while current outbreak rotates independently.
18. Hall of Fame restoration is checked species-by-species.
19. Story flags are invariant under daily/weekly resets.
20. Derived NPC visibility is reconstructed correctly after load.

## Primary source manifest

### `pret/pokegold`
- `engine/phone/scripts/trainers.asm`
- Gen II route/trainer phone event scripts

### `pret/pokecrystal`
- `engine/phone/scripts/*`
- `engine/pokegear/radio.asm`
- `constants/engine_flags.asm`
- `constants/event_flags.asm`
- `maps/Route35NationalParkGate.asm`
- `maps/Route36NationalParkGate.asm`
- `maps/UnionCaveB2F.asm`
- Goldenrod Underground daily-service scripts

### `pret/pokeheartgold`
- `src/application/pokegear/phone/scripts/phone_scripts_gym_leader.c`
- `files/tel/pmtel_book.json`
- `files/fielddata/script/scr_seq/scr_seq_0832_T11R0101.s`
- leader-specific field scripts
- `src/application/pokegear/radio/shows/buenas_password.c`
- `scr_seq_0030_D23R0102.s`
- `scr_seq_0151.s`
- `src/encounter.c`
- `include/constants/flags.h`
- `src/unk_02055418.c`
- `src/scrcmd_c.c`

### Secondary schedule cross-check
- Bulbapedia Pokégear / Fighting Dojo HGSS tables were used only to cross-check the exact 16-Leader phone registration/rematch timetable against the primary data-driven phone architecture.

## Deferred, not omitted — Phase 12

A later facility/content pass should exhaustively audit:
- Pokéathlon daily prizes/records;
- Battle Frontier facilities, streak/record/save structures;
- HGSS Safari Zone block customization and timed unlocks;
- all Apricorn/Berry daily growth/harvest timers;
- Lottery Corner;
- every department-store/day-of-week vendor;
- radio program schedule grid;
- all photo opportunities;
- every Gym Leader in-game trade;
- all phone gift/swarm/news contacts row-by-row;
- complete HGSS Union Cave Lapras encounter data;
- full time-tamper penalty behavior.

These are deliberately separated from Phase 11's recurring-state architecture so they can be audited without collapsing distinct facility save formats.