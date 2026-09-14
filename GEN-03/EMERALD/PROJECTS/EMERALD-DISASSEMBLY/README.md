# PocketMonsters-Emerald-Disassembly

Disassembly and reconstruction project for Pokémon Emerald, preserving regional and language variants as reproducible source, data, graphics, text, audio, maps, and scripts. ROM binaries are not included.

## Goal

Reconstruct each supported Pokémon Emerald release from repository source and extracted/recovered assets, without requiring a committed or bundled base ROM. Local reference ROMs may be used during reverse-engineering and verification, but they are never committed.

Target workflow:

```text
repository source + assets + tools
              ↓
             build
              ↓
        reconstructed ROM
              ↓
byte/hash verification against reference ROM
```

## Reference set

The current reference set covers Japanese, English, French, German, Italian, and Spanish releases. Exact hashes and GBA header metadata are recorded in `manifests/roms.json`.

The two currently supplied English files, `(U)` and `(USA, Europe)`, are byte-identical and share the same hashes.

## Repository policy

- ROM binaries are never committed.
- Disassembly/decompilation source, scripts, documentation, manifests, extracted/recovered graphics, text, audio, maps, data, and verification outputs are repository material.
- Human-readable/editable source forms are preferred over opaque binary blobs whenever practical.
- Sprite and graphics work should include viewable image assets such as PNG files alongside conversion metadata.
- Every reconstructed target must eventually be verified byte-for-byte or by exact cryptographic hash against its reference ROM.

## Planned layout

```text
asm/          low-level assembly and unresolved code/data
src/          reconstructed C source where applicable
include/      headers and declarations
constants/    symbolic IDs and constants
data/         structured game data
graphics/     sprites, tiles, palettes, UI and other graphics
text/         game text and text metadata
sound/        music, SFX, cries, samples and sound tables
maps/         maps, layouts, events and map scripts
tools/        extraction, conversion, build and verification tools
manifests/    reference ROM metadata and reconstruction manifests
docs/         reverse-engineering notes and project documentation
tests/        regression and reproducibility tests
build/        generated output (ignored by Git)
```

## Status

Phase 1 is in progress.

- all seven supplied ROM files have been identified and hashed; the two English inputs are byte-identical, leaving six unique release payloads
- the complete 16 MiB address space has an initial 64 KiB cross-release comparison map
- Block 00 (`0x000000-0x00FFFF`) has its first semantic anchors: GBA cartridge header, Game Freak metadata header at `0x100-0x203`, and executable startup at `0x204`
- the Game Freak metadata header has been decoded for every unique release and now supplies direct roots for Pokémon names, move names, species data, abilities, items, battle moves, sprites, palettes, icons and Poké Ball graphics
- reproducible block-analysis and metadata-header extraction tools are in `tools/`

Next work follows those roots into structured text/gameplay tables and graphics, while executable lifting continues through the remaining Block 00 code. Every extracted structure is checked across all six unique releases before reconstruction work depends on it.
