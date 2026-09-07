# Generation IV ROM Expansion Limits

Date: 2026-09-07
Scope: Pokémon Diamond / Pearl / Platinum / HeartGold / SoulSilver original ROM structure review for National Dex 1025 species + varieties/forms expansion.

## Target data model

- Species: 1025
- Pokémon varieties: 1351
- Pokémon Form records: 1579
- Future-proofing: allow Gen 10+ append-only expansion rather than hard-coding the current counts as engine maxima.

## Confirmed structural limits

| Area | Original Gen IV representation | Effective limit | Expansion status |
|---|---|---:|---|
| Box/Party Species | u16 species | 65535 | Sufficient for 1025+ |
| Wild encounter Species | u16 species | 65535 | Sufficient for 1025+ |
| Trainer Species (Pt/HGSS) | 10-bit Species + 6-bit Form in one u16 | Species 1023 | Must patch from #1024 onward |
| Stored Pokémon Form | 5-bit form field | 0-31 | Must extend for >31 local forms |
| Personal data record | 44 bytes per slot | D/P 501 slots; Pt/HGSS 508 slots in originals | NARC can grow, code/lookup must be patched |
| Level-up learnset | level 7 bits + move 9 bits in one u16 | Move ID 511 | Must replace learnset format for modern move IDs |
| Evolution branches | fixed 7 entries per species | 7 | Must make variable-length; Eevee already needs 8 |
| Ability slots | u8 abilities[2] | 2 slots, IDs <=255 | Must add Hidden Ability / wider IDs |
| Machine compatibility | 4 x u32 bitset | 128 machines | Must generalize for modern TM sets |
| Pokédex | compile-time National Dex count 493 and fixed arrays | 493 base design | Must resize/generalize save structures |
| Base sprite lookup | arithmetic/legacy layout around 494 base slots | 493 species-era design | Must replace with explicit Form/Graphic lookup |
| NARC member count | u16-style container counts | far above current needs | Container itself is not the first bottleneck |

## Key hard wall: trainer data

Platinum / HeartGold / SoulSilver trainer party data packs Species and Form into one 16-bit value.

- Species: lower 10 bits
- Form: upper 6 bits
- Maximum Species value: 1023

Therefore an internal Species ID that directly follows the National Dex fails at:

- #1024 Terapagos
- #1025 Pecharunt

This is the first confirmed Species-ID wall in the original battle/trainer data formats. The loader and trainer-data format must be patched rather than only enlarging NARC tables.

## Stored Pokémon Species vs. Form

The core Box/Party Pokémon structure already stores Species as u16, so a 1025-species expansion does not require widening the Species field itself.

However the stored Form field is only 5 bits, so one individual can natively store only form values 0-31. A future-proof engine should introduce an extended form identifier, preferably u16, while retaining compatibility with legacy data where possible.

## Personal table counts observed in the original ROMs

- Diamond: 501 x 44-byte personal records
- Pearl: 501 x 44-byte personal records
- Platinum: 508 x 44-byte personal records
- HeartGold: 508 x 44-byte personal records
- SoulSilver: 508 x 44-byte personal records

The post-493 records demonstrate that the original engine already separates National-Dex species identity from some alternate battle-parameter slots. This makes a generalized Species -> Variety -> Form architecture compatible with the direction of the original design.

## Learnset packing wall

Original level-up learnset entries pack both fields into one u16:

- 7 bits: level
- 9 bits: move ID

Thus the maximum move ID is 511. This is insufficient for a modern all-generation move database.

Recommended replacement:

```c
struct LevelUpMove {
    uint16_t move;
    uint8_t level;
    uint8_t flags;
};
```

This removes the 9-bit move-ID wall and leaves room for future learning-method flags.

## Evolution table wall

The original evolution data reserves exactly seven evolution entries per species. That matched Gen IV Eevee, but modern Eevee has eight evolutions. Use a variable-length evolution list instead of raising the fixed maximum to another arbitrary constant.

## Ability wall

Original personal data has two u8 ability slots. Modern data needs at least Ability 1, Ability 2, and Hidden Ability, while future-proofing also argues for u16 ability IDs.

Recommended logical model:

```text
Ability 1 : u16
Ability 2 : u16
Hidden    : u16
```

## TM/HM wall

The original personal record stores machine compatibility as four 32-bit bitfields, i.e. 128 total machine flags. Modern TM sets can exceed that model.

Recommended change: move machine compatibility out of the fixed personal record into a variable-length list or dynamically sized bitset.

## Pokédex wall

The original Pokédex save structure is designed around 493 species and contains fixed compile-time arrays for seen/caught/language/form data. Alternate forms are also represented by species-specific special cases.

For 1025 Species / 1579 Form records, generalize into separate species and form bitsets / metadata tables rather than adding more one-off form fields.

## Graphics architecture

The base Pokémon graphics layout is built around the original species range, while special forms are split into separate legacy resources. A future-proof engine should stop deriving graphics from Species ID arithmetic and use an explicit mapping:

```text
Species / Variety / Form
        -> GraphicSetID
        -> front/back
        -> male/female
        -> normal/shiny
        -> icon
        -> height/animation metadata
```

## ROM-space observations

Approximate unused tail space observed in the source ROM images:

- Diamond: ~5.66 MiB
- Pearl: ~5.66 MiB
- Platinum: ~30.12 MiB
- HeartGold: ~9.13 MiB
- SoulSilver: ~9.13 MiB

ROM capacity is therefore not the first architectural bottleneck. Data formats and hard-coded lookup logic fail earlier. D/P and HGSS will nevertheless require ROM/FAT growth once a full modern sprite/form asset set is added.

## Recommended Generation IV expansion architecture

Keep already-wide original fields where possible and replace compressed/fixed structures only where necessary:

```text
Species ID      -> u16, append-only
Variety ID      -> new u16
Form ID         -> new u16
Move ID         -> u16
Ability ID      -> u16
Evolution       -> variable-length
Learnset        -> variable-length, uncompressed move ID
Machine learn   -> dynamic list/bitset
Dex species     -> dynamic bitset
Dex forms       -> dynamic bitset / table
Graphics        -> Form-to-asset lookup
```

Current database counts (1025 / 1351 / 1579) must be treated as current data counts, not engine maxima, so Gen 10+ additions can be appended without another structural redesign.

## Upload policy

Do not commit original commercial ROM images or other copyrighted redistributable binaries. Repository output should contain only safe reverse-engineering notes, source code, scripts, patches/deltas, metadata, and generated analysis artifacts.
