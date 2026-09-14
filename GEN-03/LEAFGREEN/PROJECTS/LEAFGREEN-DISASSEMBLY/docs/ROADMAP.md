# Reconstruction Roadmap

## Phase 0 — Repository baseline

- [x] Initialize repository policy and scope.
- [x] Exclude retail/rebuilt ROM images from version control.
- [x] Record supported LeafGreen targets and known reference SHA-1 values.
- [ ] Establish reproducible toolchain versions.
- [ ] Add automated target/hash verification scaffolding.

## Phase 1 — Full ROM survey

Survey every supported 16 MiB ROM from `0x000000` through `0xFFFFFF` and classify ranges as:

- ARM/Thumb code
- structured game data
- text / string tables
- graphics / palettes / tiles / tilemaps
- maps / events / scripts
- audio / music / samples / cries / voicegroups
- pointer tables
- compressed data
- padding / alignment
- unknown / unresolved

The Japanese ROM is the primary structural reference. Regional and revision variants are compared in parallel so common ranges can be shared and true differences isolated.

### Required outputs

- ROM-wide address map per target
- common-vs-version-specific range map
- pointer/reference map
- function and data symbol tables
- unresolved-region manifest
- checksums for extracted/reconstructed assets

## Phase 2 — Reconstruction by region

For each classified ROM range:

1. assign a stable symbol or asset identity;
2. extract or rewrite it into a disassembly/decompilation-friendly format;
3. document source range, compression, alignment, and references;
4. add rebuild rules;
5. verify rebuilt bytes against the reference target;
6. eliminate opaque source-ROM dependencies where possible.

Temporary raw range inclusion is allowed only as a tracked intermediate state. The final goal is a semantic source/data/asset representation.

## Phase 3 — Assets

### Graphics

- Pokémon front/back sprites
- icons and footprints
- trainer front/back sprites
- overworld sprites
- tilesets and tilemaps
- battle backgrounds and interfaces
- UI/menu graphics
- fonts
- palettes

Human-viewable PNG source should be kept where practical. Identical assets across targets should be deduplicated when this preserves exact rebuild output.

### Text

- dialogue and map text
- system/menu text
- Pokémon/move/item/trainer names
- Pokédex text
- descriptions and help text
- language-specific charmaps and font relationships

### Audio

- song sequences / MIDI-equivalent sources
- sound effects
- direct sound samples
- cries
- voicegroups
- song/player tables

### Maps and scripts

- map layouts
- connections
- events
- object definitions
- scripts
- warps
- triggers
- encounters

## Phase 4 — Source reconstruction

- identify ARM/Thumb functions and calling relationships;
- name globals, constants, structs, tables, and subsystems;
- progressively translate appropriate code to C while preserving matching behavior;
- retain assembly where it is the clearest exact representation;
- maintain symbols for every understood address.

## Phase 5 — Independent rebuild

Target end state:

```text
fresh clone
   + documented toolchain
   + repository source/assets
          |
          v
       make <target>
          |
          v
   rebuilt LeafGreen image
          |
          v
      SHA-1 verify
```

No local retail source ROM should be required for the normal final build.

## Phase 6 — Multi-version completion

Complete and verify:

- Japan / Japanese (`BPGJ`)
- USA / English (`BPGE`)
- Europe Rev 1 / English (`BPGE`)
- Germany / German (`BPGD`)
- France / French (`BPGF`)
- Italy / Italian (`BPGI`)
- Spain / Spanish (`BPGS`)

Each target must document all intentional divergences from the shared source tree.
