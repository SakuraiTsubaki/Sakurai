# Pokémon Ruby (AXVE v0) Original Engine Limit Audit

Base ROM: `Pokemon - Ruby Version (USA).gba`
SHA-1: `f28b6ffc97847e94a6c21a63cacf633ee5c8df1e`
ROM size: 16 MiB (0x01000000)

## 1. Species / Dex layout observed in the original ROM

| Structure | Offset (AXVE v0) | Entries | Record size | Notes |
|---|---:|---:|---:|---|
| Species names | 0x001F716C | 440 | 11 bytes | Includes Egg / Unown form internals |
| Base stats | 0x001FEC18 | 440 | 28 bytes | Direct indexed by internal species ID |
| Species -> National Dex map | 0x001FC516 | 411 | 2 bytes | Internal 1..411 only |
| Evolution table | 0x00203B68 | 412 | 40 bytes/row compiled | 5 evolution slots per species |
| Level-up learnset pointer table | 0x00207BC8 | 412 | 4 bytes | Internal 0..411 |

The engine therefore does **not** have one single stock species count. It mixes 386 National Dex species, 412 normal engine slots, and 440 name/stat/graphics-oriented internal entries.

## 2. ROM capacity

AXVE v0 contains two very large 0xFF runs:

- 0x006B09F8 .. 0x00D00000: 0x64F608 bytes (~6.31 MiB)
- 0x00EAE244 .. 0x01000000: 0x151DBC bytes (~1.32 MiB)

The standard GBA ROM address space supports up to 32 MiB, so a 16 MiB English Ruby can be expanded by another 16 MiB. ROM byte capacity is not the first blocker for a 1579-record species/form database.

## 3. Hard / semi-hard field limits

| Parameter | Original representation | Original ceiling | 1025/1579 impact |
|---|---|---:|---|
| Internal species ID | u16 | 65535 | Safe for 1579 and future gens |
| Move ID in Pokémon save/battle | u16 | 65535 | Safe |
| Level-up move ID | 9-bit field | 511 | **Must redesign** for full modern move set |
| Level in level-up entry | 7-bit field | 127 | Safe for level 100 |
| Ability ID in BaseStats/BattlePokemon | u8 | 255 | **Must widen** for all modern abilities |
| Ability choice stored per mon | 1 bit (`altAbility`) | 2 choices | **Must redesign** for hidden ability / 3 slots |
| Base stat per stat | u8 | 255 | Safe; canonical base stats fit |
| Base EXP yield | u8 | 255 | **Must widen** for modern values >255 |
| Catch rate | u8 | 255 | Safe |
| EV yield per stat | 2 bits | 0..3 | Safe |
| Gender ratio | u8 | 255 codes | Safe |
| Egg cycles | u8 | 255 | Safe |
| Friendship | u8 | 255 | Safe |
| Growth-rate ID | u8 | 255 IDs | Safe (only 6 stock groups) |
| Egg-group ID | u8 x2 | 255 each | Safe |
| Held item ID | u16 | 65535 | Safe |
| Evolution target species | u16 | 65535 | Safe |
| Evolution branches | fixed 5 entries/species | 5 | **Must redesign** (e.g. Eevee needs >5) |
| Evolution method ID | u16 | 65535 | Field is safe, but stock logic only implements Gen 3 methods |
| TM/HM learnability | 64-bit bitset | 64 machines | **Must redesign** for modern teachable lists |
| Species display name | fixed 10 chars + EOS | 10 chars | **Must redesign** for longer modern species names |
| Pokédex category | fixed 12 bytes | 11 chars + EOS | May need variable strings |
| Pokédex height | u16 decimeters | 6553.5 m | Safe |
| Pokédex weight | u16 hectograms | 6553.5 kg | Safe |
| Captured Ball metadata | 4 bits | 16 values | Needs redesign if preserving all modern Ball types |
| Met-game metadata | 4 bits | 16 values | Needs redesign for broad cross-generation provenance |
| IV per stat | 5 bits | 0..31 | Safe |
| EV per stat | u8 | 0..255 | Safe |

## 4. Pokédex / save limits

Stock constants:

- National Dex count = 386
- `POKEMON_SLOTS_NUMBER` = 412
- `DEX_FLAGS_NO` = ceil(412/8) = 52 bytes
- Four relevant dex flag arrays exist: owned, seen, dexSeen2, dexSeen3.

Existing save sector allocation:

- One sector payload = 3968 bytes
- SaveBlock2 = 1 sector
- SaveBlock1 = 4 sectors
- Pokémon Storage = 9 sectors
- 14 sectors total per save slot

If only the dex bit arrays are enlarged and everything else remains the same:

| Tracked IDs | Flag bytes/array | SaveBlock1 spare | SaveBlock2 spare |
|---:|---:|---:|---:|
| 412 | 52 | 832 bytes | 1776 bytes |
| 1025 | 129 | 678 bytes | 1622 bytes |
| 1351 | 169 | 598 bytes | 1542 bytes |
| 1579 | 198 | 540 bytes | 1484 bytes |
| 3072 | 384 | 168 bytes | 1112 bytes |
| 3744 | 468 | 0 bytes | 944 bytes |
| 3745 | 469 | **overflow by 2** | 942 bytes |

So the current 14-sector save layout can theoretically carry dex-style bit flags for up to roughly **3744 IDs** without reallocating sectors, assuming no other SaveBlock1 growth. 1025 species and even 1579 record flags fit comfortably.

## 5. Pokédex RAM / UI

The Pokédex view stores a 4-byte list item per National Dex entry. Raising 386 -> 1025 increases the list by about 2.5 KiB, which is small relative to GBA EWRAM.

The bigger UI issue is numeric formatting: multiple stock screens explicitly render dex numbers with **3 digits**. National #1000+ therefore requires UI/layout patches even though the underlying dex number is u16.

## 6. Forms

There is no generic modern `formId` field in BoxPokemon. However the raw species field is u16, so a form/variety can be represented as its own internal record ID while mapping back to one National Dex species. 1579 current records are far below the 65535 species-ID ceiling.

This means a future-proof design can preserve the 80-byte BoxPokemon format for most forms by using:

- internal record ID (u16)
- record -> base National Dex mapping
- record -> gameplay variety mapping
- record -> visual form mapping

Egg should not consume the growing species namespace; the save structure already has explicit `isEgg` state, so an expanded engine can special-case egg display/behavior instead of treating it as an ordinary numbered species record.

## 7. Practical conclusion

### Can be expanded mostly by tables / loop bounds
- Species / form record count (u16 ID space)
- National Dex count
- Names/stat/graphics pointer tables
- Dex seen/caught flags
- Pokédex list RAM
- Evolution target IDs
- Item IDs
- Heights / weights

### Requires record-format or engine redesign
1. Level-up learnset encoding (9-bit move ID)
2. Ability ID width (u8) and 2-choice ability state (1 bit)
3. Base EXP yield width (u8)
4. Fixed five-evolution rows
5. Modern evolution-condition handlers
6. 64-bit TM/HM learnability bitset
7. 10-character species name table
8. 3-digit Pokédex UI
9. Generic form/variety metadata layer
10. Modern Ball / origin metadata if exact preservation is desired

### Overall
The stock Ruby engine is **not fundamentally limited to 386 or 412 Pokémon**. Those are compiled table and loop assumptions. The deep ceilings are mostly small packed fields inherited from Gen 3. With those few formats redesigned, 1025 Species / 1351 gameplay varieties / 1579 form records are comfortably within the GBA's u16 identity space and current save-sector budget, with room left for Generation 10 additions.
