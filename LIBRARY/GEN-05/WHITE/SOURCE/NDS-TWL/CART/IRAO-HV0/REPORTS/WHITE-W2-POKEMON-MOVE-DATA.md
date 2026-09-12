# Pokémon White IRAO-HV0 — W2 Pokémon / move / evolution / breeding structures

Status: **direct ROM decode in progress; record boundaries and the structures below are verified against the supplied White ROM.**

Source dump: `SWEETNDS-f94d4578` (`f94d4578956487c09fee20809a591e858017769e`). ROM binary is not committed.

## 1. Personal archive `a/0/1/6`

Direct member-size profile:

- members: **669**
- member `0`: **56 bytes** — zero/dummy record, shorter than normal
- members `1..667`: **60 bytes each**
- member `668`: **1300 bytes** — not a personal record; separate `650 × u16` lookup table

This means the archive is not a flat 669-species table.

### Primary and alternate-form records

- `1..649`: National Pokédex species records
- `650..667`: 18 alternate-form personal records

Base-species `formid` links reveal the 18 extra records:

| Base NatDex | Pokémon | formid | numforms | Extra personal records |
|---:|---|---:|---:|---|
| 386 | Deoxys | 650 | 4 | 650–652 |
| 413 | Wormadam | 653 | 3 | 653–654 |
| 492 | Shaymin | 655 | 2 | 655 |
| 487 | Giratina | 656 | 2 | 656 |
| 479 | Rotom | 657 | 6 | 657–661 |
| 351 | Castform | 662 | 4 | 662–664 |
| 550 | Basculin | 665 | 2 | 665 |
| 555 | Darmanitan | 666 | 2 | 666 |
| 648 | Meloetta | 667 | 2 | 667 |

Other species can advertise graphical/form counts without allocating separate personal records here (for example Unown, Burmy, Cherrim, Shellos/Gastrodon, Arceus, Deerling/Sawsbuck and Genesect). Therefore `numforms > 1` must not be interpreted as “there are that many personal-record members”.

### Member 668: Unova Pokédex lookup

The final member is exactly `650 × u16 = 1300` bytes. Decoded values are:

- species IDs `0..493` → `999`
- species ID `494` (Victini) → `0`
- `495` → `1`
- …
- species ID `649` (Genesect) → `155`

That is the BW Unova Pokédex numbering relation (`National species ID → Unova Dex number`), with `999` acting as the out-of-Unova-Dex sentinel for pre-Unova species.

### Normal 60-byte personal record

Verified/cross-checked field layout for members `1..667`:

| Offset | Size | Field |
|---:|---:|---|
| `0x00` | 6 | HP / Atk / Def / Speed / SpAtk / SpDef |
| `0x06` | 2 | type 1 / type 2 |
| `0x08` | 1 | catch rate |
| `0x09` | 1 | evolutionary-stage field |
| `0x0A` | 2 | EV-yield bitfield |
| `0x0C` | 2 | held item 1 |
| `0x0E` | 2 | held item 2 |
| `0x10` | 2 | third / hidden-context held item |
| `0x12` | 1 | gender ratio |
| `0x13` | 1 | hatch-cycle value |
| `0x14` | 1 | base friendship |
| `0x15` | 1 | growth-table ID |
| `0x16` | 2 | egg group 1 / 2 |
| `0x18` | 3 | ability 1 / ability 2 / hidden ability |
| `0x1B` | 1 | flee / auxiliary |
| `0x1C` | 2 | alternate-personal `formid` |
| `0x1E` | 2 | form/sprite-related index |
| `0x20` | 1 | number of forms |
| `0x21` | 1 | Pokédex color |
| `0x22` | 2 | base EXP |
| `0x24` | 2 | height |
| `0x26` | 2 | weight |
| `0x28..0x34` | 13 | TM/HM compatibility bitfields |
| `0x35..0x37` | 3 | zero/reserved in this White corpus |
| `0x38` | 1 | special move-tutor compatibility bitfield |
| `0x39..0x3B` | 3 | zero/reserved in this White corpus |

Direct corpus check: offsets `0x35–0x37` and `0x39–0x3B` are zero in all 667 normal/form records. Offset `0x38` is nonzero in 76 records.

## 2. Growth tables `a/0/1/7`

There are **8 members × 404 bytes**. Each member is exactly `101 × u32`, indexed by level `0..100`.

Level-100 totals identify the standard curves:

