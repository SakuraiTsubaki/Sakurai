# Pokémon Green — HGSS Johto 256 Runtime v2

Date: 2026-09-05 (Asia/Seoul)

## Purpose

Turn the v1 HGSS Johto 256 registry from a passive data block into the first live runtime layer inside Pokémon Green, while keeping the original 151-species behavior byte/semantics compatible.

## Critical v1 correction: MBC1 -> MBC5

The v1 build expanded the ROM to 1 MiB while retaining cartridge type MBC1+RAM+BATTERY and placed new data in bank $21. Stock Green only writes an 8-bit value to the ROM-bank register at $2000. On MBC1, that write does **not** directly select bank $21 because the ROM-bank low register is only five bits and upper bank bits are controlled separately. Therefore v1's bank-$21 payload existed in the image but was not safely reachable through Green's stock bank-switch convention.

v2 fixes the architecture by migrating the cartridge header to **MBC5+RAM+BATTERY ($1B)**. For a 1 MiB image, MBC5 bank numbers $00-$3F fit entirely in the low 8-bit ROM-bank register at $2000, so Green's existing bank-switch convention can address the expansion banks directly. The existing RAM enable / RAM bank layout remains compatible with the intended four SRAM banks.

v1 should be treated as a structural prototype. v2 supersedes it for runtime work.

## Runtime architecture

- ROM size: 512 KiB -> 1 MiB
- Mapper: MBC1+RAM+BATTERY -> MBC5+RAM+BATTERY
- HGSS 256 registry: bank `$21`, file offset `0x084000`
- Runtime engine/data: bank `$22`, file offset `0x088000`
- Canonical species width: 16-bit, slots `0001..0100`
- HRAM staging:
  - `$FFF4`: canonical slot low byte
  - `$FFF5`: canonical slot high byte
  - `$FFF6`: species16-active flag
- Public bank-$22 routine `GetMonHeader16`: CPU `$40B6` in this build; input `BC = canonical HGSS slot`.

### GetMonHeader hook

The original Green base-header loader is the central gateway for stats, types, catch rate, growth rate, sprite metadata, initial moves, and TM/HM flags. It lives at:

- Rev 0: ROM0 `$2F2E`
- Rev A: ROM0 `$2F1C`

v2 replaces its entry with a 26-byte ROM0 wrapper that:

1. saves the old ROM bank and the original `BC/DE/HL` registers,
2. selects MBC5 bank `$22`,
3. calls the new runtime loader at `$4000`,
4. restores `HL/DE/BC`, the previous bank and flags,
5. returns with the same register/bank contract as the original routine.

## Legacy compatibility mirror

Bank `$22` contains a 191-record x 28-byte compatibility mirror indexed by Green internal species ID 0..190.

For all 150 normal Kanto Pokédex records, the mirror is copied directly from the original Green `BaseStats` table at file offset `0x38000`. Mew is copied from Green's separate Mew record at file offset `0x4200`. The runtime loader overwrites byte 0 with the internal species index exactly as original `GetMonHeader` did.

The three pseudo-species are handled as explicit partial-header cases to preserve Green behavior:

- `$B6` fossil Kabutops: dimension `$66`, front pointer `$64C7`
- `$B7` fossil Aerodactyl: dimension `$77`, front pointer `$6624`
- `$B8` Ghost: dimension `$66`, front pointer `$67AD`

Unused/invalid internal IDs are deliberately hardened to Rhydon rather than reproducing undefined out-of-range base-stat reads.

## Species16 behavior

When `$FFF6 == 0`, the loader follows the normal Green internal-ID path.

When `$FFF6 != 0`, `$FFF5:$FFF4` is interpreted as canonical HGSS slot 1..256:

- If the slot corresponds to one of the original 151 species, the slot-to-Green bridge loads the exact Green compatibility record.
- If the slot is one of the 105 species not present in Green, v2 loads a safe prototype header from the 256-record prototype table.

The 105 prototype records currently contain:

- real HGSS Johto roster identity/order,
- real pre-Fairy HGSS-era typing,
- Steel mapped to Green unused physical type ID `$09`,
- Dark mapped to new special-range type ID `$1B`,
- safe placeholder stats (`1/1/1/1/1` in the Gen-I header),
- Rhydon graphics metadata as a non-crashing graphics placeholder,
- placeholder catch/EXP/growth/moves/TM-HM fields.

These prototype personal fields are **not final HGSS personal data** and are intentionally marked pending rather than guessed.

## Verification

Both Rev 0 and Rev A pass all current static and instruction-level runtime tests:

- valid cartridge header checksum: PASS
- valid global checksum: PASS
- IPS -> output ROM byte-for-byte roundtrip: PASS
- unexpected changes inside original 512 KiB region: **0**
- normal legacy base headers: **151/151 exact**
- canonical species16 Kanto bridge: **151/151 exact**
- added HGSS slots reachable through species16 loader: **105/105**
- added slot type bytes match registry: **105/105**
- pseudo-species partial-header behavior: PASS

## Current status

Complete in v2:

- HGSS Johto 256 order / National mapping
- pre-Fairy typing
- MBC5 1 MiB runtime-addressable expansion
- live GetMonHeader bank hook
- exact 151-species Green compatibility path
- explicit 16-bit canonical species API
- all 256 canonical slots addressable by the runtime header loader

Still pending for full HGSS parameter behavior:

- exact HGSS personal data for the 105 added species
- HGSS evolution tables
- HGSS level-up learnsets
- Steel/Dark names and type-effectiveness table integration
- move database expansion / Gen-IV move parameters
- party/box/save canonical species16 storage migration
- wild/trainer species16 references
- Pokédex 256 seen/owned storage + UI
- names, sprites, cries, Pokédex entries and other assets for added species

## Source inputs

Base ROM binaries are not committed. The deterministic builder recognizes only these Green bases:

- Rev 0 SHA-1 `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196`
- Rev A SHA-1 `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`

The runtime work uses the exact Green disassembly semantics for `GetMonHeader`, `PokedexOrder`, the base-data structure and bank switching; HGSS personal/evolution/learnset data will be imported from the pret `pokeheartgold` data set rather than inferred from later-generation databases.
