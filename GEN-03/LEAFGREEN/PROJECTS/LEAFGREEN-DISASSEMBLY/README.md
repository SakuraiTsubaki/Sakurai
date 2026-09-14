# PocketMonsters-LeafGreen-Disassembly

A complete disassembly and reconstruction project for **Pokémon LeafGreen**, preserving the game's code, data, graphics, text, audio, maps, scripts, and other assets in rebuildable source form.

> **ROM binaries are not included.**

## Goals

- Reconstruct Pokémon LeafGreen from readable, editable source and asset files.
- Eliminate dependency on a local retail `baserom.gba` for normal builds wherever technically possible.
- Preserve original game behavior and data for historical/reference targets.
- Support byte-accurate verification against known original ROM hashes.
- Separate common content from language-, region-, and revision-specific differences.
- Keep graphics, text, audio, maps, scripts, and structured game data in disassembly/decompilation-friendly formats.

## Target ROMs

| Target | Game code | Region / language |
|---|---|---|
| `japan` | `BPGJ` | Japan / Japanese |
| `usa` | `BPGE` | USA / English |
| `europe_rev1` | `BPGE` | Europe Rev 1 / English |
| `germany` | `BPGD` | Germany / German |
| `france` | `BPGF` | France / French |
| `italy` | `BPGI` | Italy / Italian |
| `spain` | `BPGS` | Spain / Spanish |

Original ROMs are used only as local read-only analysis and verification references. They are never committed to this repository.

## Repository policy

The repository may contain reconstructed or extracted project material required to understand and rebuild the game, including:

- C and ARM/Thumb assembly source
- symbols, labels, address maps, and linker data
- structured Pokémon, move, item, trainer, encounter, and map data
- event and field scripts
- readable text source
- graphics source such as PNG images, palettes, tilesets, tilemaps, icons, sprites, fonts, and UI assets
- audio source such as MIDI/sequencing data, WAV samples, cries, voicegroup data, and sound tables
- build tools, converters, extractors, verification tools, and tests
- manifests, analysis reports, checksums, and reconstruction metadata

Full original, modified, or rebuilt retail ROM binaries are excluded from version control.

## Intended build model

```text
source + data + graphics + text + audio + maps + scripts
                         |
                         v
                  build toolchain
                         |
                         v
                  LeafGreen ROM
                         |
                         v
                 hash verification
```

The long-term goal is for a fresh clone of this repository, together with the documented toolchain, to be sufficient to rebuild supported targets without requiring a local source ROM.

## Planned layout

```text
asm/            low-level ARM/Thumb assembly
src/            decompiled/reconstructed C source
include/        headers and shared definitions
constants/      symbolic constants
config/         target-specific build configuration
data/           structured game data
graphics/       editable graphics source and palettes
text/           shared and target-specific text source
sound/          music, samples, cries, and audio tables
maps/           map-side source where appropriate
scripts/        event/script source where appropriate
tools/          extraction, conversion, build, and verification tools
symbols/        symbol/address maps
analysis/       ROM layout and reverse-engineering records
tests/          rebuild and regression verification
```

The exact layout will evolve as the ROM is mapped and reconstructed.

## Reconstruction workflow

1. Identify and fingerprint each read-only reference ROM.
2. Map the full ROM address space.
3. Classify code, structured data, text, graphics, audio, maps, scripts, padding, and unknown regions.
4. Extract and restore assets into editable source formats.
5. Replace opaque ROM-range dependencies with named source/data/assets.
6. Rebuild each target.
7. Compare the generated image against the corresponding known reference hash.
8. Repeat until every region is understood or intentionally documented.

## Asset principles

Human-viewable source assets are preferred where practical. Pokémon sprite work should retain PNG source images alongside metadata and build rules required to reproduce the in-ROM representation. Identical assets shared across versions should be deduplicated when doing so does not alter target output.

## Status

Repository initialized. Full ROM mapping and reconstruction are in progress.
