# Phase 8 — Gen III names / evolution / level-up migration

## Direct ROM work completed

All 10 uploaded Gen III ROMs were independently scanned and the following were
located without reusing offsets between versions:

- fixed-size species-name table
- `gEvolutionTable`
- `gLevelUpLearnsets` pointer table

Japanese name records are 6 bytes; English/European-English records are 11 bytes.

For each target, the existing #001–386 name records were reordered into exact
National Dex order **byte-for-byte**. New #387–493 localized names are deliberately
not fabricated here; they are a separate language/encoding step.

## Evolution structure: important blocker resolved

Retail Gen III:
- `EVOS_PER_MON = 5`
- each evolution = `u16 method, u16 param, u16 target`

HGSS `a/0/3/4`:
- 7 evolution slots per species
- the same 6-byte triple layout
- Eevee (#133) actually uses all **7** slots

Therefore `EVOS_PER_MON` must become at least 7. Keeping 5 would silently lose
Leafeon/Glaceon or another Eeveelution.

Gen IV method IDs 0–15 retain the Gen III method-number lineage. HGSS extends
the enum with methods 16–26:
stone+gender, held-item day/night, known-move, party-species, gendered level,
Mt. Coronet, Eterna Forest, Route 217.

`evolution_method_compatibility.csv` records exactly which engine cases must be added.

## Level-up learnsets: no new record encoding required

This is a useful compatibility result.

Both retail Gen III and HGSS use:

    u16 value = (level << 9) | move_id
    0xFFFF    = end

That leaves 9 bits for the move ID: 0..511.

Generation IV only needs moves through #467, so the **existing Gen III learnset
word format already fits every Gen IV move ID**. The move table/effects still
need expansion, but level-up learnsets themselves do not need a wider record.

For every target a relocatable `.g4ls` archive was produced:
- 0..386 = that target ROM's original learnsets, canonicalized by species
- 387..493 = HGSS learnsets

No move values were approximated.

## Preservation / comparison

The project does not silently replace the target games with HGSS values.

Two delta ledgers were generated:
- target-original level-up list vs HGSS
- target-original evolution list vs HGSS

So the eventual adoption layer can distinguish:
`target original`, `Gen IV source`, and `project integration`.

## Not activated yet

These are staging assets, not blind ROM patches.

Before binary activation:
1. allocate relocated tables,
2. redirect every table pointer,
3. expand `NUM_SPECIES`,
4. expand `EVOS_PER_MON` 5 -> 7 and add methods 16..26,
5. expand move data through #467,
6. insert official localized names #387..493,
7. test save/trainer/wild/script references under canonical IDs.

Sprites remain on hold.
