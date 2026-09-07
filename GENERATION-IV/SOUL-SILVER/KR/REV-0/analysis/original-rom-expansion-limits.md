# Pokémon SoulSilver (KR) Rev-0 — original ROM expansion limits

Baseline checked from the project source ROM; original ROM itself is never committed.

- Game code: `IPGK`
- Region/language bucket: `KR`
- Header ROM version: `0`
- Size: 128 MiB
- SHA-1: `0330e6449306606114a92bdbb3f9d3d51d392b96`
- CRC32: `CE5CB206`
- Target model: 1025 Species / 1351 varieties / 1579 form records, with append-only room for Gen 10+

## Confirmed structural observations

| Area | SoulSilver original | Expansion implication |
|---|---|---|
| Box/Party Species | `u16` | 1025+ Species IDs are representable |
| Trainer party Species/Form | lower 10 bits Species + upper 6 bits Form in one `u16` | Species ceiling 1023; #1024+ requires loader/data-format patch |
| Stored form | 5-bit form field | >31 local forms requires extension |
| Personal data | 508 records × 44 bytes | NARC can grow; lookups/loaders must be audited |
| Level-up learnset | level 7 bits + move 9 bits packed in `u16` | Move IDs above 511 require a new learnset format |
| Evolutions | fixed 7 entries/species | Modern Eevee already exceeds the native model |
| Abilities | two `u8` slots in personal data | Hidden Ability + IDs >255 require extension |
| TM/HM compatibility | four `u32` bitfields | Native ceiling is 128 machine flags |
| National Pokédex | Gen IV 493-species fixed design | Save/UI/form handling must be generalized |
| Base graphics | legacy 493-era arithmetic layout | Replace with explicit Form → asset lookup |

The trainer packing is a hard wall: 10 Species bits represent 0–1023, so a direct National Dex ID mapping fails at #1024 Terapagos and #1025 Pecharunt.

The SoulSilver ROM currently has roughly 9.13 MiB of unused tail space. Fixed/packed data formats fail before raw ROM capacity, but a full modern sprite/form set will require ROM/FAT growth.

## Recommended logical model

```text
Species ID   -> u16, append-only
Variety ID   -> new u16
Form ID      -> new u16
Move ID      -> u16
Ability ID   -> u16
Evolution    -> variable-length
Learnset     -> variable-length, uncompressed move ID
Machine learn-> dynamic list/bitset
Dex species  -> dynamic bitset
Dex forms    -> dynamic bitset/table
Graphics     -> Form-to-asset lookup
```

Current counts 1025 / 1351 / 1579 are data counts, not engine maxima.

## Repository policy

Path follows `GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`.
Original commercial ROM images are excluded; only safe analysis, source, scripts, patches/deltas, metadata, and generated artifacts are committed.
