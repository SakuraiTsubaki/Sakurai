# Pocket Monsters Green (Japan) — Original Engine Limit Audit

## ROMs audited
- Rev.0: 524,288 bytes, SHA1 82c0eef40a5e2423699d9fd8ba15dfaa8b51d196
- Rev.A: 524,288 bytes, SHA1 4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b
- Header: MBC1+RAM+BATTERY (0x03), ROM size code 0x04 (512 KiB), RAM size code 0x03 (32 KiB)

## Hard/architectural limits in the stock engine

### 1. ROM banking
- 32 physical 16 KiB banks in the stock image.
- Stock bank-switch routines write one byte only to rROMB ($2000).
- With the stock MBC1 mapper and no upper-bank-register handling, the practical engine-visible ceiling is the present 32-bank / 512 KiB layout.
- MBC5 conversion makes the existing low-byte bank model naturally usable through bank 255 = 4 MiB.
- 8 MiB MBC5 would require explicit management of the ninth ROM-bank bit.

### 2. Species IDs
- National Pokédex count: 151.
- Legacy internal Pokémon index namespace extends to $BE = 190 entries, including MissingNo/special fossil/Ghost slots.
- Persistent MON_SPECIES is 1 byte.
- wCurSpecies / wCurPartySpecies / wPokedexNum and many battle/menu variables are byte-sized.
- Therefore the absolute unsigned-ID ceiling without widening is 255; stock code has lower local ceilings.
- GetName has an explicit namespace collision constraint below HM01=$C4, so a naïve internal-index extension without fixing GetName tops out below $C4 (195).
- Conclusion: reassigning MissingNo slots can clean Gen-I numbering but cannot solve 1025+ species. Canonical species IDs must become u16.

### 3. Base stats
- Rev.A BaseStats located at file offset 0x38000.
- 151 records × 28 bytes = 4,228 bytes.
- Same record size estimates:
  - 1,025 records = 28,700 bytes (~28.0 KiB, 2 banks)
  - 1,351 records = 37,828 bytes (~36.9 KiB, 3 banks)
  - 1,579 records = 44,212 bytes (~43.2 KiB, 3 banks)
- So base-stat storage itself is not a meaningful capacity problem after ROM expansion.
- Record fields are mostly byte-sized; BASE_EXP is only 1 byte.
- Gen-I has HP/Atk/Def/Spd/Special only; modern SpA/SpD require projection or mechanics expansion.

### 4. Party/box/save structures
- BOXMON_STRUCT_LENGTH = 0x21 = 33 bytes.
- PARTYMON_STRUCT_LENGTH = 0x2C = 44 bytes.
- Party length = 6.
- 30 mons per box, 8 boxes.
- MON_SPECIES is one byte inside each stored mon.
- Widening species alone adds at least 246 bytes across 8×30 stored boxes + 6 party slots, before daycare/battle/transient copies.
- If Species u16 + Variety u16 + Form u16 are persisted, each stored mon grows by +5 bytes relative to the original one-byte species field.
- Existing save checksums and fixed-layout migration must be versioned.

### 5. SRAM / WRAM
- Stock external SRAM: 32 KiB.
- Stock save layout stores 8 boxes across two SRAM banks; other save/HOF data occupy the rest of the original SRAM arrangement.
- MBC5+128 KiB SRAM gives substantial save-space headroom, but save banking/versioning code must be extended.
- DMG WRAM is still fixed hardware memory and cannot be enlarged by cartridge mapper; working structures must remain compact or be staged/banked.

### 6. Pokédex seen/caught
- 151 flags require ceil(151/8)=19 bytes per bitfield.
- 1025 flags require 129 bytes per bitfield.
- Capacity impact is small; the real work is replacing 151-specific loops, menu bounds, ratings and save offsets.

### 7. Move IDs / learnsets
- Stock move count = 165 ($A5 = Struggle).
- Move IDs in mons and learnsets are bytes.
- Learnsets encode `db level, move`.
- Therefore modern complete move coverage cannot coexist with a one-byte move namespace (>255 moves).
- Either keep/project to the original move set, or independently widen/rebank the move system.

### 8. Evolutions
- Stock evolution encodings support only:
  - level
  - item
  - trade
- Evolution target species is a byte.
- Modern friendship/time/location/move/party/biome/etc. evolution conditions need explicit adaptation or new engine logic.

### 9. Types
- Type IDs are byte-sized, so width is not a capacity problem.
- Stock IDs reserve gaps between Ghost ($08) and Fire ($14).
- Steel can fit a currently unused low physical slot (e.g. $09); Dark/Fairy can be appended to special-side IDs if preserving Gen-I type-based physical/special behavior.
- Type-name/effectiveness tables and bounds still need expansion.

### 10. Pointer/bank locality
- Many stock data tables use 16-bit in-bank pointers (`dw`) with an assumed/fixed ROM bank: base stats, evo/learnsets pointer table, Pokédex entries, sprites, etc.
- A table can therefore hit a 16 KiB bank-local ceiling even when total ROM space remains.
- Large-scale expansion requires bank+pointer (far-pointer) tables or banked directory indirection.
- This is the second major architectural wall after 8-bit IDs.

### 11. Sprites and cries
- Stock front-sprite loading validates dex number <=151 and invalid values fall into the Rhydon trap.
- Sprite references are not designed as a 1025+/form-aware far-pointer database.
- Cry data is indexed from an 8-bit monster ID into a 3-byte table and reuses a small set of cry SFX with pitch/tempo modifiers.
- Modern-scale distinct sprite/form/cry assets therefore need separate banked tables.

## Practical ceilings

### Stock ROM, no structural engine changes
- 151 real Pokédex species.
- 190 legacy internal Pokémon indexes ($01..$BE), but this includes MissingNo/special IDs and is not a clean 190-species Pokédex.
- A naïve namespace extension collides with GetName/HM01 at $C4, so even the full u8 range is not safely available without code fixes.
- 512 KiB practical ROM banking ceiling with current MBC1 bank-switch implementation.

### Small fixes but still 8-bit species
- At most 255 canonical species IDs in principle.
- This is still fundamentally insufficient for National Dex 1025.

### Required architecture for GREEN Complete DB
- SpeciesID u16, stable National Dex numbering, 0=NONE.
- Variety/Form IDs separated from Species and designed append-only.
- Far-pointer/banked data directory.
- MBC5 4 MiB first target; 8 MiB only if actual asset budget demands it.
- SRAM 128 KiB with save-format versioning/migration.
- Move system decision handled separately because stock move IDs are also u8.

## Bottom line
The original engine's meaningful ceiling is not the 151-entry data table. It is the combination of one-byte species IDs, byte-sized move IDs, fixed-bank 16-bit pointers, fixed save structs, and MBC1 bank switching. ROM expansion alone does not solve these. A 16-bit species ABI + banked/far-pointer data layer is the minimum clean foundation for 1025 Species / 1351 Varieties / 1579 Forms and future generations.
