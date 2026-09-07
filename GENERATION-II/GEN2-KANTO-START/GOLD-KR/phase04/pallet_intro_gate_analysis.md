# Phase 04 — Pallet starter gate analysis (Korean Gold)

## Goal
Prevent the new-game player from reaching Route 1 before receiving a starter, without deleting or replacing any original Pallet Town/Route 1 content.

## Korean Gold ROM findings
- Pallet Town map id: `0D:02`
- Map attribute record file offset: `0x095369`
- Attribute bytes: `0F 09 0A 2A 97 54 4E 8F 45 A3 46 0C`
- Original map scripts: `4E:458F`
- Original event table: `4E:46A3`
- Original event composition: 3 warps, 0 coord events, 4 BG events, 2 objects
- North/south map connections are preserved.
- Clean-bank scan found the tail of bank `4E` zero-filled from `4E:5EAA` onward; Phase 04 uses `4E:6000` for the relocated event table and `4E:6100` for the gate script.

## Gate placement
The two Route 1 approach tiles inside Pallet Town are `(8,1)` and `(9,1)`. Two wildcard coord events (`scene = FF`) are inserted there.

The engine checks map connections before coord events. Therefore the gate is deliberately placed at `y=1`, still inside Pallet Town, rather than on/outside the north connection boundary.

## Gate behavior
`4E:6100`:
1. Check project flag 1936 (`EVENT_KANTO_STARTER_CHOSEN`, allocated from an unused event-flag slot).
2. If set: end immediately; Route 1 remains accessible through the original north connection.
3. If clear: warp to Oak's Lab (`0D:06`) at `(4,10)`.

No original Route 1 trainer, NPC, object, warp, connection, BG event, or Pallet Town event is removed.

## Event-table preservation
The original 67-byte Pallet Town event table is reconstructed as:
- original filler + 3 original warp records, unchanged
- 2 new coord-event records
- original 4 BG-event records, unchanged
- original 2 object-event records, unchanged

New event table: `4E:6000`, 83 bytes.
Map attribute event pointer changes from `A3 46` to `00 60` at file offset `0x095372`.

## Cumulative build verification
- Base SHA-1: `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65`
- Phase 04 output SHA-1: `797868df5f309ebe9460f3ca85887ca527bb67af`
- Phase 04 output SHA-256: `0a945c7bbf5a27371b75b98c94605b2ff428d116d3f2073523f70450e6ea7cbe`
- Header checksum: `08`
- Global checksum: `CD92`
- Clean-base reproducibility test: byte-identical output confirmed.

## Preservation rule
This phase only adds routing logic. Original map/event records remain available and unchanged in content; no content deletion is used as a progression mechanism.
