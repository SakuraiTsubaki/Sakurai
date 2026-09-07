# Pokémon Silver National Dex Expansion

Generation II / Pokémon Silver engine expansion research and tooling.

## Current target model

- National Dex Species: **1025** current entries
- PokéAPI Pokémon / battle varieties: **1351** current entries
- PokéAPI Pokémon Form records: **1579** current entries
- Future generations: **append-only**; current counts are data counts, not engine maxima

## Current architecture decision

The project is moving away from the early `251 slots per page` prototype and toward a direct extended-ID model:

- `SPECIES_ID`: `u16`, `0x0001..`, National-Dex identity, append-only
- `VARIANT_ID`: `u16`, independent battle-data identity, append-only
- `FORM_ID`: separate form layer; local form IDs may stay compact where safe
- `EGG`: not allocated from `SPECIES_*`; represented as a state/sentinel outside the species namespace
- `0x0000`: `NONE`
- `0xffff`: reserved invalid/sentinel value

Once an ID is assigned, it must not be renumbered. Generation 10+ additions append after the last assigned ID.

## Repository policy

Commercial ROM images, modified ROM images, save files, and redistributable copyrighted binaries are **not committed**. This repository stores reverse-engineering notes, source code, scripts, hashes/manifests, and patch-generation tooling only.

## Status

See:

- `docs/original-rom-engine-limits-2026-09-07.md`
- `docs/id-architecture.md`
- `archive/core-v0.2-page-model/` for the superseded prototype
