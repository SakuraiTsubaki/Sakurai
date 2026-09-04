# Pokémon Silver multi-region ROM census — initial forensic pass

Generated from the eight project ROMs. ROM binaries are intentionally excluded from version control.

## Scope

- ROMs inspected: **8**
- Total input bytes: **14,680,064**
- Version-controlled outputs in this pass: ROM identity/header manifest, pairwise byte comparison, and reproducible census tool.

## ROM manifest

| ROM | Size | Title | Ver | Cart | Declared ROM | Header chk | Global chk | SHA-1 |
|---|---:|---|---:|---|---:|---|---|---|
| Pocket Monsters Eun (Korea).gbc | 2,097,152 | `POKEMON_SLVAAXK` | 0 | MBC3+TIMER+RAM+BATTERY | 2,097,152 | OK | OK | `cb22d7e03a74dc3a563fde6be8626626b2b392e7` |
| Pocket Monsters Gin (Japan) (Rev A).gbc | 1,048,576 | `POKEMON_SLVAAXJ` | 1 | MBC3+TIMER+RAM+BATTERY | 1,048,576 | OK | OK | `a11d5ddc26eb826086593f82370b15d16404d33e` |
| Pocket Monsters Gin (Japan).gbc | 1,048,576 | `POKEMON_SLVAAXJ` | 0 | MBC3+TIMER+RAM+BATTERY | 1,048,576 | OK | OK | `fa8c51059c1642faa570db56ef089f54d1d2011f` |
| Pokemon - Edicion Plata (Spain).gbc | 2,097,152 | `POKEMON_SLVAAXS` | 0 | MBC3+TIMER+RAM+BATTERY | 2,097,152 | OK | OK | `05bd978ab2cb104b0aff3f696896e30885203a18` |
| Pokemon - Silberne Edition (Germany).gbc | 2,097,152 | `POKEMON_SLVAAXD` | 0 | MBC3+TIMER+RAM+BATTERY | 2,097,152 | OK | OK | `8ecc58d621faaedf2a934bd2583d527220df7bb9` |
| Pokemon - Silver Version (USA, Europe).gbc | 2,097,152 | `POKEMON_SLVAAXE` | 0 | MBC3+TIMER+RAM+BATTERY | 2,097,152 | OK | OK | `49b163f7e57702bc939d642a18f591de55d92dae` |
| Pokemon - Version Argent (France).gbc | 2,097,152 | `POKEMON_SLVAAXF` | 0 | MBC3+TIMER+RAM+BATTERY | 2,097,152 | OK | OK | `a4a7e8079b7a53e4d9ef43382bbb1090b9d45d1a` |
| Pokemon - Versione Argento (Italy).gbc | 2,097,152 | `POKEMON_SLVAAXI` | 0 | MBC3+TIMER+RAM+BATTERY | 2,097,152 | OK | OK | `c9eca9d0a837beb9137bb7d779e469c54e9f8d77` |

## Immediate findings

- Japanese Rev0/RevA ROMs are **1 MiB** each; the six localized ROMs are **2 MiB** each.
- All eight Nintendo-logo headers validate: **8/8**.
- Header checksum valid: **8/8**; global checksum valid: **8/8**.
- All eight use `MBC3+TIMER+RAM+BATTERY` and declare 32 KiB external RAM.
- Japanese Rev0 and RevA differ in **19,150 / 1,048,576 bytes (1.826286%)** across the shared image.
- Japanese Rev0/RevA have **48 identical aligned 16 KiB banks out of 64**.

## Pairwise comparison

`pairwise_comparison.csv` compares all 28 ROM pairs across their shared byte range and records differing-byte counts, first/last differing offsets, and identical aligned 16 KiB banks.

A low aligned-bank identity count across languages is expected because localization can change text, fonts, code layout, and storage placement; it is not by itself evidence of gameplay differences.

## Reproducibility

`rom_census.py` reads local `.gbc` inputs without modifying them and regenerates the ROM/header manifest plus pairwise comparison data. ROM binaries themselves remain outside GitHub.

## Next forensic layers

1. Map every 16 KiB bank by content class (code / text / graphics / maps / audio / tables / free space).
2. Locate charset/font/text engines per language, with special attention to Korean 2-byte Hangul handling.
3. Recover pointer tables and text blocks, then build cross-language correspondence tables.
4. Diff Japanese Rev0 vs RevA semantically, not only bytewise.
5. Establish safe free-space and relocation maps before any modification.
