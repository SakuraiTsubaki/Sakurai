# SILVER — HGSS Expanded Johto Pokédex 268 / Stage 2

## Target

This stage supersedes the earlier 256-species data stage.

The project definition is now:

**GSC 251 species + every Generation-IV evolution of a Generation-I/II family = 268 species.**

The HGSS Johto order is used as the structural backbone, but the twelve DPPt evolutions omitted from HGSS's official 256-entry Johto Dex are also inserted beside their evolutionary families.

## Critical ID rule

Do not confuse logical species IDs with the vanilla one-byte raw IDs.

- Raw Gen-II species `0x01..0xFB`: the 251 real species.
- `0xFC`: skipped/placeholder slot.
- `0xFD`: EGG.
- `0xFE`: not defined as a species.
- `0xFF`: list/end sentinel in multiple species-list paths.
- New species therefore **do not receive raw IDs 0xFC..0x100**.
- The extended data model uses dense **16-bit logical IDs 252..268**. A conversion layer is required before party/box/save/battle routing.

## New logical species

| Logical | National | Expanded Johto | Species |
|---:|---:|---:|---|
| 252 | 424 | 126 | Ambipom |
| 253 | 429 | 230 | Mismagius |
| 254 | 430 | 222 | Honchkrow |
| 255 | 461 | 228 | Weavile |
| 256 | 462 | 122 | Magnezone |
| 257 | 463 | 185 | Lickilicky |
| 258 | 464 | 220 | Rhyperior |
| 259 | 465 | 187 | Tangrowth |
| 260 | 466 | 161 | Electivire |
| 261 | 467 | 156 | Magmortar |
| 262 | 468 | 48 | Togekiss |
| 263 | 469 | 103 | Yanmega |
| 264 | 470 | 194 | Leafeon |
| 265 | 471 | 195 | Glaceon |
| 266 | 472 | 200 | Gliscor |
| 267 | 473 | 204 | Mamoswine |
| 268 | 474 | 233 | Porygon-Z |

The end of the expanded order is Tyranitar #263, Lugia #264, Ho-Oh #265, Mewtwo #266, Mew #267, Celebi #268.

## Parameters imported

For all 17 additions, the Stage-2 records import Platinum personal-data values for:

- HP / Attack / Defense / Speed / Special Attack / Special Defense
- types
- catch rate
- Generation-IV base EXP reward
- hatch cycles
- growth rate
- egg groups
- held items where a direct Silver/raw-item mapping already exists

Gender ratio is inherited from the direct family predecessor because all 17 additions retain their family's ratio. Gen-II graphics pointers and TM/HM masks remain explicit compatibility placeholders until the graphics/move-routing stages.

## Evolution parameters

New engine methods staged in the payload:

- level up while knowing a move
- use evolution item
- trade holding item
- level up at night while holding item
- level up in a special location

Johto-native location mappings used by this project:

- Magneton → Magnezone: **Power Plant** magnetic field
- Eevee → Leafeon: **Ilex Forest** moss zone
- Eevee → Glaceon: **Ice Path** ice zone

Double Hit is staged as logical move ID 252: Normal, 35 power per hit, 90 accuracy, 10 PP, exactly two hits. No raw one-byte move ID is assigned yet; that will happen only after the move-ID audit.

## Evolution-item raw IDs

Eight verified no-effect dummy item slots are reserved without widening the Gen-II item ID:

| Raw ID | New item |
|---:|---|
| 0x93 | Shiny Stone |
| 0x94 | Dusk Stone |
| 0x95 | Razor Claw |
| 0x99 | Protector |
| 0x9A | Electirizer |
| 0x9B | Magmarizer |
| 0xA2 | Razor Fang |
| 0xAB | Dubious Disc |

## Binary payload

- ROM bank: `0x7E`
- file offset: `0x1F8000`
- magic: `SJ268P2\0`
- payload length: **10,324 bytes**
- payload body CRC32: **24660e5b**
- 268 × 16-bit logical→National-Dex map
- 268 × 16-bit expanded Johto order
- 268 × 33-byte widened base records
- 17 × 16-byte evolution records
- 1 Double Hit metadata record
- 8 evolution-item reservation records

All eight targets validate against the exact clean-source SHA-256 values and share the same payload CRC. Japanese Rev0/RevA are expanded from 1 MiB to 2 MiB; the others remain 2 MiB. Header and global checksums are regenerated and independently verified.

## Status

**DATA-STAGED / ENGINE-NOT-ROUTED.**

The 268-species data model is present in all eight generated ROMs, but the vanilla one-byte species engine still runs until the 16-bit conversion/routing stage is implemented. This is intentionally not labeled a playable 268-species final build.

## Files

- `manifest.json` — canonical machine-readable 268-species model
- `new_species_17.csv` — 17 new personal-data records
- `expanded_johto_order_268.csv` — complete expanded order
- `evolution_matrix_17.csv` — evolution parameter matrix
- `build_stage2_payload.py` — reproducible injector
- `validate_stage2.py` — independent validator
- `build_report.json` — per-ROM source/output hashes
- `ID-AND-ENGINE-NOTES.md` — raw-ID audit and next engine work
