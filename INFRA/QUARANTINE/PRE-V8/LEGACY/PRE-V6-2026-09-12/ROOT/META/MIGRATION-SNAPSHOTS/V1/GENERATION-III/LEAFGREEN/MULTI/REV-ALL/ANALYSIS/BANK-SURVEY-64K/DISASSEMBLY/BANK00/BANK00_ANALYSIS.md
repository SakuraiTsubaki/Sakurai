# LeafGreen Bank 00 — Integrated Survey + Disassembly

Analysis bank `00` covers ROM offsets `0x000000–0x00FFFF`, bus addresses `0x08000000–0x0800FFFF`.

## Confirmed execution roots

- `0x08000000`: GBA reset vector, ARM state; the first instruction branches to `0x08000204`.
- `0x08000204`: ARM startup (`crt0`) entry.
- `0x08000244`: literal word `0x080003A5` in all seven ROMs. Bit 0 selects Thumb state.
- `0x080003A4`: confirmed Thumb entry for `AgbMain`.
- `0x08000248`: ARM interrupt-dispatch body following the startup literal pool.

The public `pret/pokefirered` source has the matching startup sequence `ldr r1, =AgbMain; mov lr, pc; bx r1`, which anchors the semantic label without treating a blind linear listing as authoritative.

## Literal/data carving inside ARM startup

The words at `0x0800039C` and `0x080003A0` are literal data, not ARM instructions. They point into EWRAM and vary by build group:

|Build group|`0x0800039C`|`0x080003A0`|
|---|---:|---:|
|JP_R0|`0x03007488`|`0x03003580`|
|EN_R0 / EN_R1|`0x03007438`|`0x03003540`|
|DE_R0 / ES_R0 / FR_R0 / IT_R0|`0x03007328`|`0x03003490`|

This is an early example of why each bank is being carved into code, literal pools, pointer tables, scripts, compressed assets, text and fill before final source reconstruction.

## Bank 00 Thumb target score

High-confidence Thumb-entry candidates discovered from BL destinations / odd ROM function pointers plus plausible entry opcodes:

|ROM|High-confidence candidates|
|---|---:|
|JP_R0|261|
|EN_R0|265|
|EN_R1|260|
|DE_R0|267|
|ES_R0|266|
|FR_R0|266|
|IT_R0|268|

These counts are discovery aids, not final function counts. A candidate becomes `confirmed` only after control-flow, boundaries and embedded data are reconciled.

## Generated listings

For every one of the seven ROMs, `bank00/<ROM>/` contains:

- `bank00_startup_arm.s` — actual LLVM ARM disassembly of the anchored startup range.
- `bank00_agbmain_thumb.s` — raw LLVM Thumb disassembly beginning at the confirmed `AgbMain` entry.
- `bank00_agbmain_thumb_carved.s` — the same listing with detected PC-relative literal pools emitted as `.word` data instead of fake instructions.

## Next bank procedure

Every subsequent bank uses the same integrated pass:

1. consume incoming pointers/calls from already mapped banks;
2. score new ARM/Thumb entry candidates;
3. recursively follow control flow;
4. carve literal pools and pointer tables out of code listings;
5. identify event script/text/LZ77/graphics/audio regions;
6. compare matching/relocated regions across all seven releases;
7. emit a bank report and assembly/data source fragments with confidence labels.
