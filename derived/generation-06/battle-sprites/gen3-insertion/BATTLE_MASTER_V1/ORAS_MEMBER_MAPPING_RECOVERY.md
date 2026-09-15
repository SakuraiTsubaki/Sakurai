# ORAS Pokémon model member-mapping recovery

## Status

**Exact ORAS species/form → `a/0/0/8` member numbers remain unresolved.**

The original public mapping project referenced by contemporary ORAS reverse-engineering discussion was:

`https://github.com/mradocy/pokemonModelList`

A Project Pokémon thread from 2015 links that repository directly. A later post dated 2024-11-10 reports that the repository has been deleted and asks whether a saved copy exists.

This project therefore does not fabricate an ORAS member-number table from memory or from a later game's index.

## Facts preserved from the contemporary ORAS research

Public discussion identifies:

- Pokémon model archive: `a/0/0/8`
- more than 8000 extracted members in the archive
- recurring Pokémon/form blocks of approximately eight members
- separate blocks for some alternate forms and gender differences

The reported recurring eight-member pattern is tracked separately in:

`source-ledgers/oras_member_pattern_public.csv`

The same discussion later identifies `.pb`, `.pf`, and `.pk` members as animation-related data, particularly material and visibility animation families. Exact subtype and role remain subject to per-container verification.

Primary surviving discussion:

https://projectpokemon.org/home/forums/topic/34387-listing-the-pokemon-models-extracted-from-oras/

## Why later model lists cannot be copied as ORAS indices

Complete Sun/Moon and Ultra Sun/Ultra Moon model lists are still publicly mirrored. They are valuable cross-check material because they enumerate many Generation VI visual states, but their archive structure is different.

For example, public USUM documentation describes **nine-member** blocks such as:

1. model
2. texture
3. shiny texture
4. grayscale texture
5. battle animations
6. Refresh animations
7. idle/walk/run animations
8. lip animations
9. empty/auxiliary

This is not the reported ORAS eight-member layout. Therefore USUM numerical member ranges must never be copied into the ORAS `a/0/0/8` mapping.

Secondary cross-check only:

https://www.gamebrew.org/wiki/Ultra_Sun_and_Ultra_Moon_Pokemon_Model_Data_and_Tools_3DS

## What the later list can safely cross-check

Without importing its member numbers, the later complete list supports the existence of separate visual/model states for many Generation VI assets, including:

- five regular Floette flower colors
- Eternal Flower Floette
- five Florges flower colors
- Furfrou Natural Form + nine trims
- male/female Meowstic
- Aegislash Shield / Blade
- all four Pumpkaboo sizes
- all four Gourgeist sizes
- Xerneas state data
- Diancie / Mega Diancie
- Hoopa Confined / Hoopa Unbound

These are semantic cross-checks only. The authoritative Generation VI logical-state definition remains generation-scoped and must be reconciled against XY/ORAS evidence separately.

## Additional preserved visual evidence

The archived Pokémon Model Ripping Project lists Generation VI assets including:

- all 20 Vivillon patterns
- five Flabébé flower colors
- five regular Floette flower colors
- AZ's / Eternal Flower Floette
- five Florges flower colors
- ten Furfrou states
- Aegislash Blade / Shield
- four Pumpkaboo sizes
- four Gourgeist sizes
- Xerneas Neutral / Active
- Hoopa Confined / Unbound

This is useful evidence that preservation communities successfully extracted/rendered these distinct Generation VI visual states, but it is not an ORAS member-number table.

Reference:

https://archive.vg-resource.com/post-603626.html

## Recovery strategy

Exact ORAS mapping is recovered only through one or more of the following evidence classes:

1. surviving fork/archive/cache of the deleted `pokemonModelList` repository;
2. preserved text or CSV copied from that repository with provenance;
3. source code/tool database that maps ORAS species/form IDs to archive offsets;
4. independently documented ORAS member ranges from a second preservation project;
5. direct inspection of lawful `a/0/0/8` extracted members if such source data becomes available later.

## Required validation before promotion

An ORAS row cannot be promoted to `confirmed-game-data` solely because an eight-member arithmetic pattern looks plausible.

For every recovered block, verify where possible:

- member start/end
- member count
- file/container signatures
- model geometry member
- normal texture member
- shiny texture member
- animation/material/visibility members
- species/form identity
- gender identity where applicable
- consistency with adjacent blocks
- independent supporting source

## Prohibited shortcut

Do not derive ORAS member numbers by:

- copying XY member numbers;
- copying Sun/Moon or USUM member numbers;
- multiplying a Pokédex/form index by eight without evidence;
- assuming all forms use exactly eight members;
- assuming visually identical X/Y and ORAS resources are byte-identical.

Unknown member numbers remain explicitly unresolved until recoverable evidence exists.
