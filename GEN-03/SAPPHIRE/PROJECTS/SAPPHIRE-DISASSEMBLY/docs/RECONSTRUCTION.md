# Reconstruction Plan

## End state

A clean clone of this repository, plus the documented build toolchain, must be sufficient to generate each supported Pokémon Sapphire ROM target. No local retail ROM is a required build input.

Retail ROMs are used only during analysis and verification. They are never committed.

## Source-reconstruction rule

Whenever practical, ROM content is converted into an editable, meaningful source format rather than retained as anonymous binary blobs.

Examples:

- ARM/Thumb code -> C and/or assembly with symbols
- tables -> C/assembly/CSV/YAML as appropriate
- event logic -> script source
- dialogue and system text -> text/script source with charmap support
- Pokémon/trainer/UI graphics -> PNG + palette/metadata
- tilesets -> PNG/tiles + palettes + tilemaps/layout metadata
- maps -> structured map/layout/event sources
- fonts -> glyph images + charmap/encoding metadata
- music -> sequence/MIDI-style sources + voicegroups/samples
- SFX/cries -> sequence/sample source as appropriate
- compressed assets -> editable source plus deterministic conversion rules

Raw blobs may be used temporarily only while an area is not yet understood. Every temporary blob must retain an address/size/hash provenance record and should eventually be replaced by meaningful source.

## Multi-version strategy

Shared code/data should remain shared. Regional, language, and revision differences should be represented explicitly through target configuration, conditional assembly/build rules, or target-specific source overrides.

Initial target IDs are defined in `config/versions.yml`.

## Reconstruction phases

1. **Identity and header map**
   - Verify file hashes, sizes, GBA header fields, game code, and software version.
   - Establish target IDs and expected output hashes.

2. **ROM address map**
   - Partition every target into code, data, pointer tables, text, graphics, audio, maps, free/padding space, and unknown regions.
   - Record cross-version identical and divergent ranges.

3. **Executable disassembly/decompilation**
   - Recover ARM/Thumb functions, labels, calling relationships, literal pools, jump tables, and linker placement.
   - Replace anonymous assembly with C where byte-identical recompilation is practical.

4. **Game data reconstruction**
   - Pokémon, moves, items, trainers, encounters, shops, evolutions, Pokédex data, battle data, and other tables.

5. **Text and localization reconstruction**
   - Charmaps, fonts, control codes, pointer structures, scripts, names, dialogue, and per-language assets.

6. **Graphics reconstruction**
   - Pokémon, trainers, overworld sprites, tilesets, backgrounds, UI, fonts, battle effects, intro/credits, palettes, and tilemaps.

7. **Map and event reconstruction**
   - Layouts, connections, warps, objects, triggers, scripts, encounters, and version-specific differences.

8. **Audio reconstruction**
   - Song tables, sequences, voicegroups, samples, SFX, cries, and deterministic conversion/build rules.

9. **Byte-identical build verification**
   - Build each target without a base ROM.
   - Compare full output hashes with `config/versions.yml`.
   - Track any remaining mismatching ranges until zero differences remain.

## Verification requirements

For every reconstructed region or asset, record:

- target(s)
- ROM offset/range
- source type
- extracted/reconstructed file path
- original range hash
- rebuilt range hash
- verification state
- notes on cross-version identity/differences

The final acceptance criterion for a target is a full byte-for-byte match against its recorded retail SHA-256.
