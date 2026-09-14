# PocketMonsters-Ruby-Disassembly

Reproducible disassembly/decompilation workspace for **Pokémon Ruby**.

The goal of this repository is to reconstruct the game from editable source-form assets and code so that supported versions can eventually be rebuilt **without requiring a local source ROM**.

## Project goals

- Preserve original ROMs as read-only reference material outside Git.
- Reconstruct code as C/ASM and progressively eliminate opaque ROM-backed `incbin` regions.
- Extract and restore game data into editable source formats.
- Restore graphics as viewable assets (PNG where practical) plus palettes/tile data and conversion rules.
- Restore text, scripts, maps, events, Pokémon data, moves, items, trainers, encounters, and other tables.
- Restore music, cries, samples, and sound metadata in editable/rebuildable forms such as MIDI/WAV/source tables where practical.
- Track language- and revision-specific differences explicitly.
- Verify rebuilt ROMs against known hashes for each supported version.
- Keep generated ROM binaries out of Git.

## Target material

The project is designed to cover the available Pokémon Ruby language/revision set, including Japanese, English/USA/Europe, German, French, Italian, and Spanish releases and known revisions/debug variants represented by the project's verified source ROM set.

Version-specific material belongs under `config/versions/`, `data/versions/`, or another clearly scoped version directory rather than being duplicated without documentation.

## Repository policy

### Included

- C / ASM source
- linker/build configuration
- constants and headers
- structured game data
- maps and event scripts
- decoded text and character tables
- reconstructed graphics and palettes
- human-viewable sprite/graphics PNGs
- music/MIDI, cries/WAV, samples, and sound source data
- extraction/conversion/build/verification tools
- manifests, hashes, symbol maps, logs, documentation, and tests
- patches and other non-ROM reproducibility artifacts

### Not included

- original retail ROM images
- modified ROM images
- rebuilt/generated ROM images
- other complete game ROM binaries

Generated `.gba` files are build outputs only and must remain ignored by Git.

## Planned layout

```text
asm/                 low-level assembly and remaining reconstructed sections
src/                 decompiled C source
include/             headers
constants/           constants and IDs
data/                 structured game data
  versions/           language/revision-specific data
graphics/             reconstructed graphics, sprites, palettes, tiles
sound/                music, cries, samples, sound tables
maps/                 map/layout/event source where separated from data
text/                 decoded/localized text where separated from data
tools/                extraction, conversion, build and verification tools
config/versions/      per-version build configuration
manifests/            hashes, inventories and provenance manifests
symbols/              symbol/address maps
docs/                 reverse-engineering and format documentation
tests/                regression and rebuild verification
build/                generated files (ignored)
```

Directories will be populated as material is reconstructed; empty placeholder directories are intentionally avoided.

## Reproducibility target

For each supported version:

```text
repository source
      ↓ build
rebuilt .gba
      ↓ checksum verification
known reference hash
      ↓
byte-identical match
```

Until a version reaches a fully reconstructed state, its manifest should clearly identify unresolved regions and verification status.

## Status

### Phase 1 — source ROM inventory and structural survey ✅

- 13 source-ROM targets identified and hash-verified in `manifests/source_roms.json`.
- GBA headers and initial entry branches verified for every target.
- Large filler/data-island boundaries surveyed.
- Adjacent retail revisions compared byte-for-byte.
- Berry-glitch revision patch identified at Thumb-instruction level.
- English Rev 0/Rev 1 and German retail/debug established as distinct large-scale layout targets.
- Reproducible analyzer added at `tools/analyze_roms.py`.
- Results documented in `docs/ROM_STRUCTURE_PHASE1.md` and `manifests/rom_structure_phase1.json`.

### Phase 2 — symbolized reconstruction 🚧

- Startup/CRT anchors (`Start`, `Init`, `IntrMain`, `AgbMain`) mapped for all 13 targets.
- The full `main.c` startup/interrupt core from `AgbMain` through `ClearPokemonCrySongs` is boundary-mapped and fingerprinted: 22 functions × 13 targets = 286 verified function records.
- The next linked object is confirmed as `sprite.o`; `ResetSpriteData` starts immediately after `main.o`.
- Sprite Part 1 maps `ResetSpriteData` through `ContinueAnim`: 493 target/function records. Three layout families are required (`retail_intl`, `japan`, `german_debug`).
- Sprite Part 2 maps `AnimCmd_frame` through `InitSpriteAffineAnim`: 42 functions × 13 targets = 546 target/function records. All targets share one common function-size layout in this block.
- The contiguous mapped `sprite.o` prefix now reaches `SetOamMatrixRotationScaling`: `0x19F8` bytes in Japan, `0x1AE0` bytes in retail international builds, and `0x1AF8` bytes in German Debug.
- Reproducible analyzers and exact layouts/region fingerprints are stored under `tools/`, `symbols/`, and `docs/SPRITE_PHASE2_PART*.md`.

Current work: continue `sprite.c` at `SetOamMatrixRotationScaling`, then map sprite sheet/tile allocation, palette management, subsprites/OAM construction, and the remainder of `sprite.o` before moving into `text`, `string_util`, `link`, and `rtc`. Graphics/sprite assets will be restored separately as human-viewable PNGs plus rebuildable source data when visual asset extraction begins.
