# ENGINE-386 Runtime ABI v1

This ABI is designed for 386 species now and later generations without renumbering species.

## Canonical identity

```text
SpeciesKey {
    species_id : u16   // National Dex number for real species
    form_id    : u8    // per-species form selector
}
```

Real species use `species_id = 1..386` in the first milestone. Later generations append their National Dex IDs without changing any existing ID.

Reserved canonical values mirror Silver's special high-byte transport semantics:

- `0x0000` = no species / null
- `0xFFFD` = Egg
- `0xFFFE` = reserved special value
- `0xFFFF` = terminator / negative sentinel

## Persistent vs transient storage

Persistent data must never depend on a one-byte dynamic slot table.

- SRAM/save records: canonical `u16 species_id` plus `u8 form_id`.
- ROM species tables: canonical `u16 species_id`.
- Runtime legacy-facing fields: compact `u8 runtime_slot` only where keeping the original Silver structure materially reduces the port surface.

This avoids the fatal future limitation where a save containing more than 252 distinct species could not be represented by one global 8-bit map.

## Runtime slot conversion

The translation table maps only species, not forms:

```text
runtime_slot:u8 -> species_id:u16
```

`form_id` is carried independently in persistent records and in parallel runtime form fields. This is required because a single Pokemon can change form without changing species identity (Castform), and two Pokemon of the same species can simultaneously have different persistent forms (Unown/Deoxys).

Initial slot policy:

- `$00` null, never allocated.
- `$01..$F0` allocatable runtime slots in milestone 1.
- `$F1..$FC` held back until Silver-specific sentinel/reference audit proves them safe.
- `$FD` Egg passthrough.
- `$FE` reserved passthrough.
- `$FF` terminator passthrough.

The allocator may later raise the allocatable ceiling after audit, but no data format depends on that ceiling.

## Slot lifetime

Only the currently active working set needs slots: party, current box, battle participants, daycare working records, current encounter/trainer data, menus and temporary script values. Inactive boxes remain canonical in SRAM and therefore consume no runtime slots.

On load/current-box switch:

1. clear/rebuild the runtime species table;
2. allocate slots for canonical species entering the active working set;
3. materialize legacy-facing runtime structs;
4. keep canonical IDs available for all new-engine lookups.

On save/current-box eviction:

1. convert active runtime slots back to canonical `u16 species_id`;
2. write `form_id` independently;
3. serialize canonical records;
4. never serialize an ephemeral slot as species identity.

## Form rules through Generation III

### Unown #201

- Persistent `form_id` 0..27: A..Z, !, ?.
- Vanilla Gen II IV-derived shape is imported when opening an untouched legacy save, then converted to explicit form storage.
- Stats/type/ability data use the base species record; graphics/form index differ.

### Castform #351

- `form_id` 0 Normal, 1 Sunny, 2 Rainy, 3 Snowy.
- Outside battle, persistent form is Normal for Generation III behavior.
- In battle, Forecast/weather drives `form_id` and type overlay.
- Species identity never changes.

### Deoxys #386

- Persistent `form_id` 0 Normal, 1 Attack, 2 Defense, 3 Speed.
- Form overlay can replace base stats, graphics/palette and level-up learnset.
- All four forms are available in the target engine instead of being locked to the source Gen III cartridge version.

## Lookup contract

New engine lookup routines consume canonical values:

```text
GetBaseParameters(species_id, form_id)
GetPokemonName(species_id)
GetPokemonCry(species_id)
GetPokemonPic(species_id, form_id, side)
GetPokemonPalette(species_id, form_id, shiny)
GetEvolutionList(species_id)
GetLevelUpLearnset(species_id, form_id)
GetTMHMLearnset(species_id, form_id)
```

Legacy callers that still hold a runtime slot must call `RuntimeSlotToSpeciesID` first.

## Compatibility boundary

Time Capsule and vanilla link protocols remain explicit compatibility boundaries. They may reject or down-convert unsupported species/forms rather than leaking expanded IDs into a one-byte protocol.

## Milestone definition: 386 + forms playable

The milestone is not complete merely because data exists in ROM. It requires all of the following to pass:

- create/load/save party Pokemon from #001 through #386;
- deposit/withdraw and switch boxes without identity loss;
- encounter and battle expanded species;
- trainer parties can contain expanded species;
- evolution can target expanded species;
- level-up/TM/HM/tutor lookup resolves expanded species;
- Pokédex seen/caught resolves 386 species;
- Unown 28 forms persist and render correctly;
- Castform changes type/form under weather and reverts correctly;
- Deoxys four forms preserve their form-specific parameters;
- vanilla #001-#251 regression suite remains clean.
