# HGSS → GSC Story Integration — Phase 12
## Scope
Independent facilities and time-based systems: Pokéathlon, Crystal Battle Tower / HGSS Battle Frontier, Safari Zone customization and maturation, Apricorn trees/box, RTC rollover and anti-tamper penalty, Lottery, weekday shops, radio schedules, Photo Album, one-time Leader trades, phone gift/news/swarm state, and recurring Friday Lapras.
Detailed version-by-version matrix: `hgss_to_gsc_story_phase12.csv` (**70 rows**).
## Direct Korean HG/SS ROM verification
- Field script NARC: `a/0/1/2`
- Size: `372012` bytes
- Members: `965`
- SHA-1: `0b911f52fda9c9324295a9bc7db2350433097529`
- Korean HeartGold = Korean SoulSilver: **byte-identical archive**

Shared bytecode does not imply all version behavior/data are identical; runtime branches and separate tables remain source-specific.
| Index | Role | Size | SHA-1 | HG=SS |
|---:|---|---:|---|---|
| 29 | D23R0101 — Goldenrod Radio Tower 1F / Lottery | 2992 | `dd860ac5f10aa073e811c42e03bbb3edbcc151c9` | Yes |
| 30 | D23R0102 — Radio Tower 2F / Buena | 1636 | `4b113c3c96996e947430b7d83ffbc6479098895e` | Yes |
| 58 | D25R0103 — Union Cave B2F / Friday Lapras | 152 | `884e200bed523dcee943786b72aee0d31ac47881` | Yes |
| 69 | D31R0201 — Battle Tower | 5712 | `1742510f8eff98ed4229785b47a9def42f6698a1` | Yes |
| 94 | D37R0102 — Goldenrod Underground / recurring services | 5484 | `8e1d77f5f369dc7881ed539c14dd9006e4912e23` | Yes |
| 119 | D47R0101 — Safari Zone Gate | 3864 | `6377a46849ff005c4592c000961619438c0c2dd7` | Yes |
| 123 | D49R0101 — Pokéathlon entrance | 3324 | `a4c18ba86d39669fe5585687b397f1e2136b6600` | Yes |
| 126 | D49R0105 — Pokéathlon room | 472 | `1a123682f15dfc70f1f53a43657bc235e2c389c6` | Yes |
| 127 | D49R0106 — Pokéathlon room | 1240 | `e12e56df26f3e4a4813f16a97325e0e9202537a3` | Yes |
| 128 | D49R0107 — Pokéathlon room | 548 | `f93a0525a6e28cc3301cb7cf29e0e1b07c81be09` | Yes |
| 151 | shared Bug-Catching Contest script | 2120 | `ec17f551c33af3f02d7a5611be28dfaa2a2154c1` | Yes |
| 166 | shared Pokéathlon competition script | 2724 | `c98c8d9e005acb7ed93ed7d506f7c66bff1be629` | Yes |
| 5 | D01R0101 — Brock / trade context | 888 | `9f7f2d45eacacd4250bf1d2cd0f8a2f04148c53f` | Yes |
| 834 | T11R0601 — Lt. Surge / trade context | 720 | `63bb685e9d8ccaaca8965e5110b6d2745bc47cec` | Yes |
| 913 | T26GYM0101 — Jasmine / trade context | 1488 | `902dbb04bb136d96b30aa5ba341db4be86ea4425` | Yes |

## Key findings

### 1. Facility data must use real save substructures

HGSS allocates independent persistent data for Safari Zone, Photo Album, Pokéathlon and Apricorn Box. Pokéathlon alone is a `0xB80` structure with solo/link records, per-Pokémon course bits, Athlete Points (capped at 99,999) and unlock/daily bitfields. Photo Album stores 36 metadata-rich records. Safari Zone stores custom layouts, objects and area levels.

**Integration rule:** facility databases are not story flags.

### 2. Crystal Battle Tower and HGSS Frontier must coexist

