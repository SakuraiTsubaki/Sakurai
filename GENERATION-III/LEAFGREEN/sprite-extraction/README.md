# Pokémon LeafGreen sprite extraction

Full sprite/graphics extraction census for the seven supplied Pokémon LeafGreen ROM variants.

## Versions

- `jp_rev0` — BPGJ v0
- `de_rev0` — BPGD v0
- `es_rev0` — BPGS v0
- `en_eu_rev1` — BPGE v1
- `en_us_rev0` — BPGE v0
- `fr_rev0` — BPGF v0
- `it_rev0` — BPGI v0

## Classified sprite families

Each version produced 4,473 classified records:

- Pokémon battle front / normal: 444
- Pokémon battle front / shiny: 444
- Pokémon battle back / normal: 444
- Pokémon battle back / shiny: 444
- Pokémon icons: 440
- Pokémon footprints: 413
- Trainer battle sprites: 148
- Item icons: 376
- Overworld object-event frames: 1,320

The battle count is larger than 440 because a small number of table entries contain multi-frame decompressed sheets; every decompressed frame is retained rather than truncating to the nominal table size.

## Completeness census

In addition to the named tables, every valid GBA LZ77 block was scanned and deduplicated per ROM. Likely 4bpp graphics and 16-color palette payloads were retained as a raw graphics census so non-table UI/effect graphics are not silently missed.

Valid LZ77 blocks by version:

- jp_rev0: 4,217
- de_rev0: 4,192
- es_rev0: 4,205
- en_eu_rev1: 4,206
- en_us_rev0: 4,194
- fr_rev0: 4,195
- it_rev0: 4,207

## Output policy

Binary image assets belong in `SakuraiTsubaki/Tsubaki`; analysis, offsets, manifests, hashes, and extraction methodology belong here in `Sakurai`.

Original ROM images are never included in either repository or generated payload.
