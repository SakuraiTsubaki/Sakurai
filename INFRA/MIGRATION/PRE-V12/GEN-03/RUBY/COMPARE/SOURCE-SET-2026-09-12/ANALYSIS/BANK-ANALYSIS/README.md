# Pokémon Ruby — 64 KiB Bank Survey

This directory documents a full fixed-block survey of the 13 locally supplied Pokémon Ruby GBA ROM builds. ROM binaries are intentionally excluded.

## Analysis unit

The GBA ROM is flat memory-mapped rather than GB/GBC-style bank-switched. For comparative analysis, one logical **bank** is defined here as `0x10000` bytes (64 KiB). File offset `x` maps to GBA ROM address `0x08000000 + x`.

## Builds covered

- AXVJ v0 — Japan
- AXVE v0 — USA
- AXVE v1 — Europe
- AXVE v2 — USA/Europe
- AXVD v0/v1 — Germany retail
- AXVD v0 — Germany debug
- AXVF v0/v1 — France
- AXVI v0/v1 — Italy
- AXVS v0/v1 — Spain

Total surveyed logical-bank records: **3,200**.

## High-level physical map

### Japan (8 MiB)

- `00–65`: core ROM content (code/scripts/rodata/audio/mixed; finer symbol-level labeling pending)
- `66`: fill gap
- `67`: partial graphics-start bank; payload starts at file offset `0x0067D000`
- `68–7F`: graphics payload through end of ROM

### International retail (16 MiB)

- `00–6A`: core ROM content
- `6B`: partial core-tail bank; last non-FF byte `0x006B1FC7`
- `6C–CF`: intentional FF gap
- `D0–...`: graphics payload at fixed ROM address `0x08D00000`
- English builds: graphics tail is in `EA`; `EB–FF` trailing fill
- German/French/Italian/Spanish builds: graphics continues into `EB`; `EC–FF` trailing fill

### German debug (16 MiB)

- `00–6C`: debug core
- `6D`: partial debug-core tail; last non-FF byte `0x006DF84F`
- `6E–CF`: FF gap
- `D0–EB`: graphics region/tail
- `EC–FF`: trailing fill

The public `pret/pokeruby` linker layout independently corroborates the international graphics boundary by explicitly setting `. = 0x8D00000` before `gfx_data` / `src/data/graphics.o(.rodata)`.

## Revision/build-difference findings

- Spain v0→v1: 4 changed bytes, bank `00` only.
- Italy v0→v1: 4 changed bytes, bank `00` only.
- France v0→v1: 4 changed bytes, bank `00` only.
- Germany retail v0→v1: 4 changed bytes, bank `00` only.
- English Europe v1→USA/Europe v2: 4 changed bytes, bank `00` only.
- English USA v0→Europe v1: 5,744,535 changed bytes in 109 banks; changed-bank set is `00–6B` plus `EA`.
- Germany retail v0→debug v0: 6,751,723 changed bytes in 110 banks; changed-bank set is `00–6D`.

## Japan ↔ international graphics relocation

The first nontrivial 48-byte sequence at international file offset `0x00D00000` occurs exactly at Japanese offset `0x0067D000`. Fixed 8-byte chunk comparison also maps Japanese banks `67–7F` strongly onto international graphics banks `D0–E8`, supporting that these are corresponding logical graphics payloads relocated/expanded between builds.

## Raw-survey fields

For each ROM/bank the local master records: SHA-1, entropy, FF/00 ratios, non-fill count, longest fill runs, aligned GBA-ROM-pointer candidates, printable ASCII density, long ASCII strings, LZ10-header candidates, and a deliberately heuristic binary-content class. Heuristic labels must not be treated as exact semantic section names.

## Next pass

The next layer is symbol/asset-level attribution inside the core range (`00–6B`, or `00–6D` for debug): code, scripts, text, tables, audio, maps, graphics references, pointer ownership, and per-language relocation boundaries.
