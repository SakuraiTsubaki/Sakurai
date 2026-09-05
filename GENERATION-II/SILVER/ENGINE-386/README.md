# SILVER ENGINE-386

Goal: make Pokemon Silver run National Dex species #001-#386 plus all game-recognized forms that exist by Generation III, before adding Generation IV species.

## Runtime identity

- `species_id`: canonical unsigned 16-bit National Dex ID (`1..386`).
- `form_id`: unsigned 8-bit form selector, independent from species ID.
- Vanilla one-byte Silver species IDs are treated as transport/runtime slots only; they are not canonical species identities.
- `$FD` Egg and high sentinel semantics remain reserved. They are not reassigned to real Pokemon.

## Generation III form baseline

The initial form registry contains 36 form records across three species:

- Unown (#201): 28 forms — A..Z, Exclamation, Question.
- Castform (#351): 4 forms — Normal, Sunny, Rainy, Snowy.
- Deoxys (#386): 4 forms — Normal, Attack, Defense, Speed.

Spinda spot patterns are not assigned separate `form_id` values; they are personality-derived visual variation rather than discrete form identities in the target registry.

## Data architecture

`canonical species_id + form_id`
→ species/form lookup
→ base-parameter record + optional form override
→ compact one-byte runtime slot when an old Silver structure requires one

The compact slot layer must preserve Egg/sentinel meanings and must never expose canonical IDs >255 directly to legacy one-byte fields.

## Engine work order

1. Build canonical 001-386 species registry and form registry.
2. Port a 16-bit species-ID translation layer using `pokecrystal16` only as an architectural reference.
3. Route BaseData/name/cry/pic/palette/evolution/learnset lookup through canonical IDs.
4. Route party/box/daycare/battle/wild/trainer/static/gift/trade species storage through the conversion layer.
5. Add persistent `form_id` storage where forms must survive outside battle.
6. Implement Unown, Castform and Deoxys form rules.
7. Expand Pokédex seen/caught/form tracking to 386 species.
8. Update save/checksum/link boundaries and regression-test vanilla 1-251 behavior.
9. Port the engine to all eight Silver ROM revisions/languages.

## Current status

- Existing Generation III parameter layer for #252-#386 is staged in ROM data banks, but the vanilla engine does not yet consume it.
- ENGINE-386 starts the executable routing work. Do not describe the project as 386-playable until the runtime tests pass.
