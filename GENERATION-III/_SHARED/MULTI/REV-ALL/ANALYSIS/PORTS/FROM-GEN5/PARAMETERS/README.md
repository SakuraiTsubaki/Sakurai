# Generation V → Generation III parameter implementation

Status: **runtime implementation started**. Sprite/graphics work remains intentionally excluded.

This directory is the first executable/source-facing layer after the completed parameter survey. It is shared conceptually by Ruby/Sapphire/Emerald/FireRed/LeafGreen; revision-specific binary hooks are kept separate and are not invented here.

## Implemented in this block

- Canonical packed `Gen5PersonalRaw` matching the verified 60-byte BW personal member.
- Dependency-free NDS NitroFS + NARC extractor for `/a/0/1/6`.
- Broader parameter-corpus extractor for personal, growth, level-up, evolution, breeding-child, move and item NARCs.
- 001–649 base-species resident-table interface.
- Explicit Gen V → Gen III type-ID translation; Gen III's `TYPE_MYSTERY` gap is never raw-copied across.
- `u16` Gen V Base EXP accessor.
- normal ability 1 / normal ability 2 / hidden ability accessor.
- three held-item source slots.
- Gen V TM/HM and trailing tutor-compatibility bit accessors.
- Generated-binary `incbin` stub so ROM-derived data stays local and outside GitHub.

## Why this preserves Generation III

Native `SpeciesInfo` remains untouched. `gSpeciesInfo` continues to represent the target game's original profile. The Generation V table is an additional source profile.

This is required because the project does not replace old data merely because Generation V differs from it.

## Generated local build input

Run:

```sh
python tools/extract_gen5_personal.py "/path/to/Pokemon Black.nds" --out-dir data/gen5
```

The build-facing file is:

```text
data/gen5/personal_bw_base_000_649.bin
```

It contains members 000–649 in species order, exactly 650 × 60 = 39,000 bytes. Members above 649 are **not discarded**: the extractor also emits an all-members binary for later form routing.

For the full parameter corpus:

```sh
python tools/extract_gen5_parameter_corpus.py "/path/to/Pokemon Black.nds" --out-dir data/gen5/corpus
```

Generated NARC/member files are local build products and must not be committed.

## Next runtime hooks

### 1. Hidden ability without enlarging BoxPokemon

Generation III `BoxPokemon` has four header bits explicitly marked unused. The preferred compatibility-first design is:

- preserve native encrypted `abilityNum` as the 0/1 normal-ability selector;
- repurpose **one confirmed-unused BoxPokemon header bit** as `hiddenAbility`;
- resolve ability slot 2 only when that bit is set;
- leave old saves with the bit clear, preserving normal Gen III behavior.

Do not enlarge `BoxPokemon` for this feature.

This must be implemented independently in each RSE/FRLG codebase and tested through PC storage, trade/link, daycare, cloning/copy routines and save/load.

### 2. 16-bit Base EXP

Do not widen native `SpeciesInfo.expYield`. In the Generation V/project profile, EXP-award code calls `Gen5GetBaseExp(species)`; target-original mode continues to read the native 8-bit field.

### 3. Third held item

`Gen5GetHeldItemRaw()` returns Generation V source item IDs. They must pass through `GEN5_ITEM_ID → PROJECT_ITEM_ID`; raw DS item IDs are never stored directly in a Gen III Pokémon.

The encounter-selection probability semantics are a separate runtime hook and must be reproduced from Generation V rather than guessed.

### 4. Species 387–649

Persistent Gen III species fields are already `u16`, so no Pokémon-structure width change is needed. The work is table/index expansion: constants, names, species data routing, Pokédex, evolution, learnsets, encounters, trainers, cries/graphics references, menu bounds and all species-indexed tables. Graphics remain postponed, but table indices must already be capable of reaching 649.

### 5. Forms

Base species 000–649 and form personal records are retained separately. Form routing will use `(species, form)` rather than overwriting the base species record.

## Not yet claimed complete

- no revision-specific ROM offset hooks are claimed;
- hidden-ability save bit has not yet been wired into all Get/SetMonData paths;
- third-held-item encounter probabilities are not yet hooked;
- move-effect runtime, new abilities and post-Gen-III item effects still require dispatch code;
- BW/B2W2 differences remain separate; B2W2 data is not synthesized from BW;
- no sprite work is included.

## Verification basis

- Generation V personal source: BW `/a/0/1/6`, 60-byte members.
- Gen III native `SpeciesInfo`: six stats, two types, catch/EXP, EV yield, two items, gender, egg cycles, friendship, growth, egg groups, two abilities, flee rate and body color.
- Gen III persistent Pokémon structures already use `u16` species, held item and move IDs.
- Gen III `BoxPokemon` has four explicitly unused header bits, making a no-size-growth hidden-ability flag feasible subject to per-title regression testing.
