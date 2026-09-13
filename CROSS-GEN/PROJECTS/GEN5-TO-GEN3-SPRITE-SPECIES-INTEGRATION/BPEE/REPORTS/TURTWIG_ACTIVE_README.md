# Gen V 64x64 -> Gen III: BPEE Turtwig activation smoke build

Status: binary/static validation passed; emulator boot test not available in the current execution environment.

## Target

- Base: `Pokemon_-_Emerald_Version_(USA,_Europe)_GEN5_64x64_SPRITES.gba`
- Game code: BPEE
- National species: 387 Turtwig
- New internal species ID: 440
- Preserved original special ID range: 412-439
- Reserved new species range: 440-702 (National 387-649)

## What is active

The smoke build relocates and expands the runtime tables needed by a wild Pokémon creation/battle path: species names, BaseStats-compatible species parameters, evolution records, level-up pointers, front/back coordinates, still-front table, enemy elevation, front animation pointers/IDs/delays, Hoenn/National mapping tables, TM/HM learnability, cry routing, icon routing, and back animation IDs.

Route 101 land slot 0 is changed from Lv.2 Wurmple to Lv.2 internal species 440 so the path can be exercised immediately in an emulator.

The existing expanded BW front/back/normal/shiny battle sprite tables remain the sprite source. The inserted Turtwig front/back coordinates are computed from the non-transparent pixels of those actual 64x64 frames.

## Compatibility placeholders in this smoke build

This build intentionally does not pretend that later-generation subsystems are finished. Turtwig temporarily uses National Dex #1 as a save-bit compatibility alias, Bulbasaur's cry/icon/animation routing, no TM/HM flags, and no evolution target until Grotle (441) is activated. Leaf Storm is omitted because vanilla Emerald has no Gen IV move ID. Hidden Ability support is deferred because vanilla Gen III does not have the Gen V hidden-ability slot.

These are smoke-test bridges, not final Generation V specifications.

## Validation

`TURTWIG_ACTIVE_MANIFEST.json` records hashes, all relocated table offsets, pointer relocation counts, guard patches, derived sprite bounding boxes, and static checks. All 36 recorded checks passed. All original base pointers for the relocated metadata tables have zero aligned references remaining in the retail 16 MiB address region.

No ROM binary is committed to GitHub. The user-side patched ROM is generated locally from the user's supplied source ROM/assets.
