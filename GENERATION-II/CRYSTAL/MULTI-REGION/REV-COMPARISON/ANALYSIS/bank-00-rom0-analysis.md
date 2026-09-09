# Bank 00 (ROM0) — 7-ROM semantic analysis

## Scope

Bank 00 is the fixed 16 KiB ROM0 window (`$0000-$3FFF`). In the exact English semantic source it contains the reset/RST/interrupt vectors, cartridge header, and the resident `Home` engine. The English source's `home.asm` includes initialization, VBlank/LCD/serial/joypad handlers, decompression, graphics/text/video helpers, map-object helpers, movement/menu/printer code, game time/map/farcall/predef/window/flag/string/item/random/SRAM/math/text/tilemap/name/trainer/Pokémon/battle/audio/mobile routines, among others.

## Structural ranges

| Range | Meaning | EN0→EN1 | JP0 vs EN0 | ES0 vs EN0 | DE0 vs EN0 | FR0 vs EN0 | IT0 vs EN0 |
|---|---|---:|---:|---:|---:|---:|---:|
| `$0000-$0067` | reset/RST/interrupt vectors | 0 | 2 | 2 | 2 | 2 | 2 |
| `$0100-$014F` | entry/logo/header | 4 | 7 | 4 | 4 | 4 | 4 |
| `$0150-$3FFF` | Home engine | 0 | 13636 | 11854 | 11818 | 11764 | 11674 |

The apparent regional volume inside `Home` is large; it is not safe to model DE/IT Bank 00 as an English binary with only a few text substitutions. Semantic symbol lifting is required.

## Vector table

The seven ROMs use the same vector opcodes and differ only in two JP/EU target addresses within `$0000-$0067`.

| Vector | EN0/EN1 | JP0 | ES0 | DE0 | FR0 | IT0 | Semantic anchor |
|---|---:|---:|---:|---:|---:|---:|---|
| Reset `$0000` | `di; jp $0100` | same | same | same | same | same | entry point |
| RST `$08` | `jp $2D63` | `$2D35` | `$2D41` | `$2D4D` | `$2D44` | `$2D45` | `FarCall` → `FarCall_hl` |
| RST `$10` | same bytes | same | same | same | same | same | fixed helper |
| VBlank `$0040` | `jp $0283` | same | same | same | same | same | VBlank |
| LCD `$0048` | `jp $0552` | same | same | same | same | same | LCD |
| Timer `$0050` | `jp $3E93` | `$3E20` | `$3E61` | `$3E7D` | `$3E64` | `$3E81` | `MobileTimer` |
| Serial `$0058` | `jp $06EF` | same | same | same | same | same | Serial |
| Joypad `$0060` | `jp $092E` | same | same | same | same | same | Joypad |

This is strong evidence that the vector ABI is preserved across all seven releases while resident routine addresses move inside ROM0.

## Cartridge header (`$0100-$014F`)

| ROM | Title | Manufacturer code | RAM code | Destination | Version | Header checksum | Global checksum |
|---|---|---|---:|---:|---:|---:|---:|
| JP0 | `PM_CRYSTAL` | `BXTJ` | `$05` | `$00` | 0 | `$22` | `$9A40` |
| EN0 | `PM_CRYSTAL` | `BYTE` | `$03` | `$01` | 0 | `$27` | `$129F` |
| EN1 | `PM_CRYSTAL` | `BYTE` | `$03` | `$01` | 1 | `$26` | `$18D2` |
| ES0 | `PM_CRYSTAL` | `BYTS` | `$03` | `$01` | 0 | `$19` | `$42F4` |
| DE0 | `PM_CRYSTAL` | `BYTD` | `$03` | `$01` | 0 | `$28` | `$4982` |
| FR0 | `PM_CRYSTAL` | `BYTF` | `$03` | `$01` | 0 | `$26` | `$F2E2` |
| IT0 | `PM_CRYSTAL` | `BYTI` | `$03` | `$01` | 0 | `$23` | `$DBBA` |

All releases use CGB flag `$C0`, new licensee `01`, cartridge type `$10` (MBC3 + timer + RAM + battery), and ROM size code `$06` (2 MiB). JP uniquely declares RAM code `$05` and destination `$00`; the six non-Japanese releases declare RAM `$03` and destination `$01`.

## English Rev 0 → Rev A

Bank 00 has exactly four changed bytes, all in the header:

- `$014C`: version `00 → 01`
- `$014D`: header checksum `27 → 26`
- `$014E-$014F`: global checksum `129F → 18D2`

No byte in `$0000-$014B` or `$0150-$3FFF` changes. Therefore Bank 00 contains **no executable Home-engine revision change** between the two English revisions.

## Reconstruction implications

1. Lift vector symbols first; the region-specific jump targets give fixed anchor points for `FarCall_hl` and `MobileTimer` in DE/IT.
2. Reconstruct the Home engine by function/signature alignment, not by raw linear disassembly. The exact EN/JP/ES/FR semantic sources provide four independent symbolized references.
3. Keep the header as region/revision-specific generated data. EN Rev A can share all Bank 00 code with EN Rev 0 and differ only in header metadata/checksums.
4. After every semantic replacement, verify the complete 16 KiB Bank 00 against the local ROM, then later verify the whole-ROM SHA-1.

## Current status

- Byte accounting: complete for all seven ROMs.
- Vector semantics: identified.
- Header semantics: identified and verified.
- EN0/EN1 semantic source: exact upstream anchor.
- JP0 semantic source: exact upstream anchor.
- ES0 semantic source: exact upstream anchor.
- FR0 semantic source: exact upstream anchor.
- DE0/IT0: semantic symbol lifting pending for the `$0150-$3FFF` Home engine.

## Integrated disassembly pass (new workflow)

Bank 00 is now being processed under the combined **census + disassembly** rule. A conservative LR35902 recursive control-flow decoder was run from trusted ROM0 entry points first, then a second provisional pass added frequently referenced ROM0 `CALL/JP` targets (>=5 raw references) as heuristic seeds. The heuristic pass is useful for code discovery but does **not** by itself prove code/data boundaries; exact semantic sources and byte reconstruction remain the authority.

| ROM | Heuristic seeds | Decoded instructions | Provisional code bytes | Bank coverage |
|---|---:|---:|---:|---:|
| JP0 | 741 | 7180 | 11639 | 71.039% |
| EN0 | 580 | 6717 | 11082 | 67.639% |
| EN1 | 580 | 6717 | 11082 | 67.639% |
| ES0 | 573 | 6632 | 10907 | 66.571% |
| DE0 | 570 | 6863 | 11452 | 69.897% |
| FR0 | 570 | 6686 | 11057 | 67.487% |
| IT0 | 572 | 6997 | 11613 | 70.880% |

The remaining bytes are **not automatically data**; they are simply not proven reachable code in this pass. They include genuine data/tables/padding plus executable routines reached only indirectly or from other banks.

### Bank 00 completion state

- Physical census: **complete**
- Vector semantics: **confirmed**
- Header semantics: **confirmed**
- EN Rev0/RevA Bank 00 revision analysis: **confirmed**
- Seven-ROM recursive control-flow disassembly: **generated / provisional**
- Full Home symbol lifting: **in progress**
- Exact code/data boundary map: **in progress**
- Byte-exact semantic Bank 00 rebuild: **pending**

Bank 01 must not begin as a completed work unit until Bank 00 has either passed this completion gate or is explicitly carried as a documented unresolved bank.
