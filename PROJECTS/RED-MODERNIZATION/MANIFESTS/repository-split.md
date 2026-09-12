# RED-MODERNIZATION repository split

Canonical pair contract for the RED project.

## Sakurai owns

- official release and exact dump identity
- hashes, cartridge/header observations, bank structure and comparisons
- text/data/maps/events/disassembly/symbol research
- bug, glitch, unused/dummy and verification reports
- modernization crosswalks, design decisions, source/target locks and test evidence

Canonical source root:

`LIBRARY/GEN-01/GB/RED/`

Canonical project root:

`PROJECTS/RED-MODERNIZATION/`

## Tsubaki owns

- production graphics, sprites, palettes, fonts, icons, tilesets, UI and audio
- converted and modernized assets
- target-specific implementation inputs/outputs
- patches, build tooling and generated build artifacts that are appropriate to publish

Canonical project root:

`PROJECTS/RED-MODERNIZATION/`

## Shared identity

The repositories must use the same RELEASE-ID, COMPARISON-ID, PROJECT-ID and TARGET-ID. Repository responsibility changes; identity never does.

## ROM boundary

Original ROM binaries and byte-exact whole-ROM/whole-bank payload archives are never committed. Hashes, derived structure, reproducible tools, semantic annotations, patches and permissible derived assets may be committed with provenance.
