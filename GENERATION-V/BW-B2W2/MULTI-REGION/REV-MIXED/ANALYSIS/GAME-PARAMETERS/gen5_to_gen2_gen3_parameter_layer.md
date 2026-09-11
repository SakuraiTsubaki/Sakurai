# Generation V → Gen II / Gen III Game Parameter Layer

Status: **Phase 0 mapping complete; runtime integration is the next implementation step.**

Scope: static and runtime-facing game parameters only. Sprite/graphics work is intentionally excluded for now.

## 1. Source of truth

BW and B2W2 share several core NARC roles but **do not have identical filesystem placement for every system**.

Common/core paths:

- `a/0/1/6` — personal data
- `a/0/1/8` — level-up moves
- `a/0/1/9` — evolutions
- `a/0/2/0` — child/base-breeding Pokémon data
- `a/0/2/1` — move data
- `a/0/2/4` — item data

Version-family differences confirmed during survey:

- **BW egg moves:** `a/1/2/3` (650 files in Black)
- **B2W2 egg moves:** `a/1/2/4` (650 files in Black 2)
- **BW encounters:** `a/1/2/6`
- **B2W2 encounters:** `a/1/2/7`

The project rule is **preserve target-original data first**, then add Generation V data as a selectable/extended layer rather than destructively replacing the target tables. BW and B2W2 data are retained as separate source profiles wherever they differ.

## 2. BW personal record (0x3C / 60 bytes)

| Offset | Size | Field |
|---:|---:|---|
| 0x00 | 6 | HP / Atk / Def / Spe / SpA / SpD |
| 0x06 | 2 | type 1 / type 2 |
| 0x08 | 1 | catch rate |
| 0x09 | 1 | stage/auxiliary byte |
| 0x0A | 2 | EV yield bitfield, 2 bits × 6 stats |
| 0x0C | 2 | held item 1 |
| 0x0E | 2 | held item 2 |
| 0x10 | 2 | held item 3 / dark-grass slot |
| 0x12 | 1 | gender ratio |
| 0x13 | 1 | hatch counter |
| 0x14 | 1 | base friendship |
| 0x15 | 1 | growth rate |
| 0x16 | 2 | egg groups |
| 0x18 | 3 | ability 1 / ability 2 / hidden ability |
| 0x1B | 1 | escape/flee rate |
| 0x1C | 2 | form stats start |
| 0x1E | 2 | form sprite start |
| 0x20 | 1 | form count |
| 0x21 | 1 | Pokédex body color |
| 0x22 | 2 | base EXP |
| 0x24 | 2 | height |
| 0x26 | 2 | weight |
| 0x28 | 0x10 | TM/HM compatibility |
| 0x38 | 4 | BW-family trailing compatibility bitfield; semantic use tracked separately by version |

**Implementation policy:** retain the raw 60-byte BW record as a canonical Generation V record instead of flattening it into a Gen II/III-only structure. Target-specific adapters translate IDs and expose fields to each engine. B2W2 personal extensions/forms are surveyed separately instead of assuming the BW 60-byte record is the complete B2W2 schema.

## 3. Gen III integration

Gen III is the easier target because its persistent Pokémon species, move and held-item IDs are already 16-bit. The original `SpeciesInfo` structure already contains base stats, types, catch rate, 8-bit EXP yield, EV yield, two held items, gender, egg cycles, friendship, growth rate, egg groups, two abilities, flee rate and body color.

### Preserve + extend

Keep native `SpeciesInfo` intact and add a `Gen5PersonalTable[650]` (index 0 + National Dex 001–649) containing raw BW personal records. Add one accessor layer:

`GetSpeciesParamEx(species, field, profile)`

Profiles:

- `GEN3_ORIGINAL`
- `GEN5_BW_ORIGINAL`
- `GEN5_B2W2_ORIGINAL`
- `PROJECT_APPLIED`

### Fields needing Gen III extension

- **Base EXP:** native field is 8-bit; Gen V uses 16-bit. Add `u16` lookup for Gen V profile.
- **Held item 3:** add third held-item lookup and encounter-selection logic.
- **Hidden ability:** add ability slot 2 (third ability) and generation/acquisition rules.
- **Forms:** add form-to-personal-record routing instead of collapsing forms.
- **TM/HM:** extend compatibility from Gen III TM/HM set to the Gen V compatibility bitset.
- **Species 387–649:** extend species-indexed tables; Pokémon storage already uses `u16 species`.
- **Moves beyond Gen III:** move slots are already `u16`, so expand move-indexed tables instead of changing the Pokémon save structure.
- **Items beyond Gen III:** held item storage is already `u16`; expand item-indexed tables and effect dispatch.

### Hidden ability save compatibility candidate

