# Generation IV → Gen III Phase 2A — Graphics ID Expansion

## Completed scope

- Preserves legacy Gen III internal species IDs `0..439` and all original 440-slot graphics/coordinate/palette tables in place.
- Assigns National Dex `387..493` to new internal IDs `440..546`.
- Reserves `547..548` as safe fallback/guard entries.
- Builds new 549-entry front, back, front-coordinate, back-coordinate, normal-palette, and shiny-palette tables.
- Redirects every literal reference to the old table bases to the expanded table bases while keeping old tables byte-identical.
- Extends verified Pokémon graphics loader bounds from 412 to 548 only at revision-specific decompressor guard sites.
- Recomputes coordinates from the HGSS 64x64 rendered nontransparent bounding box for National Dex 001..493.
- Emerald additionally gets a 549-entry animated-front table with HGSS `f0+f1` streams for National Dex 001..493.
- Source sprite authority: uploaded Korean HeartGold ROM; the existing GitHub sprite master remains a cross-check/published asset set.

## Internal ID policy

`001..251 -> unchanged`; `252..386 -> legacy Gen III IDs 277..411`; `387..493 -> 440..546`. Egg remains 412 and the Gen III Unown B..?/! special slots remain 413..439. No legacy special slot is repurposed.

## Verification

- 493 selected species per target: front/back LZ streams decode to 2048 bytes; normal/shiny palettes decode to 32 bytes; generated MonCoords are valid.
- Emerald: all 493 animated-front streams decode to 4096 bytes.
- Original legacy graphics/coordinate/palette table bytes remain unchanged in their original ROM locations.
- Every generated IPS32 patch was reapplied to its pristine source ROM and matched the work ROM byte-for-byte / SHA-256.
- Verification errors: 0 for all five targets.

## Targets

- `RUBY_JP_REV0`: source `e911caa1ffbf8704cd45bbe064ade40e24efa50dfdce82adf4b2899b5f733852`, work `7e523151c54d5e724cdfad9dabc61adf24df177b995e150a75d9fcb05afa3287`, patch 1,195,781 bytes; new front `0x91e080`, back `0x91f1b0`, coords `0x9202e0/0x920b80`.
- `SAPPHIRE_JP_REV0`: source `6a5ff7656531ab41d1ea9cd8f2d045ab6228405b43f3ee09ea3ff5077c0f60c9`, work `e4ecfb60b44c38a453d6f3e33524982ad0b19ffff73104097774fb48896de6e9`, patch 1,195,781 bytes; new front `0x91e080`, back `0x91f1b0`, coords `0x9202e0/0x920b80`.
- `EMERALD_JP_REV0`: source `33f5610b9186b4add09fef68895deb00f552b997b3d133b5a961e5123506343c`, work `f3463e121b5a7183222d52b90f545864571a54a33e00ce352f6f8fc081152500`, patch 1,879,924 bytes; new front `0x111e080`, back `0x111f1b0`, coords `0x11202e0/0x1120b80`.
- `FIRERED_JP_REV1`: source `cec5fc4dbe38cd8026bd6664a1a041d9dc91e8d4249bab04e7bde70c3cdf4e06`, work `c4a274f69aa8b55042a2620dc952d113dbb8fcedd4a43209d5fe0f3a43cddd94`, patch 1,196,704 bytes; new front `0x111e080`, back `0x111f1b0`, coords `0x11202e0/0x1120b80`.
- `LEAFGREEN_JP_REV0`: source `2957b392dc09fc8df45a660af5493368d7bd378d299862f4cc115998e9da0bf2`, work `d6c5c5a13a623fbc55e494353e5089ac0d5ea8a71ae49c9b52c7b267f0f4ed2c`, patch 1,196,704 bytes; new front `0x111e080`, back `0x111f1b0`, coords `0x11202e0/0x1120b80`.

## Completion boundary

This phase completes the **graphics address-space expansion** for base species through National Dex 493. It does **not** yet claim full playable species support for 387..493: species names, base stats, types, abilities, learnsets, evolutions, icons, cries, Pokédex data, save/dex bitfields, encounters and other species-indexed gameplay tables still require coordinated expansion. DP/Pt/HGSS runtime version selection, gender switching, alternate forms, and the final Gen IV animation script selector are subsequent layers and must not be described as complete yet.
