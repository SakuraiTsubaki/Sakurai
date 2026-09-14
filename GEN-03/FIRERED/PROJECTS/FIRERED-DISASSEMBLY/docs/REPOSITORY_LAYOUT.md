# Repository Layout

This project is organized around a shared FireRed code/data base plus explicit language and revision differences.

```text
asm/                    Low-level assembly and still-unmatched routines
src/                    Decompiled C source
include/                Headers and shared declarations
constants/              Symbolic constants

data/
  pokemon/               Species data, evolutions, learnsets, Pokédex data
  moves/                 Move data
  items/                 Item data
  trainers/              Trainer classes, parties, AI-related data
  maps/                  Map metadata, events, scripts, connections
  text/                  Shared text tables and text-system data
  tilesets/              Tileset metadata, metatiles, attributes

graphics/
  pokemon/               Front/back sprites, icons, footprints, palettes
  trainers/              Trainer sprites and palettes
  overworld/             Object-event and overworld graphics
  tilesets/              Tileset source images and palettes
  interface/             UI, menus, battle interface, title/intro assets
  fonts/                 Font source images and glyph data

sound/
  songs/                 Music source data/MIDI where reconstructed
  sfx/                   Sound effects
  cries/                 Pokémon cry data
  samples/               Direct-sound and programmable-wave samples
  voicegroups/           Instrument/voice group definitions

text/
  ja/                    Japanese localization data
  en/                    English localization data
  fr/                    French localization data
  de/                    German localization data
  it/                    Italian localization data
  es/                    Spanish localization data

versions/
  jp_1_0/                Japanese 1.0 differences
  jp_rev1/               Japanese Rev 1 differences
  us_1_0/                English / USA 1.0 differences
  us_eu_rev1/            English / USA-Europe Rev 1 differences
  fr/                    French differences
  de/                    German differences
  it/                    Italian differences
  es/                    Spanish differences

tools/                   Extraction, conversion, build, and verification tools
scripts/                 Project automation
checksums/               Verified reference checksum manifests
reports/                 Reverse-engineering and reproducibility reports
tests/                   Regression and rebuild tests
```

## Rules

1. Full retail, modified, and rebuilt ROM images are never committed.
2. Reconstructed source assets are committed, including human-viewable PNG graphics.
3. Shared data stays shared; language/revision-specific differences are isolated explicitly.
4. No checksum is labeled canonical until it has been verified against the project's read-only reference ROM set.
5. A baseline is considered complete only after an independent repository-only build matches its verified reference output.
6. Raw binary fragments should be progressively replaced with documented source or structured assets wherever practical.
