# BPEE National Dex 649 — core save expansion design

Status: implementation script committed; ROM execution pending local runtime availability.

## Goal

Replace the temporary 1–263 National Dex aliases used by the 387–649 species activation build with real National Dex numbers 387–649 without shifting the retail Emerald save structures or destroying compatibility with existing saves.

## Internal species policy

- National 001–386: preserve retail Emerald mapping.
- Internal 412–439: preserve Egg / legacy Unown special slots.
- National 387–649: internal 440–702.
- The relocated species-to-National mapping table stores true National numbers 387–649 for internal 440–702.

## Retail Pokédex flag storage

Emerald stores Pokédex state redundantly:

- SaveBlock2 `pokedex.owned`
- SaveBlock2 `pokedex.seen`
- SaveBlock1 `seen1`
- SaveBlock1 `seen2`

Retail `NUM_DEX_FLAG_BYTES` is 52 bytes, giving 416 bits. Therefore National #387–416 can use already-existing unused retail bits with no save-layout change.

## Extension storage

SaveBlock1 contains a confirmed unused region:

- start: `0x3598`
- size: `0x180`
- end-exclusive: `0x3718`

The extension uses only 124 bytes of this region:

| Field | SaveBlock1 offset | Size |
|---|---:|---:|
| magic | `0x3598` | 4 |
| owned #417–649 | `0x359C` | 30 |
| seen #417–649 | `0x35BA` | 30 |
| seen1 #417–649 | `0x35D8` | 30 |
| seen2 #417–649 | `0x35F6` | 30 |
| end | `0x3614` | — |

Magic value: `0x35365844` (`DX65` in little-endian bytes).

Existing vanilla saves are handled lazily. On the first #417–649 access, a missing magic value causes only the 120 extension flag bytes to be cleared and then the magic to be written. No retail save field is moved.

## Runtime hooks

Retail BPEE functions are replaced by small Thumb→ARM entry stubs. The original function entry addresses remain stable for callers.

- `GetSetPokedexFlag` — routes #1–416 to retail arrays and #417–649 to the extension arrays while preserving Emerald's redundant seen/owned consistency checks.
- `GetNationalPokedexCount` — counts #1–649.
- `NationalPokedexNumToSpecies` — scans the relocated mapping table through internal 702.

The opposite mapping, `SpeciesToNationalPokedexNum`, already consumes the relocated species-to-National table and therefore gains true #387–649 values once the temporary aliases are replaced.

## Pokédex entry safety

Retail `gPokedexEntries` contains entries through National #386. It is expanded to indices 0–649.

For #387–649:

- height/weight: read directly from BW `/a/0/1/6` personal data;
- category: explicit `UNKNOWN` compatibility placeholder;
- description: `gText_Unknown` placeholder;
- display scale fields: safe placeholder values copied from an existing retail entry.

These placeholders are project compatibility data, not represented as Generation V official Pokédex prose.

## Footprints

Retail footprint routing is expanded through internal species 702. New species use a safe existing placeholder footprint until the actual Generation IV/V footprint asset import phase.

## Main Pokédex UI boundary

This phase does **not** claim the main browse/search Pokédex UI is 649-ready. Retail `struct PokedexView` embeds `pokedexList[NATIONAL_DEX_COUNT + 1]`, so compiled field offsets after that array depend on the 386-species constant. The full list/search/order UI must be expanded as a separate UI-memory phase rather than by blindly changing the constant in the retail binary.

Core save flags, real National-number routing, counts, caught-page data safety and National↔internal conversion are the scope of this implementation.

## Implementation

Tool:

`CROSS-GEN/TARGET/GEN5-TO-GEN3-SPRITE-SPECIES-INTEGRATION/BPEE/TOOLS/expand_pokedex_save_649_bpee.py`

The tool never commits a ROM binary. It expects the locally generated 387–649 active BPEE ROM and its manifest, emits a separate work ROM, and writes a verification manifest.
