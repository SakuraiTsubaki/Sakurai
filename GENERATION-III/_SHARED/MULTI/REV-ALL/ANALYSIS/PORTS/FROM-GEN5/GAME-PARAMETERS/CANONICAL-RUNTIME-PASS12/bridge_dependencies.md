# Gen5 evolution bridge dependencies — Pass 12

The stock FRLG `GetEvolutionTargetSpecies()` supports the smaller native Gen III evolution enum and five entries per species. The Gen5 profile is therefore routed to a separate seven-entry evaluator.

## Required services before linking the bridge

- `Project_GetTimeOfDayForEvolution`: Gen5-compatible day/night classification. FRLG's original friendship day/night code is disabled, so it must not be used as the project rule.
- `Project_GetEvolutionEnvironment`: target-map tag returning NONE / magnetic field / Moss Rock / Ice Rock for methods 25–27.
- `Project_TargetItemToGen5Item`: explicit target-item → Gen5 item-ID translation. Raw `a/0/1/9` item parameters must never be compared directly with Gen3 item IDs.
- `Project_GetCanonicalPartySpecies`: canonical party species list for Mantyke method 22.
- Trade-partner hook: method 7 requires the canonical species of the Pokémon being traded against Karrablast/Shelmet.

## Side effects kept outside condition evaluation

- Method 6: remove the held item only after a successful trade evolution.
- Method 15: Shedinja is a secondary spawn; it is not returned as Nincada's primary replacement species.
- `EVO_MODE_ITEM_CHECK`: never consumes the checked evolution item.

## Validation

Host-side selection against the uploaded Black ROM's raw seven-entry tables passed: Eevee day/night friendship, Thunder Stone, Moss Rock and Ice Rock; Karrablast paired trade and wrong-partner rejection; Burmy male/female; Mantyke with Remoraid; Magneton magnetic-field evolution; and Nincada primary Ninjask selection.

Status: source-level bridge complete; external time/map/item/trade services remain intentionally unresolved until those systems are ported and verified.
