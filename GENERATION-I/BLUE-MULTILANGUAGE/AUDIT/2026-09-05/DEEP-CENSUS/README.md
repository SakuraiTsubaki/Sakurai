# Pokémon Blue multilingual deep census — 2026-09-05

This directory is a **non-ROM analysis package** for the six project ROMs: Japanese Blue and the EN/DE/FR/IT/ES Blue releases. No ROM bytes are committed.

## Exact source anchors

The ROM hashes were checked against source/disassembly projects where available:

- JP `0da501e3e5c51ab8fef55b092dcdd7e6b050e424` → `Narishma-gb/pokeblue` (exact).
- EN `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2` → `pret/pokered` (exact).
- DE `20e72dc6f41493eee1fdd0cef54214e6c3389688` → `einstein95/pokered-de` (exact).
- FR `47faa910d0e073c600665bf9c83b6bd17babdf8a` → `einstein95/pokered-fr` (exact).
- ES `7715e7b133e8634df48918b9138374110212a108` → `einstein95/pokered-es` (exact).
- IT `f69ed1a1332f04c24c7db899a09019bb045fa8b3` → raw ROM verified locally; no exact public disassembly was verified during this pass.

EN/DE/FR/ES use the same linker bank topology (`layout.link`). IT is mapped to that topology as an **inference**, supported by its same 64-bank physical organization, blank tail, and bankwise alignment; it is not marked source-verified.

## Major structural result

### Japanese Blue

The exact Japanese linker map reports:

- ROM0: **16,384 used / 0 free**.
- ROMX: **507,903 used / 1 free byte across 31 switchable banks**.
- Total linked ROM: banks `00–1F` (32 banks = 512 KiB).
- Remaining slack is deliberately represented by source `Garbage N` sections rather than linker free space.

So JP Blue is effectively **fully packed in linker terms**.

### Western Blue family

The exact EN linker map reports:

- linked content banks `00–2C` (45 banks including ROM0),
- ROMX linked free space in banks `01–2C`: **161,714 B**,
- ROM0 linker free space: **156 B**,
- physical banks `2D–3F`: **19 completely-zero banks = 311,296 B (304 KiB)**.

EN therefore has **161,870 B** of source-confirmed linker free space including ROM0, plus **311,296 B** of physically blank tail-bank capacity, for **473,166 B combined capacity** subject to banking/reference audits. Blank banks are physical capacity, not an automatic promise that every engine pointer/banking path can address newly moved data safely.

The dedicated western localization area `20–2C` alone has **85,778 B** of source-confirmed EN linker free space.

## Localization architecture: JP → western

Several high-value structures were physically relocated rather than merely translated in place:

| Structure | JP Blue | Western EN Blue | Meaning |
|---|---|---|---|
| Move names | bank `04`, `$4000` | bank `2C`, `$4000` | western localization gained a dedicated move-name bank |
| Pokémon names (`MonsterNames`) | bank `0E`, `$5446` | bank `07`, `$421E` | name table moved out of the battle-data bank |
| Font (`FontGraphics`) | bank `04`, `$5E99` | bank `04`, `$5A80` | same general bank, different packing/layout |
| Move data (`Moves`) | bank `0E`, `$4000` | bank `0E`, `$4000` | stable anchor |
| Base stats (`BaseStats`) | bank `0E`, `$43DE` | bank `0E`, `$43DE` | stable anchor |
| Cry data (`CryData`) | bank `0E`, `$57FC` | bank `0E`, `$5446` | JP inline names push later data forward |
| Pokédex pointer table | bank `10`, `$445B` | bank `10`, `$447E` | same subsystem, repacked |
| Rhydon Pokédex record | bank `10`, `$45D7` | bank `10`, `$45FA` | JP record contains description inline; western record far-points to text |
| Rhydon description text | inline in bank `10` record | bank `2B`, `$4000` (`_RhydonDexEntry`) | western descriptions split to dedicated text bank |

Western banks `20–2A` are dedicated `Text 1–11`, bank `2B` is Pokédex description text, and bank `2C` is move names. **Those 13 dedicated localization banks do not exist in the 32-bank JP ROM.**

## Western five-language byte consensus

To avoid padding inflating similarity, the table below measures each bank only over the **union of non-trailing-zero used prefixes** across EN/DE/FR/IT/ES.

### Most localization-sensitive banks

| Bank | Role | all-5 same in used union | used union |
|---:|---|---:|---:|
| `2C` | move names | 0.000% | 1,714 B |
| `2B` | Pokédex text | 0.049% | 14,392 B |
| `27` | Text 8 | 0.094% | 12,727 B |
| `26` | Text 7 | 0.110% | 13,584 B |
| `28` | Text 9 | 0.146% | 12,985 B |
| `22` | Text 3 | 0.165% | 13,949 B |
| `25` | Text 6 | 0.180% | 13,344 B |
| `21` | Text 2 | 0.180% | 13,874 B |
| `24` | Text 5 | 0.226% | 13,744 B |
| `29` | Text 10 | 0.228% | 13,154 B |
| `20` | Text 1 | 0.234% | 13,696 B |
| `23` | Text 4 | 0.381% | 13,907 B |

