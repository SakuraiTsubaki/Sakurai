# Generation IV Full Expansion Audit — DP / Pt / HGSS

Generated from the five supplied read-only NDS ROM images. ROM binaries are not included.

## 1. Actual ROM baseline

| Game | Code | Region | ROM ver. | ROM | NitroFS files | NARCs | Tail free |
|---|---|---|---:|---:|---:|---:|---:|
| DIAMOND | `ADAE` | EN-US | 5 | 64 MiB | 356 | 149 | 5.66 MiB |
| PEARL | `APAE` | EN-US | 5 | 64 MiB | 356 | 149 | 5.66 MiB |
| PLATINUM | `CPUK` | KO-KR | 0 | 128 MiB | 461 | 215 | 30.12 MiB |
| HEARTGOLD | `IPKK` | KO-KR | 0 | 128 MiB | 511 | 308 | 9.13 MiB |
| SOULSILVER | `IPGK` | KO-KR | 0 | 128 MiB | 511 | 308 | 9.13 MiB |

Key observed data counts:

- Diamond/Pearl: Personal/Evolution/level-up tables 501 entries; move table 471; item table 442; trainer table 850.
- Platinum: Personal/Evolution/level-up tables 508 entries; move table 471; item table 442; trainer table 928.
- HeartGold/SoulSilver: Personal/Evolution/level-up tables 508 entries; move table 471; item table 514; trainer table 738; message archive 822.
- Core Pokemon battle graphics archive is 11,778,676 bytes with 2,964 members = exactly 494 × 6 members.
- Observed Personal records are 44 bytes each; move records 16 bytes; item records 34 bytes; trainer headers 20 bytes.

## 2. Recommended future-proof ABI

Use a common Gen-IV expansion ABI with game adapters, not five independent incompatible expansions.

| Domain | Recommended cap | Representation |
|---|---:|---|
| Species | 2,048 | `u16 SpeciesID` |
| Form/variant records | 4,096 | `u16 FormRecordID` |
| Moves | 2,048 | `u16 MoveID` |
| Abilities | 1,024 | `u16 AbilityID` |
| Items | 4,096 | `u16 ItemID` |
| Types | 32 | `u8 TypeID` |
| Machines | 512 | 512-bit compatibility bitset |
| Evolution methods | 256 | method + parameter block |
| Volatile states | 128+ | extensible bitset/registry |
| Ribbons/marks | 512 bits | versioned extensible bitset |
| PC boxes (extended profile) | 64 × 30 | paged storage |

The caps are deliberately powers of two with large Gen-X headroom. They are not estimates of the exact Gen-X final content count.

## 3. ROM capacity target

A 256 MiB build is a practical lower target for a heavily deduplicated all-Pokemon system-content build. A 512 MiB build is the recommended full-capacity target when preserving room for Gen-X species/forms, sprites, icons, cries, move effects, strings, and future additions.

Current 4th-gen `pokegra` density is about 23.28 KiB per species-equivalent graphics slot. If 4,096 form records each required the same six-resource density, the archive alone would be about 93.1 MiB. At HGSS icon density, 4,096 icons are about 4.2 MiB. Deduplication and shared form assets can reduce this materially.

Important: DS main RAM is only a few MiB, so expansion data must remain streamed/on-demand. Do not load 2K/4K tables wholesale into RAM.

## 4. Save profiles

- **Retail-compatible profile:** preserve the original save-chip size and PK4 compatibility as much as possible; use compact extension tables and strict migration.
- **Extended profile:** use a versioned SaveV2 (recommended 2 MiB for emulator/flashcart/custom hardware) with larger PC storage, ribbons/marks, modern met-data, and future mechanics.
- Never silently reinterpret old bitfields. Every schema change gets an explicit version and migration path.

## 5. Bug / glitch / error policy

Three simultaneous audits are required:

1. **Original defects:** known Gen-IV bugs/glitches/oversights, plus source-level defects found during decomp/static review.
2. **Expansion regressions:** truncation, overflow, stale hard-coded bounds, save corruption, UI overflow, NARC indexing, RAM/heap pressure.
3. **Modern-mechanic interactions:** ability/item/move/weather/terrain/form/transformation ordering and cross-generation behavior.

Every fix must have: reproducible trigger, affected games, root cause, patch, regression test, link/compatibility impact, and status (`KNOWN`, `REPRODUCED`, `FIXED`, `VERIFIED`).

## 6. Highest-priority structural blockers already confirmed

- Trainer party Species/Form packing uses only 10 bits for species in Platinum/HGSS-style data: IDs above 1023 cannot survive unchanged.
- Battle structures contain 8-bit Ability IDs and 5-bit Form fields in HGSS decomp structures: current/future data exceeds those assumptions.
- Many original battle/state systems use fixed bitfields. Adding modern conditions without a registry/expanded bitset will create collisions.
- Hard-coded table bounds exist in ARM9/overlay code and must be audited in addition to expanding NARC member counts.
- ROM free space is not enough by itself; RAM, save schema, script operands, UI, link protocol, and serialization must be versioned together.

## 7. Architecture

```text
Gen4 Expansion ABI
├── IDs / registries
│   ├── species 2048
│   ├── forms 4096
│   ├── moves 2048
│   ├── abilities 1024
│   └── items 4096
├── streamed data
│   ├── PersonalV2
│   ├── MoveV2
│   ├── ItemV2
│   ├── EvolutionV2
│   └── LearnsetV2
├── battle compatibility layer
│   ├── DP adapter
│   ├── Platinum adapter
│   └── HGSS adapter
├── SaveV1 compatibility / SaveV2
└── regression + conformance test suites
```

## 8. Files in this audit package

- `nds_audit.py` — read-only NDS/FNT/FAT/NARC audit script.
- `rom_audit_summary.json` — machine-readable baseline.
- `rom_capacity.csv` — ROM/header/capacity/hash inventory.
- `key_narc_limits.csv` — key archive member counts and sizes.
- `recommended_limits.csv` — proposed future-proof caps.
- `capacity_profiles.csv` — 256/512 MiB headroom profiles.
- `bug_audit_matrix.csv` — initial defect/risk matrix.

No copyrighted ROM bytes are included.
