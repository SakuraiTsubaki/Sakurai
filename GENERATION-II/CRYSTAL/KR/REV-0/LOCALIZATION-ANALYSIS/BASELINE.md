# GS Korean → Pokémon Crystal Korean — Fresh Baseline

## Scope

This directory is the research baseline for building a Korean Pokémon Crystal from the Japanese `Pocket Monsters - Crystal Version` ROM while using the officially released Korean Gold/Silver implementation as the Korean-system reference.

The target is **not** a text-copy of Korean Gold/Silver. Crystal's Japanese content, events, version-specific systems, maps, scripts, graphics, and unused data remain Crystal. Korean Gold/Silver provide the implementation reference for Hangul, text rendering, naming/input behavior, UI conventions, Korean-specific data handling, and portable graphics/assets where applicable.

## Canonical source identities

ROM binaries are read-only inputs and are never committed to GitHub.

| Role | Source label | Size | SHA-1 |
|---|---|---:|---|
| Korean implementation reference | `Pocket Monsters Geum (Korea).gbc` | 2,097,152 | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` |
| Korean implementation reference | `Pocket Monsters Eun (Korea).gbc` | 2,097,152 | `cb22d7e03a74dc3a563fde6be8626626b2b392e7` |
| Translation/content target | `Pocket Monsters - Crystal Version (Japan).gbc` | 2,097,152 | `95127b901bbce2407daf43cce9f45d4c27ef635d` |

These hashes are identity guards only. Every new analysis pass must recompute the ROM identity from the actual local input before extracting or changing data.

## Offset reset policy

All offsets, pointer maps, free-space claims, and text-slot assumptions from earlier localization attempts are **invalid as implementation inputs**.

The new workflow is:

1. identify the actual input ROM by hash and header;
2. scan its bank structure from the binary itself;
3. rediscover pointers/tables/signatures from the actual ROM;
4. classify references by subsystem;
5. build new extraction and reinsertion maps;
6. only then implement Korean text/graphics/system changes.

Old offsets may be kept only as historical comparison material and must never be copied into the new implementation without independent rediscovery and verification.

## Translation policy

- Japanese Crystal is the content/semantic source.
- Korean Gold/Silver are the Korean implementation-system source.
- Existing Korean Gold/Silver sentences are not mechanically copied into Crystal.
- Final Korean text should read naturally as if it had originally shipped in Crystal.
- Current natural Korean orthography and punctuation are used.
- Current official Korean names are preferred for Pokémon, moves, items, locations, characters, trainer classes, facilities, and system terminology.
- Crystal-only material is newly translated from the Japanese original while following the established Korean-system conventions.

## Sprite / graphics policy

Where technically portable, Korean Gold/Silver graphics are preferred over Crystal/RGBY legacy graphics for shared subjects. This includes Pokémon, trainers, characters, objects, UI graphics, fonts, icons, tiles, and related resources.

No graphic is copied blindly. Each asset must be checked against the target ROM's sprite dimensions, tile layout, palettes, compression, VRAM layout, animation assumptions, and calling code. Gold/Silver variants of the same subject must be compared rather than chosen arbitrarily.

Reusable transformed assets and patches belong in `SakuraiTsubaki/Tsubaki`; analysis, scripts, comparison tables, manifests, and validation reports belong in `SakuraiTsubaki/Sakurai`.

## Fresh analysis order

1. ROM identity + per-bank inventory
2. startup/title/intro control flow
3. Hangul font/glyph/code system in Korean Gold/Silver
4. Korean text renderer and control codes
5. name input and save-string handling
6. menu/UI text surfaces
7. Japanese Crystal text/pointer discovery
8. shared-name terminology table
9. Crystal-only text/event translation inventory
10. sprite/graphics extraction and structural comparison
11. Korean system integration into Crystal
12. relocation/far-pointer expansion where required
13. unused/dummy data audit and restoration candidates
14. regression + emulator/hardware-level validation

## Repository hierarchy

`GENERATION-II / CRYSTAL / KR / REV-0 / LOCALIZATION-ANALYSIS`

This is the first clean baseline for the new GS Korean → Crystal Korean lineage.
