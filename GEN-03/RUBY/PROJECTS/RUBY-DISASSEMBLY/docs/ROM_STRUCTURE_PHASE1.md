# ROM Structure Survey — Phase 1

This phase establishes reproducible structural anchors for the verified Pokémon Ruby source-ROM set. ROM binaries remain local and read-only; only metadata, analysis, source-form reconstruction, and tools are committed.

## Scope

- Verify every local source image against `manifests/source_roms.json`.
- Parse and validate the GBA header.
- Decode the initial ARM branch target.
- Locate large `0x00` / `0xFF` filler spans.
- Compare adjacent revisions byte-for-byte.
- Identify small revision patches at instruction level where possible.
- Establish known linker/section anchors for subsequent extraction.

The reproducible analyzer is `tools/analyze_roms.py` and the current machine-readable result is `manifests/rom_structure_phase1.json`.

## Header and entry-point observations

All 13 verified images have a valid GBA header complement checksum and identify as `POKEMON RUBY` with maker code `01`.

| Target family | Initial ARM branch | File-offset target | ROM address |
|---|---:|---:|---:|
| Japan Rev 0 (`AXVJ`) | `0xEA000032` | `0x000000D0` | `0x080000D0` |
| English Rev 0/1/2 (`AXVE`) | `0xEA000032` | `0x000000D0` | `0x080000D0` |
| German/French/Italian/Spanish retail | `0xEA00007F` | `0x00000204` | `0x08000204` |
| German debug | `0xEA00007F` | `0x00000204` | `0x08000204` |

The different entry targets are treated as version-family layout facts, not normalized away.

## ROM layout anchors

### English retail

For English Rev 0, the largest `0xFF` spans are:

- `0x006B09F8–0x00D00000` — 6,616,584 bytes
- `0x00EAE244–0x01000000` — 1,383,868 bytes

English Rev 2 begins the first large filler run at `0x006B0A0C`; its secondary data island has the same `0x00D00000` anchor and ends at the same `0x00EAE244` point.

The public `pret/pokeruby` linker script explicitly places `gfx_data` at ROM address `0x08D00000`, which corresponds to file offset `0x00D00000`, and begins it with `src/data/graphics.o(.rodata)`. This provides a strong external structural cross-check for the western retail layout.

### German debug

The German debug image has a larger primary data/code area:

- first large `0xFF` run: `0x006DF850–0x00D00000`
- second large `0xFF` run: `0x00EB0F58–0x01000000`

The debug target must therefore remain a distinct build/layout target rather than being modeled as a tiny retail patch.

### Japanese Rev 0

The Japanese image is 8 MiB and has a large `0xFF` span at:

- `0x00655178–0x0067D000`

Data resumes at `0x0067D000`. The bytes at this point begin identically to the western `0x00D00000` graphics island, so this is a strong candidate for the corresponding Japanese graphics-data relocation. It remains marked **provisional** until the Japanese layout is independently symbolized.

## Revision-difference survey

### English Rev 1 → Rev 2

Only four bytes differ.

1. Header software version at `0xBC`: `1 → 2`.
2. Header complement checksum at `0xBD`: `0x40 → 0x3F`.
3. Thumb instruction at `0x919A`: `0xDD11` (`BLE`) → `0xDB11` (`BLT`).
4. Thumb instruction at `0x91BE`: `0xDCED` (`BGT`) → `0xDAED` (`BGE`).

These two branch-condition changes alter an inclusive/exclusive loop boundary. They match the `BUGFIX_BERRY` implementation documented in `pret/pokeruby/src/rtc.c`, where the date-to-day-count loop changes from `i > 0` to `i >= 0`, adding the missing year-2000 days that caused the berry glitch.

### German / French / Italian / Spanish retail revisions

For each of these language families, Rev 0 → Rev 1 also differs by only four bytes: the header version/checksum and the same two Thumb conditional-branch changes.

The code offsets are shifted relative to English:

- `0x9366`: `0xDD11` (`BLE`) → `0xDB11` (`BLT`)
- `0x938A`: `0xDCED` (`BGT`) → `0xDAED` (`BGE`)

This byte-identical instruction patch establishes that the same RTC/day-count fix is present in these later western revisions, even where the current public `pokeruby` configuration does not model every language as a build target.

### English Rev 0 → Rev 1

This is **not** a four-byte maintenance revision:

- different bytes: **5,744,535**
- contiguous difference runs: **419,998**

The large-scale difference means English Rev 0 and Rev 1 must be represented as distinct layout targets with their own address/symbol maps. They must not be modeled as a base image plus a handful of patches.

### German retail Rev 0 → German debug Rev 0

This is also a distinct layout/build:

- different bytes: **6,751,723**
- contiguous difference runs: **263,540**

Debug-only code/data and address shifts will be tracked separately.

## Reconstruction implications

The repository should use a shared semantic source tree where content is genuinely common, while keeping version-aware linker/layout configuration and version-specific data where addresses or content differ.

Planned structure:

```text
config/versions/
  japan_rev0/
  english_rev0/
  english_rev1/
  english_rev2/
  germany_rev0/
  germany_rev1/
  germany_debug_rev0/
  france_rev0/
  france_rev1/
  italy_rev0/
  italy_rev1/
  spain_rev0/
  spain_rev1/
```

The next phase is to turn these raw layout anchors into symbolized sections: startup/CRT, engine code, read-only game data, scripts/text, maps, sound, and graphics. Every extracted region will carry source-ROM offset provenance and a rebuild/round-trip verification path.

## Cross-check references

The public `pret/pokeruby` project is used only as a structural cross-check, not as a substitute for verifying the locally supplied ROMs. Relevant reference files include:

- `ld_script.txt` — western linker/section ordering and the `0x08D00000` `gfx_data` anchor.
- `include/config.h` — `BUGFIX_BERRY` revision conditions currently modeled by that project.
- `src/rtc.c` — source-level explanation and implementation of the berry-glitch date-count fix.

Our own ROM-derived offsets, hashes, revision comparisons, and future extraction manifests remain authoritative for this repository's supported target set.
