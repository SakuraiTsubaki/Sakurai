# PocketMonsters-FireRed-Disassembly

Multi-language, multi-revision disassembly and decompilation of Pokémon FireRed, reconstructed for reproducible builds from source, graphics, text, audio, maps, and game data.

## Goal

This repository is being built so that supported Pokémon FireRed ROM revisions can be reconstructed from repository contents without requiring a local retail ROM as a build dependency.

The final ROM image is a build output and is **not** stored in this repository.

## Planned baselines

- Japanese 1.0
- Japanese Rev 1
- English / USA 1.0
- English / USA-Europe Rev 1
- French
- German
- Italian
- Spanish

Every baseline will be verified against the corresponding read-only reference ROM before being marked reproducible.

## Repository scope

The repository is intended to contain all non-ROM material required for reconstruction and analysis, including:

- C and assembly source
- build tools and scripts
- game data and constants
- maps and event scripts
- text and localization data
- Pokémon, trainer, UI, font, tileset, and other graphics
- palettes and graphics metadata
- music, sound-effect, cry, sample, and voice-group data
- version/revision differences
- checksum manifests and reproducibility reports
- extraction/reconstruction documentation and tests

Human-viewable source assets such as PNG graphics are retained alongside the data needed to rebuild them.

## ROM policy

Retail, modified, and rebuilt `.gba` ROM images are not committed. Reference ROMs remain external, read-only verification inputs during reverse engineering only; the completed repository must not require them for normal reconstruction.

## Reproducibility rule

A version is complete only when the repository can rebuild it independently and the generated output matches the verified reference checksum for that exact language/revision.

Checksum values will be added only after they have been verified against the project's reference ROM set.

## Status

Initial repository structure. Asset extraction, source reconstruction, version mapping, and byte-perfect verification are in progress.
