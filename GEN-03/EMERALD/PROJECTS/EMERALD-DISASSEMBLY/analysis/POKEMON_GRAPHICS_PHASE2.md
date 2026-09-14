# Pokémon graphics extraction — Phase 2

This phase follows the Game Freak ROM header roots for Pokémon front sprites, back sprites, normal/shiny palettes, icons, icon palette IDs, and icon palette descriptors across the six unique Emerald releases.

## Table shape

- 440 graphics slots total.
- Slots 0–412 cover the normal internal range through `SPECIES_EGG`.
- Slots 413–439 are Unown B–Z, `!`, and `?`.
- Front/back/palette descriptor tables use 8-byte entries.
- Icon pointer table uses 440 32-bit pointers.
- Icon palette-ID table uses 440 bytes.
- Only icon palettes 0–2 are real palettes. Descriptor entries 3–5 are unused and do not point to valid palette data.

## Decoded formats

- Standard animated front sprite: 64×128 4bpp (two 64×64 frames), LZ77-compressed in ROM.
- Standard back sprite: 64×64 4bpp, LZ77-compressed.
- Icon: 32×64 4bpp (two 32×32 frames), stored uncompressed.
- Normal/shiny species palette: 16 BGR555 colors (32 bytes), LZ77-compressed.
- Castform slot 385 is special: its graphics/palette payloads contain multiple forms, so the decoded byte lengths are larger than the standard entries.

## Cross-release verification

Front and back pixel data, including the exact LZ77 streams and descriptor size/tag fields, are identical in JPN, ENG_USA_EUR, FRA, DEU, ITA, and ESP.

The only used species-graphics regional difference found in these roots is slot 124, Jynx:

- JPN normal palette differs from the western releases.
- JPN shiny palette differs from the western releases.
- JPN icon graphics differ from the western releases.
- ENG_USA_EUR, FRA, DEU, ITA, and ESP share the same western Jynx data.

The icon palette-ID table is identical in all six releases and only uses palette IDs 0, 1, and 2. Those three real icon palettes are also identical in all six releases. The remaining three descriptor entries are unused/invalid, matching the decompilation source documentation.

## Deduplication

For the JPN reference set, 440 slots collapse to 416 unique rendered front-normal PNGs, 416 front-shiny PNGs, 416 back-normal PNGs, 416 back-shiny PNGs, and 416 icon PNGs. Normal and shiny species palettes each collapse to 383 unique payloads in JPN; including the western Jynx override makes 384 unique payloads across all releases.

Identical assets should therefore be stored once and referenced by the slot map rather than duplicated by language or slot.

## Repository policy

The repository stores editable/viewable PNG outputs, structured manifests, exact hashes, extraction tools, and regional overrides. ROM binaries are never committed. Preview atlases are provided so the complete 440-slot corpus can be inspected directly on GitHub.
