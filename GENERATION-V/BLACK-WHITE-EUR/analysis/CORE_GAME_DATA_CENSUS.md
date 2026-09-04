# Pokémon Black/White EUR — Core game-data census

No ROM bytes were modified. This phase resolves the fixed/record-oriented data that directly controls species, forms, Pokédex membership, evolutions, moves, items and trainer parties.

## Personal archive `a/0/1/6`

The archive contains **669 members** and is composite rather than a flat 669-species table:

- member 0: 56-byte placeholder/special entry.
- members **1..649**: base species PersonalInfo records, exactly **60 B (0x3C)** each.
- members **650..667**: exactly **18 alternate-form PersonalInfo records**, also 60 B each.
- member **668**: **1,300 B = 650 × u16** local Pokédex mapping table.

The 18 alternate-form personal records are all reachable from base-species `FormStatsIndex`; there are no orphan form-stat members. Species that report multiple forms with `FormStatsIndex=0` share the base personal stats rather than consuming additional records.

### Unova Dex mapping table

Member 668 maps species IDs 0..649 to the local Unova Pokédex number. The sentinel is **999**.

- sentinel 999: **494 entries**.
- actual local Dex numbers: **0..155**, each present exactly once (156 species).
- species 494 Victini → **0**.
- species 495 Snivy → **1**.
- species 649 Genesect → **155**.

This is a direct expansion dependency: a future expanded Unova Dex must extend/rebuild this mapping in addition to adding PersonalInfo records and form routing.

## PersonalInfo5BW 60-byte record

`personal_layout.csv` records every known field. Key fields include base stats at 0x00..0x05, types 0x06..0x07, EV yield at 0x0A, held-item slots 0x0C..0x10, abilities 0x18..0x1A, `FormStatsIndex` 0x1C, `FormSprite` 0x1E, `FormCount` 0x20, BaseEXP/height/weight 0x22..0x26, 101 TM/HM bits at 0x28..0x34, and tutor bits at 0x38.

## Evolution archive `a/0/1/9`

- **668 members × 42 B**.
- each file is **7 slots × 6 B**.
- slot layout: `u16 method + u16 parameter + u16 target species`.
- maximum nonzero evolution slots observed locally: **7**.

## Move and item tables

- `a/0/2/1`: **560 move records × 36 B**.
- `a/0/2/4`: **627 item records × 36 B**.
- `a/0/2/0`: **650 base-evolution/baby mapping members × 2 B**.

## Trainer data

- `a/0/9/2`: **616 trainer metadata members**.
- `a/0/9/3`: **616 trainer party members**.
- local party-length proof has **0 mismatches** against the four template layouts.

Template byte 0 controls per-Pokémon party record size:

| Flag | Trainers | Bytes/mon | Payload |
|---:|---:|---:|---|
| 0 | 547 | 8 | base |
| 1 | 42 | 16 | base + four explicit moves |
| 2 | 20 | 10 | base + held item |
| 3 | 7 | 18 | base + held item + four explicit moves |

The base 8-byte party record is strength/IV byte, ability-gender selector, level, padding, species u16 and form u16. Template flags append held item and/or four explicit move IDs.

## Generated ledgers

- `personal_layout.csv`
- `personal_member_census.csv`
- `personal_form_map.csv`
- `unova_dex_mapping.csv`
- `trainer_party_template_census.csv`
- `trainer_party_template_summary.csv`
- `core_game_data_summary.json`
- `core_game_data_census.py` reproduces this phase from the Black ROM + existing NitroFS inventory.
