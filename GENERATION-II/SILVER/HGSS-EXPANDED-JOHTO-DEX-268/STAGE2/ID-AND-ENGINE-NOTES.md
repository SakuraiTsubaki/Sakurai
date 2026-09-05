# Species / Item ID audit and engine-routing notes

## Species raw-ID audit

Vanilla Gold/Silver species constants are contiguous only through Celebi (`0xFB`). The next values have engine meanings that make a naive 252–256 raw-ID extension invalid:

- `0xFC`: constant intentionally skipped; Pokémon name table supplies a `?????` placeholder.
- `0xFD`: `EGG`.
- `0xFE`: no Pokémon species constant.
- `0xFF`: used as a species-list terminator/sentinel (including party/evolution traversal).

Accordingly, Stage 2 treats `252..268` only as 16-bit logical IDs. It does **not** repurpose `0xFC`, `0xFD`, `0xFE`, or `0xFF` as persistent raw species IDs.

Reference architecture: the `expand-mon-ID` work in `pokecrystal16` reserves high 8-bit values (minimum reserved index `0xFD`) and translates between compact 8-bit storage indices and 16-bit logical IDs. Silver needs an equivalent port, not a direct Crystal-content copy.

## Item raw-ID audit

The selected eight item slots are explicit `ITEM_xx` placeholders in vanilla Gold/Silver. Their vanilla attributes are dummy/no-use and their item-effect table entries are `NoEffect`. This makes them suitable for reassignment while preserving one-byte item storage.

Reserved mapping:

- `0x93` Shiny Stone
- `0x94` Dusk Stone
- `0x95` Razor Claw
- `0x99` Protector
- `0x9A` Electirizer
- `0x9B` Magmarizer
- `0xA2` Razor Fang
- `0xAB` Dubious Disc

The item names, attributes, give/take behavior, held-item checks, trade evolution checks, and stone-use handler still need engine/UI hookup.

## Required 16-bit species routing

The next stage must route at least:

1. party species lists and party-mon structs
2. box species lists and box-mon structs
3. save/load and conversion-table persistence
4. temporary battle species variables
5. base-data lookup
6. names / named-object lookup
7. evolutions and level-up learnsets
8. wild encounters and fishing/tree encounter tables
9. trainer parties and scripted battles
10. daycare / breeding / egg generation
11. trades, gifts, Bug-Catching Contest and special events
12. Pokédex order, seen/caught flags, count logic and display
13. sprites, palettes, menu icons and cries
14. Hall of Fame
15. link / Time Capsule compatibility gates

## New evolution engine methods

Stage 2 defines metadata for methods absent from vanilla G/S:

- `EV_MOVE_KNOWN`
- `EV_HELD_ITEM_TIME`
- `EV_LOCATION_LEVEL`

Vanilla `EVOLVE_ITEM` and `EVOLVE_TRADE` behavior can be extended for the newly reserved items.

## Move system

Double Hit is required for Aipom → Ambipom. Stage 2 deliberately assigns only logical move ID 252. The raw move ID must not be chosen until the Gen-II move-ID/sentinel audit is complete, mirroring the species-ID discipline established after the Stage-1 correction.
