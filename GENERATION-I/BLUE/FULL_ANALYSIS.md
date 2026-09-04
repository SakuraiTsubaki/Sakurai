# Pokémon Blue 6-ROM Full Structural Census

Targets: JP / EN / DE / FR / IT / ES retail Pokémon Blue ROM images supplied for analysis. ROM binaries themselves are intentionally not included in this package.

## Executive findings

- JP Blue is 512 KiB / 32 banks / MBC1+RAM+Battery. EN is 1 MiB / 64 banks / MBC3+RAM+Battery. DE/FR/IT/ES are 1 MiB / MBC5+RAM+Battery. All six have valid header and global checksums and SGB flag 0x03.
- Internationalization was structural, not a text-only translation: field widths, ROM banking, move-name placement, dedicated text banks, character maps/fonts, mapper type, WRAM/SRAM offsets, and save-layout positions changed.
- Western builds use nonzero data through bank 0x2C. Banks 0x2D-0x3F are exactly 0x00 in all five Western ROMs: 19 banks = 311,296 bytes of clean tail padding each.
- Bank 0x1B is bit-identical in all six ROMs. Exact layouts identify it as Tilesets 3. Audio/graphics-heavy banks 02, 09-0C, 13, 19, 1A, 1F are also extremely conserved.
- Main dialogue storage pressure ranks DE > ES > FR > IT > EN. German text banks 20-29 occupy about 22.2% more extent than EN.
- Italian and Spanish preserve the English Pokémon internal-name table byte-for-byte for all 190 internal slots; German differs on 116/190 and French on 119/190. Moves/items/trainer names are strongly localized in every continental edition.

## Header / cartridge metadata

|Lang|ROM size|Banks|Mapper|SGB|Destination|Version|SHA-1|
|---|---:|---:|---|---:|---:|---:|---|
|JP|524,288|32|MBC1+RAM+BATTERY|0x03|0|0|`0da501e3e5c51ab8fef55b092dcdd7e6b050e424`|
|EN|1,048,576|64|MBC3+RAM+BATTERY|0x03|1|0|`d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`|
|DE|1,048,576|64|MBC5+RAM+BATTERY|0x03|1|0|`20e72dc6f41493eee1fdd0cef54214e6c3389688`|
|FR|1,048,576|64|MBC5+RAM+BATTERY|0x03|1|0|`47faa910d0e073c600665bf9c83b6bd17babdf8a`|
|IT|1,048,576|64|MBC5+RAM+BATTERY|0x03|1|0|`f69ed1a1332f04c24c7db899a09019bb045fa8b3`|
|ES|1,048,576|64|MBC5+RAM+BATTERY|0x03|1|0|`7715e7b133e8634df48918b9138374110212a108`|

All header checksums and global checksums recompute correctly.

## Internationalization data-model changes

|Field|JP|EN/Western|Effect|
|---|---:|---:|---|
|`NAME_LENGTH`|6|11|Pokémon/player/nickname/save records shift|
|`MOVE_NAME_LENGTH`|8|14|longer localized move labels|
|`ITEM_NAME_LENGTH`|9|13|longer item labels|
|`TRAINER_NAME_LENGTH`|11|13|longer trainer-class labels|
|`GYM_CITY_LENGTH`|5|17|UI/localized city-name expansion|
|`NAME_BUFFER_LENGTH`|20|20|shared scratch buffer remains 20|

The save block allocates `sPlayerName` with `NAME_LENGTH`, so JP and Western raw save layouts diverge immediately at that field. Cross-region `.sav` files must not be assumed byte-compatible.

## Core text/name tables recovered

|Table|JP location|Western location|Entries|Storage|
|---|---|---|---:|---|
|Pokémon internal names|`0x039446`|`0x01C21E`|190|JP fixed 5 bytes; West fixed 10 bytes|
|Move names|`0x010000` (bank 04)|`0x0B0000` (bank 2C)|165|0x50-terminated|
|Items + floor labels|`0x004733`|EN `0x00472B` (minor per-language shifts)|83 + 14|0x50-terminated|
|Trainer classes|`0x039DB5`|`0x0399FF`|47|0x50-terminated|

### Localization delta vs English

- **Pokemon internal names:** DE 116/190, FR 119/190, IT 0/190, ES 0/190
- **Move names:** DE 158/165, FR 156/165, IT 158/165, ES 163/165
- **Items + floors:** DE 91/97, FR 86/97, IT 90/97, ES 90/97
- **Trainer classes:** DE 34/47, FR 35/47, IT 32/47, ES 30/47

Examples are preserved in the CSV tables with decoded text and raw hexadecimal bytes for reversibility.

## ROM-bank architecture

JP ends at bank 0x1F. The Western build adds banks 0x20-0x2C for Text 1-11, Pokédex text, and move names, then leaves 0x2D-0x3F zero. See `bank_roles.csv`.

