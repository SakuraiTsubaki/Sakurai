# Green runtime target: National Dex #001-386 + Generation III forms

This directory defines the first **playable runtime milestone** for the cumulative Green expansion.

## Completion target

The milestone is not complete merely because parameter tables exist in ROM. It is complete only when species #001-386 can safely pass through the normal game lifecycle:

- party creation / addition / removal
- wild encounters
- trainer parties
- battle setup and species data lookup
- EXP gain and level-up
- evolution
- move learning
- PC box deposit / withdrawal
- save / load
- Pokédex seen / owned tracking
- sprite / cry / palette lookup
- trading/link-facing serialization policy
- form creation, persistence or battle-only transformation as appropriate

## Identity ABI

Long-term identity is split into two fields:

- `species_id`: unsigned 16-bit canonical species identifier. For the first milestone this is National Dex #001-386.
- `form_id`: unsigned 8-bit form identifier local to that species. `0` is the default/base form.

This avoids consuming species IDs for forms and prevents later generations from forcing another identity redesign.

The original Green one-byte species index remains a legacy compatibility/index layer only. New long-lived party/box/save/runtime records must not treat it as the canonical identity.

## Generation III form scope

At the end of Generation III the runtime must represent the following form families:

- Unown (#201): 28 forms, A-Z plus `!` and `?`. Generation III form selection is personality-derived; the expanded engine also exposes a resolved `form_id` so rendering and later-generation migration do not depend on re-deriving it everywhere.
- Castform (#351): Normal, Sunny, Rainy, Snowy. Alternate forms are battle/contest state driven by weather and Forecast and revert outside battle.
- Deoxys (#386): Normal, Attack, Defense, Speed. All four forms are supported in one Green build. They share species #386 but have form-specific personal/learnset data where Generation III differs.
- Spinda (#327): spot appearance remains personality-pattern data, not a discrete form slot.

Counting the default form already represented by each species, #001-386 plus the 33 additional alternate form states gives **419 species-form combinations** in this milestone.

## Parameter stack order

1. Original Green / Generation I compatibility layer
2. Crystal-derived Generation II overlay for **all #001-251**, not merely the 100 newly introduced species
3. Emerald / other Generation III source overlay for #001-386
4. Generation III form override table
5. Later generations append new overlays and forms without changing the identity ABI

## Runtime migration order

1. Mapper/ROM expansion and deterministic parameter placement
2. Canonical `species_id + form_id` loader ABI
3. party/battle working records
4. box/save migration
5. species personal-data lookup
6. evolution / level-up / move lookup
7. wild + trainer encodings
8. Pokédex bitsets and regional-dex views
9. sprite/cry/palette lookup
10. Unown / Castform / Deoxys form rules
11. regression tests on both Green Rev0 and RevA

The original ROM binaries are never committed. Scripts, ledgers, reports, patches and other non-ROM outputs are committed as work proceeds.
