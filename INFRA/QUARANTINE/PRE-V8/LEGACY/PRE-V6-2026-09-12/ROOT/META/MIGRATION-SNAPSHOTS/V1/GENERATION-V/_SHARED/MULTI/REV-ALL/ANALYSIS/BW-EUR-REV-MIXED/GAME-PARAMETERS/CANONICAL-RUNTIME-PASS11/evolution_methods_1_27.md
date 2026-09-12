# BW evolution methods 1–27 — Pass 11

Source: uploaded Pokémon Black EUR ROM, NARC `a/0/1/9`. Species 1..649 use all method IDs 1..27.

| ID | Project meaning | ROM representative `(species,param,target)` |
|---:|---|---|
| 1 | Friendship | 42,0,169 |
| 2 | Friendship + day | 133,0,196 |
| 3 | Friendship + night | 133,0,197 |
| 4 | Level | 1,16,2 |
| 5 | Trade | 64,0,65 |
| 6 | Trade while holding item | 95,233,208 |
| 7 | Karrablast/Shelmet paired trade | 588,0,589 |
| 8 | Use item | 25,83,26 |
| 9 | Level, Atk > Def | 236,20,106 |
| 10 | Level, Atk = Def | 236,20,237 |
| 11 | Level, Atk < Def | 236,20,107 |
| 12 | Wurmple → Silcoon PID branch | 265,7,266 |
| 13 | Wurmple → Cascoon PID branch | 265,7,268 |
| 14 | Nincada → Ninjask | 290,20,291 |
| 15 | Nincada → Shedinja side evolution | 290,20,292 |
| 16 | Beauty | 349,170,350 |
| 17 | Use item + male | 281,109,475 |
| 18 | Use item + female | 361,109,478 |
| 19 | Level holding item + day | 440,110,113 |
| 20 | Level holding item + night | 207,327,472 |
| 21 | Level knowing move | 108,205,463 |
| 22 | Level with species in party | 458,223,226 |
| 23 | Level + male | 412,20,414 |
| 24 | Level + female | 412,20,413 |
| 25 | Level in magnetic-field environment | 82,0,462 |
| 26 | Level by Moss Rock environment | 133,0,470 |
| 27 | Level by Ice Rock environment | 133,0,471 |

Validation: all 27 methods have at least one record in species 1..649. A host-side mirror of the Gen III evaluator passed one positive case for every method plus negative regressions for wrong paired-trade partner, wrong gender, wrong time, and wrong environment.

Implementation policy: keep the raw seven-entry Gen5 evolution table and evaluate its conditions through `ProjectEvolutionContext`; do not collapse it into the smaller native Gen III evolution enum. Target-original Gen III evolution data remains a separate profile.
