# Generation V Black/White — Phase 3 Core Record Databases

## Scope

This phase decodes the core gameplay NARC records in the uploaded Black/White ROMs into reproducible CSV databases. The ROMs are read-only inputs. Raw IDs and bytes are retained wherever semantics are uncertain. Black is used for core archives that are byte-identical between versions; encounters are emitted separately for Black and White.

## Completed archives

| Archive | Members | Decoding status |
|---|---:|---|
| `a/0/1/6` personal | 669 | 1–649 species, 650–667 alternate stat/type forms, 668 regional Pokédex map |
| `a/0/1/7` growth | 8 | 101 × u32 XP totals per curve |
| `a/0/1/8` level-up moves | 668 | repeated `u16 move, u16 level`, `FFFFFFFF` terminator |
| `a/0/1/9` evolution | 668 | seven 6-byte evolution slots per record |
| `a/0/2/0` baby/base table | 650 | one u16 species ID per member |
| `a/0/2/1` moves | 560 | 36-byte move parameter records |
| `a/0/2/4` items | 627 | 36-byte item parameter records |
| `a/0/9/2` trainer data | 616 | 20-byte normal records; ID 0 dummy is 16 bytes |
| `a/0/9/3` trainer parties | 616 | template-dependent 8/16/10/18-byte Pokémon records |
| `a/1/2/3` egg moves | 650 | direct u16 lists |
| `a/1/2/6` encounters | 112 per version | 232-byte blocks; 12 members contain four seasonal blocks |

## Strong ROM-derived validations

- Personal member 668 is exactly **1300 bytes = 650 × u16** and maps National species IDs to BW Unova Pokédex numbers. It contains **156 non-999 values**, from Victini `#494 -> 0` through Genesect `#649 -> 155`; `999` means absent from the regional Pokédex.
- Base personal records point directly to alternate-stat records through `form_stats_start`. This independently reconstructs indexes 650–667.
- Growth curves 6 and 7 are byte-for-byte copies of curve 0; ordinary species 1–649 use only growth IDs [0, 1, 2, 3, 4, 5].
- Every non-empty trainer party validates exactly against the trainer template: template 0 = 8 bytes/Pokémon, 1 = 16, 2 = 10, 3 = 18. Template distribution among trainers with Pokémon is `{0: 546, 1: 42, 2: 20, 3: 7}`.
- Encounter archive layout is **100 × 232-byte members + 12 × 928-byte members**. A 928-byte member is four consecutive seasonal blocks in Spring → Summer → Autumn → Winter order. Black and White differ in **29/112** encounter members.

## Personal record (BW)

Offsets 0–39 contain the six stats, types, catch rate, EV-yield bitfield, three held-item fields, gender/hatch/friendship/growth data, egg groups, three abilities (including hidden ability), form linkage, color, base EXP, height and weight. Bytes 40–55 contain TM/HM compatibility. The first 13 bytes encode TM01–TM95 and HM01–HM06; the remaining three bytes are preserved as reserved/unknown. Bytes 56–59 are a u32 tutor compatibility field used by the three Pledge moves, the three elemental ultimate starter moves, and Draco Meteor.

## Trainer party record templates

All four templates start with `strength, ability/gender, level, padding, species(u16), form(u16)`. Template 1 adds four move IDs. Template 2 adds a held item. Template 3 adds both. The IV value used uniformly for all six stats is `(strength * 31) // 255` according to the documented Gen V trainer creation routine.

## Encounter block (232 bytes)

Bytes 0–7 are encounter-mode/tile flags. Bytes 8–151 are three 12-slot land tables (regular, double grass, shaking); bytes 152–231 are four 5-slot water/fishing tables (surf, surf spot, fishing, fishing spot). Every slot is `u16 species, u8 min level, u8 max level`. Slot-rate percentages are emitted in the CSV.

## Conservative fields

Move and item archives have several fields whose historical community labels are incomplete or implementation-specific. The database therefore preserves those bytes as `unknown_*` or `*_candidate` instead of turning old guesses into asserted facts. The raw 36-byte record is also preserved in every row.

## Outputs

- `personal.csv`, `regional_dex_mapping.csv`, `growth_curves.csv`
- `levelup_moves.csv`, `levelup_records.csv`, `evolutions.csv`, `baby_base_species.csv`, `egg_moves.csv`, `egg_move_records.csv`
- `moves.csv`, `items.csv`
- `trainers.csv`, `trainer_parties.csv`
- `encounter_records.csv`, `encounter_slots.csv`
- `audit.csv`, `schema.json`
- `build_gen5_bw_phase3_databases.py`

## Index-range caution

The personal NARC records at 650–667 are alternate-form parameter records. They must not be conflated with unrestricted normal species IDs: Generation V has special Egg/Bad Egg index behavior in part of the same beyond-649 number range. This phase records NARC member identity and form linkage, not a claim that every member index is a safe standalone species identifier.

See `PROVENANCE.md` for field-source and uncertainty notes.

## Next boundary

The next phase should bind map identities through `a/0/1/2` ZoneData, `a/1/2/5` overworld/event objects and `a/0/5/7` scripts, then connect map records to the encounter-member indices generated here.
