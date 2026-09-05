# FireRed 8-ROM Semantic Census — Stage 6

Scope: exact MapEvents parsing for all 425 maps in all eight FireRed ROMs, including object/clone events, warps, coord events, background events, hidden items, map-script tables, and high-confidence script roots.

## Source-correlated physical layouts

Validated against `pret/pokefirered` `include/global.fieldmap.h` and `asm/macros/map.inc`:

- `MapEvents`: 0x14 bytes: four u8 counts followed by four pointers.
- `ObjectEventTemplate`: 0x18 bytes; normal object script pointer at +0x10, flag at +0x14. `OBJ_KIND_NORMAL=0`; `OBJ_KIND_CLONE=255`.
- `WarpEvent`: 0x08 bytes.
- `CoordEvent`: 0x10 bytes; script pointer at +0x0C.
- `BgEvent`: 0x0C bytes; union at +0x08. `BG_EVENT_HIDDEN_ITEM=7` stores packed item/flag/quantity/underfoot data instead of a script pointer.
- Map-script table entries are 1-byte type + 4-byte pointer and terminate with type 0. `ON_FRAME_TABLE` and `ON_WARP_INTO_MAP_TABLE` point to `map_script_2` tables of `{u16 var,u16 compare,u32 script}` records terminated by `u16 var == 0`.

## Whole-map census

All eight ROMs contain 425 map headers and all 425 event blocks parsed without structural failure.

Common counts in every build:

- warps: 1,294
- coord events: 228
- background events: 702
- hidden-item background events: 183
- scripted background events: 519
- normal object events: 1,639
- map-script table entries: 325
- nested `map_script_2` entries: 350
- high-confidence script-root occurrences: 2,915
- unique script-root offsets per ROM: 1,959

Object totals differ only because of one clone object:

- JP Rev0 / JP Rev1: 1,647 objects = 1,639 normal + 8 clone
- ES/DE/EN0/EN1/FR/IT: 1,648 objects = 1,639 normal + 9 clone

## Exact structural build difference: Route 7

The only normalized map-event structural difference found against EN Rev0 is map group 3, map 25 (`Route7`). Both Japanese builds contain zero object events there; all six western builds contain one clone object.

The western record is:

- local id: 1
- graphics id: 95 (`OBJ_EVENT_GFX_CUT_TREE` in the source map definition)
- position: x=-8, y=12
- kind: 255 / clone
- target local id: 10 (`LOCALID_CELADON_BORDER_TREE` in source)
- target map: group 3, map 6 (`CeladonCity`)
- no script pointer or flag of its own

The current `pret/pokefirered` Route7 map JSON describes exactly this CUT TREE clone. The physical census therefore identifies it as a western-build Route7/Celadon border-tree clone that is absent from both Japanese ROM revisions. No cause is inferred beyond that verified build difference.

## Map-script distribution

Identical across all eight ROMs:

- ON_LOAD: 55
- ON_FRAME_TABLE: 58
- ON_TRANSITION: 130
- ON_WARP_INTO_MAP_TABLE: 33
- ON_RESUME: 47
- ON_DIVE_WARP: 0
- ON_RETURN_TO_FIELD: 2
- total: 325

High-confidence script roots are also identical by source class in all builds:

- object event roots: 1,584
- coord event roots: 228
- background event roots: 519
- direct map-script roots: 234
- nested map-script-table roots: 350
- total root occurrences: 2,915

## Validation

Every ROM passes:

- object count == Stage 3 map-header aggregate
- warp count == Stage 3 aggregate
- coord count == Stage 3 aggregate
- bg count == Stage 3 aggregate
- every MapEvents block and event-array pointer lies inside its ROM
- every 425-map map-script table terminates and parses cleanly

## Artifact policy

Review-facing summaries and exact difference ledgers are committed here. Full per-ROM object/warp/coord/bg ledgers and the full root/map table corpora are deterministic high-volume outputs of `fire_red_stage6_map_events.py`; the scanner reproduces them from the eight local ROMs without storing any ROM bytes in GitHub.

## Status

Stage 6 closes the physical map/event layer and establishes 1,959 unique high-confidence event-script roots per build. The next pass follows those roots through event bytecode to classify branch/call/text/movement/native/data edges, then proceeds to audio, RFU/Mystery Gift/e-Reader, and final ownership/free-space mapping.