The strongest signal is exactly what we would expect from true localization: **bank `2C` move names has 0.000% all-five byte identity in its used union**, and the dedicated Pokédex/general-text banks are almost entirely language-specific.

### Most stable banks

| Bank | Role | all-5 same in used union | used union |
|---:|---|---:|---:|
| `1B` | tilesets 3 | 100.000% | 16,384 B |
| `1F` | audio headers + SFX + audio engine 3 + music 3 | 99.982% | 16,378 B |
| `02` | audio headers + SFX + audio engine 1 + music 1 | 99.914% | 16,372 B |
| `0A` | Pokémon pics 2 + battle engine 4 | 99.901% | 16,124 B |
| `0C` | Pokémon pics 4 + battle engine 6 | 99.877% | 16,272 B |
| `0B` | Pokémon pics 3 + battle engine 5 | 99.821% | 16,188 B |
| `19` | tilesets 1 | 99.768% | 16,352 B |
| `13` | trainer pics + maps 9 + predefs | 99.220% | 16,290 B |
| `1E` | battle animations + overworld effects + evolution + TM prices | 98.039% | 16,320 B |
| `05` | NPC sprites 2 + battle engine 2 | 96.899% | 16,223 B |
| `09` | Pokémon pics 1 + battle engine 3 | 96.836% | 16,342 B |
| `11` | maps 5-6 + Pokédex rating + hidden-event core | 91.909% | 12,459 B |

Bank `1B` (`Tilesets 3`) is **16 KiB byte-for-byte identical across all five western versions and Japanese Blue**. It is the cleanest cross-version anchor in the current set. Audio/graphics-heavy banks are also overwhelmingly stable.

## Raw trailing-00 packing by western language

These values are raw trailing-zero padding across linked switchable banks `01–2C`; only EN has been cross-checked against an exact linker map, so the others remain padding measurements rather than safe-space declarations.

| ROM | trailing `00` total, banks 01–2C | trailing `00` in localization banks 20–2C |
|---|---:|---:|
| DE | 137,522 B | 61,508 B |
| EN | 161,715 B | 85,778 B |
| ES | 152,097 B | 76,351 B |
| FR | 155,194 B | 79,288 B |
| IT | 157,074 B | 81,389 B |

EN raw trailing padding is one byte larger than its authoritative ROMX free total because hex bank `16` (decimal 22) ends with one content byte equal to `00`; this is why raw padding is never promoted to “safe free space” automatically.

## Files

- `deep_census.py` — deterministic generator; reads local ROMs but embeds no ROM bytes.
- `deep_census_summary.json` — machine summary.
- `source_verification.csv` — hash-to-disassembly provenance status.
- `bank_matrix_compact_parts/part-01.csv` … `part-04.csv` — complete 64-bank cross-language census: bank roles, source-confirmed EN free bytes, per-ROM bank SHA-1s and trailing-zero packing.
- `western_bank_diff.csv` — bankwise EN/DE/FR/IT/ES comparison with padding-corrected used-span consensus and shared-run summary metrics.
- `EN_source_confirmed_free_space.csv` — authoritative EN linker free ranges from the exact `pret/pokered` build map.
- `JP_vs_Western_topology.csv` — bank-by-bank JP ↔ western topology and same-position similarity.
- `high_value_anchor_addresses.csv` — exact source-backed addresses for major tables/assets.
- `MANIFEST.sha256` — integrity manifest for the canonical committed census artifacts.

`deep_census.py` can additionally regenerate verbose raw ledgers (`bank_role_matrix.csv`, `western_shared_runs.csv`, `filler_runs_ge256.csv`) when the six local ROMs are present. These verbose dumps are derivations of the committed generator and compact/decision-grade ledgers; no ROM bytes are embedded.

## Interpretation rule

- `source-confirmed free` = linker-map evidence; safe candidate still requires reference/pointer audit before relocation.
- `physical blank bank` = bytes are blank; using them still requires mapper and bank-reference audit.
- `trailing padding candidate` / `internal filler candidate` = raw byte heuristic only; **never overwrite solely from this label**.
- ROM binaries remain outside GitHub.

## Next exhaustive layer

The next layer should enumerate table-by-table references and pointer provenance: map headers, text pointer tables, Pokémon/move/item/trainer tables, wild/trainer data, sprite/pic tables, SGB packets, music/SFX headers, save/SRAM structures, and every far/banked reference that would need patching when data is moved.
