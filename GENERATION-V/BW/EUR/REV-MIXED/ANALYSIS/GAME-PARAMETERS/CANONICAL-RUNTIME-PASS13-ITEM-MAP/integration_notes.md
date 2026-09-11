# Gen III item-table integration notes — Pass 13

## ID policy

Use one project-wide Gen III item namespace:

- 0..374: preserve stock FireRed/LeafGreen IDs.
- 375..376: reserve for Emerald's original Magma Emblem / Old Sea Map slots.
- 377..388: append the 12 Gen IV/V evolution items.
- project item count: 389.

Do not consume stock unknown/dummy item IDs to save space.

## Existing evolution items

The following Gen5 IDs map to native Gen3 items:
80 Sun Stone -> 93
81 Moon Stone -> 94
82 Fire Stone -> 95
83 Thunder Stone -> 96
84 Water Stone -> 97
85 Leaf Stone -> 98
221 King's Rock -> 187
226 DeepSeaTooth -> 192
227 DeepSeaScale -> 193
233 Metal Coat -> 199
235 Dragon Scale -> 201
252 Up-Grade -> 218

## New items

377 Shiny Stone <- Gen5 107
378 Dusk Stone <- Gen5 108
379 Dawn Stone <- Gen5 109
380 Oval Stone <- Gen5 110
381 Protector <- Gen5 321
382 Electirizer <- Gen5 322
383 Magmarizer <- Gen5 323
384 Dubious Disc <- Gen5 324
385 Reaper Cloth <- Gen5 325
386 Razor Claw <- Gen5 326
387 Razor Fang <- Gen5 327
388 Prism Scale <- Gen5 537

## Required target-engine changes before enabling

1. Expand `gItems` / item icon / description / validation bounds to 389.
2. Add item names per language/region; do not force English strings into Japanese ROMs.
3. Shiny/Dusk/Dawn Stone use the existing evolution-stone party-menu route.
4. Held evolution items must be legal bag/held items.
5. Razor Claw and Razor Fang require their actual held battle effects in addition to evolution behavior; do not mark the item port complete until those effects are implemented.
6. Preserve target-original item IDs and data profiles.

The Black ROM's raw 36-byte records for all 24 evolution-linked items are retained in the local Pass 13 package as source evidence.
