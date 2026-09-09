# RBY 16 KiB Bank Survey — 2026-09-09

This directory contains the bank-level structural survey for the RBY ENGLISH → ポケットモンスター Japanese-to-English retranslation/reimplementation project.

## Scope

- 12 uploaded Generation I ROMs
- 608 total 16 KiB bank records
- Japanese Red v1.0/v1.1, Green v1.0/v1.1, Blue, Yellow Rev0–Rev3
- English Red, Blue, Yellow as implementation references only
- Original ROM binaries are read-only inputs and are **not included** in this repository.

## Grounding

Bank roles are cross-checked against:

- `Narishma-gb/pokegreen` — Japanese Red/Green disassembly
- `Narishma-gb/pokeblue` — Japanese Blue disassembly
- `Narishma-gb/pokeyellow-jp` — Japanese Yellow disassembly
- `pret/pokered` — English Red/Blue implementation reference
- `pret/pokeyellow` — English Yellow implementation reference

## Major findings

- Japanese Red/Green/Blue are 32-bank / 512 KiB layouts and have no completely blank 16 KiB bank.
- Japanese RGB dialogue is generally stored inline with map scripts instead of using the English localization's dedicated text-bank layout.
- Japanese RGB critical translation locations include item names in `0x01`, move names + font in `0x04`, Pokémon/trainer names in `0x0E`, Pokédex entries in `0x10`, and map/NPC dialogue spread across the map/script banks.
- English Red/Blue use dedicated English text banks `0x20–0x2A`, Pokédex text `0x2B`, and move names `0x2C`; uploaded English Red/Blue banks `0x2D–0x3F` are exact all-zero banks.
- Japanese Yellow Rev3 has eight exact all-zero banks: `0x26`, `0x27`, `0x2A–0x2F`, totaling **128 KiB**.
- Those Rev3 Yellow banks correspond to garbage-only storage in Rev0–Rev2 and are empty in the Rev3 Japanese disassembly.
- Japanese Yellow bank `0x3B` is **not** empty: it contains Pikachu PCM. English Yellow bank `0x3B` is empty, so the English assumption must never be imported into the Japanese base.
- Japanese Yellow Rev3 and English Yellow have 16 whole banks that are byte-identical: `0x0C`, `0x1B`, `0x21–0x25`, `0x31–0x39`.
- Japanese RGB bank `0x1B` is whole-bank identical to the English implementation reference; several graphics/audio banks also retain very high informative same-offset byte identity.
- Documented `Garbage` sections and long trailing zero/FF regions are **candidates only** until exact symbol boundaries and pointer reachability are audited. They are not automatically classified as safe free space.

## Implementation consequence

The Japanese originals do not use the English dedicated-text-bank architecture. The correct implementation path is therefore:

`extract Japanese inline text → translate → allocate new English text storage → rebuild pointers/call structure → adapt English font/UI/text routines`

Do **not** overwrite Japanese map banks wholesale with English text banks.

For Japanese Yellow Rev3 specifically, English Yellow's `0x26–0x2F` layout cannot be copied wholesale because Japanese Rev3 banks `0x28` and `0x29` are active. The confirmed new-text candidates are `0x26`, `0x27`, and `0x2A–0x2F`, subject to final pointer/reachability checks during implementation.

## Full package

`rby_bank_survey_package_2026-09-09.tar.gz` contains:

- `rby_bank_full_survey_report_2026-09-09.md`
- `rby_bank_full_survey_2026-09-09.csv`
- `rby_bank_revision_and_localization_diffs_2026-09-09.csv`
- `rby_bank_full_survey_summary_2026-09-09.json`
- `rby_bank_full_survey.py`

Package SHA-256:

`879ed5846b74499f55deaea38658972f4f6a3cd3b54cac035a3e6ef322f0d0df`

The similarity metric in the final survey excludes positions where both compared bytes are only `0x00`/`0xFF` fill. It is diagnostic evidence, not proof of semantic or pointer equivalence.
