# Pokémon Green — G386F3 GetMonHeader Hook v1

This gate is the first point where the original Green engine **actively consumes** the cumulative Generation II/III parameter layer.

## Runtime flow

1. Original `GetMonHeader` runs unchanged, preserving every legacy edge case.
2. Its final `ld [rROMB], a / ret` is replaced by `jp $0008`.
3. `$0008-$0024` is a fixed-bank trampoline placed in RST-vector space that the disassembly explicitly marks unused.
4. The trampoline switches to bank `$21` and calls `$5300` to translate Green's legacy 8-bit internal species ID to canonical `u16` National Dex ID.
5. It returns to ROM0, switches to bank `$20`, and calls `$4080` inside the reserved G386F3 header code slot.
6. The bank `$20` helper reads the canonical Generation III personal record and overlays the safe Generation I-compatible fields.
7. `BankswitchBack` restores the original bank and the caller resumes normally.

## Active fields

- Base HP
- Base Attack
- Base Defense
- Base Speed
- Catch rate
- Base EXP
- Growth rate

The original Green **Special**, types, sprite pointers, level-1 moves and TM/HM bits remain intact at this gate.

### Why Special is not changed yet

Generation I has one Special stat; Generation III has Sp. Atk and Sp. Def. Averaging, choosing one side, or inventing a projection without a project rule would silently change balance.

### Why types are not changed yet

The Gen3 layer already knows Steel and Dark, but stock Green does not. Magnemite/Magneton's later Steel typing cannot be enabled safely until the type constants, effectiveness chart, names, battle routines and UI are expanded together.

## First observable inherited change

Raticate (#020, legacy Green internal ID `$A6`) changes **catch rate 90 → 127**, matching the Generation III overlay. Of the National Dex #001-150 records stored contiguously in Green's base-stats table, this is the only field difference in the currently activated safe subset.

## Verification

- legacy ID helper: all 256 input values machine-code-emulated — PASS
- canonical Kanto overlay helper: all 151 species machine-code-emulated — PASS
- invalid canonical IDs: no-op — PASS
- Rev0 header/global checksums — PASS
- RevA header/global checksums — PASS
- cumulative IPS round-trip, Rev0/RevA — PASS
- Game Boy boot test — not run; no emulator is available in this execution environment

This is **not yet** a claim that species #152-386 can occupy party/box/battle records. The next gate is the widened `u16 species_id + u8 form_id` working-record path.