Crystal already has a complete Battle Tower: three-Pokémon party, seven-battle sequence, challenge/save state and SRAM history of previously selected trainers. HGSS adds a separate five-facility Frontier (Tower, Factory, Hall, Castle, Arcade), Battle Points and per-facility Print progress.

The target keeps both source-era rulesets instead of replacing Crystal's Tower with the HGSS Frontier.

### 3. Safari Zone aging is encounter-table logic

HGSS stores each arranged area and every placed object with ID/x/y/z. Encounter-relevant blocks have Plains, Forest, Peak and Water categories. Bonus slots contain one/two object-level requirements.

Verified aging threshold tables:

```text
Plains: 1, 5, 10, 15, 20
Forest: 2, 6, 11, 16, 21
Peak:   3, 7, 12, 17, 22
Water:  4, 8, 13, 18, 23
```

After elapsed days, the engine compares encounter arrays before/after maturation. Baoba's “new Pokémon” call is queued only for areas whose effective table changed.

### 4. The RTC penalty is exactly 1440 minutes on a new console

`SysInfoRTC_HandleContinueOnNewConsole` sets `penaltyInMinutes = 1440`. Forward minutes count it down. During a penalty, day-based Safari maturation and Apricorn Box processing are skipped, even though ordinary daily rollover still occurs.

Backward RTC movement updates the stored date/time without awarding negative-time progress.

### 5. Field Apricorn trees and Apricorn Box are distinct

Legacy GSC daily harvestable trees are preserved. HGSS has stable tree indices/color mapping and a separate Apricorn Box save array. Tree refresh, Apricorn inventory, Apricorn Box processing and Kurt's Ball job must not share one timer.

### 6. Lottery rules are source-specific

**G/S/C:** weekly Lucky Number cycle; PP Up (2 digits), Exp. Share (3/4), Master Ball (exact).  
**HGSS:** daily Lottery Corner; Ultra Ball (1), PP Up (2), Exp. Share (3), Max Revive (4), Master Ball (exact).

HGSS day rollover directly advances the Loto ID RNG.

### 7. Radio schedule is code-driven

HGSS Pokémon Music reads the actual RTC weekday.

Before National Dex:
- Mon/Fri: March
- Tue/Sat: Lullaby
- Wed: March
- Thu: Lullaby
- Sun: March unless GB Sounds condition applies

After National Dex:
- Wed: Hoenn Sound
- Thu: Sinnoh Sound
- other days retain the verified March/Lullaby branches
- Sunday can use GB Sounds when the item is owned.

Because Hoenn/Sinnoh Sound changes encounters, this must feed the encounter engine, not only BGM.

### 8. Photo Album is persistent structured data

Each saved photo stores map/coordinates/date/time, player data, lead nickname, subject, camera parameters, and up to six party species/forms/shiny/gender records. The album has 36 slots. Scheduled Cameron/Leader appearances are world-state scheduling layered over this database.

### 9. Gym Leader trades are full NPC trades

Verified HGSS one-time examples:
- Lt. Surge: Pikachu → foreign Pikachu `Volty`
- Brock: Bonsly → Rhyhorn `Hornlette`
- Jasmine: eligible player Pokémon → Steelix `Rusty`

Each has a distinct completion flag. OT/nickname/item/IV/personality metadata must be retained.

### 10. Phone contact and encounter notifications are separate classes

HGSS defines 75 phone contacts (IDs 0–74). They include story/service contacts, ordinary trainers, 16 Gym Leaders, Baoba, gifts, news and rematches. Gen II phone swarms remain separate from HGSS's postgame mass-outbreak subsystem.

### 11. Friday Lapras remains recurring

Union Cave B2F has a Lv20 Lapras every Friday in both Gen II and HGSS. HGSS gives it the Gen IV move/ability data. Weekly encounter resolution must not be treated like a permanent legendary-hide flag.

## Recommended save namespaces

