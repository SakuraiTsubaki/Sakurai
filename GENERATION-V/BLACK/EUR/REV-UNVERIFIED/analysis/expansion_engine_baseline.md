# Generation V — Pokémon Black Expansion Engine Baseline

## Scope

This document records the current baseline for expanding Pokémon Black Version (EUR) on the Generation V engine.

The exact ROM revision has **not yet been verified from the NDS header / hashes**, so this workspace is intentionally labeled `REV-UNVERIFIED`.

Pokémon White Version (EUR) is tracked separately under its own GAME hierarchy and may be used for paired-version comparison.

## Current data targets

These counts are separate logical layers, not one Pokémon count:

- National Pokédex Species: **1025**
- PokéAPI Pokémon varieties: **1351**
- Pokémon Form records: **1579**

### Logical model

1. `Species` — National Pokédex species identity and species-wide metadata.
2. `Variety` — gameplay/battle variants with distinct parameters where applicable.
3. `Form` — appearance/form-level records, including forms that may share gameplay data.

## Future-generation requirement

The engine must **not** hard-code 1025 / 1351 / 1579 as permanent maxima.

Current architectural target:

- 16-bit Species identifiers
- 16-bit Variety identifiers
- 16-bit Form identifiers where the original structures can be safely migrated
- count-driven / appendable data tables wherever practical
- engine-only sentinel/special IDs separated from normal National Pokédex numbering

This is a **design target**, not yet a claim about the original ROM's confirmed field widths.

## Original ROM limit audit

Audit targets:

- Species ID storage width, masks and comparisons
- Form ID storage / packed form bits
- personal-data record count and lookup logic
- NARC member counts and index validation
- hard-coded 649 comparisons and loop bounds
- Pokédex indexing and seen/caught bitfields
- party / PC / save-data Pokémon structures
- evolution and learnset references
- encounter and trainer references
- sprite/model/icon/form references
- ARM9 and overlay validation/clamp routines
- existing post-649 internal/form records
- RAM/heap/overlay practical limits

Findings must be classified as:

1. **Data/table limits** — archive/table size only.
2. **Code limits** — constants, masks, loops, switches, validation logic.
3. **Save-format limits** — packed fields or fixed-size bitsets requiring migration.
4. **Practical runtime limits** — filesystem, memory, overlay and heap constraints.

## Verification status

### Confirmed project decisions

- Future generations must be addable without redesigning the entire ID namespace.
- Species / Variety / Form are handled as distinct layers.
- Commercial ROM images are never committed to GitHub.
- Safe analysis, tools, schemas, metadata and legally distributable patches may be committed.

### Not yet verified from the ROM

- Exact original Species ID field width across every subsystem.
- Exact Form field width across save/battle/UI subsystems.
- Exact usable post-649 personal/form slots.
- Every hard-coded 649/650-related ARM9 or overlay constant.
- Exact revision of the uploaded EUR Pokémon Black ROM.

## Repository policy

Canonical hierarchy:

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

This analysis belongs in `Sakurai`. Reusable patches, generated build assets and implementation resources belong in `Tsubaki`.

Original `.nds` files and other non-redistributable commercial binaries must never be committed.
