# Pokémon Red — Bank-by-bank audit + disassembly pipeline

## Fixed rule
Every bank is investigated and disassembled in the same pass. A bank is not marked complete merely because bytes were compared.

Pipeline per bank:
1. Preserve the original 16 KiB bank bytes and SHA-1.
2. Generate a lossless `db` skeleton locally.
3. Generate an LR35902 linear decode listing as a discovery aid.
4. Identify code/data/pointer/text/gfx/audio/map boundaries.
5. Trace direct and banked references; assign per-ROM labels.
6. Map semantic equivalents across JP Rev0, JP RevA, EN, DE, FR, IT, ES.
7. Replace raw regions with typed semantic source only when boundaries are verified.
8. Round-trip check the bank and eventually the whole ROM byte-for-byte.

## Current state
- Unique ROMs: 7. The second English upload is byte-identical and retained only as an inventory duplicate.
- Bank instances: 384 total (JP Rev0 32 + JP RevA 32 + five international ROMs × 64).
- Lossless local bank skeletons: 384/384 generated.
- LR35902 discovery listings: 384/384 generated.
- Skeleton round-trip verification: 384/384 PASS.
- Bank 00 semantic seeding: started on all 7 ROMs.
- Bank 00 EN semantic baseline: pret/pokered Home layout and symbols are used only as a reference; each uploaded ROM is mapped independently.
- 126 Bank 00 EN anchors were tested against other ROMs using normalized opcode-pattern signatures.
  - JP Rev0: 119/126 candidate mappings.
  - JP RevA: 119/126 candidate mappings.
  - DE/FR/IT/ES: 125/126 candidate mappings each.
- Candidate mappings are not considered final labels until control-flow/context checks confirm them.

## Bank 00 observations
International releases retain many Home routine addresses, while Japanese Red places numerous equivalent routines at different offsets. For example, the EN `DisableLCD` routine at `$0061` has a strong opcode-pattern candidate at `$0167` in both JP ROM revisions. This demonstrates why absolute-address copying is forbidden.

The English Home bank reference layout includes LCD/copy primitives, startup and joypad handling, map/overworld logic, Pokémon and sprite helpers, text and VRAM routines, interrupt/audio/serial logic, menus and inventory, trainer/map helpers, bank switching, generic utilities, RNG/predefs, hidden events, and predef text dispatch.

## Repository rule
Full raw byte skeletons and complete raw linear listings are ROM-equivalent derivatives, so they remain local and are not committed. GitHub receives the disassembler, mapping/verification tools, manifests, semantic maps, reports, and progressively reconstructed source that is safe to publish.

## Completion definition for each bank
A bank reaches `SEMANTIC_COMPLETE` only when:
- code/data boundaries are classified;
- all reachable code is decoded and labeled;
- pointer/reference structures are resolved;
- known tables/assets/text blocks are typed;
- cross-version semantic mapping is recorded;
- unresolved bytes are explicitly documented;
- byte-exact round-trip succeeds.
