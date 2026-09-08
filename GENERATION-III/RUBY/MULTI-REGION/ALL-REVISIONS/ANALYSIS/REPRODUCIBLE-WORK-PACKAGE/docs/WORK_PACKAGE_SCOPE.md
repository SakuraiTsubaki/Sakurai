# Work Package Scope

## Principle

Every byte of every supplied ROM is accounted for by the 64 KiB page fingerprint table. No original ROM byte is stored in this GitHub-safe package.

## Reproducible layers

1. **Identity layer** — immutable hashes, exact file size, GBA cartridge header and complement check.
2. **Address layer** — page-level fingerprints spanning offset `0x00000000` through EOF with no gaps.
3. **Revision layer** — contiguous changed ranges between every same-language revision pair.
4. **Compression layer** — validated GBA BIOS-LZ77 (`0x10`) candidates.
5. **Pointer layer** — deterministic scanner for 32-bit GBA ROM pointers in `0x08000000 + file_offset` space.
6. **Round-trip layer** — split and reassemble without byte changes.
7. **Regression layer** — rerun all checks from the original ROM folder.

## Next semantic layers

- ARM/Thumb function discovery and symbol map
- script/event opcode recovery
- text table/encoding extraction
- map header/layout/event/connection tables
- species/moves/items/trainer/battle parameter tables
- graphics, tilesets, palettes, sprites and animation tables
- sound/M4A sequence and sample tables
- save-block structures and checksums
- cross-language pointer/table relocation map
- revision-specific bug-fix map

These layers should reference ROM IDs and offsets from `manifests/roms.json`, never opaque filenames alone.