|Bank|Role|Cross-version observation|
|---|---|---|
|`02`|audio 1|Audio 1 — JP↔EN ~99.85% same-offset bytes|
|`09`|pics 1 / battle engine 3|Pics 1 / Battle 3 — ~96.23% JP↔EN|
|`0A`|pics 2 / battle engine 4|Pics 2 / Battle 4 — ~98.42%|
|`0C`|pics 4 / battle engine 6|Pics 4 / Battle 6 — ~99.01%|
|`19`|tilesets 1|Tilesets 1 — ~99.63%|
|`1A`|battle engine 11 / tilesets 2|Battle 11 / Tilesets 2 — ~99.75%|
|`1B`|tilesets 3|Tilesets 3 — 100% exact across all six|
|`1F`|audio 3|Audio 3 — ~99.95% JP↔EN|

Bank-level conservation proves that large portions of audio, graphics, tile data, and battle code were inherited with minimal byte changes, while localized text/control banks were heavily rebuilt.

## Western text pressure

|Lang|Text banks 20-29 extent|vs EN|Bank 2B Pokédex extent|Bank 2C move extent|
|---|---:|---:|---:|---:|
|EN|110,455|1.000×|14,392|1,551|
|DE|134,964|1.222×|13,895|1,681|
|FR|117,912|1.068×|13,371|1,619|
|IT|115,358|1.044×|13,816|1,644|
|ES|120,374|1.090×|13,727|1,714|

The extent metric is the sum of each bank’s last nonzero byte + 1; it is a storage-pressure proxy, not a semantic character count.

## Encoding / font implications

- JP and Western builds reuse byte values for different glyph sets: the same high-byte range that encodes kana in JP encodes Latin letters/accents in Western builds.
- French/German and Italian/Spanish use distinct regional accent/punctuation charmap variants. Raw text bytes therefore cannot be transplanted safely without the matching font/charmap/output assumptions.
- The CSVs retain `*_raw` columns so every decoded name can be audited against original ROM bytes. Some JP glyph codes are graphically shared between hiragana/katakana; contextual decoding may therefore display one Unicode form even when the tile is visually shared.

## Similarity and inheritance

Whole-file similarity between Western ROMs is inflated by the shared zero tail. Restricting comparison to used banks 00-2C gives:
- EN↔DE: 61.6088%
- EN↔FR: 61.9922%
- EN↔IT: 63.2986%
- EN↔ES: 64.0388%
- DE↔FR: 62.5958%
- DE↔IT: 61.9531%
- DE↔ES: 61.9992%
- FR↔IT: 63.3567%
- FR↔ES: 62.8327%
- IT↔ES: 64.1846%

JP↔EN same-offset overlap over the first 512 KiB is 43.65%; this underestimates inherited logic where internationalization relocated blocks. `bank_relocation_matches_64b.csv` contains relocation candidates.

## Free space / expansion observations

- JP: all 32 banks contain meaningful/nonconstant data; no fully blank bank exists.
- Western: banks 2D-3F are fully zero, totaling 304 KiB (311,296 bytes) per ROM. This is excellent candidate capacity for a controlled rebuild, but references/bank-switching/linker logic still must be made mapper-aware before treating it as usable runtime content.
- Local zero/FF runs inside used banks are catalogued separately in `fill_runs_ge64.csv`; they are candidates only, not automatically safe free space.

## Mapper / compatibility consequences

- JP uses MBC1, EN uses MBC3, and continental Europe uses MBC5. A patch that hardcodes mapper register behavior or assumes MBC1/MBC3 banking must be audited before cross-porting.
- All six advertise 32 KiB external RAM and SGB support, but mapper and name/save layout changes mean cartridge/header parity does not imply binary save compatibility.
- Western DE/FR/IT/ES share MBC5 and the same high-level expanded field widths; they are much closer engineering siblings to each other than to JP. EN remains structurally close but uses MBC3.

## Files in this census package

- `metadata.csv/json` — hashes, header, mapper, checksum verification
- `banks.csv`, `bank_roles.csv` — per-bank statistics and semantic roles
- `pairwise_same_offset.csv`, `pairwise_bank_similarity.csv`, `western_used_region_similarity.csv`, `jp_vs_west_bank_similarity.csv` — binary similarity
- `bank_relocation_matches_64b.csv` — likely relocated 64-byte blocks
- `fill_runs_ge64.csv` — fill/free-space candidates
- `pokemon_internal_names.csv`, `move_names.csv`, `item_floor_names.csv`, `trainer_names.csv` — cross-language aligned core name tables
- `table_localization_stats.csv`, `text_bank_usage.csv` — localization deltas / storage pressure
- `latin_text_candidates.csv` — broad candidate-string census for Western builds
- `analyze_blue_roms.py`, `extract_core_tables.py`, `build_report.py` — reproducible analysis scripts

## Reference disassemblies

- EN exact-match reference: `pret/pokered` (builds Blue SHA-1 `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`).
- JP exact-match reference: `Narishma-gb/pokeblue` (builds Blue SHA-1 `0da501e3e5c51ab8fef55b092dcdd7e6b050e424`).

This census deliberately separates verified ROM facts from engineering inference. A bank being zero or containing long fill runs is evidence of padding, not by itself proof that arbitrary code can use it safely without mapper/reference changes.
