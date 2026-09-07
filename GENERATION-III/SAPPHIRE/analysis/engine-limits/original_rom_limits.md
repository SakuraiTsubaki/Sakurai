# Pokémon Sapphire (USA) Rev-0 — original ROM limits audit

Baseline ROM:

- Title: Pokémon Sapphire Version (USA), Rev-0
- Game code: `AXPE`
- ROM size: `0x01000000` bytes = 16 MiB
- SHA-1: `3ccbbd45f8553c36463f13b938e833f652b793e4`
- Matches the pret/pokeruby Sapphire Rev-0 build baseline.

This report separates **numeric field capacity**, **compiled-engine assumptions**, **save-layout constraints** and **ROM-space pressure**. The current project targets 1025 canonical species, 1351 Pokémon/variety records and 1579 form records while leaving room for later generations.

## 1. Species ID capacity

Stored Pokémon species IDs are 16-bit in the original engine. Therefore the fundamental numeric species-ID space is much larger than the original 412-species working domain.

The original ~412 limit is primarily imposed by:

- constants such as the original Pokémon slot count;
- fixed-size tables;
- loops/bounds checks;
- National Dex conversion code;
- save bitfields;
- Egg/Unown special-case arithmetic.

Conclusion: **1025 canonical species and 1579 current form records do not require widening the core species field.** They do require removing original table/bounds assumptions.

## 2. Target future-proof namespace

The active project policy is:

```text
0x0000          NONE
0x0001..0x0FFF  canonical National-Dex species (#1..#4095 capacity)
0x1000..0xEFFF  runtime varieties/forms
0xF000..0xFFEF  reserved engine namespace
0xFFF0..0xFFFF  special/sentinel values (Egg/invalid/etc.)
```

Current National Dex species occupy #1..#1025. Generation 10+ can append at #1026 without moving form IDs.

## 3. BaseStats

Direct inspection of the built Rev-0 ROM shows a 28-byte stride between consecutive BaseStats records. The earlier relocation proof found the original table at approximately `0x001FEBA8` and successfully relocated its 412-record domain.

Capacity examples:

- 412 records × 28 bytes = 11,536 bytes.
- 1,579 records × 28 bytes = 44,212 bytes (~43.2 KiB).

Therefore BaseStats count itself is not a meaningful ROM-size bottleneck at the current scope.

Important native field limits inside BaseStats include:

- six base stats: u8 each;
- type IDs: u8 each;
- catch rate: u8;
- base EXP yield: u8;
- ability IDs: two u8 slots;
- held items: u16 each;
- compact EV-yield bitfields.

The final architecture should retain exact canonical data outside this narrow ABI and widen/redirect fields where needed rather than silently truncating values.

## 4. Level-up learnset hard limit

The native packed `LevelUpMove` format uses:

- 9 bits for move ID;
- 7 bits for level.

That produces a hard native learnset move-ID ceiling of **511**.

This limit is independent of the four move slots stored on an individual Pokémon, which are wider. Therefore later-generation moves cannot be represented faithfully in native level-up learnsets without replacing/widening the learnset format and auditing every reader.

Status: **engine extension required** for full modern move IDs.

## 5. Ability hard limits

Native BaseStats contains only:

- `ability1` as u8;
- `ability2` as u8.

The original engine also assumes selection between two normal ability slots. This creates two separate limits:

1. ability ID range is limited to 0..255 by native storage;
2. there is no native third/hidden-ability slot.

Status: **engine extension required** for complete modern abilities/hidden abilities.

## 6. Base EXP hard limit

Native BaseStats stores base EXP yield as u8, giving a 0..255 range.

Canonical imported values must not be silently clamped. Either widen the runtime representation or keep base EXP in an extended table and update consumers.

Status: **engine extension required** for exact out-of-range values.

## 7. Evolution table limit

The original design gives each species a fixed five-entry evolution array.

This is structurally unsuitable for a future-proof all-generation registry because later species can have many branches and newer trigger types.

