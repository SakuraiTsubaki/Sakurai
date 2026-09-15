# Generation VI No.650–721 logical visual-state inventory validation

## Status

**PASS — generation-scoped logical inventory definition. Archive/member reconciliation is still pending.**

Builder:

`tools/build_gen6_650_721_logical_states.py`

The builder encodes every Generation VI new species from National Dex 650 through 721 and expands every currently established Generation VI visual state that matters to the battle-master source/target model.

## Counts

- National Dex species: **72** (`650–721` inclusive)
- logical visual-state records produced: **125**
- states requiring a Generation III battle target: **124**
- source/provenance-only visual states: **1** (`Xerneas — Neutral Mode`)
- ORAS-only states in this No.650–721 set: **2** (`Mega Diancie`, `Hoopa Unbound`)

## Expanded species/state counts

| Dex | Species | Generation VI logical states | Count |
| ---: | --- | --- | ---: |
| 666 | Vivillon | 20 wing patterns | 20 |
| 668 | Pyroar | male / female | 2 |
| 669 | Flabébé | Red / Yellow / Orange / Blue / White Flower | 5 |
| 670 | Floette | five normal flower colors + Eternal Flower | 6 |
| 671 | Florges | Red / Yellow / Orange / Blue / White Flower | 5 |
| 676 | Furfrou | Natural Form + nine trims | 10 |
| 678 | Meowstic | male / female | 2 |
| 681 | Aegislash | Shield Forme / Blade Forme | 2 |
| 710 | Pumpkaboo | Small / Average / Large / Super Size | 4 |
| 711 | Gourgeist | Small / Average / Large / Super Size | 4 |
| 716 | Xerneas | Neutral Mode / Active Mode | 2 |
| 718 | Zygarde | 50% Forme only in Generation VI | 1 |
| 719 | Diancie | Diancie / Mega Diancie | 2 |
| 720 | Hoopa | Hoopa Confined / Hoopa Unbound | 2 |

Every other species in `650–721` contributes exactly one Generation VI logical visual state in this stage.

## Battle-target distinction

Not every visual source state becomes a separate Generation III battle sprite.

### Xerneas

Generation VI has Neutral Mode and Active Mode. Xerneas appears in Active Mode in battles; Neutral Mode is an out-of-battle visual state. Therefore:

- `Neutral Mode` — retained for provenance/source reconstruction; `gen3_battle_target_required=no`
- `Active Mode` — canonical battle visual; `gen3_battle_target_required=yes`

### Aegislash

Shield Forme and Blade Forme both appear during battle and have distinct battle meaning. Both require independent logical targets.

## Special Generation VI data state

### Eternal Flower Floette

Eternal Flower Floette is retained because it exists in Generation VI game data, even though it was not legitimately obtainable during Generation VI. Its presence in the data is not rewritten as normal player availability.

## ORAS additions within No.650–721

### Mega Diancie

Mega Diancie was introduced in Omega Ruby and Alpha Sapphire. It is therefore represented as:

- XY: `not-in-XY`
- ORAS: `ORAS-only`

### Hoopa Unbound

Hoopa Unbound was introduced in Omega Ruby and Alpha Sapphire and is accessed through the Prison Bottle mechanic. It is represented as:

- XY: `not-in-XY`
- ORAS: `ORAS-only`

## Generation-bound naming

Pumpkaboo/Gourgeist use the Generation VI-era English size labels:

- Small Size
- Average Size
- Large Size
- Super Size

Later renaming in Pokémon Legends: Z-A is not backported into this Generation VI inventory.

## Archive mapping status

The logical state inventory deliberately does not pretend that semantic state identity and archive member identity are already the same table.

All generated rows currently start with:

`archive_mapping_status=unresolved`

The separate XY public member-range ledger provides reported mappings for many states, but promotion requires archive/member signature and loading-logic verification. ORAS exact species/form member ranges remain under reconstruction.

## Reproducibility invariant

The builder contains assertions for:

- exact species range `650–721`;
- exact output count `125`;
- exactly `124` battle-target rows;
- exactly one source-only row;
- Vivillon = 20 states;
- Floette = 6 states;
- Furfrou = 10 states;
- Aegislash = 2 states;
- Pumpkaboo = 4 states;
- Gourgeist = 4 states;
- Zygarde = Generation VI 50% Forme only;
- ORAS-only set = Mega Diancie + Hoopa Unbound.

Failure of any invariant aborts generation rather than silently producing a changed master inventory.
