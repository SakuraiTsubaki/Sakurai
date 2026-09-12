# Generation V → Gen II / Gen III Form Storage

Status: **storage architecture fixed from uploaded-ROM inspection + decomp cross-check; binary hooks not yet applied.**

## 1. What the uploaded ROMs show

### Gen II

Uploaded Korean Gold/Silver and Japanese Crystal base-data tables contain only the 251 real species records. There is no generic persistent `form` byte in the Gen II boxed/party Pokémon structure.

The original Gen II boxed structure stores species, item, moves, OT ID, experience, stat experience, DVs, PP, happiness, Pokérus, caught data, and level. There is no spare byte inside the boxed-mon record reserved for forms.

Original Unown form handling is therefore not a generic form field; its letter is derived from the Pokémon's DVs.

The Gen II box container also stores a separate `BoxSpecies[]` list even though every boxed-mon record already begins with its own species byte. The party structure has a dedicated one-byte `Unused` field after status. These two facts provide a no-size-growth path for the first extension byte.

### Gen III

Uploaded Japanese Emerald / FireRed / LeafGreen species data confirms the legacy internal ordering:

- 001–251: Gen I–II species
- 252–276: `OLD_UNOWN_*` legacy/dummy range
- 277–411: National Dex 252–386
- `SPECIES_EGG` is a pseudo-species constant after the real species data, not an ordinary 28-byte `SpeciesInfo` record

The Gen III `BoxPokemon` persistent structure does not contain a generic form field. It does, however, contain four explicitly unused header bits, while secure substruct 3 contains four `unusedRibbons` bits.

## 2. Generation V form-count verification

Direct extraction from the uploaded Pokémon Black ROM (`/a/0/1/6`) gives a maximum `form_count` of **28** among National Dex 001–649:

- Unown #201: 28
- Arceus #493: 17
- Rotom #479: 6
- Genesect #649: 5
- Castform #351: 4
- Deoxys #386: 4
- Deerling #585: 4
- Sawsbuck #586: 4
- Burmy/Wormadam: 3
- other Gen IV/V form species: 2–5

Therefore a universal project form ID needs **at least 5 bits**. Four bits are insufficient if forms are to be explicitly selectable rather than always re-derived.

## 3. Project form-ID contract

Use a 5-bit persistent form selector:

- `0..27`: explicit form IDs
- `28..30`: reserved
- `31`: `FORM_AUTO`

`FORM_AUTO` preserves target-original behavior where appropriate. Examples:

- Gen II Unown: derive from DVs
- Gen III Unown: derive from personality
- Castform: weather-derived battle form
- Arceus: item/type-derived form when using original Generation V semantics
- Genesect: Drive-derived form

Scripts, events, editors, tests, and project-specific content may instead assign an explicit `0..27` form.

## 4. Gen III persistent storage — no BoxPokemon size increase

Do **not** enlarge `BoxPokemon`.

Store the 5-bit form selector across fields that are explicitly unused by the original Gen III engine:

- form bits 0..3 → `BoxPokemon.unused:4`
- form bit 4 → bit 0 of `PokemonSubstruct3.unusedRibbons`

The remaining three `unusedRibbons` bits remain untouched.

Required accessor contract:

```c
u8 GetBoxMonForm(struct BoxPokemon *boxMon);
void SetBoxMonForm(struct BoxPokemon *boxMon, u8 form);
```

Rules:

1. always mask to 5 bits;
2. use the normal encrypted-substruct access/checksum path for the high form bit;
3. do not directly mutate encrypted bytes without checksum regeneration;
4. `FORM_AUTO` is stored as value 31;
5. old saves with all unused bits zero naturally decode as explicit base form 0; migration code may optionally convert selected species to `FORM_AUTO` to preserve original dynamic behavior.

### Battle runtime

Do not depend on repurposing an unidentified byte inside `BattlePokemon` until its use is fully audited. Use a separate runtime array instead:

```c
u8 gBattleMonForms[MAX_BATTLERS_COUNT];
```

When a battler is created, resolve persistent form + dynamic rules into this runtime form.