Recommended replacement:

```text
Species ID
  -> evolution-list index/pointer
  -> variable-length Evolution[]
```

Status: **replace fixed per-species array with variable-length storage**.

## 8. Pokédex seen/owned storage

The original Dex flag arrays are sized from the original Pokémon slot count. With 412 flags, each bitfield requires 52 bytes.

For 1025 canonical National Dex entries:

```text
ceil(1025 / 8) = 129 bytes
```

Each affected bitfield therefore grows by 77 bytes. Seen/owned data exists in multiple save structures/copies, so this is not a one-line constant change.

The important constraint is the original fixed SaveBlock/RAM layout: blindly increasing Dex arrays shifts following data and can cause overlap or invalidate serialization assumptions.

Status: **save/RAM layout audit and coordinated migration required**.

Forms should not consume independent National Dex seen/owned bits unless explicitly desired; the canonical Dex bitset should be indexed by National Dex species, while form discovery can use a separate optional structure.

## 9. Egg and Unown special cases

Original Ruby/Sapphire internal Species IDs include compatibility/special slots for Egg and multiple Unown forms, and portions of the engine perform arithmetic or bounds logic around those ranges.

These assumptions conflict with the new canonical `SPECIES_* == National Dex` policy.

Status: **audit every Egg/Unown special-case consumer and replace it with registry/form lookups before renumbering becomes authoritative**.

## 10. ROM-space observations

The 16 MiB Rev-0 image contains substantial obvious `0xFF` regions, including large runs in the upper half of the ROM. A working scan identified approximately:

```text
0x006B0A54..0x00CFFFFF  ~6.31 MiB
0x00EAE3F0..0x00FFFFFF  ~1.32 MiB
```

for roughly 7.6 MiB of conspicuous FF-filled space in those large runs alone.

This does **not** mean every byte may be used blindly: pointer reachability, linker/layout constraints and hidden/non-FF free regions must still be considered. However, current parameter tables are small enough that raw ROM capacity is not the first blocker.

The historical Phase-0 experiment expanded the image to 32 MiB and relocated BaseStats to `0x01000000`, proving that expansion/relocation is practical when references are repointed correctly.

## 11. Graphics and cries are likely the large-space pressure

Uncompressed 64×64 4bpp battle sprites are 2048 bytes each.

For 1579 form records, front+back images alone would be roughly:

```text
1579 × 2048 × 2 = 6,467,584 bytes (~6.17 MiB)
```

before compression/deduplication. Icons, palettes and cries add more.

In practice LZ compression and resource sharing reduce this substantially. The project therefore uses a deduplication rule: visually identical sprites/palettes/icons and identical reusable assets should share one resource rather than be stored repeatedly.

Status: **assets, not BaseStats, are expected to become the dominant ROM-space cost.**

## 12. Priority order for removing ceilings

1. Introduce the new Species/Variety/Form registry and remove `412`-domain assumptions.
2. Audit and replace Egg/Unown arithmetic/special ranges.
3. Expand canonical Dex storage to 1025 while redesigning save/RAM layout safely.
4. Replace packed 9-bit level-up move encoding.
5. Extend ability IDs/slots, including hidden abilities.
6. Widen or externalize base EXP.
7. Replace fixed five-entry evolution arrays.
8. Repoint names, Dex maps/data/UI, learnsets, TM/HM masks, graphics, icons, palettes and cries through the registry.
9. Deduplicate form assets.
10. Regression-test original #1..#386 behavior, then post-Gen-III species, high-ID forms, save/load and Generation-10 append behavior.

## Bottom line

The original Sapphire engine is **not fundamentally capped at 412 species by the species field itself**. The practical ceilings come from fixed tables, save layouts, compact learnset/ability/base-EXP encodings and special-case code. The current 1025/1351/1579 target is feasible, but a clean future-proof implementation requires coordinated engine restructuring rather than only appending data.