# GREEN modern parameter migration — Phase 1

## Confirmed ROM structure

- Pocket Monsters Green JP Rev 0 and Rev A are both 512 KiB.
- Pokémon base-stat records 001–150 start at `0x38000`.
- Record size is 28 bytes.
- Mew (#151) is stored separately at `0x04200`.
- The 001–150 base-stat table is byte-identical between Rev 0 and Rev A.

## Modern-value migration started

The first pass records every Generation I species whose ordinary-form base stats were explicitly buffed after Generation V. There are **20** such Generation I species: 14 changed in Generation VI and 6 changed in Generation VII. No ordinary Generation I species received a later Generation VIII/IX inter-generation base-stat adjustment.

The data model does **not** overwrite the read-only source ROM. It preserves the Green value and records the current value separately. Generation I's single `Special` field is treated as source history; the implementation model will use separate `Sp. Atk` and `Sp. Def`.

## Type changes seeded

Seven original Kanto species have a modern type differing from their Green type: Clefairy, Clefable, Jigglypuff, Wigglytuff, Magnemite, Magneton, and Mr. Mime.

## Next parameter families

Continue the same ledger for abilities/hidden abilities, catch rate and base experience changes, growth/EV/friendship/egg metadata, evolution methods, move parameters, learnsets/TM compatibility, held-item data, and battle-rule changes.
