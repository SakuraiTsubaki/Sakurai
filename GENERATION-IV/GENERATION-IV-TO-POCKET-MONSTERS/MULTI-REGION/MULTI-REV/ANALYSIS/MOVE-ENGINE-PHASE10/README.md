# Phase 10 - Generation IV move namespace / move-data bridge

## Active Generation IV sources

All five uploaded Generation IV ROMs were parsed from their active move tables:

- Diamond / Pearl: `poketool/waza/waza_tbl.narc`
- Platinum: `poketool/waza/pl_waza_tbl.narc`
- HeartGold / SoulSilver: `a/0/1/1`

Every active archive contains 471 records of 16 bytes.

The official Generation IV move namespace stops at #467 Shadow Force.
Archive records 468-470 physically exist but are outside `NUM_MOVES`; they are
preserved separately as extra/archive data, not activated as invented moves.

## DP / Pt / HGSS differences

Diamond and Pearl active tables are byte-identical.
HeartGold and SoulSilver active tables are byte-identical.

All official new moves #355-467 are byte-identical between DP, Platinum and
HGSS.

Across move IDs 0-467, only two records differ between those active profiles:

- #95 Hypnosis: DP accuracy 70 -> Platinum/HGSS accuracy 60.
- #258 Hail: Platinum -> HGSS changes `unkB` from 0x02 to 0x00.

The complete version matrix is retained instead of flattening these differences.

## 113 new moves

#355 Roost through #467 Shadow Force gives 113 new moves.

HGSS categories:
- Physical: 52
- Special: 29
- Status: 32

This category is the authoritative source for the Generation IV
physical/special split.

## Gen III 12-byte layout

The retail Gen III ROM uses 12 physical bytes per `gBattleMoves` record.
Only bytes 0-8 contain original fields; bytes 9-11 are zero in all 355 records
in all 10 uploaded Gen III targets.

Phase 10 reuses those bytes without changing the stride:

- byte 9 = Gen IV category
- bytes 10-11 = exact `u16` Gen IV effect ID

The move table still grows from 355 entries to 468 entries:

- old size: 4260 bytes
- new size: 5616 bytes
- growth: 1356 bytes

## 16-bit effect requirement

Retail Gen III's effect namespace ends at 213.
Official HGSS move data reaches effect ID 276.

Among #355-467:
- 56 moves use an effect ID above 213
- they use 54 distinct higher effect IDs

Therefore an 8-bit effect dispatcher cannot faithfully implement Generation IV.
`GetMoveEffect16()` is the required source of truth.

## 16-bit range requirement

Generation IV range values extend through bit 10.
The exact range is stored separately in `gGen4MoveMeta`.

The old Gen III `target` byte is retained only as a compatibility mirror.
It is insufficient for all Generation IV moves.

Examples:
- #367 Acupressure = 0x0200 SINGLE_TARGET_USER_SIDE
- #382 Me First = 0x0400 FRONT

## Physical/special split

Retail Gen III uses move type to pick Attack/Defense vs Sp.Atk/Sp.Def.
Phase 10 supplies the replacement move-category hook:

- category 0 -> physical
- category 1 -> special
- category 2 -> status

Type remains responsible for STAB, type effectiveness and immunities.

## Ten Gen III staging tables

A 468 x 12 staging table was built for each uploaded Gen III ROM.

For #000-354:
- bytes 0-8 are preserved byte-for-byte from that target ROM
- formerly-zero bytes 9-11 receive category and exact effect16

For #355-467:
- scalar values come from active HGSS
- category and exact effect16 are stored
- exact range and HGSS flag metadata are preserved separately

These are staging tables, not a claim of playable binary activation.

Full activation still requires:
1. relocate the expanded move table and redirect references;
2. migrate effect dispatch to 16-bit IDs;
3. migrate target selection to 16-bit Generation IV range;
4. replace type-based physical/special battle logic;
5. implement missing Generation IV effect handlers;
6. add names/descriptions/UI/TM and learnset integration.

Sprites remain on hold.
