# Gen III canonical species runtime gate

The project must **not** switch live stored Gen III Pokémon species IDs to canonical National-Dex IDs 001..649 until every required species-ID consumer has been converted.

## Completed

- exact internal <-> National mapping for all 386 real Gen III species
- OLD_UNOWN removal policy
- canonical SpeciesInfo 0..649 build output
- persistent form storage design
- BW `(species, form)` personal routing
- correction to reuse stock `gBattleMonForms[]`
- Generation III FORM_AUTO preservation for Unown and version-dependent Deoxys

## Blocking before canonical runtime can be enabled

| Component | Required action |
|---|---|
| `include/constants/species.h` | renumber and extend to canonical 001..649, EGG 650 |
| species names | reindex and extend |
| level-up learnsets | reindex pointer/data layer and add Gen V profile |
| evolution table | reindex sources and targetSpecies; expand 5 -> 7 entries |
| TM/HM learnsets | reindex and extend compatibility layer |
| `NationalPokedexNumToSpecies` / `SpeciesToNationalPokedexNum` | simplify to canonical identity after migration |
| `SpeciesToCryId` | remove OLD_UNOWN-hole compensation and rebuild cry mapping |
| Pokédex orders | remove OLD_UNOWN and extend through 649 where applicable |
| wild encounter data | rewrite embedded species IDs |
| trainer party data | rewrite embedded species IDs |
| daycare/breeding | audit species/evolution/baby references |
| Hall of Fame | migrate persistent species IDs |
| link/trade | add versioned canonical <-> original Gen III translation |
| Battle/Trainer Tower | rewrite/migrate stored species IDs |
| Easy Chat Pokémon groups | rewrite species-ID lists |
| Pokédex seen/caught bitsets | preserve National indexing but extend capacity through 649 |
| graphics metadata | reindex later; sprite/graphics work remains paused |

## Rule

`canonical_runtime_enabled = false` until every blocking category above is converted and regression-tested.

The canonical SpeciesInfo table is therefore a validated **build target**, not yet a claim that current uploaded ROM binaries store canonical species IDs at runtime.
