# Pokémon Silver Original ROM / Engine Limits

Date: 2026-09-07
Scope: supplied Japanese, Japanese Rev A, English, German, French, Italian, Spanish, and Korean Pokémon Silver ROMs, cross-checked against `pret/pokegold` source structure.

## Target data model

- National Dex Species: 1025 current
- Battle varieties: 1351 current
- Pokémon Form records: 1579 current
- Generation 10+: append-only; current counts must not become compile-time engine ceilings

## ROM / mapper limits observed

All supplied Silver ROMs use cartridge type `0x10`: MBC3 + timer/RTC + RAM + battery.

- Japanese / Japanese Rev A ROMs: 1 MiB, 64 banks
- English / German / French / Italian / Spanish / Korean ROMs: 2 MiB, 128 banks
- SRAM header size: 32 KiB

With the original MBC3 design retained, 2 MiB / 128 ROM banks is the practical ROM ceiling. The Japanese builds can be expanded from 1 MiB to 2 MiB without changing the mapper; the supplied international/Korean builds are already at that ceiling.

Among the six supplied native 2 MiB builds, 20 banks are all-zero in common (327,680 bytes / 320 KiB). If the two Japanese 1 MiB builds are included after zero-padding them to 2 MiB, the common all-zero set is 11 banks (180,224 bytes / 176 KiB): `63 67 6F 73 74 75 76 77 7C 7D 7E`.

This is enough for substantial parameter tables, but not for an all-generation full sprite/form asset set.

## First engine wall: 8-bit Species

Original runtime and stored-mon paths use one-byte species values. Examples in `pret/pokegold` include:

```asm
wCurSpecies:: db
```

and BoxMon:

```asm
DEF MON_SPECIES rb
```

Original Pokémon constants occupy `0x01..0xfb` for 251 Pokémon, skip `0xfc`, and use `0xfd` for Egg. Wild encounter logic also explicitly rejects values at `NUM_POKEMON + 1`.

Therefore the unmodified engine's effective Pokémon species limit is **251**, not 255.

## Required fix: extended identity

The project target is direct extended identity rather than preserving the original special-value layout:

```text
SPECIES_ID : u16
VARIANT_ID : u16
EGG        : outside normal SPECIES_* allocation
```

All 8-bit copies, comparisons, lists, and lookup indices must be audited. Widening only the BaseData lookup is insufficient.

## BoxMon structure opportunity

The Generation II BoxMon structure is 32 bytes and contains two unused bytes after Pokerus in the disassembly. Reusing compatible unused space may allow extended species/form metadata without increasing the 32-byte BoxMon size.

This matters because PC storage is already tightly packed into SRAM.

International layout:

- 20 Pokémon per box
- 14 boxes
- 280 PC Pokémon capacity

The source explicitly splits the boxes across SRAM sections because all boxes do not fit in one SRAM bank.

## BaseData

Original BaseData is 32 bytes per species. The original `GetBaseData` assumes one bank and an 8-bit species index.

Approximate raw BaseData size if generalized:

| Records | Bytes | Approx. KiB |
|---:|---:|---:|
| 251 | 8,032 | 7.8 |
| 1,025 | 32,800 | 32.0 |
| 1,351 | 43,232 | 42.2 |
| 1,579 | 50,528 | 49.3 |
| 4,096 | 131,072 | 128.0 |

The data itself is not the main limit. The loader must become bank-aware and ID-wide.

## Pokédex

Original seen/caught storage is a bit array sized to `NUM_POKEMON`.

- 251 species: 32 bytes each for Seen and Caught
- 1025 species: 129 bytes each
- 4096-capacity bitset: 512 bytes each

The bitmaps are small. The real problem is their placement inside fixed WRAM/save layouts and all UI/counting routines that assume the original count.

## Moves / items are separate 8-bit walls

A full modern-species project can keep Gen II move semantics and avoid widening move IDs initially. If every modern move/item is eventually imported, the original one-byte IDs become another major structural rewrite.

Stored Pokémon have four one-byte move fields. Therefore a complete modern move database cannot be represented by the original BoxMon move fields without an additional encoding or wider structure.

## Fixed-width names

The international source defines fixed lengths including:

```text
MON_NAME_LENGTH           = 11
MOVE_NAME_LENGTH          = 13
ITEM_NAME_LENGTH          = 13
TRAINER_CLASS_NAME_LENGTH = 13
```

Long modern official names therefore require either controlled abbreviations per language or a pointer/variable-length rendering redesign.

## Graphics become the ROM-space wall

Parameter tables for ~1351 battle variants are relatively small. Full graphics are not.

A raw 7x7 2bpp front sprite is 49 tiles x 16 bytes = 784 bytes before compression. 1351 such front sprites alone are about 1 MiB, before back sprites, animation frames, bitmasks, palettes, menu icons, shiny/gender/form variants, or the rest of the game.

Therefore MBC3's 2 MiB ROM ceiling is likely to become the final hard limit once the project moves from parameter expansion to comprehensive 1579-form graphics.

## Limit summary

| Area | Original | Expansion direction |
|---|---:|---|
| Species ID | 251 effective | u16 append-only |
| Battle variety | no general namespace | new u16 namespace |
| Form | mostly special-case | general form mapping |
| BaseData | 251 x 32, one-bank lookup | multi-bank table |
| Pokédex | 251-bit-era arrays | relocated/resized bitsets |
| BoxMon | 32 bytes | preserve size if possible using unused bytes |
| Move ID | u8 | keep Gen II moves initially or redesign later |
| Item ID | u8 | same issue as moves |
| ROM | MBC3 2 MiB | hard ceiling unless mapper architecture changes |
| SRAM | 32 KiB | preserve compact save structures |

## Current conclusion

The first obstacle is **not raw free ROM space**. It is the pervasive one-byte species identity model.

The correct order is:

1. define stable 16-bit Species/Variant IDs and remove Egg from the species namespace;
2. patch every storage/runtime path that truncates species identity;
3. generalize BaseData/name/dex/form lookup tables;
4. keep the original 32-byte BoxMon structure where safe;
5. measure graphics compression against remaining MBC3 ROM space;
6. only then decide whether a mapper/RTC architecture change is required.

## Upload policy

No original or modified commercial ROM images are committed. ROM hashes, analysis, code, scripts, metadata, and patch-generation material are allowed.
