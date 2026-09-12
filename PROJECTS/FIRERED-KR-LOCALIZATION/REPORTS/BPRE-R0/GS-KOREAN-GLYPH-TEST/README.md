# FireRed × GS Korean glyph injection test v0.1

Date: 2026-09-10

## Scope

Proof-of-concept for rendering genuine GS Korean Hangul glyph pixels through the existing Pokémon FireRed text engine. The base ROM is used read-only; no ROM binary is stored in this repository.

## Base

- Release: `BPRE-R0`
- Dump: `UPLOAD-d3b80645`
- ROM: `Pokemon - Fire Red Version (USA).gba`
- Game code: `BPRE`
- Revision: `0`
- Size: `16,777,216` bytes
- SHA-1: `d3b806453369b4b086c792eb3c05a02f00057f50`
- SHA-256: `b59a65bb439b7dfdf2ffbbe5102be03de2501a71f5e081eec1c76f9d2ef3ba00`
- Header checksum: `0x68`, valid
- Dump status: `reference-mismatch`; all byte offsets below are dump-scoped until rebased/verified against the canonical BPRE-R0 release.

## Test

The injected test string is `가나다라`.

GS Korean charmap codes:

| Character | GS code | FireRed test glyph ID |
|---|---:|---:|
| 가 | `0x0101` | `0x01` |
| 나 | `0x023A` | `0x02` |
| 다 | `0x02D9` | `0x03` |
| 라 | `0x03C3` | `0x04` |

FireRed path:

- Existing `FONT_NORMAL_COPY_1` renderer
- `JPN` extended control code enables Japanese glyph addressing
- Japanese tall font base in the supplied USA Rev 0 dump: `0x1FB300`
- Tall glyph dimensions: 8×16
- The four Japanese tall-font slots above are replaced by converted GS Korean 8×16 1bpp glyph masks.

Text payload:

`FC 06 01 FC 15 01 02 03 04 FF`

This means `FONT_NORMAL_COPY_1`, `JPN`, glyphs `01 02 03 04`, then end-of-string.

The payload replaces the beginning of all three supplied-dump copies of `Press START to open the MENU!` at:

- `0x18EA66`
- `0x1B1CCE`
- `0x1B1D5F`

## Output validation

Local generated test ROM:

- SHA-1: `672e3c97b9fb891d62b855832c9e2871f745b74b`
- SHA-256: `e6f241a6b731e639bd77915c893765e28cfdc31b45ebef96ee1cd4e2005144d7`
- Size unchanged: `16,777,216` bytes
- GBA header checksum remains valid: `0x68`
- GS 1bpp → FireRed packed-font → decoded mask round-trip: exact for all four test glyphs
- IPS reapplication to the exact base dump reproduces the output ROM byte-for-byte

## Interpretation

This v0.1 proves glyph-format conversion and use of FireRed's existing 8×16 renderer on the exact supplied dump. It is not yet the final Korean text engine: there is no FireRed-wide 2-byte/extended Hangul decoder, line-breaking system, Korean naming input, SRAM string migration, or complete 2,353-glyph installation yet.

Research evidence belongs in Sakurai. Distributable patches, generated build inputs and production reproduction artifacts belong in Tsubaki. ROM binaries remain local and are never committed.