```text
POKEATHLON_SAVE
CRYSTAL_BATTLE_TOWER_SAVE
HGSS_FRONTIER_SAVE
SAFARI_ZONE_SAVE
PHOTO_ALBUM_SAVE
APRICORN_BOX_SAVE

RTC_STORED_DATETIME
RTC_PENALTY_MINUTES
DAILY_FLAGS
WEEKLY_FLAGS

LOTTERY_CURRENT_ID
LOTTERY_CYCLE_CLAIMED

PHONE_CONTACTS
PHONE_GIFTS
PHONE_NEWS
PHONE_REMATCH
PHONE_SWARMS

SCHEDULED_NPC_STATE
WEEKLY_STATIC_ENCOUNTER_STATE
```

## Verification checklist
1. Pokéathlon records, athlete points and daily bits survive/reset independently.
2. Crystal Battle Tower state cannot overwrite HGSS Frontier current-run/record/Print data.
3. BP is independent from money, coins and Athlete Points.
4. Safari layout and block coordinates survive save/load.
5. Safari area age follows the area when arrangements change.
6. Block changes recalculate the correct typed-object encounter conditions.
7. Baoba notification occurs only after effective encounter-table change.
8. New-console RTC penalty is exactly 1440 minutes.
9. RTC penalty freezes Safari maturation and Apricorn Box day processing.
10. Backward clock changes grant no forward progress.
11. GSC weekly and HGSS daily Lottery modes retain their own prizes/cadence.
12. Goldenrod weekday vendors and haircut daily-use state coexist with Rocket/story flags.
13. Crystal rooftop sale is not replaced by HGSS 6F raffle.
14. Hoenn/Sinnoh Sound require National Dex and alter encounter selection.
15. Photo Album safely handles all 36 slots and preserves metadata.
16. Scheduled photo actors cannot duplicate a leader assigned to the Dojo.
17. Surge/Brock/Jasmine trades set completion only after a completed trade.
18. Full bag/party/invalid selections cannot consume pending rewards/trades.
19. All 75 phone IDs fit and preserve behavior classes.
20. Gen II phone swarms and HGSS mass outbreaks coexist.
21. Friday Lapras follows weekly recurrence after save/load and week rollover.

## Primary source manifest

- `pret/pokegold`: phone, daily tree, Goldenrod recurring shop, Lucky Number systems
- `pret/pokecrystal`: Battle Tower engine/maps/SRAM, Buena/radio, Union Cave B2F, Fuchsia Safari closure
- `pret/pokeheartgold`:
  - `include/pokeathlon/pokeathlon_save.h`
  - `src/pokeathlon/*`
  - `include/safari_zone.h`
  - `src/unk_02097268.c`
  - `src/unk_02055418.c`
  - `src/sav_system_info.c`
  - `src/apricorn_tree_sys.c`
  - `src/unk_02031B0C.*`
  - `include/photo_album.h`
  - `src/field_take_photo.c`
  - `src/application/pokegear/radio/shows/pokemon_music.c`
  - `include/constants/phone_contacts.h`
  - `files/tel/pmtel_book.json`
  - `include/constants/npc_trade.h`
  - field scripts listed in the direct-ROM table

Secondary sources were used only to cross-check schedules/prize tables and trade presentation (Bulbapedia/Serebii).

## Phase 12 conclusion

Phase 12 establishes that HGSS's post-story/time-based content depends on multiple persistent databases and a shared RTC transaction layer. Correct backport order is:

```text
save expansion
→ RTC callbacks
→ facility data formats
→ UI
→ field actors/scripts
→ encounter/battle integration
→ save/load + rollover + clock-tamper verification
```

Phase 13 should enumerate the contents inside these formats row-by-row: every Pokéathlon course/event, every Frontier mode/Frontier Brain threshold, every Safari area/block/bonus encounter, every photo spot, every phone gift/news/swarm entry and every radio channel/program.
