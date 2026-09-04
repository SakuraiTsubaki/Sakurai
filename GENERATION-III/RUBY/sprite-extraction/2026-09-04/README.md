# Pokemon Ruby sprite extraction — 2026-09-04

## Scope

13 supplied Pokemon Ruby GBA ROMs were inspected: Japanese, English/European revisions, German including debug, French, Italian, and Spanish revisions.

The original ROM files are not stored in this repository.

## Confirmed sprite layers extracted

- Pokemon battle front sprites: 440 internal slots
- Pokemon battle back sprites: 440 internal slots
- Pokemon normal palettes: 440
- Pokemon shiny palettes: 440
- Pokemon menu icons: 440 internal slots, 2 rendered frames per slot
- Pokemon footprints: 413 slots
- Trainer front sprites: 83 slots
- Trainer back sprites: 3 slots (Brendan, May, Wally), 4 frames each
- Overworld/object-event graphics IDs: 218
- Valid object-event graphics-info records: 213
- Overworld frames extracted: 1,563

Both raw graphics/palette data and rendered PNG previews were generated for the confirmed layers.

## Catch-all compressed graphics census

A secondary 4-byte-aligned GBA LZ77 scan was run to avoid silently missing compressed graphical assets outside the primary sprite tables.

Criteria: decompressed size 128..0x20000 bytes and divisible by 32.

- Unique decompressed candidate blocks across all 13 ROMs: 1,970
- Japanese Ruby candidates: 1,676
- Each non-Japanese Ruby in this set: 1,665

The catch-all layer intentionally includes sprite-like graphics plus some UI/background/tilemap data. Raw decompressed binary is authoritative; generic PNG previews are heuristic.

## Cross-version result

All 12 non-Japanese Ruby ROMs in this set are byte-identical at the confirmed core sprite-content layer. Their table offsets vary by localization/revision.

Japanese Ruby confirmed core differences versus USA Ruby:

- Pokemon internal slot 124 (Jynx): normal palette differs
- Pokemon internal slot 124 (Jynx): shiny palette differs
- Pokemon internal slot 124 (Jynx): icon raw graphics differs
- Trainer front index 20: Hex Maniac differs
- Trainer front index 46: Sailor differs
- Trainer front index 55: Cooltrainer M differs
- Trainer front index 62: Psychic F differs
- Icon palette-table entries 3, 4, and 5 differ, but normal species icon indices in this ROM set use only palette indices 0, 1, and 2

Pokemon front/back raw battle tile graphics, footprints, trainer palettes, trainer backs, and overworld/object-event graphics are otherwise identical at the confirmed comparison layer.

## Local generated archive

`ruby_all_sprites_extracted.tar.gz`

SHA-256: `88bdc41235d210b78c93db07b9663f8fe26653c35be97da10564be613070c84e`

The bulk binary asset archive is intended for the private `Tsubaki` asset repository; this public repository contains analysis/offset/comparison records only.
