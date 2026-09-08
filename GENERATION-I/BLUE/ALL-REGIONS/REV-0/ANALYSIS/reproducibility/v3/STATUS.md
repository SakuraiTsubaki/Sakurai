# v3 status

Validated whole-ROM physical scope:

- 6 supplied ROMs
- 5,767,168 source bytes
- 352 physical 16 KiB banks
- 22,528 stable 0x100-byte scaffold chunks
- exact local source hash checks for all six ROMs
- zero-gap / zero-overlap scaffold inherited from v2

v3 structural work inventory:

- 352 bank work-unit records
- 7,020 16-bit pointer-table candidates
- per-bank opcode/pointer-shaped xref summaries
- per-bank text-like candidate summaries plus top candidates by address/length
- per-bank 16-byte tile-unit structural statistics
- semantic confidence/evidence and next-extractor assignment for every bank

Current semantic state is intentionally mixed: physical reproducibility is complete; semantic decoding is promoted only area by area after reversible extraction succeeds.
