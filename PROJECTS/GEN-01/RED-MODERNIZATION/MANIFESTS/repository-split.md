# RED v6 repository split

## Sakurai owns

- Official release identity and exact dump identity.
- Hashes, cartridge/header observations, bank structure and comparisons.
- Text/data/maps/events/disassembly/symbol research.
- Bug, glitch, unused/dummy research and verification evidence.
- Modernization crosswalks, design decisions, source locks and tests.

Canonical research source root: `LIBRARY/GEN-01/RED/`.
Canonical research project root: `PROJECTS/GEN-01/RED-MODERNIZATION/`.

## Tsubaki owns

- Release-provenanced extracted/normalized production resources.
- Graphics, sprites, palettes, fonts, icons, tilesets, UI and audio.
- Converted/modernized assets, target implementation, patches and builds.

Canonical production project root: `PROJECTS/GEN-01/RED-MODERNIZATION/`.

## Pair invariant

Both repositories use identical `GEN-01`, `RED`, `GB`, `CART`, RELEASE-ID, DUMP-ID, COMPARISON-ID, PROJECT-ID and TARGET-ID values.

## ROM boundary

Original ROM binaries and byte-exact whole-ROM/whole-bank payload archives are never committed. Hashes, derived structure, reproducible tools, semantic annotations, patches and permissible derived assets may be committed with provenance.
