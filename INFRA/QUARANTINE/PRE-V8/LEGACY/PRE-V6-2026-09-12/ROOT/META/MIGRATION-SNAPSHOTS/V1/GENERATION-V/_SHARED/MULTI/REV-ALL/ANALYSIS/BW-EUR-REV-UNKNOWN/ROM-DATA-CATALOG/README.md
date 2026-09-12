# Generation V BW — Phase 2 ROM Data Catalog

Status: **Phase 2 structural/semantic catalog completed** for the uploaded Pokémon Black / Pokémon White SweeTnDs EUR/English ROM pair.

## Method

The uploaded ROMs remain read-only. The NitroFS/FAT/FNT and ARM9 overlay table were parsed directly. Every named NitroFS file was classified with an explicit confidence state rather than forcing an invented role.

Confidence states:

- `confirmed`: BW-specific research/tools agree with the ROM structure.
- `high`: strong direct structural evidence and/or explicit BW mapping; some field semantics remain to decode.
- `high_inferred`: strong ROM-internal evidence, but exact field decoding is pending.
- `medium`: likely role from archive documentation/signatures; runtime-reference audit pending.
- `structure_only`: Nintendo graphics/3D/audio format is identifiable, but gameplay role is unresolved.
- `unknown`: preserved as unknown.

## Coverage

- Named NitroFS files: **247**
- NARC containers: **237**
- Raw named files: **10**
- ARM9 overlays: **237**
- Black/White-different named NitroFS files: **5**
- Black/White-different ARM9 overlay blobs: **180**

The 5 named NitroFS archives that differ between Black and White remain:

- `a/0/2/6` — title/version assets
- `a/0/8/6` — semantic role still unresolved
- `a/1/2/6` — wild encounter data
- `a/1/7/8` — 649 × 249-byte per-species data; strongly inferred Pokédex availability/location matrix, exact fields pending
- `a/2/3/1` — 73-member version-dependent archive; semantic role still unresolved

## Core BW1 data archives confirmed in this phase

| Path | Members | Role | Status |
|---|---:|---|---|
| `a/0/0/2` | 288 | system/message text | confirmed |
| `a/0/0/3` | 472 | story/field text | confirmed |
| `a/0/1/6` | 669 | personal Pokémon parameters | confirmed |
| `a/0/1/7` | 8 | experience/growth tables | confirmed |
| `a/0/1/8` | 668 | level-up learnsets | confirmed |
| `a/0/1/9` | 668 | evolution data | confirmed |
| `a/0/2/0` | 650 | baby/base-species table | confirmed |
| `a/0/2/1` | 560 | move parameter data | confirmed |
| `a/0/2/4` | 627 | item parameter data | high |
| `a/0/5/7` | 899 | field/map event scripts | high |
| `a/0/9/2` | 616 | trainer data (`trdata`) | confirmed |
| `a/0/9/3` | 616 | trainer party/Pokémon data (`trpoke`) | confirmed |
| `a/1/2/3` | 650 | egg move data | high |
| `a/1/2/5` | 428 | overworld/map event-object data | confirmed |
| `a/1/2/6` | 112 | wild encounter data | confirmed |
| `a/1/7/8` | 649 | per-species Pokédex availability/location candidate | high_inferred |

### BW vs B2W2 path warning

Do **not** reuse B2W2 archive paths blindly. A concrete example is trainer data:

- BW1: `trdata = a/0/9/2`, `trpoke = a/0/9/3`
- B2W2: many tools/documentation use shifted trainer paths.

This phase therefore treats the uploaded BW ROM structure as authoritative and external NARC lists only as supporting evidence.

## Script / map linkage confirmed

BW research identifies `a/0/5/7` as the script archive and `a/1/2/5` as overworld data. `a/0/1/2` is the ZoneData map-association table linking map state to resources such as scripts/overworld data. The uploaded ROM has 428 overworld members; old forum notes sometimes quote 427, so the ROM count is retained as the authoritative value for this dump.

## Overlay note

All 237 ARM9 overlay records were parsed and compared. **180** overlay blobs differ between Black and White. A byte difference in an overlay is not automatically a gameplay/content difference; code relocation, compressed-size changes and address shifts must be separated from actual version logic.

Overlay 21 is singled out for the next decoding pass because BW research/tools locate embedded gameplay tables there, including Poké Mart inventory data.

## Unused/dummy policy

Archives identified by old lists as blank/dev/unused are **not** treated as definitively unused until code/script reference tracing proves they are unreachable in normal execution. They remain candidates for the project's later unused-content normalization phase.

## Primary working artifacts

Generated locally from the ROMs:

- `gen5_bw_phase2_nitrofs_catalog_raw.csv`
- `gen5_bw_phase2_nitrofs_semantic_catalog.csv`
- `gen5_bw_phase2_overlay9_catalog.csv`
- `gen5_bw_phase2_DATA_CATALOG_README.md`
- `scan_gen5_nitrofs_catalog.py`
- `build_gen5_bw_phase2_catalog.py`

ROM binaries are not committed.

## References used for cross-checking

- Project Pokémon RawDB — Pokémon Black internal file list/data labels
- Project Pokémon BW Trainer Editor research (`trdata=a/0/9/2`, `trpoke=a/0/9/3`)
- Project Pokémon BW overworld/script research (`a/1/2/5`, `a/0/5/7`, ZoneData `a/0/1/2`)
- Project Pokémon egg-move research (`a/1/2/3`)
- TrainerTyrant documentation for BW/B2W2 trainer-path distinction
- MartEditBW documentation for BW `overlay9_21`

## Next phase

Phase 3 should decode these archives at **field/record level**, beginning with Pokémon personal data, moves, items, trainers, encounters, scripts/ZoneData/overworld links, then Pokédex and overlay-embedded gameplay tables. The goal is a reproducible schema, not merely archive names.
