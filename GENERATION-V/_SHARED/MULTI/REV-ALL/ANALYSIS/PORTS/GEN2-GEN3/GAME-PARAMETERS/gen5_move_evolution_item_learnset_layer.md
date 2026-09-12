# Generation V → Gen II / Gen III: Move, Evolution, Item, Learnset Layer

Status: **structure mapping in progress; verified formats are separated from partially identified fields.**

Sprites are out of scope for this phase.

## 1. Move data

### Generation V source

BW/B2W2 move data is stored at `a/0/2/1`.

Each BW move record is **36 bytes (0x24)**.

| Offset | Size | Field |
|---:|---:|---|
| 0x00 | 1 | type |
| 0x01 | 1 | effect category |
| 0x02 | 1 | damage category: physical / special / status |
| 0x03 | 1 | power |
| 0x04 | 1 | accuracy |
| 0x05 | 1 | PP |
| 0x06 | 1 | priority (signed) |
| 0x07 | 1 | multi-hit data |
| 0x08 | 2 | result effect |
| 0x0A | 1 | effect chance |
| 0x0B | 1 | status/auxiliary |
| 0x0C | 1 | minimum turns |
| 0x0D | 1 | maximum turns |
| 0x0E | 1 | critical stage |
| 0x0F | 1 | flinch |
| 0x10 | 2 | effect ID |
| 0x12 | 1 | target HP change / recoil (signed semantics) |
| 0x13 | 1 | user HP change / healing |
| 0x14 | 1 | target selector |
| 0x15 | 3 | affected stats 1–3 |
| 0x18 | 3 | stat magnitudes 1–3 |
| 0x1B | 3 | stat chances 1–3 |
| 0x1E | 2 | flag/auxiliary bytes; exact semantic split tracked separately |
| 0x20 | 2 | move flags bitfield portion |
| 0x22 | 2 | trailing flags/auxiliary; verify against BW and B2W2 before runtime use |

Confirmed move metadata includes flags for contact, charge, recharge, Protect, Magic Coat, Snatch, Mirror Move, punch, sound, Gravity restrictions, thawing, far-target behavior in Triple Battles, healing and Substitute interaction.

### Gen III target

Native Gen III `BattleMove` is much smaller and has no per-move physical/special/status field. Therefore **do not widen the original table destructively**. Add a Generation V move-extension table keyed by 16-bit move ID and expose it through move accessors.

Gen III Pokémon already store move IDs as `u16`, so the save structure does not need a move-ID-width migration. Required runtime extensions:

- expand move constants/tables through the Gen V move count,
- per-move damage category,
- Gen V effect dispatcher,
- target/range behavior including Triple-Battle metadata where relevant,
- Gen V flags and interaction hooks,
- Gen V priority, recoil/healing and multi-hit semantics.

### Gen II target

Gen II stored move IDs are 8-bit, so a **10-bit-or-wider move-ID migration** is prerequisite for a full Gen V move list. Keep original move table as `GEN2_ORIGINAL`; add an extended move table for `GEN5_BW_ORIGINAL`, `GEN5_B2W2_ORIGINAL` and `PROJECT_APPLIED`.

Required engine changes include:

- wider party/box move storage or a compatible sidecar encoding,
- wider move variables in WRAM and menus,
- move-name/description indexing,
- per-move physical/special/status category,
- effect dispatcher expansion,
- target and priority handling,
- contact/sound/punch/etc. flags for ability/item interaction.

## 2. Level-up learnsets

### Generation V source

BW/B2W2 level-up data is at `a/0/1/8`.

Each learned-move entry is **4 bytes**:

- `u16 move_id` little-endian
- `u8 level`
- `u8 auxiliary`

A `FF FF FF FF` entry terminates the list. Historical BW research shows the fourth byte is usually zero but can be nonzero; it must be preserved as raw source data until its semantics are fully verified. Duplicated move entries can be ignored by the original game in some circumstances, so insertion logic must not assume the list is a simple unconstrained array.

### Target strategy

Do not force the Gen V list into the original fixed/packed target representation. Store a canonical Gen V learnset stream and write target adapters:

- Gen III: species → list of `(u16 move, level, aux)`; convert to native-style logic at runtime.
- Gen II: same canonical list, but depends on the widened move-ID layer first.

This allows every BW/B2W2 learnset to coexist with each target game's original learnset.

## 3. Evolution data

### Generation V source

BW/B2W2 evolution data is at `a/0/1/9`.

Each species record is **42 bytes** = seven 6-byte entries:

`u16 method, u16 parameter, u16 target_species`