## 5. Gen II persistent storage — first extension byte without increasing mon size

Gen II has no generic form field, but the original layout exposes two storage locations that can carry the same project extension byte depending on where the Pokémon lives:

- **party:** `party_struct.Unused` (one byte)
- **PC box:** repurpose the redundant per-slot `BoxSpecies[]` entry; the actual low 8 bits of species remain in each boxed-mon record's own `Species` field

The original `BoxSpecies[]` list is therefore no longer treated as a second copy of species. Routines that previously scan it must be changed to read the boxed-mon record species and project extension byte explicitly, using box count instead of the old species-list terminator convention.

### Extension byte 0

- bits 0–1: species ID bits 8–9
- bits 2–6: form ID bits 0–4
- bit 7: reserved for the first per-Pokémon extension flag (candidate: ability selector bit 0)

This one byte is enough to provide, without growing the original boxed/party Pokémon structures:

- 10-bit species ID (0–1023)
- 5-bit form ID (0–31)

The remaining Generation V per-mon expansion (move-ID high bits, full ability selector, nature/other verified state) is handled separately; it must not be conflated with the form layer until its storage audit is complete.

### Required Gen II hooks for extension byte 0

- party ↔ box copy
- box deposit / withdraw / release / move
- active-box load/save
- daycare transfer
- battle initialization
- link/trade serialization
- Hall of Fame serialization or form reconstruction policy
- any routine that scans `sBoxSpecies`

The `sBoxSpecies` reference audit already identifies Bill's PC, temporary-mon handling, and Lucky Number logic as direct users that need conversion.

## 6. SRAM differences across uploaded Gen II targets

Uploaded ROM headers are not identical:

- Korean Gold: MBC3+RTC+RAM+battery, RAM-size code `0x03`
- Korean Silver: MBC3+RTC+RAM+battery, RAM-size code `0x03`
- Japanese Crystal: MBC3+RTC+RAM+battery, RAM-size code `0x05`
- international Crystal Rev A: MBC3+RTC+RAM+battery, RAM-size code `0x03`

Therefore later sidecar storage beyond extension byte 0 must be audited per version. Japanese Crystal's mobile-era SRAM layout must not be assumed for Korean Gold/Silver or international Crystal.

## 7. Species-ID policy after OLD_UNOWN removal

Project canonical species IDs are National Dex IDs:

- `0`: NONE
- `1..649`: actual Pokémon, National Dex 1:1
- `650`: project pseudo-species EGG for interfaces that require a species-like egg token

`OLD_UNOWN_*` is removed from the project ID space. Unown forms use species 201 + form ID.

Legacy Gen III ROM data is translated during migration/rebuild:

- old 1..251 → unchanged
- old 277..411 → project 252..386
- old 252..276 (`OLD_UNOWN`) → discarded from canonical species tables
- old runtime Unown-form pseudo IDs → species 201 + form

## 8. Preservation rule

The original ROMs remain read-only. The project keeps documentation of the original OLD_UNOWN slots, duplicate Gen II box-species list, and original form algorithms even when those storage conventions are repurposed in the project runtime.

`FORM_AUTO` is specifically retained so the original Gen II/III behavior can coexist with explicit Generation V-style form selection.

## 9. Next binary implementation steps

1. Gen III: add `MON_DATA_FORM` accessor and migration logic without changing `sizeof(BoxPokemon)`.
2. Gen III: add `gBattleMonForms[]` and route all form-dependent parameter lookup through `(species, form)`.
3. Gen III: rebuild species-indexed tables to canonical National Dex ordering after removing OLD_UNOWN slots.
4. Gen II: implement extension-byte-0 helpers for `party_struct.Unused` and repurposed `BoxSpecies[]` entries.
5. Gen II: patch every `sBoxSpecies` consumer to use box count + boxed-mon species + extension byte.
6. Gen II: audit storage for the remaining move-ID/ability/nature extension state separately per ROM family.
7. Route Gen V personal/form records using `(species, form)` rather than duplicate species IDs.
