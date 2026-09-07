# Silver Extended Pokémon ID Architecture

Date: 2026-09-07

## Goals

1. Support the current National Dex (1025 Species), PokéAPI battle varieties (1351 Pokémon resources), and 1579 Pokémon Form records.
2. Avoid redesigning the ID namespace when Generation 10 or later generations add more content.
3. Keep original Generation II data intact where possible while replacing 8-bit species assumptions in engine-facing paths.
4. Keep Egg outside the species namespace.

## Stable IDs

```text
SPECIES_NONE = 0x0000
SPECIES_BULBASAUR = 0x0001
...
SPECIES_PECHARUNT = 0x0401   ; National Dex #1025
SPECIES_GEN10_FIRST = 0x0402 ; append when assigned
...
0xffff = reserved invalid/sentinel
```

`SPECIES_ID` is `u16` and append-only. National-Dex identity is not reused for battle forms/varieties.

## Separate battle-variant namespace

```text
VARIANT_ID : u16
```

The current PokéAPI `pokemon` resource count is 1351, but 1351 is not an engine maximum. IDs are stable and append-only.

A variant maps back to exactly one National-Dex species:

```text
Variant -> Species
```

A species may have one or many battle variants.

## Form namespace

PokéAPI `pokemon-form` records are a presentation/form layer and are not added to the species count.

Logical relation:

```text
Species
  -> Variant(s)
      -> Form(s)
          -> graphics / palette / icon / display metadata
```

A compact local-form value can still be used in stored-mon data if every variant stays within that local range. The external/global form table remains independent so it can grow beyond the current 1579 records.

## Egg

Original Gold/Silver uses an 8-bit special species value for Egg. The expanded engine must not spend a normal species ID on Egg.

Preferred logical model:

```text
is_egg(mon) -> state/flag/sentinel path
```

All original `cp EGG`-style checks must eventually route through a common Egg predicate or equivalent extended-ID-aware logic.

## Save compatibility strategy

The original BoxMon structure has two bytes after Pokerus that are unused in the disassembly. They are valuable compatibility space, but the long-term architecture must not assume that the old `251-per-page` encoding is canonical.

Target direction:

- retain the 32-byte BoxMon layout if possible;
- reuse otherwise-unused bytes for extended identity/form metadata where safe;
- patch all duplicate/fast species lists and runtime variables that currently store only one byte;
- do not silently truncate extended IDs when moving between party, box, battle, daycare, Hall of Fame, wild, trainer, evolution, link, or UI paths.

## Future-proofing rule

Current counts:

```text
NUM_SPECIES  = 1025
NUM_VARIANTS = 1351
NUM_FORMS    = 1579
```

These are **data counts only**.

Engine-facing maxima are wider:

```text
SPECIES_ID  : u16
VARIANT_ID  : u16
FORM table  : appendable
```

Do not renumber existing IDs when a new generation releases.