The FRLG `BoxPokemon` header has four explicitly unused bits outside the encrypted substructures. A backward-size-compatible implementation can reserve one/two of those bits for an extended ability selector while keeping the existing one-bit `abilityNum` semantics for normal ability slots. This must be verified per target ROM/revision before binary patching.

`BattlePokemon` already stores the resolved ability as an 8-bit value, so battle code can operate on the final ability ID after initialization.

## 4. Gen II integration

Gen II needs a real compatibility layer because persistent Pokémon species and moves are 8-bit IDs.

### Required structural expansions

- **Species IDs:** 251 → 649 requires at least 10 bits.
- **Move IDs:** 251 → Gen V move count requires at least 10 bits.
- **Abilities:** entirely new species ability table + per-Pokémon ability selection + battle/field hooks.
- **Hidden abilities:** third ability slot and acquisition state.
- **Modern EV yield/system:** Gen II uses stat experience, not the Gen III–V EV model.
- **Base friendship:** Gen II creation code initializes a global constant (`BASE_HAPPINESS`); Gen V requires per-species base friendship.
- **Base EXP:** retain native 8-bit original value but add Gen V 16-bit value and Gen V experience-award path.
- **Held item 3:** add third slot and probability/encounter logic.
- **Forms:** add a form index and species→form personal lookup.
- **TM/HM:** expand both move IDs and compatibility bitsets.

### Growth-rate opportunity

Crystal defines six growth table indexes. Source search shows `GROWTH_SLIGHTLY_FAST` and `GROWTH_SLIGHTLY_SLOW` are defined but are not referenced by species base-stat files in the current pokecrystal source. This makes indexes 1 and 2 candidates for Gen III–V **Erratic** and **Fluctuating** formulas without changing any species that actually use the original four active groups. Direct verification is still required for each uploaded Korean/Japanese/English target ROM before applying this optimization.

### Save-layout policy

Do **not** blindly enlarge `BOXMON_STRUCT_LENGTH`; that would cascade through SRAM box layout, party structures, daycare, Hall of Fame and link/trade code. Prefer, in order:

1. repurpose confirmed-unused bits/bytes,
2. repurpose legacy fields when the project intentionally replaces their system (for example stat-exp → modern EV storage),
3. add compact sidecar state,
4. only then enlarge save structures and migrate save format.

A full 10-bit species implementation must update live WRAM species variables, party/box species lists, daycare, Hall of Fame, Pokédex indexing and every table accessor; it cannot be treated as a single table-size patch.

## 5. Canonical adapter rules

### Type IDs

Do not copy raw type numbers into earlier engines. Gen III has the legacy Mystery-type slot between Steel and Fire; Gen V does not. Use an explicit type-ID map. Gen II also uses its own numeric assignments.

### Item IDs

Never copy Gen V item numbers directly into Gen II/III held-item fields. Maintain `GEN5_ITEM_ID → TARGET_ITEM_ID` mapping with target-original IDs preserved.

### Ability IDs

Gen III ability IDs through the original Gen III set are compatible conceptually with later abilities, but all post-Gen-III abilities require constants, names/descriptions and actual effect routines. Storing the number alone is not considered implemented.

### Forms

Do not overwrite base species data with one form. Use `(species, form)` → personal-record routing and preserve every confirmed BW/B2W2 form record separately.

## 6. Implementation order

1. **Resident Gen V personal layer** — copy all 001–649 BW/B2W2 personal records into target-accessible storage.
2. **Parameter accessor** — target-original / BW-original / B2W2-original / project-applied profiles.
3. **Gen III first functional pass** — 649 species indexing, 16-bit base EXP, third held item, third ability, forms, expanded TM/HM.
4. **Gen II ID layer** — 10-bit species + 10-bit moves without destructive save expansion.
5. **Gen II parameter functions** — per-species friendship, modern EV yield, growth formulas, abilities, forms, held-item 3.
6. **Level-up / egg moves / evolutions** from the correct BW/B2W2 NARCs.
7. **Move table and effects** including physical/special/status category and Gen V effect semantics.
8. **Item table and effects** including battle/field/evolution/form interactions.
9. **Cross-system verification** — battle, breeding, evolution, save/load, PC, trade/link, Pokédex, trainer/wild data.

## 7. Current decision

The project will **not stop at changing fields that already existed in Gen II/III**. Existing fields are only the compatibility baseline. Every Generation V parameter that has no target equivalent gets an explicit data structure and, where required, an engine implementation. No unsupported Gen V value will be silently discarded.

## Verification sources

- Project Pokémon BW/B2W2 ROM research: `personal.narc` structure and version-family NARC locations.
- pret/pokefirered: `struct PokemonSubstruct0`, `BoxPokemon`, `BattlePokemon`, `SpeciesInfo`, `BattleMove`, `LevelUpMove`, `Evolution`.
- pret/pokecrystal: base-data constants, party/box structure, growth-rate table, experience routines.
