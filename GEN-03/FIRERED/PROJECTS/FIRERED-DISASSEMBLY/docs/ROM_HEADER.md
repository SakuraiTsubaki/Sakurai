# Standard GBA ROM header reconstruction

The first `0x100` bytes of all eight FireRed baselines have been audited directly.

## Shared bytes

The following regions are byte-identical in all eight baselines:

- `0x000000..0x000003`: ARM branch to `0x08000204`
- `0x000004..0x00009F`: standard GBA Nintendo logo
- `0x0000A0..0x0000AB`: ASCII title `POKEMON FIRE`
- `0x0000B0..0x0000BB`: maker/fixed/reserved fields except the later revision/checksum bytes
- `0x0000C0..0x0000FF`: GPIO mirrors and erased `0xFF` padding

## Per-build bytes

The variant-dependent fields are:

- `0xAC..0xAF`: game code (`BPRJ`, `BPRE`, `BPRF`, `BPRD`, `BPRI`, `BPRS`)
- `0xBC`: software version (0 or 1)
- `0xBD`: complement checksum derived from the header

Maker code is `01` in every baseline.

## Source reconstruction

`src/rom_header.s` emits the branch, fixed GPIO/padding structure, and empty standard-header slots. `tools/fix_gba_header.py` then populates the format-defined logo and version metadata from `config/versions.json`, and regenerates the complement checksum.

A local assembly/link/fix test was run for all eight baselines. The generated `0x000000..0x0000FF` region matched each corresponding canonical ROM **byte-for-byte**.

## Status

**Reconstruction status: VERIFIED / SOURCE-REGENERATABLE**

No original ROM bytes are needed at build time for this region.
