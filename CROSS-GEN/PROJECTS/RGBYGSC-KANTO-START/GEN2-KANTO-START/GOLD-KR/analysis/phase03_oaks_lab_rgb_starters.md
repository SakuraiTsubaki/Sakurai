# GOLD KR Phase 03 — Oak's Lab RGB starters

## Base ROM
- `Pocket Monsters Geum (Korea).gbc`
- SHA-1: `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65`

## Actual Korean Gold Oak's Lab structure
The Oak's Lab map attribute record was identified directly in the Korean Gold ROM at file offset `0x096071`:

`00 06 05 37 B6 4B 59 BC 56 6C 5C 00`

Decoded relevant fields:
- map group/map: `0D:06` from the Korean disassembly map constants
- dimensions: 5 x 6 blocks
- block data: bank `37`, address `4BB6`
- map scripts: bank `59`, address `56BC`
- map events: bank `59`, address `5C6C`

The original event table is exactly 148 bytes long and ends at `59:5D00`. It contains:
- 2 warp events
- 0 coordinate events
- 16 background events
- 4 object events

Bank 59 from `59:5D00` onward contains a large zero-filled region, so the expanded event data can be relocated without overwriting neighboring original data.

## Preservation-first relocation
The expanded table is placed at `59:6000`.

All original event records are retained. The original object count byte changes from 4 to 7, and three new object records are appended. No original warp, background event, NPC/object record, or script pointer is removed.

The Oak's Lab map-attribute event pointer at file offset `0x09607A` changes from `5C6C` to `6000`.

## Starter objects
Three `SPRITE_POKE_BALL` / `OBJECTTYPE_SCRIPT` objects are added:

| Starter | Position | Script | Visibility flag | Choice flag |
|---|---:|---|---:|---:|
| Bulbasaur | (3,5) | `59:6100` | 1933 | 1937 |
| Charmander | (4,5) | `59:6140` | 1934 | 1938 |
| Squirtle | (5,5) | `59:6180` | 1935 | 1939 |

Common starter-selected flag: 1936.

Flags 1932–2047 are in the unused tail range of the original 2048-event flag space; Phase 03 uses 1933–1939 and leaves 1932 reserved for the next intro-flow step.

## Collision verification
Oak's Lab uses `TILESET_LAB`. The actual Korean Gold block map was read at `37:4BB6`. All three selected coordinates resolve to block `01`, whose four collision quadrants are all `FLOOR`, so the object placements do not occupy a wall, bookshelf, warp carpet, or other special collision tile.

## givepoke return semantics
The event engine's `Script_givepoke` copies register B from `GivePoke` into `wScriptVar`. `GivePoke` uses:
- 0: successfully added to party
- 1: party full, successfully sent to Box
- 2: total failure

Therefore the new starter scripts branch to failure only on `ifequal 2`. Treating zero as failure would incorrectly reject the normal party-success path.

## Script behavior
Each starter ball:
1. refuses to run again if the common starter flag is already set;
2. displays the selected Pokémon picture and cry;
3. gives the species at level 5 with no held item;
4. aborts without changing starter flags if `GivePoke` returns 2;
5. on success, sets the common and species-choice flags;
6. disappears all three starter balls, which also sets their per-object visibility flags.

## Phase 03 verification
Cumulative build SHA-1: `544bbf68574034518dac22e4e6e905bb509aafe0`
SHA-256: `d1546e2a0205b3ead358c69bb273206c71a72e67745fa0dd8f87ff128a4092e5`
Header checksum: `08` — valid
Global checksum: `B9AF` — valid

A clean-base reproduction test using the generated patcher produced a byte-identical Phase 03 ROM image.

## Next dependency
Pallet Town currently has no scene/coordinate event that forces the early-game Oak flow. Route 1 also retains its original GSC Kanto trainers. The next phase should add a one-time Pallet/Oak intro gate so the player cannot enter Route 1 before receiving a starter, while preserving every original Pallet and Route 1 event.
