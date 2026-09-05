# Pokémon Green — HGSS Johto Pokédex 256 parameter layer

Build date: 2026-09-05 (Asia/Seoul)

## What is installed now

This pass physically expands both supplied Pokémon Green ROM revisions from 512 KiB (32 × 16 KiB banks) to 1 MiB (64 banks) while retaining cartridge type `0x03` (MBC1+RAM+BATTERY).

A self-describing `HGJD256` parameter block is installed in MBC1-selectable ROM bank `0x21`, file offset `0x084000`. Bank `0x20` is deliberately left unused because MBC1 cannot select it normally in the switchable `0x4000-0x7FFF` window when the lower five bank bits are zero.

The block contains:

- exact HGSS Johto regional Pokédex roster/order: 256 unique slots;
- regional slot -> National Dex mapping;
- HGSS-era (pre-Fairy) primary/secondary type pair for every slot;
- 2-byte canonical species-ID target width;
- 32-byte seen/owned bitset target size for 256 entries;
- Green legacy internal-ID -> HGSS canonical-slot bridge (190 internal indexes, 151 real Kanto species + MissingNo holes);
- HGSS canonical-slot -> Green legacy internal-ID reverse bridge;
- developer-facing ASCII identifiers;
- completion flag: 254 required, Mew and Celebi optional;
- reserved per-species fields for exact HGSS personal/base-stat, evolution and level-up-learnset tables.

The five Generation IV additions occur at the HGSS slots:

| Johto slot | National Dex | Pokémon |
|---:|---:|---|
| 102 | 469 | Yanmega |
| 124 | 424 | Ambipom |
| 181 | 463 | Lickilicky |
| 183 | 465 | Tangrowth |
| 197 | 473 | Mamoswine |

## Parameter block format v1

Block start: `0x084000` (bank `0x21`)

Header size: `0x60` bytes. Per-species record: `0x10` bytes.

Each species record is little-endian:

```
u16 canonical_johto_id
u16 national_dex
u8  type1
u8  type2
u8  legacy_green_internal_id   # 0 if not present in vanilla Green
u8  flags
u16 developer_name_offset
u16 hgss_personal_offset       # 0xFFFF in this pass
u16 hgss_evolution_offset      # 0xFFFF in this pass
u16 hgss_learnset_offset       # 0xFFFF in this pass
```

Type enum stored by this layer:

`NORMAL=0, FIGHTING=1, FLYING=2, POISON=3, GROUND=4, ROCK=5, BUG=6, GHOST=7, STEEL=8, FIRE=9, WATER=10, GRASS=11, ELECTRIC=12, PSYCHIC=13, ICE=14, DRAGON=15, DARK=16`.

Feature flags in the header are currently `0x0007`:

- bit 0: 256-slot HGSS roster/order populated;
- bit 1: HGSS-era type pairs populated;
- bit 2: Green legacy bridge populated;
- bits 3-5: personal/base stats, evolution, learnset runtime payloads not yet populated.

## Why the canonical species ID is 16-bit

Green uses `0x00` as a null/terminator in many species-bearing structures. There are only 255 non-zero values in one byte, but the HGSS Johto Dex has 256 real species. Reusing `0x00` for Celebi (or any other species) would collide with null semantics in party/trainer/wild/save/battle paths. The expansion therefore reserves a clean 16-bit canonical species identity instead of creating a hidden sentinel collision.

## What is *not* hooked yet

This pass is the structural/data-layer milestone. Vanilla gameplay code still uses the original 8-bit Green species paths. The newly installed 256-species registry is therefore not yet exposed in normal gameplay.

Still pending for the runtime conversion:

1. 16-bit species accessors and bank-switch helper for bank `0x21+`;
2. party/box/save format expansion and save migration;
3. Pokédex seen/owned storage expansion from 151 bits to 256 bits;
4. Pokédex UI/list/index conversion hooks;
5. exact HGSS `personal` data import (base stats, catch rate, growth, etc.);
6. exact HGSS evolution data import;
7. exact HGSS level-up learnsets and move-system compatibility policy;
8. Steel/Dark battle-engine integration for Green;
9. Johto/Gen-IV species names, sprites, cries, dex entries and encounter/trainer integration.

These fields are intentionally marked pending rather than filled with guessed or modern-generation values.

## ROM integrity

The first 512 KiB of each patched ROM differs from its supplied base only at four standard header/checksum bytes:

- `0x0148`: ROM size `0x04` -> `0x05` (512 KiB -> 1 MiB);
- `0x014D`: recomputed header checksum;
- `0x014E-0x014F`: recomputed global checksum.

No existing game code/data in the original 32 banks is overwritten in this pass.

### Rev 0

- input SHA-1: `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196`
- output SHA-1: `47801542242756f72f1532a44fbc8ae44c68462d`
- IPS SHA-1: `24142459e09a489ad101de03b1da7368c85ba25d`
- output header/global checksum: `9B / 4D44`

### Rev A

- input SHA-1: `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`
- output SHA-1: `7a7eeb0441a7349c32455bc347d2dccbc32fd479`
- IPS SHA-1: `568b76a55380ed4d906ba4e79bcc27493ec6aca5`
- output header/global checksum: `9A / 64B6`

Both IPS files were reapplied in memory to their exact expected base ROM and reproduced the generated 1 MiB output byte-for-byte.

## Files

- `build_hgss_johto256.py` — deterministic builder + IPS generator + verifier
- `hgss_johto256_registry.csv` — 256-row readable registry
- `build_manifest.json` — build/status/hash manifest
- `green_hgss_johto256_parameters_rev0.ips` — Rev 0 patch
- `green_hgss_johto256_parameters_reva.ips` — Rev A patch

ROM binaries are build products only and are not intended for GitHub storage.
