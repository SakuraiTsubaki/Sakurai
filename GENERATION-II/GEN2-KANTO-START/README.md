# GEN2 Kanto Start

## Project premise

GEN2 Kanto Start is a Generation II based project in which a new adventure begins in Kanto. Generation I RGBY Kanto is expanded and ported into Generation II GSC Kanto, preserving both the larger Generation I structures and the additional Generation II content as one integrated RGBYGSC Kanto.

## Fixed principles

- New Game begins in Generation II Kanto.
- RGBY Kanto is expanded into GSC Kanto rather than replacing it.
- Preserve all original content and integrate version differences.
- Never shrink a larger map or structure to match a smaller one.
- Preserve all events, NPCs, objects, interactions, rooms, floors, passages, facilities, hidden items, signs, trainers, warps, and version-specific elements.
- Restore Generation I spaces removed or reduced in GSC while retaining all GSC additions.
- Keep the Generation II day/time system, but remove day/time access restrictions from content.
- Convert verified official external/distribution events into in-game events while preserving their original theme and conditions as much as possible.
- Before map edits, inspect original tilesets, tile graphics/sprites, block/metatile data, palettes, attributes, collisions, map data, event data, and ROM bank layout.
- Do not grow data in place when it would overwrite neighboring ROM data. Relocate safely to verified unused space or additional banks; expand the ROM if necessary.
- Distinguish RGB, Yellow, Gold/Silver, Crystal, external-event, and project-integration changes in documentation.
- Validate every integration through real gameplay: warps, collision, NPCs, flags, trainers, items, day/time behavior, external-event conversions, map connections, save/load.

## Working order

Original research -> RGBY comparison -> GSC comparison -> version-difference inventory -> tileset/tile-sprite research -> map size/structure comparison -> choose larger/combined structure -> restore removed space -> integrate GSC additions -> NPC/object inventory -> event inventory -> external-event research -> remove day/time access restrictions -> data-size check -> ROM-bank analysis -> secure safe free banks -> relocate/integrate data -> fix pointers -> verify warps/collision/events -> gameplay verification.

## Repository role

This repository stores analysis, inventories, comparison reports, map/event research, technical notes, validation logs, and documentation for GEN2 Kanto Start.

Implementation source, scripts, patches, generated work assets, and other project build materials belong in the matching `GENERATION-II/GEN2-KANTO-START/` path of the private `SakuraiTsubaki/Tsubaki` repository.

Original commercial ROM images are not committed to GitHub.