| Growth ID | Level 100 EXP | Interpretation | Used by primary species? |
|---:|---:|---|---|
| 0 | 1,000,000 | Medium Fast | yes (251) |
| 1 | 600,000 | Erratic | yes (22) |
| 2 | 1,640,000 | Fluctuating | yes (14) |
| 3 | 1,059,860 | Medium Slow | yes (175) |
| 4 | 800,000 | Fast | yes (52) |
| 5 | 1,250,000 | Slow | yes (135) |
| 6 | 1,000,000 | duplicate of ID 0 | no |
| 7 | 1,000,000 | duplicate of ID 0 | no |

IDs 0, 6 and 7 are byte-identical. Primary species `1..649` use only IDs `0..5`.

## 3. Level-up learnsets `a/0/1/8`

- members: **668** (`0..667`, matching dummy + primary species + alternate personal forms; there is no member for the final regional-Dex lookup table)
- entry width: **4 bytes**
- value: little-endian `u32`, low 16 bits = move ID, high 16 bits = level
- terminator: `FF FF FF FF`
- member 0 consists only of the terminator

Example: member 1 begins `0x00010021`, which decodes to move ID `33` at level `1`.

## 4. Evolution data `a/0/1/9`

- members: **668**
- every member: **42 bytes**
- layout: **7 × (`u16 method`, `u16 parameter`, `u16 target_species`)**

Direct non-empty-slot distribution across all 668 records:

- 365 records: 0 evolution slots
- 291 records: 1 slot
- 10 records: 2 slots
- 1 record: 3 slots
- 1 record: all 7 slots

The seven-slot record is NatDex 133 (Eevee), confirming that all seven slots are live data rather than padding.

## 5. Baby/base-species table `a/0/2/0`

- **650 members**
- every member: **2 bytes (`u16`)**
- indexing covers `0..649` only; alternate personal form slots are not independently indexed here.

## 6. Move parameters `a/0/2/1`

- **560 members**
- every member: **36 bytes (`0x24`)**
- archive therefore covers move IDs `0..559`
- record 0 is all zeroes

The 36-byte layout cross-checks against BW research/RawDB. Direct sanity check on move ID 1 produces type=0, physical category, power=40, accuracy=100, PP=35, matching Pound.

Key offsets:

| Offset | Size | Field |
|---:|---:|---|
| `0x00` | 1 | type |
| `0x01` | 1 | effect category |
| `0x02` | 1 | physical / special / status category |
| `0x03` | 1 | power |
| `0x04` | 1 | accuracy |
| `0x05` | 1 | PP |
| `0x06` | 1 signed | priority |
| `0x07` | 1 | multi-hit data |
| `0x08` | 2 signed | result effect |
| `0x0A` | 1 | effect chance |
| `0x0B..0x0F` | 5 | status / duration / crit / flinch fields |
| `0x10` | 2 | effect ID |
| `0x12` | 1 | recoil / target HP change |
| `0x13` | 1 | healing / user HP change |
| `0x14` | 1 | target selector |
| `0x15..0x17` | 3 | affected stats 1–3 |
| `0x18..0x1A` | 3 | stat magnitudes 1–3 |
| `0x1B..0x1D` | 3 | stat-effect chances 1–3 |
| `0x1E..0x1F` | 2 | padding / auxiliary bytes in the surveyed format |
| `0x20` | 2 | move flags |
| `0x22..0x23` | 2 | trailing padding / auxiliary |

## 7. Egg moves `a/1/2/3`

- **650 members**, indexed `0..649`
- member 0 is empty
- normal family file begins with `u16 count`, then `count × u16 move_id`
- species with no list typically contain only `00 00`

Example: member 1 is 30 bytes = count `14` + fourteen 16-bit move IDs.

## 8. Immediate implications

1. Any extractor/rebuilder must treat personal member 668 as a regional-Dex mapping table, not a Pokémon stat record.
2. Alternate forms occupy personal/learnset/evolution slots through 667, while breeding/base-species tables stop at 649.
3. Form count, personal-form allocation and visual form allocation are separate concepts.
4. Growth IDs 6/7 must be preserved even though no primary species uses them; they are real archive members, not safe deletion candidates.
5. All source bytes marked reserved/unknown remain preserved until runtime-reference tracing proves their meaning.

## Cross-check references

- Project Pokémon PPRE: BW archive mapping (`personal=a/0/1/6`, growth `a/0/1/7`, learnsets `a/0/1/8`, evolution `a/0/1/9`).
- Project Pokémon RawDB `nds/fmt.py`: Gen V personal, move, evolution and learnset structures.
- ABZB Pokémon ROM Balancer notes: Gen V personal byte map and TM/HM/tutor compatibility region.

Direct ROM measurements and member-level values take precedence over external notes when they disagree.
