# Pokémon Red ROM set — structural overview

## Scope

- Input `.gb` files found: **8** recognized files
- Unique recognized ROM images: **7**
- Exact duplicate groups: **1**
- Unique regions/revisions: DE/REV-0, USA-EUROPE/REV-0, ES/REV-0, FR/REV-0, IT/REV-0, JP/REV-0, JP/REV-A

## Cartridge families

- MBC1+RAM+BATTERY: 2 ROM(s)
- MBC3+RAM+BATTERY: 1 ROM(s)
- MBC5+RAM+BATTERY: 4 ROM(s)

## Japanese revision delta

JP Rev 0 vs Rev A differs in **46167 bytes**, across **31 banks**, represented by **5437 contiguous differing ranges**.

## Reproducibility boundary

This analysis stores addresses, hashes, statistics, and difference ranges but no replacement byte values. It documents and verifies the ROM set without embedding original ROM data.

## Next semantic layers

Structural reproducibility is complete at file/header/bank/difference level. Add semantic layers separately: control-flow/code map, pointer map, text map, graphics map, species/move/item tables, maps/events, save structure, and expansion constraints.
