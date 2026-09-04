# Pokémon Gold 8-ROM Structural Census — 2026-09-05

> Scope: the eight locally supplied Pokémon Gold ROM images (JP Rev 0, JP Rev A, EN, DE, FR, IT, ES, KR). Original ROM bytes are never stored in this repository. This report records derived metadata, structure, fingerprints, validated deltas, and reproducible analysis only.

## Executive result

The first full structural pass is complete across all 8 ROMs. It establishes three distinct layout families: compact Japanese 1 MiB builds, 2 MiB Western builds, and a heavily customized 2 MiB Korean build. The Western European localizations (DE/FR/IT/ES) preserve most English code/assets but consume two English-empty banks (`0x27`, `0x58`) for localization overflow. The Korean build preserves a substantial common engine/assets core but adds a dedicated two-byte Hangul text system, Hangul glyph banks, composition/naming logic, a CGB-only rendering path, and different Pokédex packing. Japanese Rev A is not a broad content rewrite: its dominant binary delta is one 5-byte sprite-animation bug fix in bank `0x23`, followed by address relocation/pointer fixups.

## Source identity and reproducibility

| Code | ROM family | Size | 16 KiB banks | SHA-1 |
|---|---|---:|---:|---|
| JP0 | Japan Rev 0 | 1 MiB | 64 | `8814f1039450a5d3684b1389f588ccd7ee7c3436` |
| JPA | Japan Rev A / Rev 1 | 1 MiB | 64 | `a222402235d484ee8e39f3f31bae57cf13daf585` |
| EN | USA/Europe English | 2 MiB | 128 | `d8b8a3600a465308c9953dfa04f0081c05bdcb94` |
| DE | German | 2 MiB | 128 | `9254195d461ea942eaaa08cc4b83de3cf82aea0d` |
| FR | French | 2 MiB | 128 | `c147c0d8c2b71b7628a7233436f5c052b5b17081` |
| IT | Italian | 2 MiB | 128 | `032608fe8947b627584a4a0eccc7bf9ad3588426` |
| ES | Spanish | 2 MiB | 128 | `162ea54c6a3cff374642e6dd842f9bffac847e7b` |
| KR | Korean | 2 MiB | 128 | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` |

All eight header and global checksums were validated in the baseline census. EN matches the exact ROM targeted by `pret/pokegold`; JP0/JPA match the exact Rev 0/Rev 1 hashes documented by `Narishma-gb/pokesilver`; KR matches the exact ROM targeted by `Narishma-gb/pokegold-kr`. Their layout/source trees are therefore used as exact-match structural references rather than generic similarity references.

## Bank occupancy

| ROM | Banks | Non-zero banks | All-zero banks |
|---|---:|---:|---:|
| JP0 | 64 | 64 | 0 |
| JPA | 64 | 64 | 0 |
| EN | 128 | 100 | 28 |
| DE | 128 | 102 | 26 |
| FR | 128 | 102 | 26 |
| IT | 128 | 102 | 26 |
| ES | 128 | 102 | 26 |
| KR | 128 | 104 | 24 |

An all-zero bank is only an occupancy fact. It is **not** declared safe free space until reference/pointer/control-flow analysis proves it unreachable and unused.

### Exact common non-zero banks

All eight ROMs have exactly identical full 16 KiB contents at the same bank indices for seven non-zero banks:

| Bank | Exact-match reference role |
|---|---|
| `0x0C` | Tileset Data 4 |
| `0x2A` | Map Blocks 1 |
| `0x30` | Sprites 1 |
| `0x37` | Map Blocks 3 / Tileset Data 5 |
| `0x3B` | Songs 2 |
| `0x3C` | Songs 3 / sound effects / cries |
| `0x3D` | Songs 4 |

This is direct byte-level evidence for a shared core across Japanese, Western, and Korean releases.

The five Western ROMs (EN/DE/FR/IT/ES) share 47 exact same-index banks; 21 are non-zero shared content and 26 are common zero banks. The 21 non-zero banks are `0C 12 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 2A 2B 30 37 3B 3C 3D`, dominated by Pokémon/trainer picture data, map blocks, sprites, and audio.

## Layout families

### Japanese 1 MiB family

The Japanese layout is tightly packed into banks `0x00-0x3F`. Map scripts are distributed across `0x13`, `0x22`, `0x26-0x29`, `0x2C-0x2D`, `0x2F`, `0x34-0x36`; title/options/font/intro share bank `0x39`; Pokédex/mail content is packed into bank `0x11`. No wholly zero bank exists in either supplied Japanese revision.

### Western 2 MiB family

The English layout expands script/text storage into high banks: standard scripts `0x40`, phone scripts `0x41`, map scripts through `0x42-0x62`, common text `0x64-0x66`, Pokédex `0x68-0x6B`, names `0x6C`, move descriptions `0x6D`, item descriptions `0x6E`, and other localized strings/GFX around `0x70`.

The DE/FR/IT/ES builds preserve that broad architecture but make two major localization-overflow allocations that EN leaves completely zero:

| Bank | EN | DE/FR/IT/ES usage | Evidence |
|---|---|---|---|
| `0x27` | all zero | localized landmark/location-name table | Direct decoded strings: city/town/cave/tower names |
| `0x58` | all zero | localized map-text/script overflow | Non-zero localized script/text payload; EN bank is completely zero |

Bank `0x27` examples include German `ROSALIA CITY`, French `VILLE GRIOTTE`, Italian `FIORPESCOPOLI`, and Spanish `CIUDAD CEREZO`, followed by their respective localized city/landmark name sequences. The English equivalents reside in the landmark-name material associated with bank `0x24`, demonstrating relocation/overflow rather than a new gameplay table.

Bank `0x58` occupancy is language-dependent and leaves substantial trailing zero space:

| ROM | Last non-zero bank offset | Non-zero bytes | Trailing zero bytes |
|---|---:|---:|---:|
| DE | `0x24BF` | 9,122 | 6,976 |
| FR | `0x1FAD` | 7,823 | 8,274 |
| IT | `0x1EA9` | 7,564 | 8,534 |
| ES | `0x1EDE` | 7,613 | 8,481 |

These trailing areas remain **candidate** free space only; they are not yet certified safe.

### Korean 2 MiB family

The Korean ROM is structurally more divergent than the Western translations. Exact-match source confirms Korean text uses a two-byte codepoint: first byte `0x01-0x0B` selects one of 11 Hangul tables, and the second byte selects the character entry.

Key Korean-only/repurposed banks:

| Bank | Role |
|---|---|
| `0x68` | Pokédex entries 001-128 |
| `0x69` | Pokédex entries 129-251 |
| `0x6A-0x6B` | all-zero/unassigned in KR (EN uses them for later Pokédex ranges) |
| `0x71` | Hangul structure tables, naming-screen Jamo GFX, Hangul composition/search logic |
| `0x72` | DMG error screen |
| `0x78-0x7A` | Hangul glyph tables 1-3 |
| `0x7B` | Diploma GFX |
| `0x7F` | double-byte/Hangul renderer and runtime glyph-cache/display support |

Bank `0x7F` contains `PlaceDoubleByteChar`, Hangul-glyph lookup/cache logic, dynamic glyph drawing into VRAM, text box/display support, and CGB bank handling. This explains the Korean header's CGB-only status at an architectural level: the localization is not merely different strings; it relies on a dedicated rendering system using additional CGB resources.

KR banks corresponding to EN map-script banks `0x54-0x57` and `0x59-0x62` are physically non-zero. The current exact-match Korean disassembly leaves these as not-yet-sectioned WIP ROM regions, so they are recorded as present but **not claimed fully disassembled**.

## Text and name-table census

A conservative Western 0x50-terminated candidate scan finds:

| ROM | Candidate strings |
|---|---:|
| EN | 2,493 |
| DE | 2,547 |
| FR | 2,536 |
| IT | 2,508 |
| ES | 2,506 |

Two localized description banks have especially clean table counts in every Western ROM:

| Bank | Reference role | Candidate strings per ROM |
|---|---|---:|
| `0x6D` | Move descriptions | 251 |
| `0x6E` | Item descriptions | 160 |

Bank `0x6C` is the dense names bank, with candidate counts around 709-734 depending on language and control/character encoding. These are detection counts, not yet the canonical logical-entry ledger; the next semantic extraction phase will resolve pointers and table boundaries so each logical name/string gets a stable ID and provenance.

## Japanese Rev 0 → Rev A / Rev 1

Raw byte comparison reports 10,841 differing bytes in 426 contiguous ranges across banks `00 04 05 09 0A 0F 14 21 23 24`. This sounds large, but nearly all of it is relocation noise caused by one 5-byte code insertion.

### Validated semantic fix

In `_InitSpriteAnimStruct`, Rev 0 increments `wSpriteAnimCount` and can allow the 8-bit counter to wrap to `0`. Sprite-animation structure index `0` is also the deinitialized/empty marker. Rev A inserts this 5-byte guard at ROM offset `0x08D038` (bank `0x23`, CPU address approximately `0x5038`):

```text
7E A7 20 01 34
```

Semantically: load the counter, test zero, and increment once more if it wrapped to zero. The revision also moves `pop af` to the correct position around this inserted branch. This prevents a newly initialized sprite-animation structure from receiving the reserved zero index.

Because bank `0x23` grows by five bytes at this point, all later bank-23 labels shift by +5. Exactly 16 isolated one-byte changes outside bank `0x23` and the ROM header are validated +5 low-byte pointer/address fixups, spread across banks `00, 04, 05, 09, 0A, 0F, 14, 21, 24`. The supplied `jp_reva_external_pointer_fixups.csv` records every offset and context.

Therefore the correct interpretation is: **one small sprite-animation correctness fix + systematic relocation fixups**, not ten kilobytes of independently changed game logic.

## Similarity observations

Even where a bank is not byte-identical, many engine/resource banks remain nearly aligned across localizations. Examples of same-index byte equality versus EN include DE/FR/IT/ES bank `0x07` at ~99.99%, and KR bank `0x2B` at ~99.994%, `0x07` at ~99.976%, `0x3A` at ~99.90%, `0x32` at ~99.69%, and `0x36` at ~99.22%. These are useful anchors for cross-language symbol/section propagation.

## Pointer census status

The reproducible tool also emits a heuristic far-pointer candidate matrix based on byte triples shaped like `(bank, little-endian ROMX address)`. It is intentionally **not treated as authoritative**, because arbitrary compressed/graphics/text bytes can match that pattern. Validated pointers are only promoted into the ledger after code/table context or exact-match disassembly confirms them. The large raw heuristic matrix is therefore reproducible locally but omitted from the repository's compact validated dataset.

## Current classification of work

This pass completes the **physical/structural census**: source identity, ROM/header family, bank occupancy, exact bank equivalence, reference bank roles, cross-language bank similarity, Western localization overflow, text-density/string candidates, Korean text architecture, and the complete Japanese revision delta classification.

The next pass is the **semantic object census**. It will assign stable logical records and exact ROM locations/references to: character maps/font glyphs; Pokémon/move/item/trainer/location names; Pokédex data; text pointer tables; map groups/maps/events/scripts; trainers/wild encounters; graphics/sprites/tilesets; audio; save/WRAM/SRAM structures; startup/title/intro/credits; unused/debug/dummy data; and verified free-space/reference maps. Every derived non-ROM ledger/report/tool should continue to be committed automatically.

## Reproducible artifacts

- `tools/gold_full_census.py`: generates the structural census from local `.gbc` inputs without embedding ROM payloads.
- `analysis/full-census/full_census.json`: source identities and headline revision result.
- `analysis/full-census/bank_inventory.csv`: every bank's role reference, hash, entropy, occupancy, and fill-run metrics.
- `analysis/full-census/bank_similarity_to_en.csv`: same-index and best-match structural similarity to EN.
- `analysis/full-census/pairwise_bank_comparison.csv`: exact-bank and same-index pairwise comparisons.
- `analysis/full-census/common_exact_banks.csv`: exact common-bank groups.
- `analysis/full-census/layout_reference.csv`: EN/Western, JP, and KR reference-bank role map.
- `analysis/full-census/text_likeness_by_bank.csv`: encoding-family text-likeness metrics.
- `analysis/full-census/western_string_candidate_summary.csv`: compact candidate-string counts by bank/language.
- `analysis/full-census/western_localization_overflow.csv`: validated `0x27`/`0x58` localization overflow occupancy.
- `analysis/full-census/jp_rev0_to_reva_diff_ranges.csv`: all raw revision difference ranges.
- `analysis/full-census/jp_reva_external_pointer_fixups.csv`: all validated external +5 fixups.

### Reference source trees

- `pret/pokegold` — exact English ROM reconstruction and bank layout.
- `Narishma-gb/pokesilver` — exact Japanese Gold Rev 0/Rev 1 reconstruction/WIP and revision conditional.
- `Narishma-gb/pokegold-kr` — exact Korean ROM reconstruction/WIP, Korean charmap, layout, Hangul renderer/composition logic.
