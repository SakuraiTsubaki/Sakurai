# Pokémon Yellow original ROM limit audit

Baseline: uploaded USA/Europe Pokémon Yellow ROM SHA-1 `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1`, cross-checked against `pret/pokeyellow`.

## Cartridge / memory

- USA/Europe and European localizations: 1 MiB ROM, header ROM size `$05` = 64 x 16 KiB banks; cartridge type `$1B` = MBC5+RAM+BATTERY; RAM size `$03` = 32 KiB (4 x 8 KiB banks).
- Japanese Pikachu revisions: 1 MiB ROM, cartridge type `$13` = MBC3+RAM+BATTERY; RAM size `$03` = 32 KiB.
- International ROM has CGB compatibility flag `$80`; Japanese revisions checked use `$00` and SGB flag `$03`.
- Standard MBC3 hardware ceiling: 2 MiB ROM / 32 KiB SRAM.
- Standard MBC5 hardware ceiling: 8 MiB ROM / 128 KiB SRAM.
- Stock Yellow ROM bank state is one byte and the bank switch routine writes only the low MBC5 bank register, so the stock software model only reaches 256 bank numbers (4 MiB) even though MBC5 hardware can reach 512 banks (8 MiB). A 9-bit/extended bank layer is required for the full MBC5 ROM range.

## Raw ROM observations

USA/Europe ROM:
- BaseStats begins at file offset `0x383DE`.
- Records 1 and 2 are exactly 28 bytes apart; 151 records end at `0x39462`.
- Bank `$3B` is entirely zero-filled in the raw ROM and is a clear 16 KiB empty bank.
- A raw scan finds about 170.6 KiB of trailing zero padding across bank ends. This is only an apparent-padding figure; reuse must be checked against section/layout semantics.

Other raw scans:
- Japanese Rev D contains wholly zero banks `$26`, `$27`, `$2A-$2F`.
- Japanese Rev 0A/B/C have no wholly zero 16 KiB banks.
- European versions have no wholly zero bank in the raw image, although they contain substantial end-of-bank padding.

## Species / Pokédex identity limits

- National Pokédex constants: 151 (`NUM_POKEMON`).
- Internal Pokémon index table: 190 (`$01-$BE`, `NUM_POKEMON_INDEXES`).
- Species/dex working variables such as `wCurPartySpecies` and `wPokedexNum` are one byte.
- `wPokedexOwned` / `wPokedexSeen` are flag arrays sized for 151 species (19 bytes each).
- Name lookup treats values `$C4` and above as TM/HM identifiers, so the stock shared-name/index design has a practical collision before the full 8-bit range.
- A 1025-species registry therefore requires a new identity layer (recommended: 16-bit Species ID; separate 16-bit Variety and Form IDs).

## Base Pokémon data

Stock BaseStats is 28 bytes per species and stores:
- one-byte dex number
- five base stats: HP / Attack / Defense / Speed / Special
- two one-byte types
- one-byte catch rate
- one-byte base EXP
- sprite dimensions and two 16-bit sprite pointers
- four starting moves
- one growth-rate byte
- TM/HM bitfield

Consequences:
- modern Sp. Atk and Sp. Def cannot both be represented by the stock five-stat engine;
- modern base EXP values above 255 require an expanded field if exact values are preserved;
- types themselves still fit in one-byte fields, but Dark/Steel/Fairy and their matchups are absent from the engine;
- abilities, gender, egg groups, generic per-mon friendship, nature, held item and explicit form/variety identity are not native fields.

## Moves / evolutions

- Stock Yellow has 165 moves (`$01-$A5`) and move IDs are one byte.
- The same `$C4` name-routing boundary also constrains the stock name system for moves.
- Full modern learnsets therefore require a redesigned move ID/name/data system (recommended: 16-bit Move ID).
- Evolution engine defines Level / Item / Trade and uses a 3-entry evolution buffer. Modern branching/conditions require a variable evolution list and additional condition opcodes.
- Active moves remain four; four-move battle slots are not themselves a blocker.

## Names / graphics

- `NAME_LENGTH = 11`, i.e. fixed 10-character visible names plus terminator in the normal fixed-name layout. Modern species/form names exceed this.
- Pokémon battle picture canvas is fixed at `PIC_WIDTH = 7` tiles = 56x56 pixels.
- `SPRITEBUFFERSIZE` is 7x7 1bpp tiles = 392 bytes; three sprite buffers live in SRAM bank 0.
- Gen-IV-style 80x80 art requires a 10x10 sprite path plus battle-layout/decompression changes. The buffer enlargement itself is possible with careful SRAM layout, but the engine is hard-coded around 7x7 in many places.

## Save / PC limits

- Party: 6.
- Box: 20 Pokémon.
- Number of boxes: 12.
- Total stock PC storage: 240 Pokémon.
- Boxed-mon struct: 33 bytes; party-mon struct: 44 bytes.
- Full box block: `$462` = 1122 bytes including species list, 20 boxed-mon structs, OT names and nicknames.
- Six boxes occupy each of SRAM banks 2 and 3.

A 1025-species National Dex cannot be represented as a one-of-each living collection in the stock 240-slot PC. Merely widening identity fields can be fitted with a save redesign, but increasing living storage toward 1025+ is an SRAM-capacity problem. For a unified long-term engine, migrate all language builds to an MBC5-style 128 KiB SRAM layout or use a non-stock mapper/save model.

## Recommended ceiling strategy

1. Migrate Japanese builds from MBC3 to the same MBC5 abstraction as international builds before heavy asset growth.
2. Upgrade ROM bank identity to at least 9 bits (prefer a 16-bit bank field in software) so all 8 MiB MBC5 ROM is addressable.
3. Use 16-bit Species / Variety / Form / Move IDs and versioned registries with counts, never fixed 1025/1351/1579 maxima.
4. Keep core Gen-I-compatible battle fields separate from extended modern metadata.
5. Redesign save/PC layout independently; 32 KiB SRAM is adequate for a modest expanded identity layer but not for a living National Dex of 1025+ Pokémon.
6. Treat 8 MiB ROM / 128 KiB SRAM as the standard-MBC5 hardware ceiling. Anything beyond that requires compression/content paging or a non-standard mapper/emulator target.
