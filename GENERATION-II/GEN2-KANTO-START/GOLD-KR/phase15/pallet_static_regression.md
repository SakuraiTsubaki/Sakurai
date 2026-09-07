# GEN2 Kanto Start — Gold KR Phase 15 Pallet Static Regression

## Result
**PASS — no ROM change in Phase 15.**

Validated target: Gold KR Phase 14
- SHA-1: `ddbc98b9c1fafa052e7cfcc38fc120963a5e0974`
- SHA-256: `6cc489183a199f63e858db8610ad63f2e2c62bba217a4887e1c02e6431fff70c`
- Header checksum: `08`
- Global checksum: `E96F`

## Layered regression
The Phase 10→11, 11→12, 12→13, and 13→14 binaries were compared byte-for-byte. All changed bytes remain inside each phase's documented patch regions plus the Game Boy global checksum bytes. No later phase mutated unrelated regions.

Individual validators also pass for Phase 11, 12, 13, and 14.

## Pallet exterior
Final Phase 14 event table at `4E:6A00` parses as:
- 3 warps — all original GSC Pallet destinations preserved
- 2 coord events — RGBY north triggers at `(10,1)` and `(11,1)`, scripts `4E:6500` and `4E:6510`
- 4 background events — original GSC signs preserved
- 5 objects — GSC Teacher, GSC Fisher, RGBY girl, RGBY technology/profile NPC, Professor Oak

Pallet outdoor sprite set remains the Phase 11 integrated set; only previously unused swimmer slots were repurposed for Oak/Lass while sprites actually used by Pallet/Route 1 remain available.

## Integrated tilesets
Phase 10 substrate is intact:
- Pallet `1D`
- Red House 1F `1E`
- Red House 2F `1F`
- Green/Blue House `20`
- Oak Lab `21`

The extended tileset table remains at `05:7800`, and later phases did not overwrite the integrated graphics/metatile/collision packages.

## Oak Lab and starters
Event table at `59:6000` parses as:
- 2 warps
- 0 coord events
- 16 background events
- 7 objects = original 4 + 3 starter balls

Starter balls remain at `(3,5)`, `(4,5)`, `(5,5)`, with scripts:
- `59:6100`
- `59:6140`
- `59:6180`

Phase 13/14 palette work did not touch the Lab integration region.

## Phase 12 fidelity layer
Still present:
- dedicated RGBY girl and technology-NPC scripts/text
- Yellow Professor Oak tutorial backpic hook
- Route 29 Rattata tutorial remains separate from the Pikachu/Oak path

## Phase 13/14 palette layer
Still present:
- GSC CGB/time-of-day profile
- Red/Blue SGB profile
- Japanese Green SGB profile
- Yellow SGB profile
- Yellow CGB profile
- saved profile bits 1946–1948
- Phase 14 technology-NPC selector cycles through all five states and reloads the map after a change

## Reproducibility
Both Phase 14 replay ROMs are byte-identical to the primary Phase 14 build:
- Phase 13 → Phase 14 delta replay: PASS
- clean Korean Gold → cumulative Phase 14 replay: PASS

## Limitation
This is a **static binary regression**, not an emulator playtest. A compatible emulator runtime has not been run in this environment, so Pallet is locked as **static integration complete / runtime playtest pending** rather than fully play-verified.