There are seven slots per Pokémon.

### Gen III target

Gen III uses the same conceptual three-field evolution entry but FRLG's native table has fewer slots per species. Preserve the native table and add a **7-entry Gen V evolution table**. Add method translation/handlers for Gen V conditions absent in Gen III.

### Gen II target

Gen II evolution records are variable/compact and use 8-bit species/item/move-era assumptions. Do not encode Gen V evolutions into the legacy stream directly. Add an extended evolution accessor operating on widened species IDs and target item IDs. New condition handlers must be implemented explicitly.

## 4. Item data

### Generation V source

BW/B2W2 item data is at `a/0/2/4`. Black contains 627 NARC members in the surveyed file tree.

The BW item record research identifies, in order:

- `u16 price` (BW shop price derives from stored unit × 10)
- battle-use/effect byte
- gain/effect parameter
- berry/auxiliary byte
- fling effect
- fling power
- Natural Gift power / related type metadata
- access/toss/register/use flags
- pocket
- item type
- item category
- several effect/auxiliary bytes
- BW sort index / reverse-sort index
- six signed EV changes
- HP restore
- PP restore
- three signed friendship changes for the 0–99, 100–199 and 200–255 friendship bands

Some intermediate item bytes remain only partially identified in the historical documentation. **They are retained verbatim and are not assigned invented semantics.**

### Gen III target

Gen III already has 16-bit held-item storage and an item attribute/effect dispatch system. Integration therefore uses:

`GEN5_ITEM_ID → PROJECT_ITEM_ID`

rather than overwriting original item IDs. Extend:

- item table/count,
- bag pockets and sorting,
- field-use callbacks,
- battle-use callbacks,
- held-item effect dispatch,
- fling/natural-gift style metadata where relevant,
- evolution/form-change item hooks.

### Gen II target

Gen II item IDs and item engine are 8-bit-era structures. Full Gen V item integration needs wider IDs or a mapped extended namespace plus changes to bag, PC, marts, held items, scripts, battle effects, field use and evolution logic.

Preserve all Gen II original item IDs. No Gen V raw item ID is written into a Gen II save field without translation.

## 5. Egg moves and breeding family data

### Important BW/B2W2 path split

- **BW:** egg moves are in `a/1/2/3` (650 NARC members in Black).
- **B2W2:** egg moves are in `a/1/2/4` (650 NARC members in Black 2).

Historical BW research shows each family file begins with a little-endian **egg-move count**, followed by `u16` move IDs. Species later in the same evolution family can have empty data while the base/breeding species carries the list. `a/0/2/0` supplies breeding/base-child relationships and must be integrated with the egg-move lookup.

### Target strategy

Keep BW and B2W2 egg-move lists separate, then expose a breeding-profile selector. Gen II/III original egg moves remain available under the target-original profile.

## 6. Experience/growth data

BW has a dedicated growth-table NARC at `a/0/1/7`. Do not derive all experience behavior only from the one-byte growth-group ID. Preserve the Generation V tables/formulas as their own profile.

Gen III already has the six modern growth groups conceptually, so adapter work is straightforward.

Gen II has six table indexes but only four are used by actual species in the original Crystal source; the two legacy 'slightly fast'/'slightly slow' slots are candidates for Erratic/Fluctuating after direct ROM verification in every target revision. This is an implementation optimization, not yet a universal fact for all uploaded language ROMs.

## 7. Runtime profile design

All systems use an explicit data profile:

- `TARGET_ORIGINAL`
- `GEN5_BW_ORIGINAL`
- `GEN5_B2W2_ORIGINAL`
- `PROJECT_APPLIED`

Accessors should cover at minimum:

- species personal data
- move parameters
- level-up moves
- evolution entries
- egg moves
- item parameters
- TM/HM/tutor compatibility
- experience/growth behavior

This prevents a Gen V import from destroying target-original data and lets BW/B2W2 differences remain testable.

## 8. Next implementation blocks

1. Extract raw BW and White NARCs for the tables above and byte-compare version differences.
2. Add B2W2 source ROMs when available and create separate B2W2 corpora.
3. Build Gen III runtime accessors first because species/move/item storage is already 16-bit.
4. Add Gen III hidden-ability selector, third held item, 16-bit base EXP, 7-evolution table and extended move metadata.
5. Build Gen II widened species/move namespace and save-compatible sidecar/bit packing before enabling 252+ species or 256+ moves.
6. Hook breeding, evolution, battle, PC/save and link/trade paths.
7. Validate every field against original BW/B2W2 behavior; unsupported semantics remain marked unresolved rather than guessed.
